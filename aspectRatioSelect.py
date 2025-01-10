import hashlib
import time


class AspectRatioSelect:
    def __init__(self):
        self.aspect_dict = {
            "1:1": (1, 1),
            "16:9": (16, 9),
            "9:16": (9, 16),
            "4:3": (4, 3),
            "3:4": (3, 4),
        }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
                "default_value": (["1:1", "16:9", "9:16", "4:3", "3:4"],),
            }
        }

    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("x", "y")

    FUNCTION = "get_aspect_ratio"

    OUTPUT_NODE = {False}

    CATEGORY = "Playbook 3D"

    def get_aspect_ratio(self, id, label, default_value):
        ratio = self.aspect_dict.get(default_value, (1, 1))

        return ratio


NODE_CLASS_MAPPINGS = {"Playbook Aspect Ratio Select": AspectRatioSelect}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Aspect Ratio Select": "Playbook Aspect Ratio Select"
}
