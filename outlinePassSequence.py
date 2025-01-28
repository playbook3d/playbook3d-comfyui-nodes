from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time
import zipfile
import tempfile
import os

class OutlineRenderPassSequence:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
            "optional": {
                "run_id": ("STRING", {"multiline": False})
            }
        }

    @classmethod
    def IS_CHANGED(cls, image):
        # always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Images",)
    FUNCTION = "parse_outline_sequence"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_outline_sequence(self, api_key, run_id=None):
        """
        Fetches a ZIP file containing outline pass frames for a given run_id,
        unzips the images, and returns them as a batched tensor.
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

        # 3) Construct the endpoint using run_id
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            if run_id:
                url = f"{base_url}/upload-assets/get-download-urls/{run_id}"
            else:
                url = f"{base_url}/upload-assets/get-download-urls"

            outline_request = requests.get(url, headers=headers)
            if outline_request.status_code == 200:
                outline_url = outline_request.json().get("outline_zip", None)
                if not outline_url:
                    raise ValueError("No outline zip found for the provided parameters.")

                # 5) Download the zip file
                outline_response = requests.get(outline_url)
                if outline_response.status_code != 200:
                    raise ValueError("Failed to download the outline zip file.")

                zip_content = outline_response.content

                # Extract images from the zip file
                images_batch = self.extract_images_from_zip(zip_content)
                return (images_batch,)

            else:
                raise ValueError(
                    f"Failed to retrieve outline URL. Status code: {outline_request.status_code}"
                )
        except Exception as e:
            print(f"Error processing outline sequence: {e}")
            raise ValueError("Outline pass not uploaded or processing error occurred.")

    def extract_images_from_zip(self, zip_content):
        """
        Extracts outline images from a ZIP. Returns a torch tensor
        containing all images in a batch (B, C, H, W).
        """
        images = []
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "outline_sequence.zip")
            with open(zip_path, 'wb') as f:
                f.write(zip_content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                image_files = sorted(
                    [f for f in zip_ref.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                )
                for file_name in image_files:
                    with zip_ref.open(file_name) as img_file:
                        image = Image.open(BytesIO(img_file.read()))
                        image = ImageOps.exif_transpose(image)
                        image = image.convert("RGB")
                        image = np.array(image).astype(np.float32) / 255.0
                        image = torch.from_numpy(image)[None,]
                        images.append(image)

        if images:
            images_batch = torch.cat(images, dim=0)
            return images_batch
        else:
            raise ValueError("No images found in the outline zip file.")

NODE_CLASS_MAPPINGS = {
    "Outline Pass Sequence": OutlineRenderPassSequence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Outline Pass Sequence": "Outline Pass Sequence"
}
