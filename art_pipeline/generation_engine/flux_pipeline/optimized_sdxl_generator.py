#!/usr/bin/env python3
"""
OPTIMIZED SDXL GENERATOR - RTX 5070 MAX POWER
=============================================
Configurações otimizadas para usar 100% da RTX 5070
"""

import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from pathlib import Path
import time
from datetime import datetime
import gc

class OptimizedSDXLGenerator:
    def __init__(self):
        self.device = "cuda"
        self.pipe = None
        
        # Configurações OTIMIZADAS para RTX 5070
        self.optimization_config = {
            # GPU Memory - usar TODA a VRAM
            "enable_cpu_offload": False,  # DESATIVAR para usar GPU 100%
            "enable_attention_slicing": False,  # DESATIVAR para usar GPU 100%
            "enable_vae_slicing": False,  # DESATIVAR para usar GPU 100%
            "enable_xformers": True,  # ATIVAR para performance máxima
            
            # Precision - máxima qualidade
            "torch_dtype": torch.float16,
            "variant": "fp16",
            
            # Batch processing - processar múltiplas em paralelo
            "batch_size": 2,  # RTX 5070 aguenta 2 imagens simultâneas em 1024x1024
            
            # Memory management
            "use_safetensors": True,
            "low_cpu_mem_usage": False,  # Usar toda RAM também
        }
        
        # Configurações de geração otimizadas
        self.generation_config = {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30,  # Mais steps = melhor qualidade
            "guidance_scale": 8.0,  # Mais guidance = melhor aderência
            "clip_skip": 1,  # Sem clip skip para máxima qualidade
        }

    def setup_optimized_pipeline(self):
        """Configura pipeline SDXL com otimizações máximas."""
        print("Configurando SDXL OTIMIZADO para RTX 5070...")
        print("ATENÇÃO: Vai usar MÁXIMA GPU e VRAM!")
        
        # Limpa cache GPU
        torch.cuda.empty_cache()
        gc.collect()
        
        try:
            # Carrega SDXL com configurações otimizadas
            print("Carregando SDXL base model...")
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=self.optimization_config["torch_dtype"],
                variant=self.optimization_config["variant"],
                use_safetensors=self.optimization_config["use_safetensors"],
                low_cpu_mem_usage=self.optimization_config["low_cpu_mem_usage"]
            )
            
            # Move TUDO para GPU
            print("Movendo pipeline COMPLETO para GPU...")
            self.pipe = self.pipe.to(self.device)
            
            # Aplicar otimizações de performance
            print("Aplicando otimizações de performance...")
            
            # XFormers para attention otimizada (se disponível)
            if self.optimization_config["enable_xformers"]:
                try:
                    self.pipe.enable_xformers_memory_efficient_attention()
                    print("✓ XFormers memory efficient attention ATIVADO")
                except:
                    print("⚠ XFormers não disponível, continuando sem...")
            
            # Scheduler otimizado
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config,
                use_karras_sigmas=True,  # Melhor qualidade
                algorithm_type="dpmsolver++",  # Mais rápido
            )
            print("✓ Scheduler DPMSolver++ otimizado configurado")
            
            # Compile modelo para máxima performance (PyTorch 2.0+)
            if hasattr(torch, 'compile'):
                print("Compilando modelo com torch.compile...")
                self.pipe.unet = torch.compile(self.pipe.unet, mode="max-autotune")
                print("✓ UNet compilado para máxima performance")
            
            # Verifica VRAM disponível
            if torch.cuda.is_available():
                vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print(f"✓ VRAM Total: {vram_gb:.1f}GB")
                print(f"✓ VRAM Livre: {torch.cuda.memory_reserved(0) / (1024**3):.1f}GB")
            
            print("🚀 SDXL OTIMIZADO configurado para MÁXIMA PERFORMANCE!")
            return True
            
        except Exception as e:
            print(f"❌ Erro no setup otimizado: {e}")
            return False

    def generate_optimized_batch(self, prompts, negative_prompt=None, seeds=None):
        """Gera batch de imagens com máxima utilização da GPU."""
        if not self.pipe:
            print("Pipeline não inicializado!")
            return []
            
        batch_size = min(len(prompts), self.optimization_config["batch_size"])
        print(f"Gerando batch de {batch_size} imagens em paralelo...")
        
        # Negative prompt padrão
        if negative_prompt is None:
            negative_prompt = "blurry, low quality, amateur, multiple characters, text, watermark, bad anatomy"
        
        # Seeds aleatórias se não fornecidas
        if seeds is None:
            seeds = [torch.randint(0, 2**32, (1,)).item() for _ in prompts]
        
        results = []
        
        try:
            start_time = time.time()
            
            # Processa em batches
            for i in range(0, len(prompts), batch_size):
                batch_prompts = prompts[i:i+batch_size]
                batch_seeds = seeds[i:i+batch_size]
                
                print(f"Processando batch {i//batch_size + 1}...")
                
                # Generator para cada seed
                generators = [
                    torch.Generator(device=self.device).manual_seed(seed) 
                    for seed in batch_seeds
                ]
                
                # Geração em batch
                batch_images = self.pipe(
                    prompt=batch_prompts,
                    negative_prompt=[negative_prompt] * len(batch_prompts),
                    width=self.generation_config["width"],
                    height=self.generation_config["height"],
                    num_inference_steps=self.generation_config["num_inference_steps"],
                    guidance_scale=self.generation_config["guidance_scale"],
                    generator=generators
                ).images
                
                results.extend(batch_images)
                
                # Força limpeza de memória entre batches
                torch.cuda.empty_cache()
            
            total_time = time.time() - start_time
            avg_time = total_time / len(prompts)
            
            print(f"🚀 {len(prompts)} imagens geradas em {total_time:.1f}s")
            print(f"⚡ Média: {avg_time:.1f}s por imagem")
            print(f"💪 Performance: {60/avg_time:.1f} imagens/minuto")
            
            return results
            
        except Exception as e:
            print(f"Erro na geração: {e}")
            return []

    def test_max_performance(self):
        """Testa performance máxima com múltiplas imagens."""
        print("TESTE DE PERFORMANCE MÁXIMA RTX 5070")
        print("=" * 50)
        
        # Prompts de teste Hades-Egyptian
        test_prompts = [
            "Anubis egyptian god with jackal head, golden collar, dramatic chiaroscuro lighting, pen and ink style, hades game art",
            "Ra sun god with falcon head, solar disk crown, egyptian temple background, dramatic lighting, digital art masterpiece"
        ]
        
        # Gera batch
        images = self.generate_optimized_batch(test_prompts)
        
        if images:
            # Salva resultados
            output_dir = Path("../../assets/work_in_progress/max_performance_test")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for i, image in enumerate(images):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"max_perf_test_{i+1}_{timestamp}.png"
                filepath = output_dir / filename
                image.save(filepath, "PNG")
                print(f"Salvo: {filepath}")
            
            print(f"\n🎯 TESTE CONCLUÍDO: {len(images)} imagens de alta qualidade!")
            return True
        else:
            print("❌ Falha no teste de performance")
            return False

def main():
    """Executa teste de performance máxima."""
    generator = OptimizedSDXLGenerator()
    
    if generator.setup_optimized_pipeline():
        generator.test_max_performance()
    else:
        print("Falha na configuração do pipeline")

if __name__ == "__main__":
    main()