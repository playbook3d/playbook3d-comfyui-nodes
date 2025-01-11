import hashlib
import time

class PlaybookLoRASelection:
    def init(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "default_value": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "LoRA name."
                    }
                ),
                "id": (
                    "STRING",
                    {
                        "default": "Node ID",
                        "multiline": False,
                        "tooltip": "LoRA selection node identifier"
                    }
                ),
                "label": (
                    "STRING",
                    {
                        "default": "Node Label",
                        "multiline": False,
                        "tooltip": "LoRA selection node's label"
                    }
                ),
                "base_model": (
                    ["SD1.5", "SDXL", "CogVideoX", "Flux"],
                    {
                        "default": "SD1.5",
                        "tooltip": "Which base model is this LoRA meant for?"
                    }
                ),
            }
        }
    
    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("lora_name",)
    FUNCTION = "parse_lora"
    OUTPUT_NODE = {False}
    CATEGORY = "Playbook 3D"

    def parse_lora(self, default_value, id, label, base_model):
        return (default_value,)

NODE_CLASS_MAPPINGS = {
    "Playbook LoRA Selection": PlaybookLoRASelection
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook LoRA Selection": "Playbook LoRA Selection (Dynamic Input)"
}
