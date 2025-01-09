class AspectRatioSelect:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
                "dropdown_option": (
                    "STRING",
                    {
                        "WIDGET": "COMBO",
                        "VALUES": ["Option1", "Option2", "Option3"],
                        "DEFAULT": "Option1",
                    },
                ),
            }
        }

    # RETURN_TYPES = ("INT", "INT")
    RETURN_TYPES = "STRING"
    # RETURN_NAMES = ("x", "y")
    RETURN_NAMES = "x"

    FUNCTION = "return_aspect_ratio"

    OUTPUT_NODE = {False}

    CATEGORY = "Playbook 3D"

    def get_aspect_ratio(self, id, label, aspect_ratio):
        return aspect_ratio


NODE_CLASS_MAPPINGS = {"Playbook Aspect Ratio Select": AspectRatioSelect}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Aspect Ratio Select": "Playbook Aspect Ratio Select"
}
