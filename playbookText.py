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
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Text", "Trigger Words")

    FUNCTION = "parse_text"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook 3D"

    def parse_text(self, id, default_value = None, trigger_words = None):
        return [default_value, trigger_words]
    
NODE_CLASS_MAPPINGS = { "Playbook Text": PlaybookText}
NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Text": "Playbook Text (External)"}
