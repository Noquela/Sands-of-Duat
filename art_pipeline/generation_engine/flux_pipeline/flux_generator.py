#!/usr/bin/env python3
"""
FLUX.1-DEV GENERATOR - HADES STYLE
==================================

Sistema otimizado de geração usando Flux.1-dev para arte no estilo Hades
com controle total de qualidade e consistência.
"""

import torch
from diffusers import FluxPipeline
from pathlib import Path
import time
from PIL import Image
import json
from datetime import datetime

class HadesFluxGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = Path("../../assets/work_in_progress/testing")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações otimizadas para RTX 5070
        self.config = {
            "model_id": "black-forest-labs/FLUX.1-dev",
            "torch_dtype": torch.bfloat16,
            "variant": "fp16",
            "use_safetensors": True
        }
        
        # Settings otimizados para estilo Hades
        self.generation_params = {
            "width": 1024,
            "height": 1024, 
            "num_inference_steps": 28,  # Otimizado para qualidade/velocidade
            "guidance_scale": 7.5,      # Aderência ao prompt
            "max_sequence_length": 256  # Prompts detalhados
        }
        
        # Base prompts do estilo Hades
        self.style_prompts = {
            "base_style": "hand-painted digital art, dramatic chiaroscuro lighting, vibrant saturated colors, black ink outlines, pen and ink style, heroic proportions, dynamic composition",
            "hades_elements": "inspired by Supergiant Games Hades art style, Jen Zee art style, Mike Mignola influence",
            "egyptian_fusion": "ancient egyptian mythology, hieroglyphic elements, pharaonic architecture, desert mysticism",
            "quality_terms": "masterpiece, highly detailed, professional game art, concept art quality, sharp focus"
        }
        
        # Negative prompt otimizado
        self.negative_prompt = """
        blurry, low quality, amateur, sketch, dull colors, soft lighting, pastel colors,
        anime style, cartoon, chibi, realistic photography, 3d render, multiple characters,
        crowd, text, watermark, signature, logo, bad anatomy, deformed, distorted
        """.strip().replace('\n', ' ')

    def setup_pipeline(self):
        """Inicializa pipeline Flux.1-dev otimizado."""
        print("🚀 Inicializando Flux.1-dev Pipeline...")
        print(f"💾 GPU: {torch.cuda.get_device_name(0)}")
        
        try:
            # Carrega Flux.1-dev
            self.pipe = FluxPipeline.from_pretrained(
                self.config["model_id"],
                torch_dtype=self.config["torch_dtype"],
                variant=self.config["variant"], 
                use_safetensors=self.config["use_safetensors"]
            )
            
            # Move para GPU e otimiza
            self.pipe = self.pipe.to(self.device)
            
            # Otimizações de memória para RTX 5070
            if hasattr(self.pipe, 'enable_model_cpu_offload'):
                self.pipe.enable_model_cpu_offload()
            
            if hasattr(self.pipe, 'enable_attention_slicing'):
                self.pipe.enable_attention_slicing(1)
                
            print("✅ Flux.1-dev Pipeline pronto!")
            return True
            
        except Exception as e:
            print(f"❌ Erro no setup: {e}")
            return False

    def build_hades_prompt(self, subject, character_type="character", specific_elements=""):
        """Constrói prompt otimizado no estilo Hades."""
        
        # Base do prompt
        prompt_parts = [
            self.style_prompts["base_style"],
            self.style_prompts["hades_elements"],
            self.style_prompts["egyptian_fusion"],
            subject,
            specific_elements,
            self.style_prompts["quality_terms"]
        ]
        
        # Adiciona elementos específicos por tipo
        if character_type == "deity":
            prompt_parts.insert(-1, "divine aura, godlike presence, regal bearing, supernatural elements")
        elif character_type == "hero":
            prompt_parts.insert(-1, "heroic stance, determined expression, warrior attitude")
        elif character_type == "creature":
            prompt_parts.insert(-1, "mystical creature, otherworldly, magical essence")
        elif character_type == "environment":
            prompt_parts.insert(-1, "architectural grandeur, atmospheric lighting, epic scale")
            
        # Remove partes vazias e junta
        prompt = ", ".join([part.strip() for part in prompt_parts if part.strip()])
        
        return prompt

    def generate_test_image(self, subject, character_type="character", seed=None):
        """Gera imagem de teste para validação."""
        if not self.pipe:
            print("❌ Pipeline não inicializado!")
            return None
            
        print(f"🎨 Gerando: {subject}")
        
        # Constrói prompt
        prompt = self.build_hades_prompt(subject, character_type)
        print(f"📝 Prompt: {prompt[:100]}...")
        
        # Configura gerador com seed
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
            
        try:
            # Geração com Flux.1-dev
            start_time = time.time()
            
            image = self.pipe(
                prompt=prompt,
                negative_prompt=self.negative_prompt,
                width=self.generation_params["width"],
                height=self.generation_params["height"],
                num_inference_steps=self.generation_params["num_inference_steps"],
                guidance_scale=self.generation_params["guidance_scale"],
                max_sequence_length=self.generation_params["max_sequence_length"],
                generator=generator
            ).images[0]
            
            generation_time = time.time() - start_time
            print(f"⚡ Gerado em {generation_time:.1f}s")
            
            # Salva com metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_{subject.replace(' ', '_').lower()}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Adiciona metadata
            metadata = {
                "prompt": prompt,
                "negative_prompt": self.negative_prompt,
                "parameters": self.generation_params,
                "generation_time": generation_time,
                "seed": seed,
                "character_type": character_type
            }
            
            image.save(filepath, "PNG", optimize=True)
            
            # Salva metadata em JSON
            metadata_file = filepath.with_suffix('.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
            print(f"💾 Salvo: {filepath}")
            return image, filepath
            
        except Exception as e:
            print(f"❌ Erro na geração: {e}")
            return None, None

    def test_hades_style(self):
        """Executa testes para validar o estilo Hades."""
        print("🧪 TESTANDO GERAÇÃO ESTILO HADES")
        print("=" * 50)
        
        # Testes básicos do estilo
        test_subjects = [
            ("Anubis egyptian god with jackal head", "deity"),
            ("Ra sun god with falcon head and solar disk crown", "deity"),
            ("egyptian warrior hero in pharaonic armor", "hero"),
            ("ancient egyptian temple with massive columns", "environment")
        ]
        
        results = []
        
        for subject, char_type in test_subjects:
            print(f"\n🎭 Teste: {subject}")
            
            image, filepath = self.generate_test_image(
                subject=subject, 
                character_type=char_type,
                seed=42  # Seed fixo para consistência
            )
            
            if image:
                results.append({
                    "subject": subject,
                    "type": char_type, 
                    "filepath": str(filepath),
                    "success": True
                })
            else:
                results.append({
                    "subject": subject,
                    "type": char_type,
                    "filepath": None,
                    "success": False
                })
                
            # Pausa para evitar overheating
            time.sleep(3)
        
        # Salva relatório de testes
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(test_subjects),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "config": self.generation_params,
            "results": results
        }
        
        report_file = self.output_dir / "hades_style_test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n📊 RELATÓRIO DE TESTES:")
        print(f"✅ Sucessos: {report['successful']}/{report['total_tests']}")
        print(f"💾 Relatório: {report_file}")
        
        return results

def main():
    """Executa setup e testes do Flux.1-dev."""
    generator = HadesFluxGenerator()
    
    # Setup do pipeline
    if generator.setup_pipeline():
        print("🎯 Pipeline configurado com sucesso!")
        
        # Executa testes do estilo Hades
        results = generator.test_hades_style()
        
        print("\n🏆 FASE 2 - SETUP TÉCNICO CONCLUÍDO!")
        print("Flux.1-dev está pronto para gerar assets no estilo Hades")
        
    else:
        print("❌ Falha no setup do pipeline")

if __name__ == "__main__":
    main()