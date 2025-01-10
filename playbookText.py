import hashlib
import time

class PlaybookText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return{
            "required": {
                "id": ("STRING", { "multiline": False, "default": "Node ID"},),
                "label": ("STRING", { "multiline": False, "default": "Node Label"},),
            },
            "optional": {
                "default_value": ("STRING", {"multiline": True},),
                "trigger_words": ("STRING", {"multiline": True})
            }
        }

    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "trigger_words")

    FUNCTION = "parse_text"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_text(self, id, label, default_value = None, trigger_words = None):
        return [default_value, trigger_words]
    
NODE_CLASS_MAPPINGS = { "Playbook Text": PlaybookText}
NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Text": "Playbook Text (External)"}
