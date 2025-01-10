class AspectRatioSelect:
    def __init__(self):
        self.aspect_dict = {
            "1:1": (1, 1),
            "16:9": (16, 9),
            "9:16": (4, 3),
            "4:3": (4, 3),
            "3:4": (4, 3),
        }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
                "aspect_ratio": (["1:1", "16:9", "9:16", "4:3", "3:4"],),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("x", "y")

    FUNCTION = "get_aspect_ratio"

    OUTPUT_NODE = {False}

    CATEGORY = "Playbook 3D"

    def get_aspect_ratio(self, id, label, aspect_ratio):
        ratio = self.aspect_dict[aspect_ratio]

        return {"x": ratio[0], "y": ratio[1]}


NODE_CLASS_MAPPINGS = {"Playbook Aspect Ratio Select": AspectRatioSelect}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Aspect Ratio Select": "Playbook Aspect Ratio Select"
}
