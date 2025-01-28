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
        # Always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)

    FUNCTION = "parse_depth"
    OUTPUT_NODE = {False}
    CATEGORY = "Playbook 3D"

    def parse_depth(self, api_key, run_id=None, default_value=None):
        """
        This method fetches the user's access_token from the
        Playbook3D token endpoint, checks run_id, and then 
        makes a request to fetch the Depth image.
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

        # 3) Check run_id
        if not run_id or not run_id.strip():
            print("No run_id provided. Returning default image.")
            return [default_value]

        # 4) Construct the endpoint using run_id and fetch the Depth pass
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            url = f"{base_url}/upload-assets/get-download-urls/{run_id}"

            depth_request = requests.get(url, headers=headers)
            if depth_request.status_code == 200:
                depth_url = depth_request.json().get("depth")
                if depth_url:
                    depth_response = requests.get(depth_url)
                    image = Image.open(BytesIO(depth_response.content))
                    image = ImageOps.exif_transpose(image)
                    image = image.convert("RGB")
                    image = np.array(image).astype(np.float32) / 255.0
                    image = torch.from_numpy(image)[None,]
                    return [image]
                else:
                    print("No 'depth' key found in the JSON response. Returning default image.")
                    return [default_value]
            else:
                print(f"Depth request returned status code {depth_request.status_code}")
                return [default_value]

        except Exception as e:
            print(f"Error retrieving depth pass: {e}")
            return [default_value]


NODE_CLASS_MAPPINGS = {
    "Playbook Depth": DepthRenderPass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Depth": "Playbook Depth Render Pass"
}
