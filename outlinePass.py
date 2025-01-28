from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time

class OutlineRenderPass:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", { "multiline": False }),
            },
            "optional": {
                "run_id": ("STRING", { "multiline": False }),
                "default_value": ("IMAGE",)
            }
        }

    @classmethod
    def IS_CHANGED(cls, image):
        # always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)

    FUNCTION = "parse_outline"
    OUTPUT_NODE = {False}
    CATEGORY = "Playbook 3D"

    def parse_outline(self, api_key, run_id=None, default_value=None):
        """
        Fetches the outline pass for the specified run_id.
        """
        base_url = "https://accounts.playbook3d.com"

        # 1) Check API key
        if not api_key or not api_key.strip():
            print("No api_key provided. Returning default image.")
            return [default_value]

        # 2) Retrieve user token
        user_token = None
        try:
            jwt_request = requests.get(f"{base_url}/token-wrapper/get-tokens/{api_key}")
            if jwt_request is not None:
                user_token = jwt_request.json().get("access_token", None)
            if not user_token:
                print("Could not retrieve user_token. Returning default image.")
                return [default_value]
        except Exception as e:
            print(f"Error retrieving token: {e}")
            return [default_value]


        # 3) Construct the request URL with run_id
        if run_id:
            url = f"{base_url}/upload-assets/get-download-urls/{run_id}"
        else:
            url = f"{base_url}/upload-assets/get-download-urls"

        # 4) Fetch the outline pass
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            outline_request = requests.get(url, headers=headers)

            if outline_request.status_code == 200:
                outline_url = outline_request.json().get("outline")
                if outline_url:
                    outline_response = requests.get(outline_url)
                    image = Image.open(BytesIO(outline_response.content))
                    image = ImageOps.exif_transpose(image)
                    image = image.convert("RGB")
                    image = np.array(image).astype(np.float32) / 255.0
                    image = torch.from_numpy(image)[None,]
                    return [image]
                else:
                    print("No 'outline' key found in the JSON response. Returning default image.")
                    return [default_value]
            else:
                print(f"Outline request returned status code {outline_request.status_code}")
                return [default_value]

        except Exception as e:
            print(f"Error retrieving outline pass: {e}")
            return [default_value]


NODE_CLASS_MAPPINGS = {
    "Playbook Outline": OutlineRenderPass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Outline": "Playbook Outline Render Pass"
}
