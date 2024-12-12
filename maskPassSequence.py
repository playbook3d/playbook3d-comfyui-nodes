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
                "id": ("STRING", {"multiline": False}),
                "label": ("STRING", {"multiline": False}),
                "blur_size": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 50.0}),
                "mask_1_prompt_default_value": ("STRING", {"multiline": True}),
                "mask_2_prompt_default_value": ("STRING", {"multiline": True}),
                "mask_3_prompt_default_value": ("STRING", {"multiline": True}),
                "mask_4_prompt_default_value": ("STRING", {"multiline": True}),
                "mask_5_prompt_default_value": ("STRING", {"multiline": True}),
                "mask_6_prompt_default_value": ("STRING", {"multiline": True}),
                "mask_7_prompt_default_value": ("STRING", {"multiline": True}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, image):
        # Always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = (
        "IMAGE",
        "MASK", "STRING",
        "MASK", "STRING",
        "MASK", "STRING",
        "MASK", "STRING",
        "MASK", "STRING",
        "MASK", "STRING",
        "MASK", "STRING",
        "MASK"
    )

    RETURN_NAMES = (
        "mask_pass",
        "mask_1", "mask_1_prompt",
        "mask_2", "mask_2_prompt",
        "mask_3", "mask_3_prompt",
        "mask_4", "mask_4_prompt",
        "mask_5", "mask_5_prompt",
        "mask_6", "mask_6_prompt",
        "mask_7", "mask_7_prompt",
        "mask_8"
    )

    FUNCTION = "parse_mask_sequence"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_mask_sequence(
        self,
        api_key,
        id,
        label,
        blur_size,
        mask_1_prompt_default_value,
        mask_2_prompt_default_value,
        mask_3_prompt_default_value,
        mask_4_prompt_default_value,
        mask_5_prompt_default_value,
        mask_6_prompt_default_value,
        mask_7_prompt_default_value
    ):
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

                # Process the zip file
                zip_content = mask_response.content
                (
                    composite_masks_batch,
                    mask_1_batch,
                    mask_2_batch,
                    mask_3_batch,
                    mask_4_batch,
                    mask_5_batch,
                    mask_6_batch,
                    mask_7_batch,
                    mask_8_batch
                ) = self.extract_masks_from_zip(zip_content, blur_size)

                # Return the outputs in the same format as maskPass.py
                return [
                    composite_masks_batch,
                    mask_1_batch, mask_1_prompt_default_value,
                    mask_2_batch, mask_2_prompt_default_value,
                    mask_3_batch, mask_3_prompt_default_value,
                    mask_4_batch, mask_4_prompt_default_value,
                    mask_5_batch, mask_5_prompt_default_value,
                    mask_6_batch, mask_6_prompt_default_value,
                    mask_7_batch, mask_7_prompt_default_value,
                    mask_8_batch
                ]
            else:
                raise ValueError("Failed to retrieve mask URL.")
        except Exception as e:
            print(f"Error processing mask sequence: {e}")
            raise ValueError("Mask pass not uploaded or processing error occurred.")

    def extract_masks_from_zip(self, zip_content, blur_size):
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

                        color_codes = [
                            "#ffe906",
                            "#0589d6",
                            "#a2d4d5",
                            "#000016",
                            "#00ad58",
                            "#f084cf",
                            "#ee9e3e",
                            "#e6000c"
                        ]
                        color_tuples = [tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for color in color_codes]

                        for idx, color in enumerate(color_tuples):
                            mask_array = ((composite_mask == np.array(color)).all(axis=2)).astype(np.uint8) * 255
                            mask_image = Image.fromarray(mask_array, mode='L')
                            if blur_size > 0:
                                mask_image = mask_image.filter(ImageFilter.GaussianBlur(radius=blur_size))
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
