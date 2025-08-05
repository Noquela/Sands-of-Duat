#!/usr/bin/env python3
"""
Hades-Style Art Generator for Sands of Duat
Creates professional-quality Egyptian underworld art in the style of Hades game.
"""

import argparse
import logging
import os
import sys
import time
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import torch
    from diffusers import StableDiffusionPipeline, DiffusionPipeline
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    import numpy as np
    DIFFUSERS_AVAILABLE = True
except ImportError as e:
    print(f"Missing AI dependencies: {e}")
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    DIFFUSERS_AVAILABLE = False


class HadesStyleArtGenerator:
    """Professional Hades-style art generator for Egyptian underworld theme."""
    
    def __init__(self, model: str = "sdxl", device: str = "auto", high_quality: bool = True):
        self.model = model
        self.high_quality = high_quality
        self.pipeline = None
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Setup device
        if DIFFUSERS_AVAILABLE:
            self.device = self._setup_device(device)
        else:
            self.device = "cpu"
        
        # Optimized Hades-Style Egyptian Prompts (CLIP token-efficient)
        self.art_style_base = (
            "Hades game style, masterpiece illustration, cel-shaded, "
            "dramatic chiaroscuro lighting, painterly brushwork, "
            "Egyptian mythology, underworld atmosphere, "
            "professional concept art, rich details"
        )
        
        self.duat_atmosphere = (
            "Egyptian underworld, golden hieroglyphs, ancient magic, "
            "dramatic shadows, ornate decorations, burial chamber"
        )
        
        # Ultra-detailed prompts for each asset type
        self.prompts = {
            "cards": {
                # Attack Cards
                "sand_strike": f"{self.art_style_base}, {self.duat_atmosphere}, "
                             "magnificent swirling sand tornado with supernatural force, "
                             "thousands of golden sand particles dancing with ethereal energy, "
                             "powerful desert sorcerer in dynamic casting pose, flowing robes, "
                             "intricate hieroglyphic sand magic circles glowing with ancient power, "
                             "detailed Egyptian bronze armor with scarab motifs, "
                             "dramatic lighting creating strong shadows and highlights, "
                             "painterly texture showing individual brush strokes, card art composition",
                
                "tomb_strike": f"{self.art_style_base}, {self.duat_atmosphere}, "
                             "menacing undead mummy pharaoh emerging from ornate golden sarcophagus, "
                             "ancient linen bandages unwrapping dramatically in supernatural wind, "
                             "exquisite golden death mask with precious stone inlays, "
                             "ceremonial khopesh sword with hieroglyphic engravings glowing, "
                             "richly detailed tomb interior with painted wall murals, "
                             "flickering torch light creating deep chiaroscuro shadows, "
                             "scattered burial treasures and canopic jars, imposing intimidating presence, "
                             "hand-painted details in clothing and armor textures",
                
                "ra_solar_flare": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                "mighty Ra the sun god in all his divine glory, majestic falcon head, "
                                "casting devastating solar magic with supernatural intensity, "
                                "brilliant golden solar flare energy radiating outward, "
                                "ornate sun disk crown with intricate astronomical symbols, "
                                "complex layered hieroglyphic spell circles floating in the air, "
                                "blazing solar powers creating lens flares and energy distortions, "
                                "divine authoritative presence commanding respect and awe, "
                                "rich Egyptian regalia with gold and precious stone details, "
                                "painterly brush work emphasizing the divine nature",
                
                "scarab_swarm": f"{self.art_style_base}, {self.duat_atmosphere}, "
                              "spectacular massive swarm of hundreds of golden scarab beetles, "
                              "each beetle with individually detailed jeweled carapaces, "
                              "iridescent wing sheaths catching supernatural light, "
                              "mystical insect magic creating ethereal energy trails, "
                              "ancient Egyptian sacred burial scarabs with hieroglyphic markings, "
                              "dramatic swirling cloud formation with perfect composition, "
                              "desert tomb environment with sandstone architecture, "
                              "ominous yet beautiful atmosphere, rich environmental details, "
                              "hand-painted texture work showing individual scarab details",
                
                # Defense Cards  
                "ankh_blessing": f"{self.art_style_base}, {self.duat_atmosphere}, "
                               "magnificent ornate golden ankh symbol as centerpiece, "
                               "radiating pure healing light with supernatural luminescence, "
                               "divine protection aura with ethereal energy waves, "
                               "incredibly intricate Egyptian engravings and hieroglyphs, "
                               "peaceful healing energy creating warm golden glow, "
                               "sacred temple background with painted murals and columns, "
                               "blessed atmosphere filled with floating light particles, "
                               "museum-quality detail in metalwork and stone carving, "
                               "painterly technique emphasizing the sacred nature",
                
                "isis_grace": f"{self.art_style_base}, {self.duat_atmosphere}, "
                            "divine Isis goddess in all her maternal glory, magnificent winged arms outstretched, "
                            "protective divine aura radiating motherly love and power, "
                            "elegant flowing Egyptian dress with intricate pleating and embroidery, "
                            "elaborate jewelry with precious stones and gold filigree work, "
                            "ornate golden headdress with sacred symbols and feathers, "
                            "healing magic emanating from graceful hands with visible energy streams, "
                            "majestic temple of Isis background with towering columns, "
                            "serene yet powerful expression, hand-painted facial details, "
                            "rich fabric textures and jewelry craftsmanship",
                
                "pyramid_power": f"{self.art_style_base}, {self.duat_atmosphere}, "
                               "colossal ancient pyramid channeling immense mystical energy, "
                               "brilliant golden capstone glowing with supernatural power, "
                               "complex geometric sacred patterns covering the stone blocks, "
                               "visible energy ley lines crackling with electric power, "
                               "magnificent desert night sky filled with constellations, "
                               "monumental architecture emphasizing massive scale and grandeur, "
                               "atmospheric perspective showing the pyramid's imposing presence, "
                               "detailed stone block textures with archaeological accuracy, "
                               "dramatic lighting creating strong architectural shadows",
                
                # Utility Cards
                "papyrus_scroll": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                "ancient papyrus scroll with aged texture and worn edges, "
                                "luminous hieroglyphs magically appearing and glowing with wisdom, "
                                "Thoth's divine wisdom magic creating floating symbols, "
                                "elegant ibis feather quill with gold nib and intricate details, "
                                "scholarly magical spells written in flowing hieroglyphic script, "
                                "great library of Alexandria atmosphere with towering shelves, "
                                "knowledge power manifesting as floating books and scrolls, "
                                "warm candlelight illuminating the scholarly environment, "
                                "hand-painted texture work on papyrus and parchment materials",
                
                "desert_whisper": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                "enigmatic mysterious figure shrouded in flowing desert robes, "
                                "intricate sand magic swirling in complex patterns around them, "
                                "face hidden in shadow with only luminous eyes visible, "
                                "ancient secrets whispered through supernatural wind, "
                                "magical incantations creating visible sound waves, "
                                "mystical desert winds carrying sand particles in spirals, "
                                "ethereal ghostly presence with translucent qualities, "
                                "dramatic fabric textures flowing in supernatural breeze, "
                                "atmospheric depth creating sense of otherworldly mystery",
                
                "thoths_wisdom": f"{self.art_style_base}, {self.duat_atmosphere}, "
                               "majestic Thoth the ibis-headed god of knowledge and wisdom, "
                               "numerous sacred scrolls and tablets floating around him magically, "
                               "complex multi-layered hieroglyphic magic circles glowing, "
                               "divine wisdom emanating as visible energy and light, "
                               "grand hall of two truths with towering columns and murals, "
                               "ornate scales of justice with feather of Ma'at, "
                               "scholarly magic creating floating equations and symbols, "
                               "rich architectural details in Egyptian temple design, "
                               "wise and knowing expression with hand-painted detail",
                
                "anubis_judgment": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "imposing Anubis jackal-headed god of the afterlife, "
                                 "carefully weighing a human heart against the feather of Ma'at, "
                                 "ornate sacred scales of justice with intricate metalwork, "
                                 "solemn weighing of the heart ceremony with divine gravity, "
                                 "magnificent judgment hall of the dead with painted walls, "
                                 "solemn divine presence commanding respect and awe, "
                                 "afterlife trial atmosphere with supernatural lighting, "
                                 "detailed Egyptian ceremonial regalia and decorations, "
                                 "hand-painted facial features showing divine authority",
                
                "pharaohs_resurrection": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                       "mighty pharaoh rising dramatically from ornate golden sarcophagus, "
                                       "magnificent royal burial mask with precious stone inlays, "
                                       "supernatural resurrection magic swirling with divine energy, "
                                       "undead royal power radiating authority and majesty, "
                                       "treasure-filled tomb chamber with piles of gold and artifacts, "
                                       "regal undead presence commanding respect despite death, "
                                       "dramatic lighting emphasizing the resurrection moment, "
                                       "rich details in royal regalia and burial goods, "
                                       "hand-painted textures on mummy wrappings and gold",
                
                "mummys_wrath": f"{self.art_style_base}, {self.duat_atmosphere}, "
                              "terrifying enraged mummy warrior in full battle fury, "
                              "ancient linen bandages dramatically unwrapping and flowing, "
                              "dark cursed burial magic emanating dark energy, "
                              "tomb guardian fury with glowing angry eyes, "
                              "ornate Egyptian weapons and ceremonial armor, "
                              "vengeful undead spirit radiating supernatural malevolence, "
                              "dynamic action pose showing imminent attack, "
                              "detailed texture work on aged bandages and metal, "
                              "dramatic shadows creating menacing atmosphere",
                
                # Missing utility card
                "sand_grain": f"{self.art_style_base}, {self.duat_atmosphere}, "
                             "elemental sand manipulation magic in its purest form, "
                             "individual grains of sand glowing with golden energy, "
                             "simple yet elegant magical gesture creating sand patterns, "
                             "desert mage focusing mystical power through fingertips, "
                             "swirling sand forming geometric magical symbols, "
                             "basic but beautiful sand magic with visible energy flow, "
                             "minimalist composition emphasizing the magic's elegance, "
                             "hand-painted details showing individual sand particles"
            },
            
            "characters": {
                "player_character": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                  "heroic Egyptian adventurer with commanding presence, "
                                  "incredibly detailed character design with personality, "
                                  "ornate bronze and gold armor featuring intricate hieroglyphic engravings, "
                                  "confident heroic stance radiating determination and courage, "
                                  "ancient Egyptian weapons with ceremonial details and craftsmanship, "
                                  "determined expression showing inner strength and resolve, "
                                  "protagonist energy with natural leadership qualities, "
                                  "dynamic ready-for-adventure pose, hand-painted armor textures",
                
                "anubis_guardian": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "towering imposing Anubis temple guardian with divine authority, "
                                 "majestic jackal-headed warrior radiating supernatural power, "
                                 "elaborate ceremonial Egyptian armor with sacred symbols, "
                                 "ornate staff of judgment topped with divine hieroglyphs, "
                                 "commanding divine authority presence inspiring awe and respect, "
                                 "eternal guardian of the dead with unwavering vigilance, "
                                 "intimidating yet noble pose showing protective nature, "
                                 "rich details in armor craftsmanship and divine regalia",
                
                "desert_scorpion": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "giant desert scorpion creature, chitinous exoskeleton with golden markings, "
                                 "venomous stinger raised, menacing claws, "
                                 "sand creature design, predatory stance, desert predator",
                
                "pharaoh_lich": f"{self.art_style_base}, {self.duat_atmosphere}, "
                              "undead pharaoh final boss, ornate golden death mask, "
                              "royal Egyptian regalia, dark necromantic aura, "
                              "floating above throne, commanding presence, ancient evil power",
                
                "temple_guardian": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                 "stone temple guardian construct, hieroglyphic carved body, "
                                 "ancient magic animating statue, imposing size, "
                                 "temple defender, carved Egyptian details, mystical glow in eyes"
            },
            
            "environments": {
                "menu_background": f"{self.art_style_base}, breathtaking cinematic Egyptian underworld landscape, "
                                 "vast endless desert with colossal ancient pyramids silhouetted majestically, "
                                 "rolling golden sand dunes stretching to the horizon, "
                                 "mysterious otherworldly atmosphere with supernatural lighting, "
                                 "dramatic entrance portal to the underworld realm, "
                                 "epic monumental scale emphasizing the journey ahead, "
                                 "dramatic atmospheric lighting with deep shadows and golden highlights, "
                                 "rich environmental storytelling through ancient monuments",
                
                "combat_background": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                   "ancient Egyptian tomb chamber interior, stone pillars with hieroglyphs, "
                                   "flickering torch lighting, mysterious shadows, "
                                   "burial treasures scattered, sacred Egyptian architecture",
                
                "deck_builder_background": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                         "scholarly chamber in Egyptian temple, papyrus scrolls everywhere, "
                                         "magical writing implements, Thoth's wisdom shrine, "
                                         "peaceful study atmosphere, ancient library aesthetic",
                
                "progression_background": f"{self.art_style_base}, {self.duat_atmosphere}, "
                                        "map of the Egyptian underworld, Duat realm passages, "
                                        "glowing pathways through afterlife, divine judgment chambers, "
                                        "mystical journey map, celestial Egyptian art style"
            },
            
            "ui_elements": {
                "ornate_button": f"{self.art_style_base}, ornate Egyptian button design, "
                               "golden hieroglyphic border, carved stone texture, "
                               "ancient Egyptian decorative elements, clickable UI element",
                
                "card_frame": f"{self.art_style_base}, elegant Egyptian card frame border, "
                            "intricate golden decorations, hieroglyphic patterns, "
                            "papyrus texture background, professional card game design",
                
                "health_orb": f"{self.art_style_base}, Egyptian scarab health orb, "
                            "golden beetle with gem center, life force energy, "
                            "glowing magical essence, UI health indicator design",
                
                "mana_crystal": f"{self.art_style_base}, Egyptian ankh mana crystal, "
                              "mystical blue energy core, golden ankh structure, "
                              "magical power reservoir, UI mana indicator design"
            }
        }
        
        # Comprehensive negative prompts for museum-quality control
        self.negative_prompt = (
            "blurry, low quality, distorted, pixelated, noisy, watermark, signature, text, "
            "bad anatomy, deformed, ugly, amateur art, simple drawing, rushed artwork, "
            "cartoon style, anime style, manga style, low detail, boring composition, "
            "modern elements, contemporary clothing, photography, realistic photo, "
            "AI-generated look, artificial appearance, plastic textures, "
            "flat lighting, no depth, no shadows, oversaturated, undersaturated, "
            "generic, boring, uninspired, copy-paste, template-like, "
            "low resolution, compression artifacts, jpeg artifacts, "
            "symmetrical composition, centered subject, predictable layout"
        )
        
        # Egyptian color palette
        self.egyptian_colors = {
            'gold': '#FFD700',
            'bronze': '#CD7F32', 
            'deep_gold': '#B8860B',
            'royal_blue': '#4169E1',
            'desert_sand': '#DEB887',
            'papyrus': '#F5E6A3',
            'obsidian': '#0C0C0C',
            'carnelian': '#B22222',
            'turquoise': '#40E0D0',
            'ivory': '#FFFFF0'
        }
    
    def _setup_device(self, device: str) -> str:
        """Setup compute device with optimizations."""
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                torch.backends.cudnn.benchmark = True
                torch.backends.cuda.enable_flash_sdp(True)
            else:
                device = "cpu"
                self.logger.warning("CUDA not available, using CPU")
        
        if device == "cuda" and torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            self.logger.info(f"Using GPU: {gpu_name} ({memory_gb:.1f} GB)")
        
        return device
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system."""
        log_dir = Path("logs") / datetime.now().strftime("%Y-%m-%d")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "hades_art.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def load_pipeline(self):
        """Load the AI art generation pipeline."""
        if not DIFFUSERS_AVAILABLE:
            self.logger.warning("AI generation not available, using professional placeholders")
            return
        
        self.logger.info(f"Loading {self.model} pipeline for Hades-style art...")
        
        model_configs = {
            "sdxl": {
                "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
                "pipeline": DiffusionPipeline
            },
            "sdturbo": {
                "model_id": "stabilityai/sd-turbo", 
                "pipeline": StableDiffusionPipeline
            }
        }
        
        if self.model not in model_configs:
            raise ValueError(f"Unknown model: {self.model}")
        
        config = model_configs[self.model]
        
        try:
            kwargs = {
                "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
                "use_safetensors": True,
                "variant": "fp16" if self.device == "cuda" else None
            }
            
            self.pipeline = config["pipeline"].from_pretrained(
                config["model_id"], **kwargs
            ).to(self.device)
            
            if self.device == "cuda":
                self.pipeline.enable_model_cpu_offload()
                self.pipeline.enable_vae_slicing() 
                self.pipeline.enable_attention_slicing("max")
            
            self.logger.info(f"Pipeline loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load AI pipeline: {e}")
            self.pipeline = None
    
    def generate_professional_image(self, prompt: str, output_path: str,
                                  width: int = 1024, height: int = 1024,
                                  steps: int = 80, cfg: float = 8.5,
                                  seed: Optional[int] = None) -> bool:
        """Generate a professional-quality Hades-style image."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.pipeline:
                return self._generate_professional_placeholder(prompt, output_path, width, height)
            
            self.logger.info(f"Generating Hades-style art: {prompt[:60]}...")
            
            # Ultra-enhanced prompt for museum-quality Hades style
            enhanced_prompt = f"{prompt}, masterpiece, museum quality, best quality, highly detailed, professional concept art, hand-painted illustration, rich textures, dramatic lighting, painterly brushwork, artistic excellence"
            
            generator = None
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            
            start_time = time.time()
            
            # Generate with high quality settings
            result = self.pipeline(
                prompt=enhanced_prompt,
                negative_prompt=self.negative_prompt,
                num_inference_steps=steps,
                guidance_scale=cfg,
                width=width,
                height=height,
                generator=generator
            )
            
            # Post-process for Hades style
            image = result.images[0]
            image = self._enhance_hades_style(image)
            
            # Save with high quality
            image.save(output_path, quality=95, optimize=True)
            
            generation_time = time.time() - start_time
            self.logger.info(f"Generated in {generation_time:.2f}s: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate image: {e}")
            return self._generate_professional_placeholder(prompt, output_path, width, height)
    
    def _enhance_hades_style(self, image: Image.Image) -> Image.Image:
        """Apply Hades-style post-processing effects."""
        # Enhance colors and contrast like Hades
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # Boost saturation
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)  # Boost contrast
        
        enhancer = ImageEnhance.Sharpness(image) 
        image = enhancer.enhance(1.1)  # Sharpen details
        
        return image
    
    def _generate_professional_placeholder(self, prompt: str, output_path: str,
                                         width: int = 1024, height: int = 1024) -> bool:
        """Generate professional Egyptian-style placeholder."""
        try:
            self.logger.info(f"Creating professional placeholder: {prompt[:40]}...")
            
            # Create base with Egyptian gradient
            img = Image.new('RGB', (width, height), color='#1a1611')
            draw = ImageDraw.Draw(img)
            
            # Egyptian gradient background
            for y in range(height):
                ratio = y / height
                # Deep brown to golden sand gradient
                r = int(26 + ratio * 60)  # 26 -> 86
                g = int(22 + ratio * 40)  # 22 -> 62  
                b = int(17 + ratio * 20)  # 17 -> 37
                color = (r, g, b)
                draw.line([(0, y), (width, y)], fill=color)
            
            # Ornate Egyptian border
            border_width = max(4, width // 80)
            gold_color = '#DAA520'
            
            # Outer border
            draw.rectangle([0, 0, width-1, height-1], outline=gold_color, width=border_width)
            
            # Inner decorative border  
            inner_margin = border_width * 3
            draw.rectangle([inner_margin, inner_margin, width-inner_margin-1, height-inner_margin-1], 
                          outline='#B8860B', width=2)
            
            # Egyptian decorative elements
            center_x, center_y = width // 2, height // 2
            
            # Draw ornate ankh symbol
            symbol_size = min(width, height) // 4
            ankh_color = '#FFD700'
            
            # Ankh oval (top)
            oval_top = center_y - symbol_size // 2
            oval_bottom = center_y - symbol_size // 6
            draw.ellipse([center_x - symbol_size//3, oval_top,
                         center_x + symbol_size//3, oval_bottom], 
                        outline=ankh_color, width=6)
            
            # Ankh vertical line
            draw.rectangle([center_x - symbol_size//12, oval_bottom,
                           center_x + symbol_size//12, center_y + symbol_size//2], 
                          fill=ankh_color)
            
            # Ankh horizontal line
            draw.rectangle([center_x - symbol_size//2, center_y - symbol_size//24,
                           center_x + symbol_size//2, center_y + symbol_size//24], 
                          fill=ankh_color)
            
            # Decorative hieroglyphs around the ankh
            self._draw_hieroglyph_decorations(draw, center_x, center_y, symbol_size, '#CD7F32')
            
            # Title text
            title_size = max(16, width // 40)
            try:
                title_font = ImageFont.truetype("arial.ttf", title_size)
            except:
                title_font = ImageFont.load_default()
            
            title_text = "SANDS OF DUAT"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            title_y = center_y - symbol_size - 40
            
            draw.text((title_x, title_y), title_text, fill='#F5E6A3', font=title_font)
            
            # Subtitle (prompt description)
            subtitle_size = max(12, width // 60)
            try:
                subtitle_font = ImageFont.truetype("arial.ttf", subtitle_size)
            except:
                subtitle_font = ImageFont.load_default()
            
            # Process prompt for display
            display_text = self._format_prompt_for_display(prompt)
            subtitle_bbox = draw.textbbox((0, 0), display_text, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            subtitle_y = center_y + symbol_size + 30
            
            draw.text((subtitle_x, subtitle_y), display_text, fill='#DEB887', font=subtitle_font)
            
            # Save high-quality placeholder
            img.save(output_path, quality=95, optimize=True)
            self.logger.info(f"Professional placeholder created: {output_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create placeholder: {e}")
            return False
    
    def _draw_hieroglyph_decorations(self, draw, center_x, center_y, size, color):
        """Draw decorative hieroglyph-style elements."""
        # Simple geometric patterns inspired by hieroglyphs
        offset = size // 2 + 20
        
        # Left side decorations
        draw.rectangle([center_x - offset - 10, center_y - 15, 
                       center_x - offset, center_y + 15], fill=color)
        draw.ellipse([center_x - offset - 20, center_y - 8,
                     center_x - offset - 5, center_y + 8], outline=color, width=2)
        
        # Right side decorations  
        draw.rectangle([center_x + offset, center_y - 15,
                       center_x + offset + 10, center_y + 15], fill=color)
        draw.ellipse([center_x + offset + 5, center_y - 8,
                     center_x + offset + 20, center_y + 8], outline=color, width=2)
    
    def _format_prompt_for_display(self, prompt: str) -> str:
        """Format prompt text for elegant display."""
        # Extract key terms from prompt
        key_terms = []
        if "card" in prompt.lower():
            key_terms.append("Card Art")
        if "character" in prompt.lower():
            key_terms.append("Character")
        if "environment" in prompt.lower():
            key_terms.append("Environment")
        if "ui" in prompt.lower():
            key_terms.append("UI Element")
        
        # Find Egyptian theme elements
        egyptian_terms = []
        terms_to_check = ["ankh", "anubis", "isis", "ra", "thoth", "pharaoh", "pyramid", "desert", "sand", "mummy"]
        for term in terms_to_check:
            if term in prompt.lower():
                egyptian_terms.append(term.title())
        
        # Combine for display
        if key_terms and egyptian_terms:
            return f"{' '.join(key_terms)} - {', '.join(egyptian_terms[:2])}"
        elif key_terms:
            return ' '.join(key_terms)
        else:
            # Fallback to truncated prompt
            return prompt[:30] + "..." if len(prompt) > 30 else prompt
    
    def generate_complete_card_set(self, output_dir: str) -> int:
        """Generate all cards with Hades-level artistic quality."""
        card_dir = Path(output_dir) / "cards"
        card_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        total_cards = len(self.prompts["cards"])
        
        self.logger.info(f"Generating {total_cards} Hades-style cards...")
        
        for i, (card_name, prompt) in enumerate(self.prompts["cards"].items()):
            output_path = str(card_dir / f"{card_name}.png")
            
            if self.generate_professional_image(
                prompt, output_path,
                width=512, height=768,  # Card aspect ratio
                steps=50 if self.high_quality else 20,
                cfg=7.5,
                seed=42 + i
            ):
                successful += 1
                self.logger.info(f"Card {i+1}/{total_cards} completed: {card_name}")
            
            # Small delay to prevent overheating
            time.sleep(0.5)
        
        self.logger.info(f"Card generation completed: {successful}/{total_cards}")
        return successful
    
    def generate_complete_character_set(self, output_dir: str) -> int:
        """Generate all characters with Hades-level detail."""
        char_dir = Path(output_dir) / "characters"
        char_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        total_chars = len(self.prompts["characters"])
        
        self.logger.info(f"Generating {total_chars} Hades-style characters...")
        
        for i, (char_name, prompt) in enumerate(self.prompts["characters"].items()):
            output_path = str(char_dir / f"{char_name}.png")
            
            if self.generate_professional_image(
                prompt, output_path,
                width=512, height=768,  # Character portrait
                steps=60 if self.high_quality else 25,
                cfg=8.0,
                seed=100 + i
            ):
                successful += 1
                self.logger.info(f"Character {i+1}/{total_chars} completed: {char_name}")
            
            time.sleep(0.5)
        
        self.logger.info(f"Character generation completed: {successful}/{total_chars}")
        return successful
    
    def generate_complete_environment_set(self, output_dir: str) -> int:
        """Generate all environments with cinematic quality."""
        env_dir = Path(output_dir) / "environments"
        env_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        total_envs = len(self.prompts["environments"])
        
        self.logger.info(f"Generating {total_envs} cinematic environments...")
        
        for i, (env_name, prompt) in enumerate(self.prompts["environments"].items()):
            output_path = str(env_dir / f"{env_name}.png")
            
            if self.generate_professional_image(
                prompt, output_path,
                width=1920, height=1080,  # HD background
                steps=70 if self.high_quality else 30,
                cfg=7.0,
                seed=200 + i
            ):
                successful += 1
                self.logger.info(f"Environment {i+1}/{total_envs} completed: {env_name}")
            
            time.sleep(0.5)
        
        self.logger.info(f"Environment generation completed: {successful}/{total_envs}")
        return successful


def main():
    parser = argparse.ArgumentParser(description="Hades-Style Art Generator for Sands of Duat")
    parser.add_argument("--model", default="sdxl", choices=["sdxl", "sdturbo"],
                       help="AI model for generation (sdxl for highest quality)")
    parser.add_argument("--prompt", help="Custom prompt to generate")
    parser.add_argument("--out", help="Output path")
    parser.add_argument("--generate-all", action="store_true", 
                       help="Generate complete professional asset set")
    parser.add_argument("--cards-only", action="store_true", help="Generate cards only")
    parser.add_argument("--characters-only", action="store_true", help="Generate characters only")
    parser.add_argument("--environments-only", action="store_true", help="Generate environments only") 
    parser.add_argument("--high-quality", action="store_true", default=True,
                       help="Use highest quality settings (default)")
    parser.add_argument("--fast", action="store_true", help="Use fast generation mode")
    
    args = parser.parse_args()
    
    # Initialize Hades-style generator
    generator = HadesStyleArtGenerator(
        model=args.model,
        high_quality=not args.fast
    )
    generator.load_pipeline()
    
    output_base = args.out or "game_assets"
    
    print("SANDS OF DUAT - Hades Style Art Generator")
    print("=" * 50)
    
    if args.generate_all:
        print("Generating complete professional asset set...")
        
        card_count = generator.generate_complete_card_set(output_base)
        char_count = generator.generate_complete_character_set(output_base)
        env_count = generator.generate_complete_environment_set(output_base)
        
        print(f"\nGeneration Complete:")
        print(f"  Cards: {card_count}/13")
        print(f"  Characters: {char_count}/5")
        print(f"  Environments: {env_count}/4")
        
    elif args.cards_only:
        card_count = generator.generate_complete_card_set(output_base)
        print(f"Generated {card_count} cards")
        
    elif args.characters_only:
        char_count = generator.generate_complete_character_set(output_base)
        print(f"Generated {char_count} characters")
        
    elif args.environments_only:
        env_count = generator.generate_complete_environment_set(output_base)
        print(f"Generated {env_count} environments")
        
    elif args.prompt and args.out:
        success = generator.generate_professional_image(args.prompt, args.out)
        if success:
            print(f"Successfully generated: {args.out}")
        else:
            print("Generation failed")
            sys.exit(1)
    else:
        print("Use --generate-all for complete set, or --prompt/--out for single image")
        sys.exit(1)


if __name__ == "__main__":
    main()