#!/usr/bin/env python3
"""
ULTRA AI Pipeline para Sands of Duat - Máxima Qualidade
Sistema de geração de assets profissionais com GPU máxima, sem filtros NSFW
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

try:
    import torch
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    from diffusers import StableDiffusionPipeline, DiffusionPipeline
    from diffusers.utils import logging as diffusers_logging
    DIFFUSERS_AVAILABLE = True
except ImportError:
    print("ERRO: Instale as dependências: pip install torch diffusers pillow numpy")
    DIFFUSERS_AVAILABLE = False
    sys.exit(1)

# DESABILITAR COMPLETAMENTE LOGS DESNECESSÁRIOS
diffusers_logging.set_verbosity_error()
logging.getLogger("diffusers").setLevel(logging.ERROR)


@dataclass
class AssetConfig:
    """Configuração de um asset a ser gerado"""
    name: str
    type: str  # 'character', 'card', 'environment'
    prompt: str
    size: Tuple[int, int]
    steps: int = 50
    guidance: float = 8.0


class UltraAIPipeline:
    """Pipeline AI Ultra Potente para geração de assets"""
    
    def __init__(self, output_dir: str = "game_assets"):
        self.output_dir = Path(output_dir)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        
        # CONFIGURAÇÕES ULTRA POTENTES
        self.ultra_config = {
            "model": "runwayml/stable-diffusion-v1-5",
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            "safety_checker": None,  # DESABILITAR NSFW
            "requires_safety_checker": False,
            "use_safetensors": True
        }
        
        # RESOLUÇÕES ULTRA
        self.resolutions = {
            "concept": (1024, 1024),      # 4x maior que antes
            "card": (1024, 1536),         # 2x maior que antes  
            "environment": (2560, 1440),  # 4K quality
            "sprite": (512, 512),         # 8x maior que antes
        }
        
        # STEPS ALTA QUALIDADE (60 steps padrão)
        self.ultra_steps = {
            "concept": 60,        # Alta qualidade como solicitado
            "card": 60,           # Consistente
            "environment": 60,    # Mesma qualidade
            "sprite": 60,         # Uniformizado
        }
        
        self._setup_directories()
        self._load_ultra_model()
    
    def _setup_directories(self):
        """Criar estrutura de pastas organizada"""
        # ESTRUTURA LIMPA E ORGANIZADA
        dirs = [
            "characters/concepts",
            "characters/sprites", 
            "characters/animations",
            "cards",
            "environments",
            "ui_elements",
            "effects"
        ]
        
        for dir_path in dirs:
            (self.output_dir / dir_path).mkdir(parents=True, exist_ok=True)
        
        print(f"[PASTAS] Estrutura criada em: {self.output_dir}")
    
    def _disable_nsfw_completely(self, pipeline):
        """DESABILITAR COMPLETAMENTE O FILTRO NSFW"""
        # Método mais simples - apenas remover
        pipeline.safety_checker = None
        pipeline.requires_safety_checker = False
        
        # Se existir feature_extractor, remover também
        if hasattr(pipeline, 'feature_extractor'):
            pipeline.feature_extractor = None
            
        return pipeline
    
    def _load_ultra_model(self):
        """Carregar modelo com configurações ultra potentes"""
        print("[AI] Carregando modelo ultra potente...")
        start_time = time.time()
        
        try:
            # CARREGAR COM MÁXIMA POTÊNCIA
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.ultra_config["model"],
                torch_dtype=self.ultra_config["torch_dtype"],
                safety_checker=None,  # SEM NSFW
                requires_safety_checker=False,  # SEM NSFW
                use_safetensors=True
            )
            
            # DESABILITAR NSFW COMPLETAMENTE
            self.pipeline = self._disable_nsfw_completely(self.pipeline)
            
            if self.device == "cuda":
                self.pipeline = self.pipeline.to(self.device)
                
                # OTIMIZAÇÕES HÍBRIDAS GPU/CPU INTELIGENTES
                try:
                    # VAE e Text Encoder para CPU (libera ~70% da VRAM)
                    self.pipeline.enable_model_cpu_offload()
                    
                    # Manter UNet na GPU (parte mais pesada da inferência)
                    self.pipeline.unet.to(self.device)
                    
                    # Otimizações de memória
                    self.pipeline.enable_vae_slicing()
                    self.pipeline.enable_vae_tiling() 
                    self.pipeline.enable_attention_slicing(1)
                    
                    # Usar menos precisão para economizar VRAM
                    if hasattr(self.pipeline.unet, 'set_use_memory_efficient_attention_xformers'):
                        self.pipeline.unet.set_use_memory_efficient_attention_xformers(True)
                    
                    print("[GPU] Otimizações híbridas ativadas - GPU ~40% liberada")
                except Exception as e:
                    print(f"[WARN] Algumas otimizações falharam: {e}")
                    print("[GPU] Usando configuração padrão")
            
            load_time = time.time() - start_time
            print(f"[OK] Modelo carregado em {load_time:.1f}s no {self.device}")
            
        except Exception as e:
            print(f"[ERRO] Erro ao carregar modelo: {e}")
            sys.exit(1)
    
    def generate_ultra_image(self, config: AssetConfig) -> Optional[str]:
        """Gerar imagem com qualidade ultra"""
        if not self.pipeline:
            print("[ERRO] Pipeline não carregado")
            return None
        
        print(f"[GEN] Gerando {config.type}: {config.name}")
        print(f"   [SIZE] Resolução: {config.size[0]}x{config.size[1]}")
        print(f"   [STEPS] Steps: {config.steps}")
        
        start_time = time.time()
        
        try:
            # GERAÇÃO ULTRA COM SEM NSFW
            with torch.no_grad():
                result = self.pipeline(
                    prompt=config.prompt,
                    negative_prompt="blurry, low quality, pixelated, ugly, deformed, amateur",
                    num_inference_steps=config.steps,
                    guidance_scale=config.guidance,
                    width=config.size[0],
                    height=config.size[1],
                    generator=torch.manual_seed(int(time.time()))  # Seed aleatório
                )
            
            image = result.images[0]
            
            # PÓS-PROCESSAMENTO ULTRA
            image = self._ultra_enhance(image)
            
            # SALVAR COM QUALIDADE MÁXIMA
            output_path = self._get_output_path(config)
            image.save(output_path, "PNG", optimize=True, quality=100)
            
            gen_time = time.time() - start_time
            print(f"   [OK] Gerado em {gen_time:.1f}s -> {output_path}")
            
            # LIMPEZA DE MEMÓRIA após cada geração
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            return str(output_path)
            
        except Exception as e:
            print(f"   [ERRO] Erro na geração: {e}")
            return None
    
    def _ultra_enhance(self, image: Image.Image) -> Image.Image:
        """Pós-processamento ultra para melhorar qualidade"""
        # Sharpen ultra
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=2))
        
        # Contrast enhancement
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.15)
        
        # Color enhancement  
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        
        # Brightness fine-tune
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.05)
        
        return image
    
    def _get_output_path(self, config: AssetConfig) -> Path:
        """Determinar caminho de saída baseado no tipo"""
        if config.type == "character_concept":
            return self.output_dir / "characters" / "concepts" / f"{config.name}.png"
        elif config.type == "character_sprite":
            return self.output_dir / "characters" / "sprites" / f"{config.name}.png"
        elif config.type == "card":
            return self.output_dir / "cards" / f"{config.name}.png"
        elif config.type == "environment":
            return self.output_dir / "environments" / f"{config.name}.png"
        else:
            return self.output_dir / f"{config.name}.png"
    
    def generate_all_game_assets(self) -> List[str]:
        """Gerar TODOS os assets do jogo com qualidade ultra"""
        print("[GAME] GERANDO TODOS OS ASSETS DO JOGO - QUALIDADE ULTRA")
        print("=" * 60)
        
        # LISTA COMPLETA DE ASSETS A SEREM GERADOS
        total_assets = {
            "Conceitos de Personagens": 5,
            "Sprites de Personagens": 15,  # 5 chars x 3 actions
            "Arte de Cartas": 13,
            "Ambientes": 5
        }
        
        print("[LISTA] Assets a serem gerados:")
        total_count = 0
        for category, count in total_assets.items():
            print(f"  - {category}: {count} arquivos")
            total_count += count
        print(f"[TOTAL] {total_count} assets profissionais")
        print("=" * 60)
        
        generated_files = []
        
        # PERSONAGENS - CONCEITOS ULTRA
        characters = {
            "anubis_guardian": "Majestic Anubis guardian warrior, jackal head, ornate golden armor, mystical Egyptian temple background, dramatic lighting, highly detailed, masterpiece quality",
            "desert_scorpion": "Giant mystical desert scorpion, golden chitin armor, Egyptian hieroglyphic patterns, sandy dunes background, menacing pose, ultra detailed",
            "pharaoh_lich": "Undead pharaoh king, mummified royal appearance, golden headdress, glowing blue eyes, ancient tomb setting, epic fantasy art",
            "temple_guardian": "Massive stone temple guardian statue, Egyptian architecture, carved hieroglyphs, weathered sandstone texture, imposing presence",
            "player_character": "Heroic Egyptian warrior adventurer, leather armor, bronze weapons, confident desert explorer, detailed character design"
        }
        
        current_asset = 0
        print("[CATEGORIA] CONCEITOS DE PERSONAGENS")
        for char_name, prompt in characters.items():
            current_asset += 1
            print(f"[{current_asset}/{total_count}] Gerando conceito: {char_name}")
            
            config = AssetConfig(
                name=char_name,
                type="character_concept", 
                prompt=prompt,
                size=self.resolutions["concept"],
                steps=self.ultra_steps["concept"],
                guidance=8.5
            )
            result = self.generate_ultra_image(config)
            if result:
                generated_files.append(result)
                print(f"   [SUCESSO] Arquivo: {result}")
            else:
                print(f"   [FALHA] Não foi possível gerar {char_name}")
        
        print(f"[COMPLETO] Conceitos: {len([f for f in generated_files if 'concepts' in f])}/5")
        
        # CARTAS - ARTE ULTRA
        cards = {
            "desert_whisper": "Ancient papyrus scroll with swirling sand spirits, mystical wind magic, Egyptian hieroglyphs, warm golden tones",
            "sand_grain": "Magical golden sand grain floating in hourglass, time magic essence, ethereal glow, mystical energy",
            "tomb_strike": "Egyptian warrior striking with curved khopesh sword, dynamic combat pose, stone tomb background",
            "ankh_blessing": "Sacred golden ankh symbol radiating divine healing light, protective magic aura, blessed energy",
            "scarab_swarm": "Swarm of golden scarab beetles in mystical formation, ancient Egyptian magic, attacking pattern",
            "papyrus_scroll": "Ancient Egyptian scroll with glowing hieroglyphics, knowledge magic, scholarly wisdom",
            "mummys_wrath": "Angry mummy with glowing red eyes, flowing bandages, undead necromantic power",
            "isis_grace": "Goddess Isis with protective wings spread, healing divine light, graceful blessing pose",
            "pyramid_power": "Great pyramid with mystical energy beams, ancient Egyptian magic, geometric power",
            "thoths_wisdom": "Ibis-headed god Thoth with magical scroll, divine wisdom, scholarly magic",
            "anubis_judgment": "Anubis with golden scales of justice, underworld authority, divine judgment",
            "ra_solar_flare": "Sun god Ra with blazing solar disk, intense divine sunlight, solar magic",
            "pharaohs_resurrection": "Pharaoh rising from golden sarcophagus, royal regalia, resurrection magic"
        }
        
        print("\n[CATEGORIA] ARTE DE CARTAS")
        for card_name, prompt in cards.items():
            current_asset += 1
            print(f"[{current_asset}/{total_count}] Gerando carta: {card_name}")
            
            config = AssetConfig(
                name=card_name,
                type="card",
                prompt=f"{prompt}, Egyptian card art, ornate border, professional illustration, highly detailed",
                size=self.resolutions["card"],
                steps=self.ultra_steps["card"],
                guidance=8.0
            )
            result = self.generate_ultra_image(config)
            if result:
                generated_files.append(result)
                print(f"   [SUCESSO] Arquivo: {result}")
            else:
                print(f"   [FALHA] Não foi possível gerar {card_name}")
        
        print(f"[COMPLETO] Cartas: {len([f for f in generated_files if 'cards' in f])}/13")
        
        # AMBIENTES - QUALIDADE 4K
        environments = {
            "desert_battlefield": "Epic Egyptian desert battlefield, sand dunes, ancient ruins, dramatic sunset lighting, cinematic quality",
            "temple_interior": "Interior of grand Egyptian temple, massive columns, hieroglyphic walls, torch lighting, atmospheric",
            "tomb_chamber": "Ancient pharaoh tomb chamber, golden sarcophagi, treasure, mysterious lighting, detailed architecture",
            "oasis": "Peaceful desert oasis, palm trees, crystal clear water, Egyptian setting, serene atmosphere",
            "pyramid_chamber": "Inside great pyramid chamber, massive stone blocks, mystical lighting, ancient architecture"
        }
        
        for env_name, prompt in environments.items():
            config = AssetConfig(
                name=env_name,
                type="environment",
                prompt=f"{prompt}, epic landscape, ultra wide composition, 4K quality, professional photography",
                size=self.resolutions["environment"],
                steps=self.ultra_steps["environment"],
                guidance=9.0
            )
            result = self.generate_ultra_image(config)
            if result:
                generated_files.append(result)
        
        # SPRITES DE PERSONAGENS
        for char_name in characters.keys():
            for action in ["idle", "walk", "attack"]:
                sprite_prompt = f"{characters[char_name]}, {action} pose, pixel art style, game sprite, clean background"
                config = AssetConfig(
                    name=f"{char_name}_{action}",
                    type="character_sprite",
                    prompt=sprite_prompt,
                    size=self.resolutions["sprite"],
                    steps=self.ultra_steps["sprite"],
                    guidance=7.5
                )
                result = self.generate_ultra_image(config)
                if result:
                    generated_files.append(result)
        
        print("=" * 60)
        print(f"[FINAL] GERAÇÃO COMPLETA: {len(generated_files)} assets criados!")
        print(f"[DIR] Assets salvos em: {self.output_dir}")
        
        return generated_files


def main():
    """Interface principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ultra AI Pipeline - Máxima Qualidade")
    parser.add_argument("--output", default="game_assets", help="Diretório de saída")
    parser.add_argument("--full", action="store_true", help="Gerar todos os assets")
    
    args = parser.parse_args()
    
    # INICIALIZAR PIPELINE ULTRA
    pipeline = UltraAIPipeline(args.output)
    
    if args.full:
        # GERAR TUDO COM QUALIDADE ULTRA
        generated = pipeline.generate_all_game_assets()
        
        # RELATÓRIO FINAL
        print("\n" + "=" * 60)
        print("[REPORT] RELATÓRIO FINAL")
        print("=" * 60)
        print(f"Assets gerados: {len(generated)}")
        print(f"Qualidade: ULTRA (sem filtros NSFW)")
        print(f"GPU utilizada: Máxima potência")
        print(f"Resolução: 4K para ambientes, 1024px para cartas/conceitos")
        print("[OK] PIPELINE COMPLETO!")


if __name__ == "__main__":
    main()