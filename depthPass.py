from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time

class DepthRenderPass:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", { "multiline": False }),
            },
            "optional": {
                "default_value": ("IMAGE",)
            }
        }



    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)

    FUNCTION = "parse_depth"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_depth(self, api_key, default_value=None):
        base_url = "https://accounts.playbookengine.com"
        user_token = None

        jwt_request = requests.get(f"{base_url}/token-wrapper/get-tokens/{api_key}")

        try:
            if jwt_request is not None:
                user_token = jwt_request.json()["access_token"]
        except Exception as e:
            print(f"Error with node: {e}")
            return [default_value]

        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            depth_request = requests.get(f"{base_url}/upload-assets/get-download-urls", headers=headers)
            if depth_request.status_code == 200:
                depth_url = depth_request.json()["depth"]
                depth_response = requests.get(depth_url)
                image = Image.open(BytesIO(depth_response.content))
                image = ImageOps.exif_transpose(image)
                image = image.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
                return [image]
            else:
                return [default_value]
        except Exception:
            return [default_value]
        


NODE_CLASS_MAPPINGS = {
    "Playbook Depth": DepthRenderPass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Depth": "Playbook Depth Render Pass"
}