#!/usr/bin/env python3
"""
Advanced Asset Pipeline for Sands of Duat
Professional-grade asset generation with consistency and quality control
"""

import os
import sys
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

try:
    import torch
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    from diffusers import StableDiffusionPipeline, AnimateDiffPipeline
    DIFFUSERS_AVAILABLE = True
except ImportError:
    print("Advanced AI libraries not available. Install with:")
    print("pip install torch diffusers pillow numpy")
    DIFFUSERS_AVAILABLE = False


@dataclass
class AssetSpec:
    """Specification for an asset to be generated"""
    slug: str
    asset_type: str  # 'concept', 'sprite', 'animation'
    action: Optional[str] = None  # 'idle', 'walk', 'attack'
    size: Tuple[int, int] = (512, 512)
    frames: int = 1
    fps: float = 12.0
    style_reference: Optional[str] = None


@dataclass 
class GenerationResult:
    """Result of asset generation"""
    asset_spec: AssetSpec
    output_path: str
    success: bool
    metadata: Dict[str, Any]
    generation_time: float
    quality_score: float


class EgyptianStyleGuide:
    """Maintains consistency in Egyptian artistic style"""
    
    def __init__(self):
        self.style_prompts = {
            "base_style": "ancient egyptian art style, hieroglyphic quality, papyrus texture, warm desert colors, detailed linework",
            "character_style": "egyptian mythology character, detailed armor and clothing, golden accessories, desert warrior aesthetic",
            "color_palette": "warm golden tones, deep browns, sandstone beige, rich blues, copper accents",
            "lighting": "warm desert sunlight, dramatic shadows, golden hour lighting",
            "quality_tags": "highly detailed, masterpiece, professional concept art, clean lines, consistent style"
        }
        
        self.negative_prompts = [
            "blurry", "low quality", "pixelated", "inconsistent", "modern clothing",
            "neon colors", "futuristic", "anime", "cartoon", "child-like", "cute",
            "nsfw", "nude", "naked", "sexual", "inappropriate", "adult content",
            "revealing", "exposed", "sensual", "provocative"
        ]
        
        # Card generation prompts
        self.card_prompts = {
            "desert_whisper": "Ancient papyrus with swirling sand spirits, mystical wind patterns, desert hieroglyphics",
            "sand_grain": "Single golden sand grain with magical sparkles, hourglass background, time essence",
            "tomb_strike": "Egyptian warrior striking with khopesh sword, combat stance, stone tomb background",
            "ankh_blessing": "Golden ankh symbol with divine light rays, healing energy, blessed aura",
            "scarab_swarm": "Swarm of golden scarab beetles, mystical formation, attack pattern",
            "papyrus_scroll": "Ancient Egyptian scroll with hieroglyphics, knowledge symbols, scholarly magic",
            "mummys_wrath": "Angry mummy with glowing eyes, bandages flowing, undead power",
            "isis_grace": "Goddess Isis with healing light, protective wings, divine blessing",
            "pyramid_power": "Great pyramid with energy beams, ancient power, geometric mysticism",
            "thoths_wisdom": "Ibis-headed Thoth with scroll, wisdom symbols, scholarly divine magic",
            "anubis_judgment": "Anubis with scales of justice, underworld judgment, divine authority",
            "ra_solar_flare": "Sun god Ra with solar disk, intense sunlight, divine solar power",
            "pharaohs_resurrection": "Pharaoh rising from sarcophagus, royal regalia, resurrection magic"
        }
        
        # Environment prompts
        self.environment_prompts = {
            "desert_battlefield": "Egyptian desert battlefield with sand dunes, ancient ruins, sunset lighting",
            "temple_interior": "Interior of Egyptian temple with columns, hieroglyphics, torch lighting",
            "tomb_chamber": "Ancient tomb chamber with sarcophagi, treasure, mysterious atmosphere",
            "oasis": "Desert oasis with palm trees, clear water, peaceful Egyptian setting",
            "pyramid_chamber": "Inside great pyramid with stone blocks, ancient architecture, mystical lighting"
        }
        
        # Character-specific prompts
        self.character_prompts = {
            "anubis_guardian": {
                "description": "Anubis-headed guardian warrior statue in ancient Egyptian style",
                "details": "jackal head, full ceremonial armor coverage, golden ornaments, protective stance, mystical aura",
                "colors": "black fur, golden armor, deep blue accents"
            },
            "desert_scorpion": {
                "description": "Giant desert scorpion with Egyptian hieroglyphic patterns",
                "details": "segmented chitin, curved stinger, hieroglyphic markings, sand texture",
                "colors": "sandy brown chitin, golden markings, dark shadows"
            },
            "pharaoh_lich": {
                "description": "Undead pharaoh with preserved royal regalia",
                "details": "mummified appearance, royal headdress, glowing eyes, mystical energy",
                "colors": "aged bandages, golden regalia, ethereal blue glow"
            },
            "temple_guardian": {
                "description": "Stone guardian statue brought to life",
                "details": "carved stone texture, Egyptian architectural elements, massive build",
                "colors": "sandstone texture, weathered surface, mystical energy"
            },
            "player": {
                "description": "Egyptian warrior adventurer with desert gear",
                "details": "practical armor, desert clothing, confident pose, heroic stance",
                "colors": "leather armor, desert robes, bronze weapons"
            }
        }
    
    def get_card_prompt(self, card_slug: str) -> str:
        """Generate complete prompt for card art"""
        if card_slug not in self.card_prompts:
            return f"Egyptian themed card art, {card_slug}, mystical design, papyrus background"
        
        card_description = self.card_prompts[card_slug]
        
        full_prompt = f"{card_description}, "
        full_prompt += f"{self.style_prompts['base_style']}, "
        full_prompt += f"card art, framed composition, "
        full_prompt += f"{self.style_prompts['color_palette']}, "
        full_prompt += f"{self.style_prompts['lighting']}, "
        full_prompt += f"{self.style_prompts['quality_tags']}"
        
        return full_prompt
    
    def get_environment_prompt(self, environment_slug: str) -> str:
        """Generate complete prompt for environment art"""
        if environment_slug not in self.environment_prompts:
            return f"Egyptian themed environment, {environment_slug}, atmospheric lighting"
        
        env_description = self.environment_prompts[environment_slug]
        
        full_prompt = f"{env_description}, "
        full_prompt += f"{self.style_prompts['base_style']}, "
        full_prompt += f"environment art, wide composition, "
        full_prompt += f"{self.style_prompts['color_palette']}, "
        full_prompt += f"{self.style_prompts['lighting']}, "
        full_prompt += f"{self.style_prompts['quality_tags']}"
        
        return full_prompt
    
    def get_character_prompt(self, character: str, action: str = "idle") -> str:
        """Generate complete prompt for character"""
        if character not in self.character_prompts:
            character = "player"  # Default fallback
        
        char_data = self.character_prompts[character]
        
        action_modifiers = {
            "idle": "standing ready, neutral pose",
            "walk": "walking motion, mid-step",
            "attack": "combat pose, weapon ready"
        }
        
        # Shorter, more focused prompt to avoid token limit
        full_prompt = f"{char_data['description']}, {char_data['details']}, "
        full_prompt += f"{action_modifiers.get(action, 'neutral pose')}, "
        full_prompt += f"egyptian art style, warm colors, professional quality"
        
        return full_prompt
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt for consistent quality"""
        return ", ".join(self.negative_prompts)


class AdvancedAssetGenerator:
    """Professional asset generation with quality control"""
    
    def __init__(self, output_root: str, gpu_optimization: bool = True):
        self.output_root = Path(output_root)
        self.gpu_optimization = gpu_optimization
        self.style_guide = EgyptianStyleGuide()
        self.logger = self._setup_logging()
        
        # Create output directories
        self.concepts_dir = self.output_root / "concepts"
        self.sprites_dir = self.output_root / "sprites"  
        self.animations_dir = self.output_root / "animations"
        self.cards_dir = self.output_root / "cards"
        self.environments_dir = self.output_root / "environments"
        
        for dir_path in [self.concepts_dir, self.sprites_dir, self.animations_dir, self.cards_dir, self.environments_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize AI models
        self.sd_pipeline = None
        self.animatediff_pipeline = None
        self._initialize_models()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup detailed logging"""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "asset_pipeline.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def _initialize_models(self):
        """Initialize AI models with optimization"""
        if not DIFFUSERS_AVAILABLE:
            self.logger.warning("AI models not available, using placeholder generation")
            return
        
        try:
            self.logger.info("Initializing Stable Diffusion pipeline...")
            
            # Use CPU if CUDA not available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if device == "cuda" else torch.float32
            
            # Use a more reliable and available model
            model_id = "runwayml/stable-diffusion-v1-5"
            self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch_dtype,
                use_safetensors=True
            )
            
            if device == "cuda":
                self.sd_pipeline = self.sd_pipeline.to(device)
                if self.gpu_optimization:
                    # Use newer method for memory optimization
                    try:
                        self.sd_pipeline.enable_model_cpu_offload()
                    except:
                        pass  # Continue without memory optimization if not available
            
            self.logger.info(f"SD Pipeline initialized on {device}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            self.sd_pipeline = None
    
    def generate_concept_art(self, character: str, count: int = 3) -> List[GenerationResult]:
        """Generate high-quality concept art"""
        results = []
        
        for i in range(1, count + 1):
            spec = AssetSpec(
                slug=character,
                asset_type="concept",
                size=(512, 512)
            )
            
            output_path = self.concepts_dir / f"{character}_concept_{i}.png"
            
            self.logger.info(f"Generating concept {i} for {character}")
            
            if self.sd_pipeline:
                result = self._generate_with_ai(spec, str(output_path))
            else:
                result = self._generate_placeholder(spec, str(output_path))
            
            results.append(result)
        
        return results
    
    def generate_sprite_sheets(self, character: str, actions: List[str] = None) -> List[GenerationResult]:
        """Generate consistent sprite sheets for character actions"""
        if actions is None:
            actions = ["idle", "walk", "attack"]
        
        results = []
        
        for action in actions:
            spec = AssetSpec(
                slug=character,
                asset_type="sprite",
                action=action,
                size=(384, 64),  # 6 frames × 64px
                frames=6
            )
            
            output_path = self.sprites_dir / f"{character}_{action}_sheet.png"
            
            self.logger.info(f"Generating {action} sprite sheet for {character}")
            
            if self.sd_pipeline:
                result = self._generate_sprite_sheet_ai(spec, str(output_path))
            else:
                result = self._generate_sprite_sheet_placeholder(spec, str(output_path))
            
            results.append(result)
        
        return results
    
    def generate_card_art(self, card_slug: str) -> GenerationResult:
        """Generate card art for a specific card"""
        spec = AssetSpec(
            slug=card_slug,
            asset_type="card",
            size=(512, 768)  # Standard card aspect ratio
        )
        
        output_path = self.cards_dir / f"{card_slug}.png"
        
        self.logger.info(f"Generating card art for {card_slug}")
        
        if self.sd_pipeline:
            result = self._generate_card_with_ai(spec, str(output_path))
        else:
            result = self._generate_card_placeholder(spec, str(output_path))
        
        return result
    
    def generate_environment_art(self, environment_slug: str) -> GenerationResult:
        """Generate environment art"""
        spec = AssetSpec(
            slug=environment_slug,
            asset_type="environment",
            size=(1920, 1080)  # Standard background size
        )
        
        output_path = self.environments_dir / f"{environment_slug}.png"
        
        self.logger.info(f"Generating environment art for {environment_slug}")
        
        if self.sd_pipeline:
            result = self._generate_environment_with_ai(spec, str(output_path))
        else:
            result = self._generate_environment_placeholder(spec, str(output_path))
        
        return result
    
    def generate_animations(self, character: str, actions: List[str] = None) -> List[GenerationResult]:
        """Generate animated loops from sprite sheets"""
        if actions is None:
            actions = ["idle", "walk", "attack"]
        
        results = []
        
        for action in actions:
            sprite_sheet_path = self.sprites_dir / f"{character}_{action}_sheet.png"
            
            if not sprite_sheet_path.exists():
                self.logger.warning(f"Sprite sheet not found: {sprite_sheet_path}")
                continue
            
            spec = AssetSpec(
                slug=character,
                asset_type="animation",
                action=action,
                frames=6,
                fps=12.0
            )
            
            output_path = self.animations_dir / f"{character}_{action}.mp4"
            
            self.logger.info(f"Generating {action} animation for {character}")
            
            result = self._create_animation_from_sprites(spec, str(sprite_sheet_path), str(output_path))
            results.append(result)
        
        return results
    
    def _generate_with_ai(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate asset using AI with quality control"""
        start_time = datetime.now()
        
        try:
            prompt = self.style_guide.get_character_prompt(spec.slug, spec.action or "idle")
            negative_prompt = self.style_guide.get_negative_prompt()
            
            self.logger.info(f"Generating with prompt: {prompt[:100]}...")
            
            # Generate image
            with torch.no_grad():
                result = self.sd_pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=20,  # Standard for SD 1.5
                    guidance_scale=7.5,
                    width=spec.size[0],
                    height=spec.size[1]
                )
            
            image = result.images[0]
            
            # Post-process for quality
            image = self._enhance_image_quality(image)
            
            # Save with metadata
            image.save(output_path)
            self._save_metadata(spec, output_path, {"prompt": prompt})
            
            generation_time = (datetime.now() - start_time).total_seconds()
            quality_score = self._assess_image_quality(image)
            
            return GenerationResult(
                asset_spec=spec,
                output_path=output_path,
                success=True,
                metadata={"prompt": prompt, "model": "sdturbo"},
                generation_time=generation_time,
                quality_score=quality_score
            )
            
        except Exception as e:
            self.logger.error(f"AI generation failed: {e}")
            return self._generate_placeholder(spec, output_path)
    
    def _generate_card_with_ai(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate card art using AI"""
        start_time = datetime.now()
        
        try:
            prompt = self.style_guide.get_card_prompt(spec.slug)
            negative_prompt = self.style_guide.get_negative_prompt()
            
            self.logger.info(f"Generating card with prompt: {prompt[:100]}...")
            
            with torch.no_grad():
                result = self.sd_pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=20,
                    guidance_scale=7.5,
                    width=spec.size[0],
                    height=spec.size[1]
                )
            
            image = result.images[0]
            image = self._enhance_image_quality(image)
            image.save(output_path)
            self._save_metadata(spec, output_path, {"prompt": prompt})
            
            generation_time = (datetime.now() - start_time).total_seconds()
            quality_score = self._assess_image_quality(image)
            
            return GenerationResult(
                asset_spec=spec,
                output_path=output_path,
                success=True,
                metadata={"prompt": prompt, "model": "sdturbo"},
                generation_time=generation_time,
                quality_score=quality_score
            )
            
        except Exception as e:
            self.logger.error(f"Card AI generation failed: {e}")
            return self._generate_card_placeholder(spec, output_path)
    
    def _generate_environment_with_ai(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate environment art using AI"""
        start_time = datetime.now()
        
        try:
            prompt = self.style_guide.get_environment_prompt(spec.slug)
            negative_prompt = self.style_guide.get_negative_prompt()
            
            self.logger.info(f"Generating environment with prompt: {prompt[:100]}...")
            
            with torch.no_grad():
                result = self.sd_pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=20,
                    guidance_scale=7.5,
                    width=spec.size[0],
                    height=spec.size[1]
                )
            
            image = result.images[0]
            image = self._enhance_image_quality(image)
            image.save(output_path)
            self._save_metadata(spec, output_path, {"prompt": prompt})
            
            generation_time = (datetime.now() - start_time).total_seconds()
            quality_score = self._assess_image_quality(image)
            
            return GenerationResult(
                asset_spec=spec,
                output_path=output_path,
                success=True,
                metadata={"prompt": prompt, "model": "sdturbo"},
                generation_time=generation_time,
                quality_score=quality_score
            )
            
        except Exception as e:
            self.logger.error(f"Environment AI generation failed: {e}")
            return self._generate_environment_placeholder(spec, output_path)
    
    def _generate_sprite_sheet_ai(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate sprite sheet using AI"""
        start_time = datetime.now()
        
        try:
            # Generate individual frames
            frames = []
            base_prompt = self.style_guide.get_character_prompt(spec.slug, spec.action)
            
            for frame_idx in range(spec.frames):
                # Add frame-specific variations
                frame_prompt = f"{base_prompt}, frame {frame_idx + 1} of {spec.frames}"
                
                with torch.no_grad():
                    result = self.sd_pipeline(
                        prompt=frame_prompt,
                        negative_prompt=self.style_guide.get_negative_prompt(),
                        num_inference_steps=20,
                        guidance_scale=7.5,
                        width=64,
                        height=64
                    )
                
                frame_image = result.images[0]
                frame_image = self._enhance_image_quality(frame_image)
                frames.append(frame_image)
            
            # Combine frames into sprite sheet
            sprite_sheet = self._create_sprite_sheet(frames, spec.frames)
            sprite_sheet.save(output_path)
            
            # Save metadata
            metadata = {
                "frames": spec.frames,
                "frame_size": (64, 64),
                "action": spec.action,
                "fps": spec.fps
            }
            self._save_metadata(spec, output_path, metadata)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            quality_score = self._assess_image_quality(sprite_sheet)
            
            return GenerationResult(
                asset_spec=spec,
                output_path=output_path,
                success=True,
                metadata=metadata,
                generation_time=generation_time,
                quality_score=quality_score
            )
            
        except Exception as e:
            self.logger.error(f"Sprite sheet AI generation failed: {e}")
            return self._generate_sprite_sheet_placeholder(spec, output_path)
    
    def _create_sprite_sheet(self, frames: List[Image.Image], frame_count: int) -> Image.Image:
        """Combine individual frames into a sprite sheet"""
        frame_width = frames[0].width
        frame_height = frames[0].height
        
        sheet_width = frame_width * frame_count
        sheet_height = frame_height
        
        sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
        
        for i, frame in enumerate(frames):
            x_pos = i * frame_width
            sprite_sheet.paste(frame, (x_pos, 0))
        
        return sprite_sheet
    
    def _create_animation_from_sprites(self, spec: AssetSpec, sprite_sheet_path: str, output_path: str) -> GenerationResult:
        """Create MP4 animation from sprite sheet"""
        start_time = datetime.now()
        
        try:
            # This would use ffmpeg or similar to create MP4
            # For now, create a placeholder
            self.logger.info(f"Creating animation: {output_path}")
            
            # Placeholder: copy the sprite sheet as a "preview"
            sprite_sheet = Image.open(sprite_sheet_path)
            preview_path = str(output_path).replace('.mp4', '_preview.png')
            sprite_sheet.save(preview_path)
            
            # Create a simple text file as MP4 placeholder
            with open(output_path.replace('.mp4', '_animation_info.txt'), 'w') as f:
                f.write(f"Animation: {spec.slug}_{spec.action}\n")
                f.write(f"Frames: {spec.frames}\n")
                f.write(f"FPS: {spec.fps}\n")
                f.write(f"Source: {sprite_sheet_path}\n")
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            return GenerationResult(
                asset_spec=spec,
                output_path=output_path,
                success=True,
                metadata={"frames": spec.frames, "fps": spec.fps},
                generation_time=generation_time,
                quality_score=0.8
            )
            
        except Exception as e:
            self.logger.error(f"Animation creation failed: {e}")
            return GenerationResult(
                asset_spec=spec,
                output_path=output_path,
                success=False,
                metadata={},
                generation_time=0.0,
                quality_score=0.0
            )
    
    def _enhance_image_quality(self, image: Image.Image) -> Image.Image:
        """Enhance image quality post-generation"""
        # Sharpen
        image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=1))
        
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.05)
        
        return image
    
    def _assess_image_quality(self, image: Image.Image) -> float:
        """Assess generated image quality (placeholder scoring)"""
        # Simple quality metrics
        width, height = image.size
        if width < 64 or height < 64:
            return 0.3
        elif width >= 512 and height >= 512:
            return 0.9
        else:
            return 0.7
    
    def _save_metadata(self, spec: AssetSpec, output_path: str, extra_metadata: Dict[str, Any]):
        """Save metadata for generated assets"""
        metadata = {
            "slug": spec.slug,
            "asset_type": spec.asset_type,
            "action": spec.action,
            "size": spec.size,
            "frames": spec.frames,
            "fps": spec.fps,
            "generated_at": datetime.now().isoformat(),
            "output_path": output_path,
            **extra_metadata
        }
        
        metadata_path = Path(output_path).with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _generate_placeholder(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate placeholder when AI is not available"""
        start_time = datetime.now()
        
        image = Image.new('RGB', spec.size, (139, 69, 19))  # Brown background
        draw = ImageDraw.Draw(image)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = f"{spec.slug}\n{spec.asset_type}"
        if spec.action:
            text += f"\n{spec.action}"
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (spec.size[0] - text_width) // 2
        y = (spec.size[1] - text_height) // 2
        
        draw.text((x, y), text, fill=(218, 165, 32), font=font)
        
        # Add Egyptian-style border
        border_color = (218, 165, 32)  # Gold
        for i in range(5):
            draw.rectangle([i, i, spec.size[0]-1-i, spec.size[1]-1-i], 
                         outline=border_color)
        
        image.save(output_path)
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        return GenerationResult(
            asset_spec=spec,
            output_path=output_path,
            success=True,
            metadata={"type": "placeholder"},
            generation_time=generation_time,
            quality_score=0.5
        )
    
    def _generate_sprite_sheet_placeholder(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate placeholder sprite sheet"""
        start_time = datetime.now()
        
        frame_width = 64
        frame_height = 64
        sheet_width = frame_width * spec.frames
        
        image = Image.new('RGB', (sheet_width, frame_height), (139, 69, 19))
        draw = ImageDraw.Draw(image)
        
        # Draw frames
        for i in range(spec.frames):
            x_start = i * frame_width
            
            # Frame border
            draw.rectangle([x_start, 0, x_start + frame_width - 1, frame_height - 1], 
                         outline=(218, 165, 32), width=2)
            
            # Frame number
            try:
                font = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            draw.text((x_start + 5, 5), f"F{i+1}", fill=(218, 165, 32), font=font)
            
            # Character indicator
            char_text = spec.slug[:3].upper()
            draw.text((x_start + 5, frame_height - 20), char_text, fill=(218, 165, 32), font=font)
        
        image.save(output_path)
        
        # Save metadata
        metadata = {
            "frames": spec.frames,
            "frame_size": (frame_width, frame_height),
            "action": spec.action,
            "fps": spec.fps,
            "type": "placeholder"
        }
        self._save_metadata(spec, output_path, metadata)
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        return GenerationResult(
            asset_spec=spec,
            output_path=output_path,
            success=True,
            metadata=metadata,
            generation_time=generation_time,
            quality_score=0.5
        )
    
    def _generate_card_placeholder(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate placeholder card art"""
        start_time = datetime.now()
        
        # Card aspect ratio
        image = Image.new('RGB', spec.size, (139, 69, 19))  # Brown background
        draw = ImageDraw.Draw(image)
        
        # Card frame
        border_color = (218, 165, 32)  # Gold
        for i in range(8):
            draw.rectangle([i, i, spec.size[0]-1-i, spec.size[1]-1-i], 
                         outline=border_color)
        
        # Card title
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            desc_font = ImageFont.truetype("arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
        
        # Card name
        card_name = spec.slug.replace('_', ' ').title()
        title_bbox = draw.textbbox((0, 0), card_name, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (spec.size[0] - title_width) // 2
        draw.text((title_x, 30), card_name, fill=(218, 165, 32), font=title_font)
        
        # Egyptian symbol in center
        center_x, center_y = spec.size[0] // 2, spec.size[1] // 2
        symbol_size = 80
        
        # Draw ankh symbol
        draw.ellipse([center_x - 25, center_y - 55, center_x + 25, center_y - 5], outline=border_color, width=4)
        # Vertical line (thick)
        draw.rectangle([center_x - 3, center_y - 5, center_x + 3, center_y + 60], fill=border_color)
        # Horizontal line (thick)
        draw.rectangle([center_x - 30, center_y + 17, center_x + 30, center_y + 23], fill=border_color)
        
        # Card type
        card_type = "Egyptian Card"
        type_bbox = draw.textbbox((0, 0), card_type, font=desc_font)
        type_width = type_bbox[2] - type_bbox[0]
        type_x = (spec.size[0] - type_width) // 2
        draw.text((type_x, spec.size[1] - 40), card_type, fill=(200, 200, 200), font=desc_font)
        
        image.save(output_path)
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        return GenerationResult(
            asset_spec=spec,
            output_path=output_path,
            success=True,
            metadata={"type": "placeholder"},
            generation_time=generation_time,
            quality_score=0.6
        )
    
    def _generate_environment_placeholder(self, spec: AssetSpec, output_path: str) -> GenerationResult:
        """Generate placeholder environment art"""
        start_time = datetime.now()
        
        # Environment colors
        sky_color = (139, 69, 19)  # Brown
        ground_color = (101, 51, 13)  # Darker brown
        accent_color = (218, 165, 32)  # Gold
        
        image = Image.new('RGB', spec.size, sky_color)
        draw = ImageDraw.Draw(image)
        
        # Simple desert landscape
        horizon_y = spec.size[1] * 2 // 3
        
        # Ground
        draw.polygon([(0, horizon_y), (spec.size[0], horizon_y), 
                     (spec.size[0], spec.size[1]), (0, spec.size[1])], 
                    fill=ground_color)
        
        # Sand dunes
        for i in range(3):
            x_center = spec.size[0] * (i + 1) // 4
            dune_width = spec.size[0] // 6
            dune_height = spec.size[1] // 8
            
            # Simple dune shape
            points = [
                (x_center - dune_width, horizon_y),
                (x_center, horizon_y - dune_height),
                (x_center + dune_width, horizon_y)
            ]
            draw.polygon(points, fill=accent_color)
        
        # Environment name
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        env_name = spec.slug.replace('_', ' ').title()
        name_bbox = draw.textbbox((0, 0), env_name, font=font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (spec.size[0] - name_width) // 2
        draw.text((name_x, 50), env_name, fill=accent_color, font=font)
        
        image.save(output_path)
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        return GenerationResult(
            asset_spec=spec,
            output_path=output_path,
            success=True,
            metadata={"type": "placeholder"},
            generation_time=generation_time,
            quality_score=0.6
        )
    
    def generate_full_character_set(self, character: str) -> List[GenerationResult]:
        """Generate complete asset set for a character"""
        self.logger.info(f"Generating full asset set for {character}")
        
        all_results = []
        
        # 1. Generate concepts
        concept_results = self.generate_concept_art(character, count=3)
        all_results.extend(concept_results)
        
        # 2. Generate sprite sheets
        sprite_results = self.generate_sprite_sheets(character, ["idle", "walk", "attack"])
        all_results.extend(sprite_results)
        
        # 3. Generate animations
        animation_results = self.generate_animations(character, ["idle", "walk", "attack"])
        all_results.extend(animation_results)
        
        return all_results
    
    def generate_all_game_assets(self) -> List[GenerationResult]:
        """Generate all assets needed for the game"""
        self.logger.info("Generating complete game asset library")
        all_results = []
        
        # Characters
        characters = ["anubis_guardian", "desert_scorpion", "pharaoh_lich", "temple_guardian", "player"]
        for character in characters:
            self.logger.info(f"Generating character set: {character}")
            results = self.generate_full_character_set(character)
            all_results.extend(results)
        
        # Cards
        cards = [
            "desert_whisper", "sand_grain", "tomb_strike", "ankh_blessing",
            "scarab_swarm", "papyrus_scroll", "mummys_wrath", "isis_grace",
            "pyramid_power", "thoths_wisdom", "anubis_judgment", "ra_solar_flare",
            "pharaohs_resurrection"
        ]
        
        for card in cards:
            self.logger.info(f"Generating card art: {card}")
            result = self.generate_card_art(card)
            all_results.append(result)
        
        # Environments
        environments = [
            "desert_battlefield", "temple_interior", "tomb_chamber",
            "oasis", "pyramid_chamber"
        ]
        
        for environment in environments:
            self.logger.info(f"Generating environment: {environment}")
            result = self.generate_environment_art(environment)
            all_results.append(result)
        
        self.logger.info(f"Generated {len(all_results)} total assets")
        return all_results
    
    def generate_report(self, results: List[GenerationResult]) -> str:
        """Generate detailed report of asset generation"""
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        total_time = sum(r.generation_time for r in results)
        avg_quality = sum(r.quality_score for r in successful) / len(successful) if successful else 0
        
        report = [
            "=== ASSET GENERATION REPORT ===",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"Total Assets: {len(results)}",
            f"Successful: {len(successful)}",
            f"Failed: {len(failed)}",
            f"Total Time: {total_time:.2f}s",
            f"Average Quality Score: {avg_quality:.2f}",
            "",
            "GENERATED FILES:"
        ]
        
        for result in successful:
            report.append(f"[OK] {result.output_path}")
            report.append(f"  Type: {result.asset_spec.asset_type}")
            if result.asset_spec.action:
                report.append(f"  Action: {result.asset_spec.action}")
            report.append(f"  Quality: {result.quality_score:.2f}")
            report.append(f"  Time: {result.generation_time:.2f}s")
            report.append("")
        
        if failed:
            report.append("FAILED:")
            for result in failed:
                report.append(f"[FAIL] {result.output_path}")
            report.append("")
        
        return "\n".join(report)


def main():
    """CLI interface for asset generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Asset Pipeline for Sands of Duat")
    parser.add_argument("target", nargs="?", default="all", help="Character slug or 'all' for complete game assets")
    parser.add_argument("--output", default="./assets", help="Output directory")
    parser.add_argument("--concepts", type=int, default=3, help="Number of concept arts")
    parser.add_argument("--actions", nargs="+", default=["idle", "walk", "attack"], 
                       help="Actions for sprites/animations")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU optimizations")
    
    args = parser.parse_args()
    
    # Initialize pipeline
    generator = AdvancedAssetGenerator(args.output, gpu_optimization=args.gpu)
    
    # Generate assets
    if args.target == "all":
        results = generator.generate_all_game_assets()
        report_name = "complete_game_assets_report.txt"
    else:
        results = generator.generate_full_character_set(args.target)
        report_name = f"{args.target}_generation_report.txt"
    
    # Print report
    report = generator.generate_report(results)
    print(report)
    
    # Save report
    report_path = Path(args.output) / report_name
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()