from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time

class PlaybookImage:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
            },
            "optional": {
                "default_value": ("IMAGE",),
                "default_url": ("STRING", {"multiline": False, "default": ""})
            },
        }

    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)

    FUNCTION = "parse_image"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_image(self, id, label, default_url, default_value=None):
        image_url = default_url
        image = default_value
        try:
            if image_url.startswith('http'):
                image_request = requests.get(image_url)
                image = Image.open(BytesIO(image_request.content))
            else:
                raise ValueError("Invalid URL")
            
            image = ImageOps.exif_transpose(image)
            image = image.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[ None, ]
            return [ image ]
        except Exception as e:
            print(f"Exception while downloading Image {e}")
            return [ image ]
            
        


NODE_CLASS_MAPPINGS = {
    "Playbook Image": PlaybookImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Image": "Playbook Image (External)"
}