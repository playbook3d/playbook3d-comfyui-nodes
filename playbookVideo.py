# playbookVideo.py
import torch
import numpy as np
import cv2
import requests
from io import BytesIO
import tempfile
import os

class PlaybookVideo:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("STRING", {"multiline": False, "default": "Node ID"}),
                "label": ("STRING", {"multiline": False, "default": "Node Label"}),
                "frame_load_cap": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "skip_first_frames": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
                "select_every_nth": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),
            },
            "optional": {
                "default_value": ("VIDEO",)
            },
        }

    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("Video",)

    FUNCTION = "parse_video"

    OUTPUT_NODE = False

    CATEGORY = "Playbook 3D"

    def parse_video(self, id, label, frame_load_cap=0, skip_first_frames=0, select_every_nth=1, default_value=None):
        video_url = id
        video = default_value
        frames = []
        try:
            if id.startswith('http'):
                video_request = requests.get(video_url, stream=True)
                if video_request.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
                        for chunk in video_request.iter_content(chunk_size=1024):
                            if chunk:
                                temp_video_file.write(chunk)
                        temp_video_file_path = temp_video_file.name

                    cap = cv2.VideoCapture(temp_video_file_path)
                else:
                    raise ValueError("Failed to download video")
            else:
                raise ValueError("Invalid URL")

            frame_counter = 0
            frames_loaded = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_counter += 1

                if frame_counter <= skip_first_frames:
                    continue

                if (frame_counter - skip_first_frames - 1) % select_every_nth != 0:
                    continue

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = frame.astype(np.float32) / 255.0
                frame_tensor = torch.from_numpy(frame).permute(2, 0, 1)

                frames.append(frame_tensor)

                frames_loaded += 1
                if frame_load_cap > 0 and frames_loaded >= frame_load_cap:
                    break

            cap.release()

            if os.path.exists(temp_video_file_path):
                os.remove(temp_video_file_path)

            if frames:
                video = torch.stack(frames)

            return [video]
        except Exception as e:
            print(f"Exception while downloading or processing video: {e}")
            return [video]

NODE_CLASS_MAPPINGS = {
    "Playbook Video": PlaybookVideo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Video": "Playbook Video (External)"
}
