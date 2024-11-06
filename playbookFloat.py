class PlaybookFloat:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Playbook Float ID"})
            },
            "optional": {
                "playbook_float": ("FLOAT",
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

    RETURN_TYPES = { "FLOAT", }
    RETURN_NAMES = { "Float", }

    FUNCTION = "parse_float"

    OUTPUT_NODE = {}

    CATEGORY = { "Playbook 3D" }

    def parse_float(self, id,  playbook_number = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            return [playbook_number]
        return [float(id)]


NODE_CLASS_MAPPINGS = { "Playbook Float": PlaybookFloat }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Float": "Playbook Float (External)" }