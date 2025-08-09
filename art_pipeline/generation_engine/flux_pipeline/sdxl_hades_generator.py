#!/usr/bin/env python3
"""
SDXL HADES GENERATOR - OPTIMIZED
================================

Sistema otimizado usando SDXL para gerar assets no estilo Hades
com configurações específicas para pen & ink + chiaroscuro.
"""

import torch
from diffusers import StableDiffusionXLPipeline
from pathlib import Path
import time
from PIL import Image
import json
from datetime import datetime

class HadesSDXLGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = Path("../../assets/work_in_progress/testing")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuracoes otimizadas para SDXL + Hades style
        self.generation_params = {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "clip_skip": 2
        }
        
        # Prompt base otimizado para Hades style
        self.hades_style_base = """
        hades game art style, hand-painted digital art, dramatic chiaroscuro lighting,
        vibrant saturated colors, black ink outlines, pen and ink technique,
        heroic proportions, dynamic composition, Jen Zee art style,
        Mike Mignola influence, Supergiant Games artwork, masterpiece
        """.strip().replace('\n', ' ')
        
        # Elementos egipcios para fusao
        self.egyptian_elements = """
        ancient egyptian mythology, hieroglyphic elements, pharaonic symbols,
        desert mysticism, golden ornaments, egyptian architecture
        """.strip().replace('\n', ' ')
        
        # Negative prompt otimizado
        self.negative_prompt = """
        blurry, low quality, amateur, sketch, dull colors, soft lighting, pastel colors,
        anime style, cartoon, chibi, realistic photography, 3d render, multiple characters,
        crowd, text, watermark, signature, bad anatomy, deformed, distorted, extra limbs
        """.strip().replace('\n', ' ')

    def setup_pipeline(self):
        """Inicializa pipeline SDXL otimizado."""
        print("Inicializando SDXL Pipeline para Hades Style...")
        print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
        
        try:
            # Carrega SDXL
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                use_safetensors=True
            ).to(self.device)
            
            # Otimizacoes para RTX 5070
            self.pipe.enable_model_cpu_offload()
            if hasattr(self.pipe, 'enable_attention_slicing'):
                self.pipe.enable_attention_slicing(1)
            
            print("SDXL Pipeline configurado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro no setup SDXL: {e}")
            return False

    def build_hades_egyptian_prompt(self, subject, character_type="character", color_scheme="red_gold"):
        """Constroi prompt otimizado Hades-Egipcio."""
        
        # Paletas de cor especificas
        color_palettes = {
            "red_gold": "rich red #C41E3A and golden #FFD700 color palette, dramatic red lighting",
            "blue_mystical": "deep blue #191970 and golden #FFD700 accents, mystical blue lighting",
            "purple_shadow": "dark purple #4B0082 and silver highlights, shadowy atmosphere"
        }
        
        # Elementos por tipo de personagem
        character_elements = {
            "deity": "divine aura, godlike presence, regal bearing, supernatural radiance, majestic pose",
            "hero": "heroic stance, determined expression, warrior attitude, battle-ready pose",
            "creature": "mystical creature, otherworldly essence, threatening presence, predatory stance",
            "environment": "epic architectural scale, atmospheric perspective, cinematic composition"
        }
        
        # Constroi o prompt final
        prompt_parts = [
            self.hades_style_base,
            self.egyptian_elements,
            subject,
            character_elements.get(character_type, "detailed character design"),
            color_palettes.get(color_scheme, color_palettes["red_gold"]),
            "highly detailed, professional game art, sharp focus"
        ]
        
        prompt = ", ".join([part.strip() for part in prompt_parts if part.strip()])
        return prompt

    def generate_hades_asset(self, subject, character_type="character", color_scheme="red_gold", seed=42):
        """Gera asset no estilo Hades-Egipcio."""
        if not self.pipe:
            print("Pipeline nao inicializado!")
            return None, None
            
        print(f"Gerando: {subject}")
        
        # Constroi prompt
        prompt = self.build_hades_egyptian_prompt(subject, character_type, color_scheme)
        print(f"Prompt: {prompt[:80]}...")
        
        try:
            # Configura generator
            generator = torch.Generator(device=self.device).manual_seed(seed)
            
            # Geracao
            start_time = time.time()
            
            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.negative_prompt,
                width=self.generation_params["width"],
                height=self.generation_params["height"],
                num_inference_steps=self.generation_params["num_inference_steps"],
                guidance_scale=self.generation_params["guidance_scale"],
                generator=generator
            ).images[0]
            
            generation_time = time.time() - start_time
            print(f"Gerado em {generation_time:.1f}s")
            
            # Salva com metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_subject = subject.replace(' ', '_').replace('/', '_').lower()
            filename = f"hades_{safe_subject}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Salva imagem
            image.save(filepath, "PNG", optimize=True)
            
            # Salva metadata
            metadata = {
                "subject": subject,
                "character_type": character_type,
                "color_scheme": color_scheme,
                "prompt": prompt,
                "negative_prompt": self.negative_prompt,
                "parameters": self.generation_params,
                "generation_time": generation_time,
                "seed": seed,
                "filepath": str(filepath)
            }
            
            metadata_file = filepath.with_suffix('.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
            print(f"Salvo: {filepath}")
            return image, filepath
            
        except Exception as e:
            print(f"Erro na geracao: {e}")
            return None, None

    def test_hades_egyptian_fusion(self):
        """Testa geracao com fusao Hades-Egipcio."""
        print("TESTANDO FUSAO HADES-EGIPCIO")
        print("=" * 40)
        
        # Testes especificos
        test_cases = [
            {
                "subject": "Anubis egyptian god with jackal head, golden ceremonial collar, divine presence",
                "type": "deity",
                "colors": "red_gold",
                "expected": "Anubis no estilo Hades com collar dourado"
            },
            {
                "subject": "Ra sun god with falcon head, solar disk crown, radiant golden aura",
                "type": "deity", 
                "colors": "red_gold",
                "expected": "Ra majestoso com disco solar"
            },
            {
                "subject": "Egyptian warrior hero in pharaonic armor, determined expression, battle stance",
                "type": "hero",
                "colors": "blue_mystical",
                "expected": "Heroi egipcio estilo Zagreus"
            },
            {
                "subject": "Ancient egyptian temple interior, massive columns, hieroglyphic carvings, dramatic lighting",
                "type": "environment",
                "colors": "purple_shadow", 
                "expected": "Templo com atmosfera underworld"
            }
        ]
        
        results = []
        
        for i, test in enumerate(test_cases):
            print(f"\nTeste {i+1}/4: {test['expected']}")
            
            image, filepath = self.generate_hades_asset(
                subject=test["subject"],
                character_type=test["type"],
                color_scheme=test["colors"],
                seed=42 + i  # Seeds diferentes para variedade
            )
            
            success = image is not None
            results.append({
                "test_case": test["expected"],
                "subject": test["subject"],
                "success": success,
                "filepath": str(filepath) if filepath else None
            })
            
            if success:
                print(f"SUCESSO: {test['expected']}")
            else:
                print(f"FALHA: {test['expected']}")
                
            # Pausa para cooling
            time.sleep(2)
        
        # Relatorio
        successful = sum(1 for r in results if r["success"])
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_type": "Hades-Egyptian Fusion",
            "total_tests": len(test_cases),
            "successful": successful,
            "success_rate": successful / len(test_cases),
            "results": results
        }
        
        report_file = self.output_dir / "hades_fusion_test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\nRESULTADOS DOS TESTES:")
        print(f"Sucessos: {successful}/{len(test_cases)}")
        print(f"Taxa de sucesso: {successful/len(test_cases)*100:.1f}%")
        print(f"Relatorio salvo: {report_file}")
        
        return results

def main():
    """Executa setup e testes SDXL Hades."""
    generator = HadesSDXLGenerator()
    
    print("CONFIGURANDO GERADOR HADES-SDXL")
    print("=" * 35)
    
    # Setup do pipeline
    if generator.setup_pipeline():
        print("Pipeline SDXL configurado!")
        
        # Testa fusao Hades-Egipcio
        results = generator.test_hades_egyptian_fusion()
        
        print("\nFASE 2 - SETUP TECNICO COMPLETO!")
        print("SDXL otimizado para estilo Hades-Egipcio")
        
    else:
        print("Falha no setup do pipeline")

if __name__ == "__main__":
    main()