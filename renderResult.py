import requests
import numpy as np
from PIL import Image
from io import BytesIO
from base64 import b64encode

class UploadRenderResult:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "api_key": ("STRING", { "multiline": False })
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("URL",)

    FUNCTION = "parse_result"

    OUTPUT_NODE = { True }

    CATEGORY = "Playbook 3D"

    def parse_result(self, api_key, images):
        i = 255. * images.cpu().numpy()
        i = np.squeeze(i)
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8), 'RGB')
        buffer = BytesIO()
        img.save(buffer, "PNG")
        buffer.seek(0)
        img_data = buffer.getvalue()

        base_url = "https://accounts.playbook3d.com"
        user_token = None
        jwt_request = requests.get(f"{base_url}/token-wrapper/get-tokens/{api_key}")

        try:
            if jwt_request is not None:

                user_token = jwt_request.json()["access_token"]
        except Exception as e:
            print(f"Error with node: {e}")
            raise ValueError("API Key not found/Incorrect")

        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            result_request = requests.get(f"{base_url}/upload-assets/get-upload-urls", headers=headers)
            if result_request.status_code == 200:
                result_url = result_request.json()["save_result"]
                result_response = requests.put(url=result_url, data=img_data)
                if result_response.status_code == 200:
                    download_request = requests.get(f"{base_url}/upload-assets/get-download-urls", headers=headers)
                    download_url = download_request.json()["save_result"]
                    return [download_url]
        except Exception:
            raise ValueError("Error with uploading Result")
        raise ValueError("Error with uploading Result")


NODE_CLASS_MAPPINGS = {
    "Playbook Render Result": UploadRenderResult
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Render Result": "Playbook Render Result"
}
