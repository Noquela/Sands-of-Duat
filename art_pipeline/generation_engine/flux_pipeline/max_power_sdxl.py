#!/usr/bin/env python3
"""
MAX POWER SDXL GENERATOR - RTX 5070 100% UTILIZATION
===================================================
ASCII-SAFE version for maximum GPU utilization
"""

import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
from pathlib import Path
import time
from datetime import datetime
import gc

class MaxPowerSDXL:
    def __init__(self):
        self.device = "cuda"
        self.pipe = None
        
        # Configurações para MÁXIMA utilização da RTX 5070
        self.config = {
            "torch_dtype": torch.float16,
            "variant": "fp16",
            "use_safetensors": True,
            
            # Configurações de geração
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30,
            "guidance_scale": 8.0,
            "batch_size": 2,  # RTX 5070 aguenta 2 em paralelo
        }

    def setup_max_power(self):
        """Configura SDXL para utilização máxima da GPU."""
        print("CONFIGURANDO SDXL PARA MAXIMA UTILIZACAO GPU")
        print("RTX 5070 - MODO ALTA PERFORMANCE")
        print("=" * 50)
        
        # Limpa cache
        torch.cuda.empty_cache()
        gc.collect()
        
        try:
            print("Carregando SDXL...")
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=self.config["torch_dtype"],
                variant=self.config["variant"],
                use_safetensors=self.config["use_safetensors"],
            )
            
            print("Movendo para GPU...")
            self.pipe = self.pipe.to(self.device)
            
            # XFormers para performance máxima
            try:
                self.pipe.enable_xformers_memory_efficient_attention()
                print("XFormers ATIVADO - performance maxima!")
            except:
                print("XFormers nao disponivel, continuando...")
            
            # Scheduler otimizado
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config,
                use_karras_sigmas=True,
                algorithm_type="dpmsolver++",
            )
            
            # Compile para performance (PyTorch 2.0+)
            if hasattr(torch, 'compile'):
                print("Compilando modelo...")
                self.pipe.unet = torch.compile(self.pipe.unet, mode="max-autotune")
                print("Modelo compilado para maxima performance!")
            
            # Info da GPU
            if torch.cuda.is_available():
                vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print(f"VRAM Total: {vram_gb:.1f}GB")
            
            print("SETUP COMPLETO - PRONTO PARA MAXIMA PERFORMANCE!")
            return True
            
        except Exception as e:
            print(f"ERRO no setup: {e}")
            return False

    def generate_hades_egyptian_batch(self, num_images=4):
        """Gera batch de imagens Hades-Egyptian com máxima performance."""
        if not self.pipe:
            print("Pipeline nao inicializado!")
            return []
        
        # Prompts Hades-Egyptian otimizados
        prompts = [
            "Anubis egyptian god with jackal head, golden ceremonial collar, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant colors, heroic proportions",
            "Ra sun god with falcon head, solar disk crown, ancient egyptian temple, dramatic lighting, digital art masterpiece, Jen Zee style, dark background",
            "Egyptian warrior hero in pharaonic armor, determined expression, battle stance, hades art style, pen and ink, dramatic shadows, red and gold colors",
            "Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, atmospheric lighting, underworld ambiance, architectural grandeur"
        ][:num_images]
        
        negative_prompt = "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy, soft lighting"
        
        print(f"GERANDO {len(prompts)} IMAGENS EM BATCH - MAXIMA PERFORMANCE")
        print("=" * 60)
        
        results = []
        
        try:
            # Processa em batches de 2 (máximo da RTX 5070)
            batch_size = self.config["batch_size"]
            
            for i in range(0, len(prompts), batch_size):
                batch_prompts = prompts[i:i+batch_size]
                batch_num = i // batch_size + 1
                
                print(f"BATCH {batch_num}: Processando {len(batch_prompts)} imagens...")
                
                start_time = time.time()
                
                # Generators únicos para cada imagem
                generators = [
                    torch.Generator(device=self.device).manual_seed(42 + i + j) 
                    for j in range(len(batch_prompts))
                ]
                
                # Geração em paralelo
                batch_images = self.pipe(
                    prompt=batch_prompts,
                    negative_prompt=[negative_prompt] * len(batch_prompts),
                    width=self.config["width"],
                    height=self.config["height"],
                    num_inference_steps=self.config["num_inference_steps"],
                    guidance_scale=self.config["guidance_scale"],
                    generator=generators
                ).images
                
                batch_time = time.time() - start_time
                time_per_image = batch_time / len(batch_prompts)
                
                print(f"BATCH {batch_num} COMPLETO: {batch_time:.1f}s total, {time_per_image:.1f}s por imagem")
                
                results.extend(batch_images)
                
                # Força limpeza entre batches
                torch.cuda.empty_cache()
                
            # Salva todas as imagens
            output_dir = Path("../../assets/work_in_progress/max_power_generation")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            saved_files = []
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for i, image in enumerate(results):
                filename = f"max_power_hades_{i+1}_{timestamp}.png"
                filepath = output_dir / filename
                image.save(filepath, "PNG")
                saved_files.append(filepath)
                print(f"SALVO: {filename}")
            
            total_images = len(results)
            images_per_minute = 60 / (time_per_image if 'time_per_image' in locals() else 30)
            
            print("\n" + "=" * 60)
            print("RESULTADO FINAL:")
            print(f"Total de imagens: {total_images}")
            print(f"Performance: {images_per_minute:.1f} imagens/minuto")
            print(f"Qualidade: 1024x1024 alta resolucao")
            print(f"Arquivos salvos em: {output_dir}")
            print("MAXIMA PERFORMANCE ALCANCADA!")
            
            return saved_files
            
        except Exception as e:
            print(f"ERRO na geracao: {e}")
            return []

def main():
    """Executa teste de máxima performance."""
    generator = MaxPowerSDXL()
    
    if generator.setup_max_power():
        print("\nINICIANDO TESTE DE MAXIMA PERFORMANCE...")
        files = generator.generate_hades_egyptian_batch(4)
        
        if files:
            print(f"\nSUCESSO! {len(files)} imagens de alta qualidade geradas!")
            for f in files:
                print(f"- {f.name}")
        else:
            print("FALHA na geracao de imagens")
    else:
        print("FALHA no setup do pipeline")

if __name__ == "__main__":
    main()