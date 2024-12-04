from .depthPass import DepthRenderPass
from .outlinePass import OutlineRenderPass
from .maskPass import MaskRenderPass
from .beautyPass import BeautyRenderPass
from .renderResult import UploadRenderResult
from .playbookBoolean import PlaybookBoolean
from .playbookFloat import PlaybookFloat
from .playbookNumber import PlaybookNumber
from .playbookText import PlaybookText
from .playbookImage import PlaybookImage
from .playbookVideo import PlaybookVideo
from .saveVideoFrames import SaveVideoFrames


NODE_CLASS_MAPPINGS = {
    "Playbook Depth": DepthRenderPass,
    "Playbook Outline": OutlineRenderPass,
    "Playbook Mask": MaskRenderPass,
    "Playbook Beauty": BeautyRenderPass,
    "Playbook Render Result": UploadRenderResult,
    "Playbook Boolean": PlaybookBoolean,
    "Playbook Float": PlaybookFloat,
    "Playbook Number": PlaybookNumber,
    "Playbook Text": PlaybookText,
    "Playbook Image": PlaybookImage,
    "Playbook Video": PlaybookVideo,
    "Playbook Save Frames": SaveVideoFrames
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Depth": "Playbook Depth Render Pass",
    "Playbook Outline": "Playbook Outline Render Pass",
    "Playbook Mask": "Playbook Mask Render Pass",
    "Playbook Beauty": "Playbook Beauty Render Pass",
    "Playbook Render Result": "Playbook Render Result",
    "Playbook Boolean": "Playbook Boolean (External)",
    "Playbook Float": "Playbook Float (External)",
    "Playbook Number": "Playbook Number (External)",
    "Playbook Text": "Playbook Text (External)",
    "Playbook Image": "Playbook Image (External)",
    "Playbook Video": "Playbook Video (External)",
    "Playbook Save Frames": "Playbook Select Video Frame",
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']