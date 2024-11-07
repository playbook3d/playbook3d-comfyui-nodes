from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO

class PlaybookImage:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", { "multiline": False })
            },
            "optional": {
                "playbook_image": ("IMAGE",)
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image",)

    FUNCTION = "parse_image"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_image(self, name = None, playbook_image = None):
        image_url = name
        image = playbook_image
        try:
            if name.startswith('http'):
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