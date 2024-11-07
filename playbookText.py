class PlaybookText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return{
            "required": {
                "name": ("STRING", { "multiline": False, "default": "Playbook Text ID"},),
            },
            "optional": {
                "text": ("STRING", {"multiline": True},),
                "trigger_words": ("STRING", {"multiline": True})
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Text", "Trigger Words")

    FUNCTION = "parse_text"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook3 d"

    def parse_text(self, text = None, trigger_words = None):
        return [text, trigger_words]
    
NODE_CLASS_MAPPINGS = { "Playbook Text": PlaybookText}
NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Text": "Playbook Text (External)"}
