class PlaybookNumber:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("INT", )
            },
            "optional": {
                "playbook_number": ("INT",
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

    RETURN_TYPES = { "INT", }
    RETURN_NAMES = { "Int", }

    FUNCTION = "parse_number"

    OUTPUT_NODE = {}

    CATEGORY = { "Playbook 3D" }

    def parse_number(self, id,  playbook_number = None):
        if not id or (isinstance(id, str) and not id.strip().isdigit()):
            return [playbook_number]
        return [int(id)]


NODE_CLASS_MAPPINGS = { "Playbook Number": PlaybookNumber }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Number": "Playbook Number (External)" }