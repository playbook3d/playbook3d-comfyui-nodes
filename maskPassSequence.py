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
                "blur_size": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 50.0}),
            },
            "optional": {
                "run_id": ("STRING", {"multiline": False})
            }
        }

    @classmethod
    def IS_CHANGED(cls, image):
        # Always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = (
        "IMAGE",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK"
    )

    RETURN_NAMES = (
        "mask_pass",
        "mask_1",
        "mask_2",
        "mask_3",
        "mask_4",
        "mask_5",
        "mask_6",
        "mask_7",
        "mask_8"
    )

    FUNCTION = "parse_mask_sequence"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_mask_sequence(self, api_key, blur_size, run_id=None):
        """
        Fetches a ZIP file containing mask passes for the specified run_id,
        extracts them, and returns both the composite mask + 8 individual 
        color-based masks as a sequence (batch).
        """
        base_url = "https://accounts.playbook3d.com"

        # 1) Check if api_key is valid
        if not api_key or not api_key.strip():
            raise ValueError("No api_key provided.")

        # 2) Retrieve user token
        user_token = None
        try:
            jwt_request = requests.get(f"{base_url}/token-wrapper/get-tokens/{api_key}")
            if jwt_request is not None and jwt_request.status_code == 200:
                user_token = jwt_request.json().get("access_token", None)
                if not user_token:
                    raise ValueError("Could not retrieve user token.")
            else:
                raise ValueError("API Key not found or incorrect.")
        except Exception as e:
            print(f"Error retrieving token: {e}")
            raise ValueError("API Key not found or incorrect.")

        # 3) Check if run_id is valid
        if not run_id or not run_id.strip():
            raise ValueError("No run_id provided.")

        # 4) Construct the endpoint using run_id
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            url = f"{base_url}/upload-assets/get-download-urls/{run_id}"

            mask_request = requests.get(url, headers=headers)
            if mask_request.status_code == 200:
                mask_url = mask_request.json().get("mask_zip", None)
                if not mask_url:
                    raise ValueError("No mask zip found for the provided parameters.")

                # 5) Download the zip file
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

                return [
                    composite_masks_batch,
                    mask_1_batch,
                    mask_2_batch,
                    mask_3_batch,
                    mask_4_batch,
                    mask_5_batch,
                    mask_6_batch,
                    mask_7_batch,
                    mask_8_batch
                ]
            else:
                raise ValueError(
                    f"Failed to retrieve mask URL. Status code: {mask_request.status_code}"
                )
        except Exception as e:
            print(f"Error processing mask sequence: {e}")
            raise ValueError("Mask pass not uploaded or processing error occurred.")

    def extract_masks_from_zip(self, zip_content, blur_size):
        """
        Extracts mask images from the provided ZIP content. Returns:
          composite_masks_batch, mask_1_batch, ..., mask_8_batch
        """
        composite_masks = []
        individual_masks_list = [[] for _ in range(8)]

        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "mask_sequence.zip")
            with open(zip_path, 'wb') as f:
                f.write(zip_content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Sort the images based on file names
                image_files = sorted(
                    [f for f in zip_ref.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                )
                for file_name in image_files:
                    # Read image data from the zip file
                    with zip_ref.open(file_name) as img_file:
                        image = Image.open(BytesIO(img_file.read()))
                        image = ImageOps.exif_transpose(image)
                        image = image.convert("RGB")
                        composite_mask = np.array(image)

                        # Composite mask stored as is (RGB)
                        composite_mask_tensor = torch.from_numpy(
                            composite_mask.astype(np.float32) / 255.0
                        )[None,]
                        composite_masks.append(composite_mask_tensor)

                        # Predefined color codes
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
                        color_tuples = [
                            tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                            for color in color_codes
                        ]

                        # Create a mask for each color
                        for idx, color in enumerate(color_tuples):
                            mask_array = (
                                (composite_mask == np.array(color)).all(axis=2)
                            ).astype(np.uint8) * 255

                            mask_image = Image.fromarray(mask_array, mode='L')
                            if blur_size > 0:
                                mask_image = mask_image.filter(ImageFilter.GaussianBlur(radius=blur_size))

                            mask_tensor = torch.from_numpy(
                                np.array(mask_image).astype(np.float32) / 255.0
                            )[None,]
                            individual_masks_list[idx].append(mask_tensor)

        # Concatenate composite masks into a single batch
        composite_masks_batch = torch.cat(composite_masks, dim=0)

        # Concatenate each color mask list into a batch
        individual_masks_batches = [
            torch.cat(masks, dim=0) if masks else None
            for masks in individual_masks_list
        ]

        return (
            composite_masks_batch,
            *individual_masks_batches
        )

NODE_CLASS_MAPPINGS = {
    "Mask Pass Sequence": MaskRenderPassSequence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Mask Pass Sequence": "Mask Pass Sequence"
}
