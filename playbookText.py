class PlaybookText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return{
            "required": {
                "id": ("STRING", { "multiline": False, "default": "Playbook Text ID"},),
            },
            "optional": {
                "text": ("STRING", {"multiline": True},)
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Text",)

    FUNCTION = "parse_text"

    OUTPUT_NODE = { False }

    CATEGORY = "Playbook3 d"

    def parse_text(self, text = None):
        return [text]
    
NODE_CLASS_MAPPINGS = { "Playbook Text": PlaybookText}
NODE_DISPLAY_NAME_MAPPINGS = { "Playbook Text": "Playbook Text (External)"}
