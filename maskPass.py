from PIL import Image, ImageOps, ImageFilter
import numpy as np
import torch
import requests
from io import BytesIO
import hashlib
import time

class MaskRenderPass:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "api_key": ("STRING", { "multiline": False }),
                "blur_size": ("FLOAT", { "default": 0.0, "min": 0.0, "max": 50.0 })
            },
            "optional": {
                "default_value": ("IMAGE",),
            }
        }

    @classmethod
    def IS_CHANGED(s, image):
        # Always update
        m = hashlib.sha256()
        m.update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = (
        "IMAGE",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK",
        "MASK"
    )

    RETURN_NAMES = (
        "image",
        "mask_1",
        "mask_2",
        "mask_3",
        "mask_4",
        "mask_5",
        "mask_6",
        "mask_7",
        "mask_8"
    )

    FUNCTION = "parse_mask"
    OUTPUT_NODE = {False}
    CATEGORY = "Playbook 3D"

    def parse_mask(self, api_key, blur_size, id, default_value=None):
        base_url = "https://dev-accounts.playbook3d.com"
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
            mask_request = requests.get(f"{base_url}/upload-assets/get-download-urls", headers=headers)
            if mask_request.status_code == 200:
                mask_url = mask_request.json()["mask"]
                mask_response = requests.get(mask_url)
                image = Image.open(BytesIO(mask_response.content))
                image = ImageOps.exif_transpose(image)
                image = image.convert("RGB")

                composite_mask = np.array(image)
                composite_mask_tensor = torch.from_numpy(composite_mask.astype(np.float32) / 255.0)[None,]

                color_codes = [
                    "#ffe906",
                    "#0589d6",
                    "#a2d4d5",
                    "#000016",
                    "#00ad58",
                    "#f084cf",
                    "#ee9e3e",
                    "#e6000c"
                ]
                color_tuples = [
                    tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    for color in color_codes
                ]

                individual_masks = []
                for color in color_tuples:
                    mask_array = ((composite_mask == np.array(color)).all(axis=2)).astype(np.uint8) * 255
                    mask_image = Image.fromarray(mask_array, mode='L')
                    if blur_size > 0:
                        mask_image = mask_image.filter(ImageFilter.GaussianBlur(radius=blur_size))

                    mask_tensor = torch.from_numpy(
                        np.array(mask_image).astype(np.float32) / 255.0
                    )[None,]
                    individual_masks.append(mask_tensor)

                # Ensure all masks have the same shape
                for i in range(len(individual_masks)):
                    if individual_masks[i].shape != individual_masks[0].shape:
                        individual_masks[i] = torch.nn.functional.interpolate(
                            individual_masks[i], size=individual_masks[0].shape[2:], mode='nearest'
                        )

                return [
                    composite_mask_tensor,
                    individual_masks[0],
                    individual_masks[1],
                    individual_masks[2],
                    individual_masks[3],
                    individual_masks[4],
                    individual_masks[5],
                    individual_masks[6],
                    individual_masks[7]
                ]

            else:
                raise ValueError("Failed to retrieve mask URL.")
        except Exception as e:
            print(f"Error while processing masks: {e}")
            raise ValueError("Mask pass not uploaded or processing error occurred.")


NODE_CLASS_MAPPINGS = {
    "Playbook Mask": MaskRenderPass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Mask": "Playbook Mask Render Pass"
}
