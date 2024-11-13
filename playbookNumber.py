class PlaybookNumber:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"} ),
                "label": ("STRING", {"multiline": False, "default": "Node Label"} ),
            },
            "optional": {
                "default_value": ("INT",
                    {
                        "multiline": True, 
                        "display": "number", 
                        "min": -100,
                        "max": 100,
                        "default": 0
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("Int",)

    FUNCTION = "parse_number"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_number(self, id, label, default_value = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            return [default_value]
        return [int(id)]


NODE_CLASS_MAPPINGS = { "Playbook Number": PlaybookNumber }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Number": "Playbook Number (External)" }