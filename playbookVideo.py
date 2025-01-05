import torch
import numpy as np
import cv2
import requests
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
                "default_value": ("IMAGE",),
                "url": ("STRING", {"multiline": False, "default": ""})
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "parse_video"
    OUTPUT_NODE = False
    CATEGORY = "Playbook 3D"

    def parse_video(self, id, label, url="", frame_load_cap=0, skip_first_frames=0, select_every_nth=1, default_value=None):
        try:
            frames = []
            if url and url.startswith('http'):
                print(f"Debug: Downloading video from {url}")
                video_request = requests.get(url, stream=True)
                if video_request.status_code != 200:
                    print(f"Debug: Failed to download video, status code: {video_request.status_code}")
                    if default_value is not None:
                        print("Debug: Using default value")
                        return (default_value,)
                    return (None,)

                # Download and process video
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
                    for chunk in video_request.iter_content(chunk_size=8192):
                        if chunk:
                            temp_video_file.write(chunk)
                    temp_video_file_path = temp_video_file.name

                try:
                    cap = cv2.VideoCapture(temp_video_file_path)
                    frame_counter = 0
                    frames_loaded = 0
                    print("Debug: Starting frame extraction")

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break

                        frame_counter += 1
                        if frame_counter <= skip_first_frames:
                            continue
                        if (frame_counter - skip_first_frames - 1) % select_every_nth != 0:
                            continue

                        # Convert BGR to RGB
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # Convert to float32 and normalize to 0-1 range
                        frame = frame.astype(np.float32) / 255.0
                        # Convert to tensor and keep in [H, W, C] format
                        frame_tensor = torch.from_numpy(frame)
                        frames.append(frame_tensor)

                        frames_loaded += 1
                        if frame_load_cap > 0 and frames_loaded >= frame_load_cap:
                            break

                    cap.release()
                finally:
                    try:
                        os.unlink(temp_video_file_path)
                    except:
                        pass

                if frames:
                    print(f"Debug: Processed {len(frames)} frames")
                    frames_tensor = torch.stack(frames)  # [N, H, W, C]
                    print(f"Debug: Final tensor shape: {frames_tensor.shape}")
                    print(f"Debug: Final tensor dtype: {frames_tensor.dtype}")
                    return (frames_tensor,)

            # If no valid URL or no frames extracted
            print("Debug: No valid URL or no frames extracted")
            if default_value is not None:
                print("Debug: Using default value")
                return (default_value,)
            return (None,)

        except Exception as e:
            print(f"Debug: Exception occurred: {str(e)}")
            if default_value is not None:
                print("Debug: Using default value after exception")
                return (default_value,)
            return (None,)

NODE_CLASS_MAPPINGS = {
    "Playbook Video": PlaybookVideo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Video": "Playbook Video (External)"
}