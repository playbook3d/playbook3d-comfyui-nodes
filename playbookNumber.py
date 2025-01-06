import numpy as np

class PlaybookNumber:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"} ),
                "label": ("STRING", {"multiline": False, "default": "Node Label"} ),
                "min": ("INT", {"multiline": False, "default": 0, "display": "number"} ),
                "max": ("INT", {"multiline": False, "default": 100, "display": "number"} ),
            },
            "optional": {
                "default_value": ("INT",
                    {
                        "multiline": True, 
                        "display": "number", 
                        "min": -2147483647,
                        "max": 2147483647,
                        "default": 0
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("number",)

    FUNCTION = "parse_number"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_number(self, id, min, max, label, default_value = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            return [np.clip(default_value, min, max)]
        id_int = int(id)
        return [np.clip(id_int, min, max)]


NODE_CLASS_MAPPINGS = { "Playbook Number": PlaybookNumber }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Number": "Playbook Number (External)" }