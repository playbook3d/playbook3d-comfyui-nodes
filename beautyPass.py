from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time

class BeautyRenderPass:
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
    FUNCTION = "parse_beauty"
    OUTPUT_NODE = {False}
    CATEGORY = "Playbook 3D"

    def parse_beauty(self, api_key, run_id=None, default_value=None):
        """
        This method fetches the user's access_token from the
        Playbook3D token endpoint, checks for run_id presence,
        and then makes a request to fetch the Beauty image.
        """
        base_url = "https://accounts.playbook3d.com"

        # 1) Ensure API key is provided
        if not api_key or not api_key.strip():
            print("No api_key provided. Returning default image.")
            return [default_value]

        # 2) Get user_token from the token service
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


        # 3) Construct the endpoint using run_id and fetch the Beauty pass
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            if run_id:
                url = f"{base_url}/upload-assets/get-download-urls/{run_id}"
            else:
                url = f"{base_url}/upload-assets/get-download-urls"

            beauty_request = requests.get(url, headers=headers)
            if beauty_request.status_code == 200:
                beauty_url = beauty_request.json().get("beauty")
                if beauty_url:
                    beauty_response = requests.get(beauty_url)
                    image = Image.open(BytesIO(beauty_response.content))
                    image = ImageOps.exif_transpose(image)
                    image = image.convert("RGB")
                    image = np.array(image).astype(np.float32) / 255.0
                    image = torch.from_numpy(image)[None,]
                    return [image]
                else:
                    print("No 'beauty' key found in the JSON response. Returning default image.")
                    return [default_value]
            else:
                print(f"Beauty request returned status code {beauty_request.status_code}")
                return [default_value]

        except Exception as e:
            print(f"Error retrieving beauty pass: {e}")
            return [default_value]


NODE_CLASS_MAPPINGS = {
    "Playbook Beauty": BeautyRenderPass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Beauty": "Playbook Beauty Render Passes"
}
