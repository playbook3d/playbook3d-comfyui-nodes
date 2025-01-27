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
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Images",)
    FUNCTION = "parse_outline_sequence"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_outline_sequence(self, api_key, run_id=None):
        base_url = "https://accounts.playbook3d.com"
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
            url = f"{base_url}/upload-assets/get-download-urls"
            if run_id:
                url = f"{url}/{run_id}"

            outline_request = requests.get(url, headers=headers)
            if outline_request.status_code == 200:
                outline_url = outline_request.json().get("outline_zip", None)
                if not outline_url:
                    raise ValueError("No outline zip found for the provided parameters.")

                # Download the zip file
                outline_response = requests.get(outline_url)
                if outline_response.status_code != 200:
                    raise ValueError("Failed to download the outline zip file.")

                zip_content = outline_response.content

                # Extract images from the zip file
                images_batch = self.extract_images_from_zip(zip_content)

                return (images_batch,)
            else:
                raise ValueError("Failed to retrieve outline URL.")
        except Exception as e:
            print(f"Error processing outline sequence: {e}")
            raise ValueError("Outline pass not uploaded or processing error occurred.")

    def extract_images_from_zip(self, zip_content):
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
            raise ValueError("No images found in the zip file.")

# Register the node
NODE_CLASS_MAPPINGS = {
    "Outline Pass Sequence": OutlineRenderPassSequence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Outline Pass Sequence": "Outline Pass Sequence"
}