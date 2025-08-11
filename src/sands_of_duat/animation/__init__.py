"""
Animation Module - ComfyUI Integration for Egyptian Card Generation
Automated pipeline for generating Egyptian-themed card animations.
"""

from .comfyui_integration import ComfyUIManager, AnimationRequest
from .animation_pipeline import AnimationPipeline, PipelineStatus
from .card_animation_generator import CardAnimationGenerator
from .rtx_optimization import RTXOptimizer

__all__ = [
    'ComfyUIManager',
    'AnimationRequest', 
    'AnimationPipeline',
    'PipelineStatus',
    'CardAnimationGenerator',
    'RTXOptimizer'
]