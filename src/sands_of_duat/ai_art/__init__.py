"""
AI Art Generation Module for Sands of Duat - RTX 5070 CUDA 12.8 Optimized
==========================================================================

RTX 5070 maximum quality Egyptian art generation with ComfyUI local API.
NO FALLBACKS - NO PLACEHOLDERS - HADES QUALITY ONLY
"""

from .ai_generation_pipeline import (
    LocalSDXLGenerator,
    HadesEgyptianPrompts,
    EgyptianArtPipeline,
    get_pipeline,
    generate_all_egyptian_cards
)

__all__ = [
    'LocalSDXLGenerator',
    'HadesEgyptianPrompts',
    'EgyptianArtPipeline', 
    'get_pipeline',
    'generate_all_egyptian_cards'
]