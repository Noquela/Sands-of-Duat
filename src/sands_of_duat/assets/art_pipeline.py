"""
4K Art Pipeline - Professional asset generation with local AI.
Creates consistent Egyptian-themed assets using Stable Diffusion XL.
"""

import asyncio
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Optional AI imports
try:
    import torch
    from diffusers import StableDiffusionXLPipeline, AutoencoderKL
    from PIL import Image, ImageEnhance, ImageFilter
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    torch = None
    StableDiffusionXLPipeline = None
    AutoencoderKL = None
    Image = None

class AssetType(Enum):
    """Types of assets to generate."""
    BACKGROUND = "background"
    CARD_FRAME = "card_frame" 
    CHARACTER_PORTRAIT = "character_portrait"
    UI_ELEMENT = "ui_element"
    PARTICLE_TEXTURE = "particle_texture"
    DECORATION = "decoration"

class EgyptianStyle(Enum):
    """Egyptian art style variants."""
    CLASSICAL = "classical"  # Traditional Egyptian art
    MYSTICAL = "mystical"   # Dark, mysterious underworld
    GOLDEN = "golden"       # Bright, divine golden style
    HIEROGLYPHIC = "hieroglyphic"  # Hieroglyph-focused
    PAPYRUS = "papyrus"     # Papyrus texture style

@dataclass
class AssetSpec:
    """Specification for generating an asset."""
    name: str
    asset_type: AssetType
    style: EgyptianStyle
    dimensions: Tuple[int, int]
    prompt: str
    negative_prompt: str = ""
    guidance_scale: float = 7.5
    num_inference_steps: int = 30
    seed: Optional[int] = None
    post_processing: List[str] = field(default_factory=list)

class EgyptianArtPipeline:
    """Professional 4K Egyptian art generation pipeline."""
    
    def __init__(self):
        self.logger = logging.getLogger("art_pipeline")
        
        # Directories
        self.assets_dir = Path("assets/generated_4k")
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        for asset_type in AssetType:
            (self.assets_dir / asset_type.value).mkdir(exist_ok=True)
        
        # Pipeline state
        self.pipeline = None
        self.vae = None
        self.initialized = False
        
        # Check GPU
        self.device = "cuda" if torch and torch.cuda.is_available() else "cpu"
        self.logger.info(f"Art pipeline using device: {self.device}")
        
        # Egyptian style presets
        self._setup_style_presets()
    
    def _setup_style_presets(self):
        """Setup Egyptian art style presets."""
        self.style_presets = {
            EgyptianStyle.CLASSICAL: {
                "base_prompt": "ancient egyptian art style, traditional hieroglyphs, golden accents, papyrus texture, museum quality, detailed, professional photography, 4k",
                "negative_prompt": "modern, cartoon, anime, low quality, blurry, text, watermark, signature, frame, border",
                "guidance_scale": 7.5
            },
            EgyptianStyle.MYSTICAL: {
                "base_prompt": "dark egyptian underworld, mysterious atmosphere, purple energy, ancient magic, shadows, mystical symbols, cinematic lighting, ultra detailed, 4k",
                "negative_prompt": "bright, cheerful, modern, cartoon, low quality, blurry, text, watermark",
                "guidance_scale": 8.0
            },
            EgyptianStyle.GOLDEN: {
                "base_prompt": "golden egyptian temple, divine radiance, sun rays, golden hieroglyphs, majestic, royal, bright lighting, luxury, 4k masterpiece",
                "negative_prompt": "dark, dull, modern, cartoon, low quality, blurry, text, watermark",
                "guidance_scale": 7.0
            },
            EgyptianStyle.HIEROGLYPHIC: {
                "base_prompt": "ancient hieroglyphs, carved stone, weathered texture, authentic egyptian writing, archaeological, detailed symbols, 4k texture",
                "negative_prompt": "modern text, latin letters, cartoon, low quality, blurry, watermark",
                "guidance_scale": 8.5
            },
            EgyptianStyle.PAPYRUS: {
                "base_prompt": "aged papyrus texture, ancient paper, weathered edges, organic texture, archaeological artifact, high resolution, 4k",
                "negative_prompt": "modern paper, white, clean, cartoon, low quality, blurry",
                "guidance_scale": 6.5
            }
        }
    
    async def initialize(self) -> bool:
        """Initialize the art generation pipeline."""
        if not AI_AVAILABLE:
            self.logger.error("AI libraries not available - cannot initialize art pipeline")
            return False
        
        try:
            self.logger.info("Loading Stable Diffusion XL pipeline...")
            
            # Load VAE for better quality
            self.vae = AutoencoderKL.from_pretrained(
                "madebyollin/sdxl-vae-fp16-fix",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            # Load SDXL pipeline
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                vae=self.vae,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            
            # Move to device and optimize
            self.pipeline = self.pipeline.to(self.device)
            if self.device == "cuda":
                self.pipeline.enable_model_cpu_offload()
                self.pipeline.enable_vae_slicing()
                self.pipeline.enable_vae_tiling()
            
            self.initialized = True
            self.logger.info("✅ Egyptian art pipeline initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize art pipeline: {e}")
            return False
    
    def get_asset_specs(self) -> List[AssetSpec]:
        """Get all asset specifications for Egyptian card game."""
        specs = []
        
        # Backgrounds (4096x2048 for ultrawide scaling)
        backgrounds = [
            ("menu_background", "golden egyptian temple hall, massive columns, divine light rays, majestic entrance"),
            ("combat_background", "dark underworld chamber, purple mystical energy, ancient battle arena"),
            ("deck_builder_background", "ancient library of alexandria, scrolls, golden light, wisdom"),
            ("collection_background", "hall of gods, divine statues, golden pedestals, museum of artifacts")
        ]
        
        for name, description in backgrounds:
            specs.append(AssetSpec(
                name=name,
                asset_type=AssetType.BACKGROUND,
                style=EgyptianStyle.GOLDEN if "golden" in description else EgyptianStyle.MYSTICAL,
                dimensions=(4096, 2048),
                prompt=description,
                num_inference_steps=40  # Higher quality for backgrounds
            ))
        
        # Card Frames (1024x1024 for scaling)
        card_frames = [
            ("common_frame", EgyptianStyle.CLASSICAL, "simple egyptian border, papyrus texture, basic hieroglyphs"),
            ("rare_frame", EgyptianStyle.GOLDEN, "golden egyptian frame, ornate decorations, precious gems"),
            ("epic_frame", EgyptianStyle.MYSTICAL, "mystical frame, purple energy, magical symbols, glowing edges"),
            ("legendary_frame", EgyptianStyle.GOLDEN, "legendary golden frame, divine radiance, sun disk, royal symbols")
        ]
        
        for name, style, description in card_frames:
            specs.append(AssetSpec(
                name=name,
                asset_type=AssetType.CARD_FRAME,
                style=style,
                dimensions=(1024, 1024),
                prompt=description,
                post_processing=["make_transparent", "enhance_contrast"]
            ))
        
        # Character Portraits (1024x1024)
        characters = [
            ("ra_portrait", "Ra the sun god, falcon head, solar disk crown, golden radiance, divine authority"),
            ("anubis_portrait", "Anubis god of death, black jackal head, golden collar, mysterious aura"),
            ("isis_portrait", "Isis mother goddess, beautiful woman, isis crown, protective wings, healing aura"),
            ("set_portrait", "Set god of chaos, red eyes, dark energy, storm clouds, menacing presence"),
            ("thoth_portrait", "Thoth god of wisdom, ibis head, scroll of knowledge, mystical blue energy"),
            ("horus_portrait", "Horus sky god, falcon head, eye of horus, golden armor, royal bearing")
        ]
        
        for name, description in characters:
            specs.append(AssetSpec(
                name=name,
                asset_type=AssetType.CHARACTER_PORTRAIT,
                style=EgyptianStyle.CLASSICAL,
                dimensions=(1024, 1024),
                prompt=description,
                num_inference_steps=35
            ))
        
        # UI Elements (512x512)
        ui_elements = [
            ("health_icon", "ankh symbol, life force, golden glow"),
            ("mana_icon", "blue crystal, magical energy, mystical power"),
            ("attack_icon", "crossed khopesh swords, combat, golden blades"),
            ("shield_icon", "egyptian shield, protection, defensive barrier")
        ]
        
        for name, description in ui_elements:
            specs.append(AssetSpec(
                name=name,
                asset_type=AssetType.UI_ELEMENT,
                style=EgyptianStyle.GOLDEN,
                dimensions=(512, 512),
                prompt=description,
                post_processing=["make_transparent", "enhance_contrast"]
            ))
        
        return specs
    
    async def generate_asset(self, spec: AssetSpec) -> bool:
        """Generate a single asset from specification."""
        if not self.initialized:
            self.logger.error("Pipeline not initialized")
            return False
        
        try:
            self.logger.info(f"Generating {spec.name} ({spec.asset_type.value})")
            
            # Combine style preset with specific prompt
            style_preset = self.style_presets[spec.style]
            full_prompt = f"{spec.prompt}, {style_preset['base_prompt']}"
            full_negative = f"{spec.negative_prompt}, {style_preset['negative_prompt']}"
            
            # Generate image
            generator = torch.Generator(device=self.device)
            if spec.seed:
                generator.manual_seed(spec.seed)
            
            image = self.pipeline(
                prompt=full_prompt,
                negative_prompt=full_negative,
                width=spec.dimensions[0],
                height=spec.dimensions[1],
                num_inference_steps=spec.num_inference_steps,
                guidance_scale=spec.guidance_scale,
                generator=generator
            ).images[0]
            
            # Post-processing
            if spec.post_processing:
                image = self._apply_post_processing(image, spec.post_processing)
            
            # Save asset
            output_path = self.assets_dir / spec.asset_type.value / f"{spec.name}.png"
            image.save(output_path, "PNG", quality=95)
            
            self.logger.info(f"✅ Generated: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate {spec.name}: {e}")
            return False
    
    def _apply_post_processing(self, image: Image.Image, processes: List[str]) -> Image.Image:
        """Apply post-processing effects to generated images."""
        for process in processes:
            if process == "make_transparent":
                # Convert white/light backgrounds to transparent
                image = image.convert("RGBA")
                data = image.getdata()
                newData = []
                for item in data:
                    # Replace light colors with transparency
                    if item[0] > 200 and item[1] > 200 and item[2] > 200:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                image.putdata(newData)
            
            elif process == "enhance_contrast":
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.2)
            
            elif process == "sharpen":
                image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        return image
    
    async def generate_all_assets(self) -> Dict[str, bool]:
        """Generate all Egyptian art assets."""
        if not await self.initialize():
            return {}
        
        specs = self.get_asset_specs()
        results = {}
        
        self.logger.info(f"🎨 Generating {len(specs)} Egyptian art assets...")
        
        for spec in specs:
            success = await self.generate_asset(spec)
            results[spec.name] = success
            
            # Small delay between generations
            await asyncio.sleep(1)
        
        successful = sum(results.values())
        total = len(results)
        self.logger.info(f"🎉 Art generation complete: {successful}/{total} assets created")
        
        return results
    
    def cleanup(self):
        """Cleanup pipeline resources."""
        if self.pipeline:
            del self.pipeline
        if self.vae:
            del self.vae
        
        if torch and torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.initialized = False
        self.logger.info("Art pipeline cleaned up")

# Global art pipeline instance
egyptian_art_pipeline = EgyptianArtPipeline()