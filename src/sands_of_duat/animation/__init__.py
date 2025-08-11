"""
Animation Module - ComfyUI Integration for Egyptian Card Generation
Automated pipeline for generating Egyptian-themed card animations.
"""

# Optional imports to prevent game startup failures
try:
    from .comfyui_integration import ComfyUIManager, AnimationRequest
    from .animation_pipeline import AnimationPipeline, PipelineStatus
    from .card_animation_generator import CardAnimationGenerator
    from .rtx_optimization import RTXOptimizer
    
    ANIMATION_SYSTEM_AVAILABLE = True
    
    __all__ = [
        'ComfyUIManager',
        'AnimationRequest', 
        'AnimationPipeline',
        'PipelineStatus',
        'CardAnimationGenerator',
        'RTXOptimizer'
    ]
    
except ImportError as e:
    print(f"Animation system not available: {e}")
    ANIMATION_SYSTEM_AVAILABLE = False
    
    # Create dummy classes to prevent import errors
    class ComfyUIManager:
        def __init__(self): pass
        async def initialize(self): return False
        
    class AnimationRequest:
        def __init__(self, **kwargs): pass
        
    class AnimationPipeline:
        def __init__(self): pass
        async def initialize(self): return False
        
    class PipelineStatus:
        IDLE = "idle"
        
    class CardAnimationGenerator:
        def __init__(self): pass
        async def initialize(self): return False
        
    class RTXOptimizer:
        def __init__(self): pass
        def initialize(self): return False
    
    __all__ = []