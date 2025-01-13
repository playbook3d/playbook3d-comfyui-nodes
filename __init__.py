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
from .beautyPassSequence import BeautyRenderPassSequence
from .depthPassSequence import DepthRenderPassSequence
from .maskPassSequence import MaskRenderPassSequence
from .outlinePassSequence import OutlineRenderPassSequence
from .playbookVideo import PlaybookVideo
from .playbookAspectRatioSelect import PlaybookAspectRatioSelect
from .playbookLoraSelect import PlaybookLoRASelection
from .playbookSeed import PlaybookSeed

NODE_CLASS_MAPPINGS = {
    "Playbook Depth": DepthRenderPass,
    "Playbook Depth Sequence": DepthRenderPassSequence,
    "Playbook Outline": OutlineRenderPass,
    "Playbook Outline Sequence": OutlineRenderPassSequence,
    "Playbook Mask": MaskRenderPass,
    "Playbook Mask Sequence": MaskRenderPassSequence,
    "Playbook Beauty": BeautyRenderPass,
    "Playbook Beauty Sequence": BeautyRenderPassSequence,
    "Playbook Render Result": UploadRenderResult,
    "Playbook Boolean": PlaybookBoolean,
    "Playbook Float": PlaybookFloat,
    "Playbook Number": PlaybookNumber,
    "Playbook Text": PlaybookText,
    "Playbook Image": PlaybookImage,
    "Playbook Video": PlaybookVideo,
    "Playbook Aspect Ratio Select": PlaybookAspectRatioSelect,
    "Playbook LoRA Select": PlaybookLoRASelection,
    "Playbook Seed": PlaybookSeed,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Playbook Depth": "Playbook Depth Render Pass",
    "Playbook Depth Sequence": "Playbook Depth Render Pass Sequence",
    "Playbook Outline": "Playbook Outline Render Pass",
    "Playbook Outline Sequence": "Playbook Outline Render Pass Sequence",
    "Playbook Mask": "Playbook Mask Render Pass",
    "Playbook Mask Sequence": "Playbook Mask Render Pass Sequence",
    "Playbook Beauty": "Playbook Beauty Render Pass",
    "Playbook Beauty Sequence": "Playbook Beauty Render Pass Sequence",
    "Playbook Render Result": "Playbook Render Result",
    "Playbook Boolean": "Playbook Boolean (External)",
    "Playbook Float": "Playbook Float (External)",
    "Playbook Number": "Playbook Number (External)",
    "Playbook Text": "Playbook Text (External)",
    "Playbook Image": "Playbook Image (External)",
    "Playbook Video": "Playbook Video (External)",
    "Playbook Aspect Ratio Select": "Playbook Aspect Ratio Select (External)",
    "Playbook LoRA Select": "Playbook LoRA Select (External)",
    "Playbook Seed": "Playbook Seed",
}


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
