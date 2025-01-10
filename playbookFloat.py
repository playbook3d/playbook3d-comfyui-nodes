import hashlib
import time

import numpy as np

class PlaybookFloat:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
                "min": ("FLOAT", {"multiline": False, "default": 0, "display": "number"}),
                "max": ("FLOAT", {"multiline": False, "default": 0, "display": "number"}),
            },
            "optional": {
                "default_value": ("FLOAT",
                    {
                        "multiline": True, 
                        "display": "number", 
                        "min": -2147483647,
                        "max": 2147483647,
                        "default": 0,
                        "step": 0.1
                    },
                ),
            }
        }

    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)

    FUNCTION = "parse_float"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_float(self, id, label, min, max, default_value = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            clamped_float = np.clip(default_value, min, max)
            return [clamped_float]
        clamped_float_id = np.clip(float(id), min, max)
        return [clamped_float_id]

NODE_CLASS_MAPPINGS = { "Playbook Float": PlaybookFloat }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Float": "Playbook Float (External)" }