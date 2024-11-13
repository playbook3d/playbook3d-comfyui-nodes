class PlaybookFloat:
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
                "default_value": ("FLOAT",
                    {
                        "multiline": True, 
                        "display": "number", 
                        "min": -2147483647, 
                        "max": 2147483647, 
                        "default": 0,
                        "step": 0.01
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("Float",)

    FUNCTION = "parse_float"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_float(self, id, label, default_value = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            return [default_value]
        return [float(id)]


NODE_CLASS_MAPPINGS = { "Playbook Float": PlaybookFloat }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Float": "Playbook Float (External)" }