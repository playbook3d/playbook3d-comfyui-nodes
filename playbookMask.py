from PIL import Image, ImageOps
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time

class PlaybookMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
            },
            "optional": {
                "default_value": ("MASK",),
                "default_url": ("STRING", {"multiline": False, "default": ""})
            },
        }

    @classmethod
    def IS_CHANGED(cls, image):
        # always update - follow same pattern as other nodes
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)

    FUNCTION = "parse_mask"

    OUTPUT_NODE = {False}

    CATEGORY = "Playbook 3D"

    def parse_mask(self, id, label, default_url="", default_value=None):
        try:
            # initial url validation
            if default_url and isinstance(default_url, str) and default_url.strip().startswith(('http://', 'https://')):
                # timeout
                image_request = requests.get(default_url.strip(), timeout=10)
                
                if image_request.status_code != 200:
                    print(f"Failed to download image from URL: {default_url}. Status code: {image_request.status_code}")
                    return [default_value]
                
                # open image
                try:
                    image = Image.open(BytesIO(image_request.content))
                except Exception as e:
                    print(f"Failed to open image from URL: {e}")
                    return [default_value]
                
                # Process image
                image = ImageOps.exif_transpose(image)
                
                if image.mode != "L":
                    image = image.convert("L")
                
                mask_array = np.array(image).astype(np.float32) / 255.0
                mask_tensor = torch.from_numpy(mask_array)[None,]
                
                # Check if tensor has right shape (1, H, W)
                if len(mask_tensor.shape) != 3 or mask_tensor.shape[0] != 1:
                    print(f"Invalid mask shape: {mask_tensor.shape}. Returning default value.")
                    return [default_value]
                
                return [mask_tensor]
            else:
                # if no valid URL provided, return default value
                if not default_url:
                    print("No URL provided. Using default value.")
                else:
                    print(f"Invalid URL format: {default_url}. Using default value.")
                return [default_value]
                
        except requests.exceptions.Timeout:
            print(f"Timeout while downloading image from URL: {default_url}")
            return [default_value]
        except requests.exceptions.RequestException as e:
            print(f"Network error while downloading image: {e}")
            return [default_value]
        except Exception as e:
            print(f"Unexpected error processing mask: {e}")
            return [default_value]


NODE_CLASS_MAPPINGS = {
    "Playbook Mask": PlaybookMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Mask": "Playbook Mask (External)"
}