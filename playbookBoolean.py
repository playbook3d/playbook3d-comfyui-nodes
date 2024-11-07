class PlaybookBoolean:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "name": ("STRING", {"multiline": False, "default": "Playbook Boolean ID"}),
                "playbook_bool": ("BOOLEAN", {"default": False})
            },
        }

    RETURN_TYPES = ( "BOOLEAN", )
    RETURN_NAMES = ("Boolean", )

    FUNCTION = "parse_boolean"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_boolean(self, name,  playbook_bool = None):
        return [playbook_bool]


NODE_CLASS_MAPPINGS = { "Playbook Boolean": PlaybookBoolean }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Boolean": "Playbook Boolean (External)" }