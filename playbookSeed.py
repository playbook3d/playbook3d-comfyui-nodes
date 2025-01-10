import hashlib
import time
import random


class PlaybookSeed:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "default_value": ("INT", {"multiline": False, "default": 0, "min": 0}),
                "setting": (["Fixed", "Random"],),
            },
        }

    @classmethod
    def IS_CHANGED(s, image):
        # always update
        m = hashlib.sha256().update(str(time.time()).encode("utf-8"))
        return m.digest().hex()

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)

    FUNCTION = "get_seed"

    OUTPUT_NODE = {False}

    CATEGORY = "Playbook 3D"

    def get_seed(self, default_value, setting):
        """
        Returns a seed depending on the chosen setting.
        If setting is "Fixed", returns the given default_value.
        If setting is "Random", returns a randomly generated seed.
        """

        if setting == "Fixed":
            return default_value

        return self.generate_random_seed()

    def generate_random_seed(self, num_digits=15) -> int:
        """
        Generate a random seed with num_digits number of digits.
        """

        range_start = 10 ** (num_digits - 1)
        range_end = (10**num_digits) - 1
        return random.randint(range_start, range_end)


NODE_CLASS_MAPPINGS = {"Playbook Seed": PlaybookSeed}
NODE_DISPLAY_NAME_MAPPINGS = {"Playbook Seed": "Playbook Seed"}
