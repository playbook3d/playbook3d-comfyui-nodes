from PIL import Image, ImageOps, ImageFilter
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time
import zipfile
import tempfile
import os

class MaskRenderPassSequence:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "blur_radius": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 50.0}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, image):
        # Always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    # Output a list of images: composite masks and individual masks
    RETURN_TYPES = ("IMAGE",) + ("IMAGE",) * 8
    RETURN_NAMES = ("Composite Masks", "Mask 1", "Mask 2", "Mask 3", "Mask 4", "Mask 5", "Mask 6", "Mask 7", "Mask 8")
    FUNCTION = "parse_mask_sequence"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_mask_sequence(self, api_key, blur_radius):
        base_url = "https://accounts.playbookengine.com"
        user_token = None

        # Authenticate using the API key
        jwt_request = requests.get(f"{base_url}/token-wrapper/get-tokens/{api_key}")

        try:
            if jwt_request is not None and jwt_request.status_code == 200:
                user_token = jwt_request.json()["access_token"]
            else:
                raise ValueError("API Key not found or incorrect.")
        except Exception as e:
            print(f"Error with node: {e}")
            raise ValueError("API Key not found or incorrect.")

        try:
            headers = {"Authorization": f"Bearer {user_token}"}

            # Request the download URLs from the endpoint
            mask_request = requests.get(f"{base_url}/upload-assets/get-download-urls", headers=headers)
            if mask_request.status_code == 200:
                mask_url = mask_request.json()["mask_zip"]

                # Download the zip file
                mask_response = requests.get(mask_url)
                if mask_response.status_code != 200:
                    raise ValueError("Failed to download the mask zip file.")

                zip_content = mask_response.content

                # Process the zip file
                outputs = self.extract_masks_from_zip(zip_content, blur_radius)

                return outputs
            else:
                raise ValueError("Failed to retrieve mask URL.")
        except Exception as e:
            print(f"Error processing mask sequence: {e}")
            raise ValueError("Mask pass not uploaded or processing error occurred.")

    def extract_masks_from_zip(self, zip_content, blur_radius):
        composite_masks = []
        individual_masks_list = [[] for _ in range(8)]

        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "mask_sequence.zip")
            with open(zip_path, 'wb') as f:
                f.write(zip_content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Sort the images based on file names
                image_files = sorted([f for f in zip_ref.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                for file_name in image_files:
                    # Read image data from the zip file
                    with zip_ref.open(file_name) as img_file:
                        image = Image.open(BytesIO(img_file.read()))
                        image = ImageOps.exif_transpose(image)
                        image = image.convert("RGB")
                        composite_mask = np.array(image)

                        composite_mask_tensor = torch.from_numpy(composite_mask.astype(np.float32) / 255.0)[None,]
                        composite_masks.append(composite_mask_tensor)

                        color_codes = ["#ffe906", "#0589d6", "#a2d4d5", "#000016",
                                       "#00ad58", "#f084cf", "#ee9e3e", "#e6000c"]
                        color_tuples = [tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for color in color_codes]

                        for idx, color in enumerate(color_tuples):
                            mask_array = ((composite_mask == np.array(color)).all(axis=2)).astype(np.uint8) * 255
                            mask_image = Image.fromarray(mask_array, mode='L')
                            if blur_radius > 0:
                                mask_image = mask_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                            mask_tensor = torch.from_numpy(np.array(mask_image).astype(np.float32) / 255.0)[None,]
                            individual_masks_list[idx].append(mask_tensor)

        composite_masks_batch = torch.cat(composite_masks, dim=0)
        individual_masks_batches = [torch.cat(masks, dim=0) if masks else None for masks in individual_masks_list]

        return (composite_masks_batch, *individual_masks_batches)

# Register the node
NODE_CLASS_MAPPINGS = {
    "Mask Pass Sequence": MaskRenderPassSequence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Mask Pass Sequence": "Mask Pass Sequence"
}
