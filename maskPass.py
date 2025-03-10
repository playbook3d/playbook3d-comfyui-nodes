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
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "blur_size": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 50.0})
            },
            "optional": {
                "run_id": ("STRING", {"multiline": False}),
                "default_value": ("IMAGE",),
            }
        }

    @classmethod
    def IS_CHANGED(cls, image):
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

    def parse_mask(self, api_key, blur_size, run_id=None, default_value=None):
        """
        Fetches the mask pass for the specified run_id, applies
        optional Gaussian blur, and returns the composite + 
        individual color-based masks.
        """
        base_url = "https://accounts.playbook3d.com"

        # 1) Check API key
        if not api_key or not api_key.strip():
            print("No api_key provided. Returning default masks.")
            return [default_value] * 9

        # 2) Retrieve user token
        user_token = None
        try:
            jwt_request = requests.get(f"{base_url}/token-wrapper/get-tokens/{api_key}")
            print("jwt request: ", jwt_request)
            if jwt_request is not None:
                user_token = jwt_request.json().get("access_token", None)
                print("user token: ", user_token)
            if not user_token:
                print("Could not retrieve user_token. Returning default masks.")
                return [default_value] * 9
        except Exception as e:
            print(f"Error retrieving token: {e}")
            return [default_value] * 9


        # 3) Construct the URL with run_id
        if run_id:
            url = f"{base_url}/upload-assets/get-download-urls/{run_id}"
        else:
            url = f"{base_url}/upload-assets/get-download-urls"

        # 5) Request the mask pass
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            mask_request = requests.get(url, headers=headers)

            if mask_request.status_code == 200:
                mask_url = mask_request.json().get("mask")
                if not mask_url:
                    raise ValueError("Mask pass URL not found for this run_id.")

                mask_response = requests.get(mask_url)
                image = Image.open(BytesIO(mask_response.content))
                image = ImageOps.exif_transpose(image)
                image = image.convert("RGB")

                # Convert to tensor
                composite_mask = np.array(image)
                composite_mask_tensor = torch.from_numpy(
                    composite_mask.astype(np.float32) / 255.0
                )[None,]

                # Define the 8 known color codes in the mask
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
                    tuple(int(c.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    for c in color_codes
                ]

                # Generate individual masks
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

                # Ensure all masks have the same shape if needed
                for i in range(len(individual_masks)):
                    if individual_masks[i].shape != individual_masks[0].shape:
                        individual_masks[i] = torch.nn.functional.interpolate(
                            individual_masks[i],
                            size=individual_masks[0].shape[2:],
                            mode='nearest'
                        )

                # Return composite + 8 masks
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
                print(f"Mask request returned status code {mask_request.status_code}")
                return [default_value] * 9

        except Exception as e:
            print(f"Error while processing masks: {e}")
            return [default_value] * 9


NODE_CLASS_MAPPINGS = {
    "Playbook Mask": MaskRenderPass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Mask": "Playbook Mask Render Passes"
}
