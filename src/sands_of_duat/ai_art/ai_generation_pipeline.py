"""
SANDS OF DUAT - AI ART GENERATION PIPELINE
==========================================

Professional AI art generation system for creating consistent Egyptian underworld artwork.
Uses trained models and standardized prompts to generate high-quality game assets.
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum, auto
import logging

logger = logging.getLogger(__name__)

class AIModel(Enum):
    """Supported AI models for art generation."""
    STABLE_DIFFUSION_XL = "sdxl"
    MIDJOURNEY = "midjourney"
    DALLE3 = "dalle3"
    FLUX_PRO = "flux_pro"
    LOCAL_LORA = "local_lora"

class ArtCategory(Enum):
    """Categories of artwork to generate."""
    CARD_ART = auto()
    BACKGROUND = auto()
    UI_ELEMENT = auto()
    CHARACTER_PORTRAIT = auto()
    ENVIRONMENTAL = auto()

class ArtStyle(Enum):
    """Art style variations."""
    STANDARD = "sands_of_duat_style"
    DETAILED = "sands_of_duat_style, highly_detailed"
    CINEMATIC = "sands_of_duat_style, cinematic_lighting"
    MYSTICAL = "sands_of_duat_style, mystical_atmosphere"

@dataclass
class GenerationRequest:
    """Request for AI art generation."""
    name: str
    category: ArtCategory
    base_prompt: str
    style: ArtStyle = ArtStyle.STANDARD
    model: AIModel = AIModel.STABLE_DIFFUSION_XL
    width: int = 512
    height: int = 512
    steps: int = 30
    cfg_scale: float = 7.5
    seed: Optional[int] = None
    negative_prompt: str = ""
    
    # Quality control
    min_quality_score: float = 0.75
    max_attempts: int = 3
    
    # Metadata
    card_name: Optional[str] = None
    card_type: Optional[str] = None
    rarity: Optional[str] = None

@dataclass
class GenerationResult:
    """Result of AI art generation."""
    request: GenerationRequest
    success: bool
    image_path: Optional[str] = None
    quality_score: float = 0.0
    generation_time: float = 0.0
    attempts: int = 0
    error_message: Optional[str] = None
    model_metadata: Dict[str, Any] = None

class EgyptianPromptLibrary:
    """
    Standardized prompt library for HADES-QUALITY Egyptian underworld artwork.
    Targets the same artistic excellence as Supergiant Games' Hades.
    """
    
    BASE_STYLE = "sands_of_duat_style, egyptian_underworld_art, hades_game_art_quality"
    
    # Hades-quality art specifications
    HADES_QUALITY_ELEMENTS = [
        "supergiant_games_style",
        "hand_painted_illustration", 
        "vibrant_saturated_colors",
        "dramatic_lighting_contrasts",
        "painterly_brush_strokes",
        "professional_game_artwork",
        "award_winning_art_direction"
    ]
    
    # Core Egyptian elements with Hades-level detail
    EGYPTIAN_ELEMENTS = {
        "gods": "majestic egyptian deity, golden divine regalia, intricate hieroglyphic details, powerful divine presence, hades_character_quality",
        "artifacts": "ornate ancient egyptian artifact, gleaming gold and lapis lazuli, sacred hieroglyphic inscriptions, mystical aura, hades_item_quality",
        "locations": "atmospheric egyptian underworld chamber, dramatic torch lighting, mysterious hieroglyphic walls, rich architectural details, hades_environment_quality", 
        "spells": "dynamic egyptian mythological magic, swirling divine energy, golden mystical effects, dramatic spell casting, hades_effect_quality",
        "creatures": "imposing sacred egyptian creature, detailed mythological anatomy, divine markings, fierce expression, hades_creature_quality",
        "backgrounds": "cinematic egyptian underworld environment, layered atmospheric lighting, rich architectural depth, hades_background_quality"
    }
    
    # Hades-level quality enhancers
    QUALITY_ENHANCERS = [
        "highly detailed",
        "masterpiece_quality",
        "supergiant_games_art_style",
        "hades_game_aesthetic",
        "vibrant_rich_colors",
        "dramatic_contrasts",
        "hand_painted_texture",
        "award_winning_illustration",
        "professional_game_art",
        "painterly_style",
        "4k_resolution"
    ]
    
    # Lighting and atmosphere
    LIGHTING_STYLES = {
        "divine": "divine golden light, heavenly glow",
        "mystical": "mystical purple aura, magical energy",
        "underworld": "dim torchlight, mysterious shadows",
        "solar": "brilliant solar rays, warm golden hour",
        "moonlit": "silver moonlight, ethereal glow"
    }
    
    # Negative prompts to avoid - ensuring Hades-level quality
    NEGATIVE_PROMPTS = [
        "blurry", "low_quality", "pixelated", "watermark", "text", "signature",
        "amateur", "sketch", "unfinished", "draft", "placeholder",
        "modern_elements", "non_egyptian", "inappropriate", "ugly", "deformed",
        "bad_anatomy", "poorly_drawn", "amateur_art", "low_resolution",
        "jpeg_artifacts", "compression_artifacts", "washed_out_colors",
        "flat_lighting", "boring", "generic", "cheap_looking", "rushed",
        "inconsistent_style", "photorealistic", "3d_render", "photography"
    ]
    
    def create_card_prompt(self, card_name: str, card_type: str, 
                          rarity: str = "common") -> str:
        """Create optimized prompt for card artwork."""
        
        # Get base elements for card type
        type_key = card_type.lower()
        if type_key in self.EGYPTIAN_ELEMENTS:
            type_elements = self.EGYPTIAN_ELEMENTS[type_key]
        else:
            type_elements = self.EGYPTIAN_ELEMENTS["artifacts"]
        
        # Enhance based on rarity
        quality_level = "detailed artwork"
        if rarity == "rare":
            quality_level = "highly detailed, premium artwork"
        elif rarity == "legendary":
            quality_level = "masterpiece quality, legendary artwork, divine aura"
        
        # Combine prompt elements
        prompt_parts = [
            self.BASE_STYLE,
            type_elements,
            quality_level,
            "professional game card art",
            "rich egyptian colors",
            "intricate details"
        ]
        
        return ", ".join(prompt_parts)
    
    def create_background_prompt(self, scene_type: str) -> str:
        """Create prompt for background/environment art."""
        
        scene_elements = {
            "main_menu": "grand egyptian temple entrance with golden pillars",
            "combat": "egyptian underworld battlefield with mystical energy",
            "deck_builder": "ancient egyptian library with scrolls and artifacts",
            "collection": "pharaoh's treasure chamber with golden artifacts",
            "settings": "egyptian temple inner sanctum with hieroglyphic walls",
            "victory": "radiant egyptian paradise with golden light",
            "defeat": "dark egyptian underworld with mysterious shadows"
        }
        
        scene_desc = scene_elements.get(scene_type, scene_elements["main_menu"])
        
        prompt_parts = [
            self.BASE_STYLE,
            scene_desc,
            "cinematic composition",
            "atmospheric lighting", 
            "rich egyptian architecture",
            "game background art"
        ]
        
        return ", ".join(prompt_parts)
    
    def get_negative_prompt(self) -> str:
        """Get standardized negative prompt."""
        return ", ".join(self.NEGATIVE_PROMPTS)

class AIArtGenerator:
    """
    Main AI art generation system with multiple model support.
    """
    
    def __init__(self, output_dir: str = "assets/generated_art"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.prompt_library = EgyptianPromptLibrary()
        self.generation_log: List[GenerationResult] = []
        
        # Model configurations
        self.model_configs = {
            AIModel.STABLE_DIFFUSION_XL: {
                "api_endpoint": None,  # Configure based on service
                "default_size": (1024, 1024),
                "max_steps": 50
            },
            AIModel.LOCAL_LORA: {
                "model_path": "assets/models/sands_of_duat_lora.safetensors",
                "base_model": "sdxl_base_1.0.safetensors",
                "default_size": (768, 768)
            }
        }
        
        logger.info("AI Art Generator initialized - Chamber of Creation ready")
    
    def generate_card_art(self, card_name: str, card_type: str, 
                         rarity: str = "common") -> GenerationResult:
        """Generate artwork for a specific card."""
        
        # Create generation request
        prompt = self.prompt_library.create_card_prompt(card_name, card_type, rarity)
        
        request = GenerationRequest(
            name=f"card_{card_name.lower().replace(' ', '_')}",
            category=ArtCategory.CARD_ART,
            base_prompt=prompt,
            negative_prompt=self.prompt_library.get_negative_prompt(),
            width=512, height=640,  # Card aspect ratio
            card_name=card_name,
            card_type=card_type,
            rarity=rarity
        )
        
        return self.generate_artwork(request)
    
    def generate_background_art(self, scene_type: str) -> GenerationResult:
        """Generate background artwork for game scenes."""
        
        prompt = self.prompt_library.create_background_prompt(scene_type)
        
        request = GenerationRequest(
            name=f"bg_{scene_type}",
            category=ArtCategory.BACKGROUND,
            base_prompt=prompt,
            negative_prompt=self.prompt_library.get_negative_prompt(),
            width=1920, height=1080,  # Screen resolution
            style=ArtStyle.CINEMATIC
        )
        
        return self.generate_artwork(request)
    
    def generate_artwork(self, request: GenerationRequest) -> GenerationResult:
        """Generate artwork based on request."""
        start_time = time.time()
        
        logger.info(f"Generating artwork: {request.name}")
        logger.info(f"Prompt: {request.base_prompt}")
        
        try:
            # Route to appropriate model
            if request.model == AIModel.STABLE_DIFFUSION_XL:
                result = self._generate_with_sdxl(request)
            elif request.model == AIModel.LOCAL_LORA:
                result = self._generate_with_local_lora(request)
            else:
                raise NotImplementedError(f"Model {request.model} not yet implemented")
            
            result.generation_time = time.time() - start_time
            self.generation_log.append(result)
            
            if result.success:
                logger.info(f"✓ Generated: {result.image_path} (Quality: {result.quality_score:.2f})")
            else:
                logger.warning(f"✗ Generation failed: {result.error_message}")
            
            return result
            
        except Exception as e:
            error_result = GenerationResult(
                request=request,
                success=False,
                error_message=str(e),
                generation_time=time.time() - start_time
            )
            self.generation_log.append(error_result)
            logger.error(f"Generation error: {e}")
            return error_result
    
    def _generate_with_sdxl(self, request: GenerationRequest) -> GenerationResult:
        """Generate using Stable Diffusion XL (placeholder for API integration)."""
        
        # This would integrate with actual SDXL API
        # For now, return a mock result indicating where integration is needed
        
        return GenerationResult(
            request=request,
            success=False,
            error_message="SDXL API integration needed - configure your preferred AI service",
            attempts=1
        )
    
    def _generate_with_local_lora(self, request: GenerationRequest) -> GenerationResult:
        """Generate using local LoRA model (placeholder for local generation)."""
        
        # This would integrate with local Stable Diffusion + LoRA
        # For now, return a mock result indicating where integration is needed
        
        return GenerationResult(
            request=request,
            success=False,
            error_message="Local LoRA generation needs ComfyUI or Automatic1111 setup",
            attempts=1
        )
    
    def _evaluate_quality(self, image_path: str, request: GenerationRequest) -> float:
        """Evaluate the quality of generated artwork."""
        
        # This would implement automated quality assessment
        # For now, return a placeholder score
        
        return 0.8  # Mock quality score
    
    def batch_generate_cards(self, card_list: List[Dict[str, str]]) -> List[GenerationResult]:
        """Generate artwork for multiple cards."""
        results = []
        
        logger.info(f"Starting batch generation for {len(card_list)} cards")
        
        for i, card_info in enumerate(card_list):
            logger.info(f"Generating card {i+1}/{len(card_list)}: {card_info['name']}")
            
            result = self.generate_card_art(
                card_info['name'],
                card_info['type'],
                card_info.get('rarity', 'common')
            )
            
            results.append(result)
            
            # Small delay between generations to avoid rate limiting
            time.sleep(1)
        
        successful = sum(1 for r in results if r.success)
        logger.info(f"Batch complete: {successful}/{len(results)} successful")
        
        return results
    
    def export_generation_report(self, filename: str = "generation_report.json"):
        """Export detailed report of all generations."""
        
        report = {
            "timestamp": time.time(),
            "total_generations": len(self.generation_log),
            "successful_generations": sum(1 for r in self.generation_log if r.success),
            "average_quality": sum(r.quality_score for r in self.generation_log) / len(self.generation_log) if self.generation_log else 0,
            "generation_log": [asdict(result) for result in self.generation_log]
        }
        
        report_path = self.output_dir / filename
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Generation report exported: {report_path}")
        
        return report_path

# Global generator instance
_ai_generator: Optional[AIArtGenerator] = None

def get_ai_generator() -> AIArtGenerator:
    """Get the global AI art generator instance."""
    global _ai_generator
    if _ai_generator is None:
        _ai_generator = AIArtGenerator()
    return _ai_generator