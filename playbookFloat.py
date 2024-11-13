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
                "min": ("FLOAT", {"multiline": False, "default": "Min"}),
                "max": ("FLOAT", {"multiline": False, "default": "Max"}),
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

    def parse_float(self, id, label, min, max, default_value = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            return [np.clip(default_value, min, max)]
        float_id = float(id)
        return [np.clip(float_id, min, max)]

NODE_CLASS_MAPPINGS = { "Playbook Float": PlaybookFloat }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Float": "Playbook Float (External)" }