import hashlib
import time

class PlaybookBoolean:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
                "default_value": ("BOOLEAN", {"default": False})
            },
        }

    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ( "BOOLEAN", )
    RETURN_NAMES = ("Boolean", )

    FUNCTION = "parse_boolean"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_boolean(self, id, label, default_value):
        return [default_value]


NODE_CLASS_MAPPINGS = { "Playbook Boolean": PlaybookBoolean }

NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Boolean": "Playbook Boolean (External)" }