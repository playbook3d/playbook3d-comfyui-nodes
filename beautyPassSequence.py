# beautyPassSequence.py

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

class BeautyRenderPassSequence:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    @classmethod
    def IS_CHANGED(cls, image):
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Images",)
    FUNCTION = "parse_beauty_sequence"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_beauty_sequence(self, api_key):
        base_url = "https://dev-accounts.playbook3d.com"
        user_token = None

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
            beauty_request = requests.get(f"{base_url}/upload-assets/get-download-urls", headers=headers)
            if beauty_request.status_code == 200:
                beauty_url = beauty_request.json()["beauty_zip"]

                # Download the zip file
                beauty_response = requests.get(beauty_url)
                if beauty_response.status_code != 200:
                    raise ValueError("Failed to download the beauty zip file.")

                zip_content = beauty_response.content

                # Extract images from the zip file
                images_batch = self.extract_images_from_zip(zip_content)

                return (images_batch,)
            else:
                raise ValueError("Failed to retrieve beauty URL.")
        except Exception as e:
            print(f"Error processing beauty sequence: {e}")
            raise ValueError("Beauty pass not uploaded or processing error occurred.")

    def extract_images_from_zip(self, zip_content):
        images = []
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "beauty_sequence.zip")
            with open(zip_path, 'wb') as f:
                f.write(zip_content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get a list of image file names, sorted in ascending order
                image_files = sorted([f for f in zip_ref.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
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

NODE_CLASS_MAPPINGS = {
    "Beauty Pass Sequence": BeautyRenderPassSequence
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Beauty Pass Sequence": "Beauty Pass Sequence"
}
