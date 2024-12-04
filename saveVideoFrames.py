# saveVideoFrames.py
import os
import torch
from PIL import Image
import numpy as np

class SaveVideoFrames:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_frames": ("VIDEO",),
                "output_folder": ("STRING", {"multiline": False, "default": "./output_frames"}),
                "file_prefix": ("STRING", {"multiline": False, "default": "frame_"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_frames"
    CATEGORY = "Utility"

    OUTPUT_NODE = True

    def save_frames(self, video_frames, output_folder="./output_frames", file_prefix="frame_"):
        os.makedirs(output_folder, exist_ok=True)
        num_frames = video_frames.shape[0]

        for idx in range(num_frames):
            frame_tensor = video_frames[idx]
            frame_np = frame_tensor.permute(1, 2, 0).numpy() * 255.0
            frame_np = np.clip(frame_np, 0, 255).astype(np.uint8)
            frame_image = Image.fromarray(frame_np)
            frame_image.save(os.path.join(output_folder, f"{file_prefix}{idx:04d}.png"))

        print(f"Saved {num_frames} frames to {output_folder}")
        return []

NODE_CLASS_MAPPINGS = {
    "Save Video Frames": SaveVideoFrames
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Save Video Frames": "Save Video Frames"
}
