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
                "min_float": ("FLOAT", {"multiline": False, "default": "Min"}),
                "max_float": ("FLOAT", {"multiline": False, "default": "Max"}),
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

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("Float",)

    FUNCTION = "parse_float"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_float(self, id, label, min_float, max_float, default_value = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            clamped_float = np.clip(default_value, min_float, max_float)
            return [clamped_float]
        clamped_float_id = np.clip(float(id), min_float, max_float)
        return [clamped_float_id]

NODE_CLASS_MAPPINGS = { "Playbook Float": PlaybookFloat }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Float": "Playbook Float (External)" }