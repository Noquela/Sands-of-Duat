#!/usr/bin/env python3
"""
MASS PRODUCTION MANAGER - FASE 5
================================
Sistema de produção sistemática para gerar todos os 64 assets
com quality control integrado e tracking em tempo real.
"""

import json
import time
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
import queue

class MassProductionManager:
    def __init__(self):
        self.base_dir = Path(".")
        self.production_dir = self.base_dir / "mass_production"
        self.assets_dir = self.production_dir / "assets"
        self.logs_dir = self.production_dir / "logs"
        self.reports_dir = self.production_dir / "reports"
        
        # Load dataset
        dataset_file = Path("../lora_training/dataset/hades_egyptian/hades_egyptian_dataset.json")
        if dataset_file.exists():
            with open(dataset_file, 'r', encoding='utf-8') as f:
                self.dataset = json.load(f)
        else:
            self.dataset = {"prompts": []}
        
        # Production state
        self.production_state = {
            "status": "ready",  # ready, running, paused, completed, failed
            "start_time": None,
            "current_batch": None,
            "completed_assets": 0,
            "failed_assets": 0,
            "total_assets": len(self.dataset.get("prompts", [])) * 4,
            "quality_approved": 0,
            "quality_rejected": 0,
            "estimated_completion": None,
            "current_phase": "initialization"
        }
        
        # Production queues
        self.generation_queue = queue.Queue()
        self.quality_queue = queue.Queue()
        self.approval_queue = queue.Queue()
        
        # Statistics tracking
        self.production_stats = {
            "legendary": {"planned": 20, "completed": 0, "approved": 0},
            "epic": {"planned": 24, "completed": 0, "approved": 0},
            "rare": {"planned": 16, "completed": 0, "approved": 0},
            "common": {"planned": 4, "completed": 0, "approved": 0}
        }
        
        self.setup_production_environment()
    
    def setup_production_environment(self):
        """Setup complete production environment."""
        print("CONFIGURANDO AMBIENTE DE PRODUCAO EM MASSA")
        print("=" * 45)
        
        # Create directory structure
        directories = [
            self.production_dir,
            self.assets_dir / "legendary" / "deities",
            self.assets_dir / "epic" / "heroes", 
            self.assets_dir / "epic" / "environments",
            self.assets_dir / "rare" / "creatures",
            self.assets_dir / "common" / "ui_elements",
            self.assets_dir / "quality_control" / "pending",
            self.assets_dir / "quality_control" / "approved",
            self.assets_dir / "quality_control" / "rejected",
            self.assets_dir / "production_ready",
            self.assets_dir / "final_delivery",
            self.logs_dir,
            self.reports_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("Ambiente de producao configurado!")
        print(f"Diretorio principal: {self.production_dir}")
        print(f"Assets target: {self.production_state['total_assets']}")
        
    def create_production_batches(self):
        """Create intelligent production batches."""
        print("\nCRIANDO LOTES DE PRODUCAO INTELIGENTES")
        print("=" * 38)
        
        # Organize by priority and complexity
        batches = {
            "batch_1_legendary": {
                "priority": 1,
                "name": "Deidades Legendárias",
                "assets": [],
                "estimated_time": 0,
                "quality_threshold": 0.90,
                "max_attempts": 3
            },
            "batch_2_epic_heroes": {
                "priority": 2, 
                "name": "Heróis Épicos",
                "assets": [],
                "estimated_time": 0,
                "quality_threshold": 0.85,
                "max_attempts": 2
            },
            "batch_3_epic_environments": {
                "priority": 3,
                "name": "Ambientes Épicos", 
                "assets": [],
                "estimated_time": 0,
                "quality_threshold": 0.85,
                "max_attempts": 2
            },
            "batch_4_rare_creatures": {
                "priority": 4,
                "name": "Criaturas Raras",
                "assets": [],
                "estimated_time": 0,
                "quality_threshold": 0.80,
                "max_attempts": 2
            },
            "batch_5_common_ui": {
                "priority": 5,
                "name": "Elementos UI Comuns",
                "assets": [],
                "estimated_time": 0,
                "quality_threshold": 0.75,
                "max_attempts": 1
            }
        }
        
        # Distribute assets into batches
        for prompt_data in self.dataset.get("prompts", []):
            category = prompt_data["category"]
            rarity = prompt_data["rarity"]
            
            # Create 4 variations for each prompt
            for i in range(4):
                asset_spec = {
                    "id": f"{prompt_data['id']}_var_{i+1}",
                    "prompt": prompt_data["prompt"],
                    "character": prompt_data["character"],
                    "category": category,
                    "rarity": rarity,
                    "variation": i + 1,
                    "estimated_gen_time": 60,  # seconds
                    "estimated_qc_time": 30,   # seconds
                    "status": "pending"
                }
                
                # Route to appropriate batch
                if rarity == "legendary":
                    batches["batch_1_legendary"]["assets"].append(asset_spec)
                    batches["batch_1_legendary"]["estimated_time"] += 90
                elif rarity == "epic" and category in ["hero", "warrior", "pharaoh"]:
                    batches["batch_2_epic_heroes"]["assets"].append(asset_spec)
                    batches["batch_2_epic_heroes"]["estimated_time"] += 90
                elif rarity == "epic" and category == "environment":
                    batches["batch_3_epic_environments"]["assets"].append(asset_spec)
                    batches["batch_3_epic_environments"]["estimated_time"] += 90
                elif rarity == "rare":
                    batches["batch_4_rare_creatures"]["assets"].append(asset_spec)
                    batches["batch_4_rare_creatures"]["estimated_time"] += 90
                elif rarity == "common":
                    batches["batch_5_common_ui"]["assets"].append(asset_spec)
                    batches["batch_5_common_ui"]["estimated_time"] += 90
        
        # Save batch configuration
        batch_file = self.production_dir / "production_batches.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batches, f, indent=2, ensure_ascii=False)
        
        # Display batch summary
        total_time = 0
        for batch_id, batch in batches.items():
            count = len(batch["assets"])
            time_min = batch["estimated_time"] // 60
            total_time += batch["estimated_time"]
            print(f"{batch['name']}: {count} assets ({time_min} min)")
        
        total_time_hours = total_time // 3600
        print(f"\nTempo total estimado: {total_time_hours:.1f} horas")
        print(f"Lotes criados: {batch_file}")
        
        return batches
    
    def create_production_automation_scripts(self):
        """Create automation scripts for mass production."""
        print("\nCRIANDO SCRIPTS DE AUTOMACAO PARA PRODUCAO")
        print("=" * 42)
        
        # ComfyUI mass production script
        comfy_script = self.create_comfyui_mass_production()
        
        # Leonardo AI batch script
        leonardo_script = self.create_leonardo_ai_production()
        
        # Fooocus production guide
        fooocus_guide = self.create_fooocus_production_guide()
        
        # Quality control automation
        qc_automation = self.create_qc_automation_script()
        
        print("Scripts de automacao criados:")
        print(f"- ComfyUI Mass Production: {comfy_script}")
        print(f"- Leonardo AI Batch: {leonardo_script}")
        print(f"- Fooocus Guide: {fooocus_guide}")
        print(f"- QC Automation: {qc_automation}")
        
        return {
            "comfyui": comfy_script,
            "leonardo": leonardo_script, 
            "fooocus": fooocus_guide,
            "qc": qc_automation
        }
    
    def create_comfyui_mass_production(self):
        """Create ComfyUI mass production script."""
        
        # Prepare all assets for batch generation
        all_assets = []
        for prompt_data in self.dataset.get("prompts", []):
            for i in range(4):
                all_assets.append({
                    "id": f"{prompt_data['id']}_var_{i+1}",
                    "prompt": prompt_data["prompt"],
                    "character": prompt_data["character"],
                    "category": prompt_data["category"],
                    "rarity": prompt_data["rarity"],
                    "quality_threshold": {
                        "legendary": 0.90,
                        "epic": 0.85, 
                        "rare": 0.80,
                        "common": 0.75
                    }[prompt_data["rarity"]]
                })
        
        script_content = f'''
#!/usr/bin/env python3
"""
COMFYUI MASS PRODUCTION SYSTEM
==============================
Automated batch generation for all 64 Hades-Egyptian assets
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime

class ComfyUIMassProduction:
    def __init__(self):
        self.comfyui_url = "http://127.0.0.1:8188"
        self.assets = {json.dumps(all_assets, indent=2)}
        self.output_dir = Path("assets")
        self.completed = 0
        self.failed = 0
        
    def check_comfyui_status(self):
        """Check if ComfyUI is running."""
        try:
            response = requests.get(f"{{self.comfyui_url}}/system_stats")
            return response.status_code == 200
        except:
            return False
    
    def generate_asset(self, asset_data):
        """Generate single asset via ComfyUI API."""
        
        workflow = {{
            "3": {{
                "class_type": "KSampler",
                "inputs": {{
                    "cfg": 7.5,
                    "denoise": 1,
                    "latent_image": ["5", 0],
                    "model": ["4", 0],
                    "negative": ["7", 0], 
                    "positive": ["6", 0],
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "seed": hash(asset_data["id"]) % 1000000,
                    "steps": 30
                }}
            }},
            "4": {{
                "class_type": "CheckpointLoaderSimple",
                "inputs": {{
                    "ckpt_name": "sd_xl_base_1.0.safetensors"
                }}
            }},
            "5": {{
                "class_type": "EmptyLatentImage",
                "inputs": {{
                    "batch_size": 1,
                    "height": 1024,
                    "width": 1024
                }}
            }},
            "6": {{
                "class_type": "CLIPTextEncode",
                "inputs": {{
                    "clip": ["4", 1],
                    "text": asset_data["prompt"]
                }}
            }},
            "7": {{
                "class_type": "CLIPTextEncode",
                "inputs": {{
                    "clip": ["4", 1],
                    "text": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy"
                }}
            }},
            "8": {{
                "class_type": "VAEDecode",
                "inputs": {{
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }}
            }},
            "9": {{
                "class_type": "SaveImage",
                "inputs": {{
                    "filename_prefix": f"mass_production_{{asset_data['rarity']}}_{{asset_data['id']}}",
                    "images": ["8", 0]
                }}
            }}
        }}
        
        try:
            # Queue workflow
            response = requests.post(
                f"{{self.comfyui_url}}/prompt",
                json={{"prompt": workflow, "client_id": "mass_production"}}
            )
            
            if response.status_code == 200:
                prompt_id = response.json()["prompt_id"]
                
                # Wait for completion
                while True:
                    status_response = requests.get(f"{{self.comfyui_url}}/history/{{prompt_id}}")
                    if status_response.status_code == 200:
                        history = status_response.json()
                        if prompt_id in history:
                            return True
                    time.sleep(2)
            
            return False
            
        except Exception as e:
            print(f"Error generating {{asset_data['id']}}: {{e}}")
            return False
    
    def run_mass_production(self):
        """Execute mass production for all assets."""
        print("COMFYUI MASS PRODUCTION INICIADA")
        print("=" * 32)
        
        if not self.check_comfyui_status():
            print("ERRO: ComfyUI nao esta rodando!")
            print("Inicie ComfyUI primeiro")
            return
        
        print(f"Iniciando producao de {{len(self.assets)}} assets...")
        
        start_time = time.time()
        
        for i, asset in enumerate(self.assets):
            print(f"\\nGerando {{i+1}}/{{len(self.assets)}}: {{asset['character']}} ({{asset['rarity']}})")
            
            if self.generate_asset(asset):
                self.completed += 1
                print(f"  SUCESSO - {{asset['id']}}")
            else:
                self.failed += 1  
                print(f"  FALHA - {{asset['id']}}")
            
            # Progress update
            progress = (i + 1) / len(self.assets) * 100
            elapsed = time.time() - start_time
            eta = (elapsed / (i + 1)) * (len(self.assets) - i - 1) if i > 0 else 0
            
            print(f"  Progresso: {{progress:.1f}}% | ETA: {{eta/60:.0f}} min")
            
            # Small delay to prevent overwhelming
            time.sleep(1)
        
        total_time = time.time() - start_time
        
        print(f"\\nPRODUCAO COMPLETA!")
        print(f"Sucessos: {{self.completed}}/{{len(self.assets)}}")
        print(f"Falhas: {{self.failed}}")
        print(f"Tempo total: {{total_time/3600:.1f}} horas")
        
        # Generate report
        report = {{
            "timestamp": datetime.now().isoformat(),
            "method": "ComfyUI Mass Production",
            "total_assets": len(self.assets),
            "completed": self.completed,
            "failed": self.failed,
            "success_rate": self.completed / len(self.assets) * 100,
            "total_time_hours": total_time / 3600
        }}
        
        report_file = Path("mass_production_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Relatorio salvo: {{report_file}}")

if __name__ == "__main__":
    producer = ComfyUIMassProduction()
    producer.run_mass_production()
'''
        
        script_file = self.production_dir / "comfyui_mass_production.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_file
    
    def create_leonardo_ai_production(self):
        """Create Leonardo AI batch production script."""
        
        script_content = f'''
#!/usr/bin/env python3
"""
LEONARDO AI MASS PRODUCTION
===========================
Automated batch generation using Leonardo AI API
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime

class LeonardoAIProduction:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.headers = {{
            "Authorization": f"Bearer {{api_key}}",
            "Content-Type": "application/json"
        }}
        
        # Leonardo AI optimal settings for game art
        self.settings = {{
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Diffusion XL
            "width": 1024,
            "height": 1024,
            "num_images": 1,
            "guidance_scale": 7,
            "num_inference_steps": 30,
            "scheduler": "EULER_DISCRETE",
            "presetStyle": "LEONARDO"
        }}
        
    def generate_image(self, prompt, negative_prompt=""):
        """Generate single image via Leonardo AI API."""
        
        payload = {{
            **self.settings,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "public": False,
            "nsfw": False
        }}
        
        try:
            response = requests.post(
                f"{{self.base_url}}/generations",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                generation_id = response.json()["sdGenerationJob"]["generationId"]
                
                # Poll for completion
                for _ in range(60):  # Max 5 minutes wait
                    status_response = requests.get(
                        f"{{self.base_url}}/generations/{{generation_id}}",
                        headers=self.headers
                    )
                    
                    if status_response.status_code == 200:
                        data = status_response.json()
                        if data["generations_by_pk"]["status"] == "COMPLETE":
                            image_url = data["generations_by_pk"]["generated_images"][0]["url"]
                            return image_url
                        elif data["generations_by_pk"]["status"] == "FAILED":
                            return None
                    
                    time.sleep(5)
            
            return None
            
        except Exception as e:
            print(f"Leonardo AI error: {{e}}")
            return None
    
    def download_image(self, url, filename):
        """Download image from URL."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return True
        except:
            pass
        return False
    
    def run_production(self):
        """Run mass production with Leonardo AI."""
        
        assets = {json.dumps([{
            "id": f"{p['id']}_var_{i+1}",
            "prompt": p["prompt"], 
            "character": p["character"],
            "rarity": p["rarity"]
        } for p in self.dataset.get("prompts", []) for i in range(4)], indent=2)}
        
        print("LEONARDO AI MASS PRODUCTION")
        print("=" * 27)
        print(f"Assets para gerar: {{len(assets)}}")
        print("Custo estimado: $5-10")
        
        output_dir = Path("leonardo_assets")
        output_dir.mkdir(exist_ok=True)
        
        successful = 0
        failed = 0
        
        for i, asset in enumerate(assets):
            print(f"\\nGerando {{i+1}}/{{len(assets)}}: {{asset['character']}}")
            
            image_url = self.generate_image(asset["prompt"])
            
            if image_url:
                filename = output_dir / f"{{asset['id']}}.png"
                if self.download_image(image_url, filename):
                    successful += 1
                    print(f"  SUCESSO: {{filename}}")
                else:
                    failed += 1
                    print(f"  FALHA download: {{asset['id']}}")
            else:
                failed += 1
                print(f"  FALHA geracao: {{asset['id']}}")
            
            # Rate limiting
            time.sleep(2)
        
        print(f"\\nCOMPLETO: {{successful}} sucessos, {{failed}} falhas")

# INSTRUCOES DE USO:
# 1. Obtenha API key em: https://app.leonardo.ai/settings
# 2. Execute: producer = LeonardoAIProduction("sua-api-key")
# 3. Execute: producer.run_production()

if __name__ == "__main__":
    api_key = input("Digite sua Leonardo AI API key: ")
    if api_key:
        producer = LeonardoAIProduction(api_key)
        producer.run_production()
    else:
        print("API key necessaria!")
'''
        
        script_file = self.production_dir / "leonardo_ai_mass_production.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_file
    
    def create_fooocus_production_guide(self):
        """Create comprehensive Fooocus production guide."""
        
        guide_content = f'''
# FOOOCUS MASS PRODUCTION GUIDE
## Systematic Generation of 64 Hades-Egyptian Assets

---

## SETUP FOOOCUS FOR MASS PRODUCTION:

### 1. INSTALLATION:
- Download: https://github.com/lllyasviel/Fooocus  
- Install and run
- Wait for SDXL model download (~6GB)
- Interface ready!

### 2. OPTIMAL SETTINGS:
- **Performance:** Quality (better results) or Speed (faster)
- **Aspect Ratio:** 1024×1024 (square)  
- **Image Number:** 4 (generate 4 variations at once)
- **Guidance Scale:** 7.0
- **Style:** Fooocus V2 or Disable (for pure prompts)
- **Seed:** Random (for variation) or Fixed (for consistency)

---

## SYSTEMATIC PRODUCTION WORKFLOW:

### BATCH 1: LEGENDARY DEITIES (Priority 1)
**Target:** 20 assets (5 characters × 4 variations)  
**Quality:** Premium (>90% approval rate)  
**Time:** ~2 hours

#### 1.1 ANUBIS (4 variations):
```
Prompt: Anubis egyptian god with jackal head, golden ceremonial collar, divine presence, dramatic chiaroscuro lighting, pen and ink style, hades game art, vibrant red and gold colors, heroic proportions, masterpiece

Negative: blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy

Save as: deity_anubis_var_1.png, deity_anubis_var_2.png, deity_anubis_var_3.png, deity_anubis_var_4.png
```

#### 1.2 RA (4 variations):
```
Prompt: Ra sun god with falcon head, solar disk crown, radiant golden aura, divine majesty, dramatic lighting, hades art style, vibrant colors, pen and ink technique, masterpiece

Negative: blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy

Save as: deity_ra_var_1.png, deity_ra_var_2.png, deity_ra_var_3.png, deity_ra_var_4.png
```

#### 1.3 ISIS (4 variations):
```
Prompt: Isis goddess with wings spread, protective pose, blue and gold colors, divine aura, hades game art style, pen and ink, dramatic shadows, masterpiece

Negative: blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy

Save as: deity_isis_var_1.png, deity_isis_var_2.png, deity_isis_var_3.png, deity_isis_var_4.png
```

#### 1.4 SET (4 variations):
```
Prompt: Set chaos god with unique creature head, red and black colors, menacing expression, dramatic lighting, hades art influence, pen and ink style, masterpiece

Negative: blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy

Save as: deity_set_var_1.png, deity_set_var_2.png, deity_set_var_3.png, deity_set_var_4.png
```

#### 1.5 THOTH (4 variations):
```
Prompt: Thoth ibis god with scroll, wisdom pose, blue and silver colors, scholarly appearance, hades game art, pen and ink technique, masterpiece

Negative: blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy

Save as: deity_thoth_var_1.png, deity_thoth_var_2.png, deity_thoth_var_3.png, deity_thoth_var_4.png
```

---

### BATCH 2: EPIC HEROES (Priority 2)  
**Target:** 12 assets (3 characters × 4 variations)
**Quality:** High (>85% approval rate)
**Time:** ~1.5 hours

#### 2.1 EGYPTIAN WARRIOR (4 variations):
```
Prompt: Egyptian warrior hero in pharaonic armor, determined expression, battle stance, red gold colors, hades art style, dramatic lighting, pen and ink, masterpiece

Save as: hero_warrior_var_1.png, hero_warrior_var_2.png, hero_warrior_var_3.png, hero_warrior_var_4.png
```

#### 2.2 DIVINE PHARAOH (4 variations):
```
Prompt: Pharaoh hero with ceremonial khopesh sword, regal bearing, golden armor details, hades game art style, vibrant colors, dramatic shadows, masterpiece

Save as: hero_pharaoh_var_1.png, hero_pharaoh_var_2.png, hero_pharaoh_var_3.png, hero_pharaoh_var_4.png
```

#### 2.3 HIGH PRIESTESS (4 variations):
```
Prompt: Egyptian priestess hero with staff, flowing robes, mystical blue glow, hades art influence, pen and ink style, dramatic lighting, masterpiece

Save as: hero_priestess_var_1.png, hero_priestess_var_2.png, hero_priestess_var_3.png, hero_priestess_var_4.png
```

---

### BATCH 3: EPIC ENVIRONMENTS (Priority 3)
**Target:** 12 assets (3 environments × 4 variations)  
**Quality:** High (>85% approval rate)
**Time:** ~1.5 hours

#### 3.1 SACRED TEMPLE (4 variations):
```
Prompt: Ancient egyptian temple interior, massive stone columns, hieroglyphic carvings, dramatic shadows, atmospheric lighting, hades game art, architectural grandeur, masterpiece

Save as: env_temple_var_1.png, env_temple_var_2.png, env_temple_var_3.png, env_temple_var_4.png
```

#### 3.2 PHARAOH'S TOMB (4 variations):
```  
Prompt: Egyptian tomb chamber, sarcophagus, treasure, atmospheric lighting, mystical ambiance, hades art influence, rich colors, detailed architecture, masterpiece

Save as: env_tomb_var_1.png, env_tomb_var_2.png, env_tomb_var_3.png, env_tomb_var_4.png
```

#### 3.3 GREAT PYRAMID (4 variations):
```
Prompt: Desert pyramid exterior, sandstorm, dramatic sky, epic scale architecture, egyptian grandeur, hades game art style, cinematic composition, masterpiece

Save as: env_pyramid_var_1.png, env_pyramid_var_2.png, env_pyramid_var_3.png, env_pyramid_var_4.png
```

---

### BATCH 4: RARE CREATURES (Priority 4)
**Target:** 16 assets (4 creatures × 4 variations)
**Quality:** Good (>80% approval rate)  
**Time:** ~2 hours

#### 4.1 DESERT SPHINX (4 variations):
```
Prompt: Ancient egyptian sphinx creature, lion body, human head, golden brown colors, mystical presence, hades game art, pen and ink technique, masterpiece

Save as: creature_sphinx_var_1.png, creature_sphinx_var_2.png, creature_sphinx_var_3.png, creature_sphinx_var_4.png
```

#### 4.2 SACRED SCARAB (4 variations):
```
Prompt: Scarab beetle creature, metallic green blue carapace, magical glow, egyptian mysticism, hades art style, vibrant colors, detailed design, masterpiece

Save as: creature_scarab_var_1.png, creature_scarab_var_2.png, creature_scarab_var_3.png, creature_scarab_var_4.png
```

#### 4.3 MUMMY GUARDIAN (4 variations):
```
Prompt: Egyptian mummy guardian, bandaged undead, glowing eyes, protective stance, hades game influence, dramatic shadows, pen and ink style, masterpiece

Save as: creature_mummy_var_1.png, creature_mummy_var_2.png, creature_mummy_var_3.png, creature_mummy_var_4.png
```

#### 4.4 DESERT SCORPION (4 variations):
```
Prompt: Desert scorpion creature, massive size, threatening pose, blue and gold carapace, egyptian underworld, hades art style, dramatic lighting, masterpiece

Save as: creature_scorpion_var_1.png, creature_scorpion_var_2.png, creature_scorpion_var_3.png, creature_scorpion_var_4.png
```

---

### BATCH 5: COMMON UI (Priority 5)
**Target:** 4 assets (1 element × 4 variations)
**Quality:** Acceptable (>75% approval rate)
**Time:** ~30 minutes  

#### 5.1 SACRED FRAME (4 variations):
```
Prompt: Egyptian ornate frame border, hieroglyphic decorations, gold and blue colors, game UI style, detailed ornamentation, hades art influence, masterpiece

Save as: ui_frame_var_1.png, ui_frame_var_2.png, ui_frame_var_3.png, ui_frame_var_4.png
```

---

## PRODUCTION CHECKLIST:

### BEFORE STARTING:
- [ ] Fooocus installed and running
- [ ] SDXL model downloaded  
- [ ] Settings configured (1024×1024, 4 images)
- [ ] Output folder organized
- [ ] Naming convention ready

### DURING PRODUCTION:
- [ ] Follow batch priority order
- [ ] Generate 4 variations per prompt
- [ ] Save with consistent naming
- [ ] Quick quality check each batch
- [ ] Track progress (completed/total)

### QUALITY CONTROL:
- [ ] Single character (no multiples)
- [ ] Hades + Egyptian style fusion
- [ ] Proper resolution (1024×1024)
- [ ] No text/watermarks
- [ ] Dramatic lighting present
- [ ] Rich, vibrant colors

### AFTER COMPLETION:
- [ ] Organize by rarity folders
- [ ] Run quality control script
- [ ] Move approved assets to production
- [ ] Generate final report

---

## ESTIMATED TIMELINE:

**Total Production Time:** 6-8 hours  
- Batch 1 (Legendary): 2 hours
- Batch 2 (Epic Heroes): 1.5 hours  
- Batch 3 (Epic Environments): 1.5 hours
- Batch 4 (Rare Creatures): 2 hours
- Batch 5 (Common UI): 0.5 hours
- Quality Control: 0.5 hours

**Recommended Schedule:**
- Day 1: Batches 1-2 (3.5 hours)
- Day 2: Batches 3-5 + QC (4 hours)  
- Or: Complete in single 7-hour session

---

## TROUBLESHOOTING:

**Low Quality Results:**
- Increase steps to 40-50  
- Use "Quality" performance mode
- Add more detail words to prompt

**Wrong Style:**  
- Disable Fooocus styles
- Ensure "hades game art" in prompt
- Check negative prompt is applied

**Multiple Characters:**
- Regenerate with stronger negative
- Add "single character" to prompt
- Manual selection of best result

**Slow Generation:**
- Use "Speed" performance mode  
- Reduce steps to 20-25
- Generate 1-2 images at a time

---

## SUCCESS METRICS:

**Quality Targets:**
- Legendary: >90% approval (18/20 assets)
- Epic: >85% approval (20/24 assets)  
- Rare: >80% approval (13/16 assets)
- Common: >75% approval (3/4 assets)

**Overall Target:** 54/64 assets approved (84% success rate)

**Time Target:** Complete in 8 hours or less

**Final Deliverable:** 64 high-quality Hades-Egyptian assets ready for game integration.

---

**READY TO START MASS PRODUCTION!** 🎨⚡
'''
        
        guide_file = self.production_dir / "fooocus_mass_production_guide.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return guide_file
    
    def create_qc_automation_script(self):
        """Create quality control automation for mass production."""
        
        qc_script = '''
#!/usr/bin/env python3
"""
QUALITY CONTROL AUTOMATION - MASS PRODUCTION
============================================
Automated quality control for mass-produced assets
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image
from datetime import datetime
from typing import Dict, List, Tuple

class MassProductionQC:
    def __init__(self):
        self.base_dir = Path(".")
        self.quality_db = self.base_dir / "mass_production_quality.json"
        
        # Quality thresholds by rarity
        self.thresholds = {
            "legendary": 0.90,
            "epic": 0.85,
            "rare": 0.80, 
            "common": 0.75
        }
        
        # Quality criteria
        self.criteria = {
            "min_resolution": (1024, 1024),
            "max_file_size": 15 * 1024 * 1024,  # 15MB
            "required_format": ".png",
            "forbidden_keywords": ["multiple", "crowd", "text", "watermark"]
        }
        
        self.load_quality_database()
    
    def load_quality_database(self):
        """Load existing quality database."""
        if self.quality_db.exists():
            with open(self.quality_db, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
        else:
            self.db = {
                "evaluations": [],
                "statistics": {
                    "total": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending_review": 0
                },
                "batch_results": {}
            }
    
    def evaluate_asset(self, image_path: str, asset_info: Dict) -> Dict:
        """Evaluate single asset quality."""
        
        evaluation = {
            "asset_path": image_path,
            "asset_id": asset_info.get("id", "unknown"),
            "rarity": asset_info.get("rarity", "common"),
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_score": 0.0,
            "status": "pending",
            "issues": []
        }
        
        try:
            # File existence check
            if not os.path.exists(image_path):
                evaluation["issues"].append("File not found")
                evaluation["status"] = "rejected"
                return evaluation
            
            # Load and analyze image
            img = Image.open(image_path)
            width, height = img.size
            file_size = os.path.getsize(image_path)
            
            # Resolution check
            min_width, min_height = self.criteria["min_resolution"]
            if width >= min_width and height >= min_height:
                evaluation["checks"]["resolution"] = {"passed": True, "value": f"{width}x{height}"}
            else:
                evaluation["checks"]["resolution"] = {"passed": False, "value": f"{width}x{height}"}
                evaluation["issues"].append(f"Low resolution: {width}x{height}")
            
            # File size check
            if file_size <= self.criteria["max_file_size"]:
                evaluation["checks"]["file_size"] = {"passed": True, "value": f"{file_size//1024}KB"}
            else:
                evaluation["checks"]["file_size"] = {"passed": False, "value": f"{file_size//1024}KB"}
                evaluation["issues"].append(f"File too large: {file_size//1024}KB")
            
            # Format check
            if image_path.lower().endswith(self.criteria["required_format"]):
                evaluation["checks"]["format"] = {"passed": True, "value": "PNG"}
            else:
                evaluation["checks"]["format"] = {"passed": False, "value": "Not PNG"}
                evaluation["issues"].append("Wrong format (not PNG)")
            
            # Visual quality check (basic)
            # Check for extreme darkness or brightness
            grayscale = img.convert('L')
            avg_brightness = sum(grayscale.getdata()) / len(grayscale.getdata())
            
            if 20 <= avg_brightness <= 220:  # Reasonable brightness range
                evaluation["checks"]["brightness"] = {"passed": True, "value": f"{avg_brightness:.1f}"}
            else:
                evaluation["checks"]["brightness"] = {"passed": False, "value": f"{avg_brightness:.1f}"}
                evaluation["issues"].append(f"Unusual brightness: {avg_brightness:.1f}")
            
            # Calculate overall score
            passed_checks = sum(1 for check in evaluation["checks"].values() if check["passed"])
            total_checks = len(evaluation["checks"])
            evaluation["overall_score"] = passed_checks / total_checks if total_checks > 0 else 0
            
            # Determine status based on rarity threshold
            rarity = evaluation["rarity"]
            threshold = self.thresholds.get(rarity, 0.75)
            
            if evaluation["overall_score"] >= threshold and not evaluation["issues"]:
                evaluation["status"] = "approved"
            elif evaluation["overall_score"] >= 0.6:
                evaluation["status"] = "review"
            else:
                evaluation["status"] = "rejected"
            
        except Exception as e:
            evaluation["issues"].append(f"Error processing: {str(e)}")
            evaluation["status"] = "error"
        
        return evaluation
    
    def batch_evaluate_directory(self, directory_path: str) -> Dict:
        """Evaluate all assets in a directory."""
        
        print(f"Evaluating directory: {directory_path}")
        
        directory = Path(directory_path)
        if not directory.exists():
            return {"error": "Directory not found"}
        
        # Find all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(directory.rglob(f"*{ext}"))
        
        print(f"Found {len(image_files)} images to evaluate")
        
        # Evaluate each image
        evaluations = []
        for image_file in image_files:
            # Extract asset info from filename
            filename = image_file.stem
            parts = filename.split('_')
            
            asset_info = {
                "id": filename,
                "rarity": "common"  # default
            }
            
            # Try to determine rarity from path or filename
            path_str = str(image_file).lower()
            if "legendary" in path_str or "deity" in path_str:
                asset_info["rarity"] = "legendary"
            elif "epic" in path_str or ("hero" in path_str or "environment" in path_str):
                asset_info["rarity"] = "epic"  
            elif "rare" in path_str or "creature" in path_str:
                asset_info["rarity"] = "rare"
            
            evaluation = self.evaluate_asset(str(image_file), asset_info)
            evaluations.append(evaluation)
            
            status_symbol = {
                "approved": "✓",
                "rejected": "✗", 
                "review": "?",
                "error": "!"
            }.get(evaluation["status"], "?")
            
            print(f"  {status_symbol} {image_file.name}: {evaluation['status']} ({evaluation['overall_score']:.2f})")
        
        # Update database
        self.db["evaluations"].extend(evaluations)
        self.update_statistics()
        self.save_quality_database()
        
        # Generate batch report
        approved = [e for e in evaluations if e["status"] == "approved"]
        rejected = [e for e in evaluations if e["status"] == "rejected"]
        review = [e for e in evaluations if e["status"] == "review"]
        
        batch_report = {
            "timestamp": datetime.now().isoformat(),
            "directory": str(directory),
            "total_evaluated": len(evaluations),
            "approved": len(approved),
            "rejected": len(rejected), 
            "review": len(review),
            "approval_rate": len(approved) / len(evaluations) * 100 if evaluations else 0,
            "evaluations": evaluations
        }
        
        return batch_report
    
    def organize_by_quality(self, source_dir: str, output_base_dir: str):
        """Organize assets by quality status."""
        
        source = Path(source_dir)
        base_output = Path(output_base_dir)
        
        # Create quality directories
        approved_dir = base_output / "approved"
        rejected_dir = base_output / "rejected"
        review_dir = base_output / "review"
        
        for dir in [approved_dir, rejected_dir, review_dir]:
            dir.mkdir(parents=True, exist_ok=True)
        
        moved_count = {"approved": 0, "rejected": 0, "review": 0}
        
        # Move files based on latest evaluations
        for evaluation in self.db["evaluations"]:
            asset_path = Path(evaluation["asset_path"])
            status = evaluation["status"]
            
            if asset_path.exists() and status in moved_count:
                target_dir = {
                    "approved": approved_dir,
                    "rejected": rejected_dir,
                    "review": review_dir
                }[status]
                
                target_path = target_dir / asset_path.name
                
                try:
                    shutil.move(str(asset_path), str(target_path))
                    moved_count[status] += 1
                    print(f"Moved {asset_path.name} to {status}/")
                except Exception as e:
                    print(f"Error moving {asset_path.name}: {e}")
        
        print(f"\\nOrganization complete:")
        for status, count in moved_count.items():
            print(f"  {status.title()}: {count} files")
    
    def update_statistics(self):
        """Update quality statistics."""
        stats = {
            "total": len(self.db["evaluations"]),
            "approved": sum(1 for e in self.db["evaluations"] if e["status"] == "approved"),
            "rejected": sum(1 for e in self.db["evaluations"] if e["status"] == "rejected"),
            "pending_review": sum(1 for e in self.db["evaluations"] if e["status"] == "review"),
            "error": sum(1 for e in self.db["evaluations"] if e["status"] == "error")
        }
        self.db["statistics"] = stats
    
    def save_quality_database(self):
        """Save quality database."""
        with open(self.quality_db, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)
    
    def generate_quality_report(self) -> str:
        """Generate comprehensive quality report."""
        
        stats = self.db["statistics"]
        
        report = f"""
MASS PRODUCTION QUALITY REPORT
==============================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL STATISTICS:
- Total Evaluated: {stats["total"]}
- Approved: {stats["approved"]} ({stats["approved"]/max(stats["total"],1)*100:.1f}%)
- Rejected: {stats["rejected"]} ({stats["rejected"]/max(stats["total"],1)*100:.1f}%)
- Needs Review: {stats["pending_review"]} ({stats["pending_review"]/max(stats["total"],1)*100:.1f}%)
- Errors: {stats["error"]}

APPROVAL RATE BY RARITY:
"""
        
        # Group by rarity
        by_rarity = {}
        for eval in self.db["evaluations"]:
            rarity = eval.get("rarity", "unknown")
            if rarity not in by_rarity:
                by_rarity[rarity] = {"total": 0, "approved": 0, "rejected": 0, "review": 0}
            
            by_rarity[rarity]["total"] += 1
            by_rarity[rarity][eval["status"]] = by_rarity[rarity].get(eval["status"], 0) + 1
        
        for rarity, data in by_rarity.items():
            total = data["total"]
            approved = data.get("approved", 0)
            rate = approved / total * 100 if total > 0 else 0
            target_rate = self.thresholds.get(rarity, 0.75) * 100
            
            report += f"\\n{rarity.upper()}:"
            report += f"\\n  Total: {total} assets"
            report += f"\\n  Approved: {approved} ({rate:.1f}%)"
            report += f"\\n  Target: {target_rate:.0f}%"
            report += f"\\n  Status: {'PASS' if rate >= target_rate else 'FAIL'}"
        
        # Production status
        target_total = 64
        completion_rate = stats["total"] / target_total * 100
        
        report += f"""

PRODUCTION STATUS:
- Target Assets: {target_total}
- Generated: {stats["total"]} ({completion_rate:.1f}%)
- Production Ready: {stats["approved"]}
- Success Rate: {stats["approved"]/target_total*100:.1f}%

NEXT STEPS:
"""
        
        if stats["total"] < target_total:
            report += f"\\n- Generate remaining {target_total - stats['total']} assets"
        
        if stats["rejected"] > 0:
            report += f"\\n- Regenerate {stats['rejected']} rejected assets"
        
        if stats["pending_review"] > 0:
            report += f"\\n- Manual review of {stats['pending_review']} assets"
        
        if stats["approved"] >= target_total * 0.8:
            report += "\\n- Ready for final production phase!"
        
        return report

def main():
    """Main quality control execution."""
    qc = MassProductionQC()
    
    print("MASS PRODUCTION QUALITY CONTROL")
    print("=" * 32)
    print("1. Evaluate directory")
    print("2. Organize by quality")  
    print("3. Generate report")
    print("0. Exit")
    
    choice = input("\\nSelect option: ").strip()
    
    if choice == "1":
        directory = input("Enter directory path: ").strip()
        if directory:
            report = qc.batch_evaluate_directory(directory)
            print(f"\\nEvaluation complete:")
            print(f"- Approved: {report['approved']}")
            print(f"- Rejected: {report['rejected']}")
            print(f"- Review: {report['review']}")
            print(f"- Approval Rate: {report['approval_rate']:.1f}%")
    
    elif choice == "2":
        source = input("Source directory: ").strip()
        output = input("Output base directory: ").strip()
        if source and output:
            qc.organize_by_quality(source, output)
    
    elif choice == "3":
        report_text = qc.generate_quality_report()
        print(report_text)
        
        report_file = Path("mass_production_quality_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\\nReport saved: {report_file}")

if __name__ == "__main__":
    main()
'''
        
        qc_file = self.production_dir / "mass_production_qc.py"
        with open(qc_file, 'w', encoding='utf-8') as f:
            f.write(qc_script)
        
        return qc_file
    
    def create_production_dashboard(self):
        """Create real-time production dashboard."""
        print("\nCRIANDO DASHBOARD DE PRODUCAO EM TEMPO REAL")
        print("=" * 44)
        
        dashboard_script = f'''
#!/usr/bin/env python3
"""
PRODUCTION DASHBOARD - REAL TIME TRACKING
==========================================
Dashboard em tempo real para acompanhar produção dos 64 assets
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class ProductionDashboard:
    def __init__(self):
        self.base_dir = Path(".")
        self.status_file = self.base_dir / "production_status.json"
        self.target_assets = 64
        
        # Production targets by category
        self.targets = {{
            "legendary": 20,  # 5 deities × 4 variations
            "epic": 24,       # 6 assets × 4 variations  
            "rare": 16,       # 4 creatures × 4 variations
            "common": 4       # 1 UI × 4 variations
        }}
        
        self.load_status()
    
    def load_status(self):
        """Load current production status."""
        if self.status_file.exists():
            with open(self.status_file, 'r', encoding='utf-8') as f:
                self.status = json.load(f)
        else:
            self.status = {{
                "start_time": None,
                "current_phase": "planning",
                "total_generated": 0,
                "total_approved": 0,
                "total_rejected": 0,
                "batches_completed": 0,
                "estimated_completion": None,
                "production_rate": 0.0,  # assets per hour
                "quality_rate": 0.0      # approval percentage
            }}
    
    def scan_production_folders(self):
        """Scan folders for generated assets."""
        
        # Look for common asset directories
        asset_dirs = [
            self.base_dir / "assets",
            self.base_dir / "generated_assets", 
            self.base_dir / "leonardo_assets",
            self.base_dir / "comfy_output",
            self.base_dir / "fooocus_output"
        ]
        
        found_assets = {{
            "legendary": 0,
            "epic": 0, 
            "rare": 0,
            "common": 0
        }}
        
        total_found = 0
        
        for asset_dir in asset_dirs:
            if asset_dir.exists():
                # Count PNG files
                png_files = list(asset_dir.rglob("*.png"))
                
                for png_file in png_files:
                    filename = png_file.name.lower()
                    
                    # Classify by content
                    if any(word in filename for word in ["deity", "anubis", "ra", "isis", "set", "thoth"]):
                        found_assets["legendary"] += 1
                    elif any(word in filename for word in ["hero", "warrior", "pharaoh", "priestess", "temple", "tomb", "pyramid"]):
                        found_assets["epic"] += 1
                    elif any(word in filename for word in ["creature", "sphinx", "scarab", "mummy", "scorpion"]):
                        found_assets["rare"] += 1
                    elif any(word in filename for word in ["ui", "frame", "border"]):
                        found_assets["common"] += 1
                    else:
                        # Count as epic by default
                        found_assets["epic"] += 1
                    
                    total_found += 1
        
        return found_assets, total_found
    
    def calculate_metrics(self, found_assets, total_found):
        """Calculate production metrics."""
        
        # Update status
        self.status["total_generated"] = total_found
        
        # Calculate completion rates
        completion_rates = {{}}
        for category, found in found_assets.items():
            target = self.targets[category]
            completion_rates[category] = (found / target * 100) if target > 0 else 0
        
        overall_completion = (total_found / self.target_assets * 100)
        
        # Calculate production rate
        if self.status.get("start_time"):
            start_time = datetime.fromisoformat(self.status["start_time"])
            elapsed_hours = (datetime.now() - start_time).total_seconds() / 3600
            
            if elapsed_hours > 0:
                self.status["production_rate"] = total_found / elapsed_hours
                
                # Estimate completion time
                remaining_assets = self.target_assets - total_found
                eta_hours = remaining_assets / self.status["production_rate"] if self.status["production_rate"] > 0 else 0
                self.status["estimated_completion"] = (datetime.now() + timedelta(hours=eta_hours)).isoformat()
        
        return completion_rates, overall_completion
    
    def display_dashboard(self):
        """Display real-time production dashboard."""
        
        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 60)
        print("SANDS OF DUAT - PRODUCTION DASHBOARD")
        print("Hades-Egyptian Asset Mass Production")
        print("=" * 60)
        
        # Scan current status
        found_assets, total_found = self.scan_production_folders()
        completion_rates, overall_completion = self.calculate_metrics(found_assets, total_found)
        
        # Current time and status
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Updated: {{current_time}}")
        print(f"Phase: {{self.status.get('current_phase', 'Unknown').upper()}}")
        print()
        
        # Overall progress
        print(f"OVERALL PROGRESS: {{overall_completion:.1f}}%")
        print(f"Assets Generated: {{total_found}}/{{self.target_assets}}")
        
        # Progress bar
        progress_width = 40
        filled = int((total_found / self.target_assets) * progress_width)
        bar = "█" * filled + "░" * (progress_width - filled)
        print(f"[{{bar}}]")
        print()
        
        # Category breakdown
        print("CATEGORY PROGRESS:")
        print("-" * 40)
        
        for category, found in found_assets.items():
            target = self.targets[category]
            rate = completion_rates[category]
            status = "COMPLETE" if found >= target else "IN PROGRESS" if found > 0 else "PENDING"
            
            print(f"{{category.upper():>10}} | {{found:>2}}/{{target:>2}} | {{rate:>5.1f}}% | {{status}}")
        
        print("-" * 40)
        print()
        
        # Production metrics
        if self.status.get("production_rate", 0) > 0:
            print(f"Production Rate: {{self.status['production_rate']:.1f}} assets/hour")
            
            if self.status.get("estimated_completion"):
                eta = datetime.fromisoformat(self.status["estimated_completion"])
                print(f"Estimated Completion: {{eta.strftime('%H:%M today' if eta.date() == datetime.now().date() else '%Y-%m-%d %H:%M')}}")
        
        print()
        
        # Quality metrics (if available)
        if self.status.get("total_approved", 0) > 0 or self.status.get("total_rejected", 0) > 0:
            approved = self.status.get("total_approved", 0)
            rejected = self.status.get("total_rejected", 0)
            quality_rate = approved / (approved + rejected) * 100 if (approved + rejected) > 0 else 0
            
            print("QUALITY CONTROL:")
            print(f"Approved: {{approved}} | Rejected: {{rejected}} | Rate: {{quality_rate:.1f}}%")
            print()
        
        # Recent activity
        print("STATUS:")
        if total_found == 0:
            print("• Waiting for production to start...")
            print("• Run generation scripts to begin")
        elif total_found < self.target_assets:
            remaining = self.target_assets - total_found
            print(f"• Production in progress...")
            print(f"• {{remaining}} assets remaining")
        else:
            print("• Production complete!")
            print("• Ready for quality control")
        
        print()
        print("=" * 60)
        
        # Save updated status
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)
    
    def start_monitoring(self):
        """Start real-time monitoring."""
        print("Starting production monitoring...")
        print("Press Ctrl+C to stop")
        
        # Set start time if not set
        if not self.status.get("start_time"):
            self.status["start_time"] = datetime.now().isoformat()
            self.status["current_phase"] = "production"
        
        try:
            while True:
                self.display_dashboard()
                time.sleep(30)  # Update every 30 seconds
                
        except KeyboardInterrupt:
            print("\\nMonitoring stopped.")
            
            # Final summary
            found_assets, total_found = self.scan_production_folders()
            completion_rate = total_found / self.target_assets * 100
            
            print(f"\\nFINAL STATUS:")
            print(f"Generated: {{total_found}}/{{self.target_assets}} ({{completion_rate:.1f}}%)")
            
            if total_found >= self.target_assets:
                print("PRODUCTION COMPLETE! 🎉")
            else:
                print(f"{{self.target_assets - total_found}} assets still needed")
    
    def generate_summary_report(self):
        """Generate summary report."""
        
        found_assets, total_found = self.scan_production_folders()
        completion_rates, overall_completion = self.calculate_metrics(found_assets, total_found)
        
        report = f"""
PRODUCTION SUMMARY REPORT
========================

Generated: {{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}

OVERALL STATUS:
- Target Assets: {{self.target_assets}}
- Generated Assets: {{total_found}}
- Completion Rate: {{overall_completion:.1f}}%

CATEGORY BREAKDOWN:
"""
        
        for category, found in found_assets.items():
            target = self.targets[category]
            rate = completion_rates[category]
            report += f"\n{category.upper()}:"
            report += f"\n  Generated: {found}/{target} ({rate:.1f}%)"
            report += f"\n  Status: {'COMPLETE' if found >= target else 'INCOMPLETE'}"
        
        if self.status.get("production_rate"):
            report += f"\n\nPRODUCTION METRICS:"
            report += f"\nRate: {self.status['production_rate']:.1f} assets/hour"
        
        report += f"\n\nRECOMMENDATIONS:"
        
        if total_found >= self.target_assets:
            report += f"\n- Production complete! Run quality control."
        else:
            missing = self.target_assets - total_found
            report += f"\n- Generate remaining {missing} assets"
            
            for category, found in found_assets.items():
                target = self.targets[category]
                if found < target:
                    missing_cat = target - found
                    report += f"\n- {category.title()}: {missing_cat} more needed"
        
        # Save report
        report_file = self.base_dir / "production_summary.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        print(f"\\nReport saved: {{report_file}}")

def main():
    """Main dashboard execution."""
    dashboard = ProductionDashboard()
    
    print("PRODUCTION DASHBOARD")
    print("=" * 20)
    print("1. Start monitoring")
    print("2. Show current status")
    print("3. Generate summary report")  
    print("0. Exit")
    
    choice = input("\\nSelect option: ").strip()
    
    if choice == "1":
        dashboard.start_monitoring()
    elif choice == "2":
        dashboard.display_dashboard()
        input("\\nPress Enter to continue...")
    elif choice == "3":
        dashboard.generate_summary_report()

if __name__ == "__main__":
    main()
'''
        
        dashboard_file = self.production_dir / "production_dashboard.py"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard_script)
        
        print(f"Dashboard criado: {dashboard_file}")
        return dashboard_file
    
    def finalize_mass_production_system(self):
        """Finalize complete mass production system."""
        print("\nFINALIZANDO SISTEMA DE PRODUCAO EM MASSA")
        print("=" * 42)
        
        # Create master execution script
        master_script = f'''
#!/usr/bin/env python3
"""
MASS PRODUCTION SYSTEM - MASTER CONTROLLER
==========================================
Sistema completo de produção em massa para 64 assets Hades-Egyptian
"""

import os
import sys
from pathlib import Path

def show_main_menu():
    """Display main production menu."""
    print("MASS PRODUCTION SYSTEM - FASE 5")
    print("=" * 32)
    print("Hades-Egyptian Asset Production")
    print()
    print("PRODUCTION METHODS:")
    print("1. ComfyUI Mass Production (Automated)")
    print("2. Leonardo AI Batch (Premium Quality)")  
    print("3. Fooocus Production (Manual Guided)")
    print("4. Production Dashboard (Real-time Tracking)")
    print("5. Quality Control (Automated)")
    print()
    print("REPORTS & STATUS:")
    print("6. Show current status")
    print("7. Generate production report")
    print("8. Show production guide")
    print("0. Exit")
    
    return input("\\nSelect option: ").strip()

def run_comfyui_production():
    """Run ComfyUI mass production."""
    print("\\nCOMFYUI MASS PRODUCTION")
    print("=" * 23)
    print("Requirements:")
    print("- ComfyUI installed and running")
    print("- SDXL model loaded")
    print("- API accessible")
    print()
    
    confirm = input("ComfyUI ready? (y/n): ").lower()
    if confirm == 'y':
        os.system("python comfyui_mass_production.py")
    else:
        print("Setup ComfyUI first:")
        print("1. Download: https://github.com/comfyanonymous/ComfyUI")
        print("2. Install and run")
        print("3. Wait for SDXL download")

def run_leonardo_production():
    """Run Leonardo AI production."""
    print("\\nLEONARDO AI MASS PRODUCTION")
    print("=" * 27)
    print("Requirements:")
    print("- Leonardo AI account")
    print("- API key configured")
    print("- ~$10 budget for 64 images")
    print()
    
    api_key = input("Enter API key (or press Enter to skip): ")
    if api_key:
        os.system(f"python leonardo_ai_mass_production.py")
    else:
        print("Get API key at: https://app.leonardo.ai/settings")

def run_fooocus_production():
    """Show Fooocus production guide."""
    print("\\nFOOCUS MASS PRODUCTION GUIDE")
    print("=" * 28)
    
    guide_file = Path("fooocus_mass_production_guide.md")
    if guide_file.exists():
        print(f"Opening guide: {{guide_file}}")
        # Try to open with default app
        if os.name == 'nt':  # Windows
            os.system(f'start "" "{{guide_file}}"')
        else:  # macOS/Linux
            os.system(f'open "{{guide_file}}"' if sys.platform == 'darwin' else f'xdg-open "{{guide_file}}"')
    else:
        print("Guide file not found!")

def run_dashboard():
    """Run production dashboard."""
    print("\\nSTARTING PRODUCTION DASHBOARD")
    print("=" * 29)
    os.system("python production_dashboard.py")

def run_quality_control():
    """Run quality control."""
    print("\\nMASS PRODUCTION QUALITY CONTROL")
    print("=" * 32)
    
    assets_dir = input("Assets directory (or Enter for auto-detect): ").strip()
    if assets_dir:
        os.system(f"python mass_production_qc.py")
    else:
        # Auto-detect common directories
        possible_dirs = ["assets", "generated_assets", "leonardo_assets", "comfy_output"]
        found_dirs = [d for d in possible_dirs if Path(d).exists()]
        
        if found_dirs:
            print(f"Found directories: {{', '.join(found_dirs)}}")
            for dir_name in found_dirs:
                print(f"Evaluating {{dir_name}}...")
                os.system(f"python mass_production_qc.py")
        else:
            print("No asset directories found!")

def show_status():
    """Show current production status."""
    print("\\nCURRENT PRODUCTION STATUS")
    print("=" * 25)
    
    # Look for assets in common directories
    asset_dirs = ["assets", "generated_assets", "leonardo_assets", "comfy_output", "fooocus_output"]
    total_found = 0
    
    for dir_name in asset_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            png_count = len(list(dir_path.rglob("*.png")))
            if png_count > 0:
                print(f"{{dir_name}}: {{png_count}} PNG files")
                total_found += png_count
    
    target = 64
    completion = total_found / target * 100
    
    print(f"\\nOVERALL STATUS:")
    print(f"Generated: {{total_found}}/{{target}} assets ({{completion:.1f}}%)")
    
    if total_found >= target:
        print("🎉 PRODUCTION COMPLETE!")
        print("Next: Run quality control")
    elif total_found > 0:
        remaining = target - total_found
        print(f"⚡ IN PROGRESS - {{remaining}} more needed")
    else:
        print("⏳ NOT STARTED - Choose production method")

def show_production_guide():
    """Show production guide."""
    print("\\nPRODUCTION GUIDE")
    print("=" * 16)
    
    guide_text = f"""
MASS PRODUCTION WORKFLOW:
========================

TARGET: 64 Hades-Egyptian Assets

METHODS (Choose one):
1. COMFYUI (Recommended for batch)
   - Fully automated
   - Free
   - Requires local setup
   - Time: 2-4 hours

2. LEONARDO AI (Best quality)
   - Premium results
   - ~$10 cost
   - API automation
   - Time: 1-2 hours

3. FOOOCUS (Easiest)
   - Manual but guided
   - Free
   - Step-by-step
   - Time: 6-8 hours

WORKFLOW:
1. Choose production method
2. Start generation
3. Monitor with dashboard
4. Run quality control
5. Organize approved assets
6. Ready for game integration!

QUALITY TARGETS:
- Legendary: >90% approval (18/20)
- Epic: >85% approval (20/24)  
- Rare: >80% approval (13/16)
- Common: >75% approval (3/4)

OVERALL TARGET: 84% success rate (54/64 assets)
"""
    
    print(guide_text)

def main():
    """Main production system controller."""
    
    # Ensure we're in the right directory
    expected_files = ["comfyui_mass_production.py", "production_dashboard.py", "mass_production_qc.py"]
    missing_files = [f for f in expected_files if not Path(f).exists()]
    
    if missing_files:
        print("ERROR: Missing production files:")
        for file in missing_files:
            print(f"- {{file}}")
        print("\\nRun the mass production setup first!")
        return
    
    while True:
        choice = show_main_menu()
        
        if choice == "0":
            print("Production system closed.")
            break
        elif choice == "1":
            run_comfyui_production()
        elif choice == "2":
            run_leonardo_production()
        elif choice == "3":
            run_fooocus_production()
        elif choice == "4":
            run_dashboard()
        elif choice == "5":
            run_quality_control()
        elif choice == "6":
            show_status()
        elif choice == "7":
            os.system("python production_dashboard.py")
        elif choice == "8":
            show_production_guide()
        else:
            print("Invalid option!")
        
        if choice != "4":  # Dashboard has its own loop
            input("\\nPress Enter to continue...")

if __name__ == "__main__":
    main()
'''
        
        master_file = self.production_dir / "run_mass_production.py"
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(master_script)
        
        # Create README for the system
        readme_content = f'''
# MASS PRODUCTION SYSTEM - FASE 5
## Sands of Duat: Hades-Egyptian Asset Generation

Sistema completo de produção em massa para gerar 64 assets de qualidade profissional.

## ARQUIVOS DO SISTEMA:

### 🎯 CONTROLLER PRINCIPAL:
- `run_mass_production.py` - Interface principal unificada

### 🤖 MÉTODOS DE GERAÇÃO:
- `comfyui_mass_production.py` - Automação ComfyUI completa
- `leonardo_ai_mass_production.py` - API Leonardo AI premium
- `fooocus_mass_production_guide.md` - Guia manual completo

### 📊 MONITORAMENTO:
- `production_dashboard.py` - Dashboard tempo real
- `mass_production_qc.py` - Controle qualidade automatizado

### 📁 ESTRUTURA DE ASSETS:
```
mass_production/
├── assets/
│   ├── legendary/deities/        # 20 assets (5×4)
│   ├── epic/heroes/             # 12 assets (3×4)  
│   ├── epic/environments/       # 12 assets (3×4)
│   ├── rare/creatures/          # 16 assets (4×4)
│   └── common/ui_elements/      # 4 assets (1×4)
├── quality_control/
│   ├── approved/               # Assets aprovados
│   ├── rejected/               # Assets rejeitados  
│   └── review/                 # Assets para revisão
└── production_ready/           # Assets finais
```

## COMO USAR:

### 1. EXECUÇÃO PRINCIPAL:
```bash
python run_mass_production.py
```

### 2. ESCOLHER MÉTODO:
- **ComfyUI:** Automação completa (recomendado)
- **Leonardo AI:** Qualidade premium (~$10)
- **Fooocus:** Manual guiado (gratuito)

### 3. MONITORAMENTO:
```bash
python production_dashboard.py
```

### 4. CONTROLE DE QUALIDADE:
```bash  
python mass_production_qc.py
```

## MÉTRICAS DE SUCESSO:

**TARGET TOTAL:** 64 assets únicos  
**TEMPO ESTIMADO:** 2-8 horas (dependendo do método)  
**QUALIDADE ALVO:** 84% aprovação geral (54/64 assets)

**Por Categoria:**
- Legendary (Deities): 20 assets, >90% qualidade
- Epic (Heroes/Environments): 24 assets, >85% qualidade  
- Rare (Creatures): 16 assets, >80% qualidade
- Common (UI): 4 assets, >75% qualidade

## WORKFLOW RECOMENDADO:

1. **Setup:** Verificar requisitos do método escolhido
2. **Geração:** Executar produção em massa
3. **Monitoramento:** Acompanhar progresso em tempo real
4. **Quality Control:** Validar e aprovar assets
5. **Organização:** Mover assets aprovados para produção
6. **Integração:** Assets prontos para o jogo

## PRÓXIMAS FASES:
- ✅ FASE 1-4: Completas
- 🔄 FASE 5: Em execução (Mass Production)  
- ⏳ FASE 6: Quality Control Extremo
- ⏳ FASE 7: Integração Final

Sistema desenvolvido para qualidade **Hades + Egyptian** profissional.
'''
        
        readme_file = self.production_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"Sistema mestre criado: {master_file}")
        print(f"README criado: {readme_file}")
        print(f"Diretório principal: {self.production_dir}")
        
        return master_file

def main():
    """Execute mass production system setup."""
    manager = MassProductionManager()
    
    print("FASE 5 - SISTEMA DE PRODUCAO EM MASSA")
    print("=" * 40)
    
    # 1. Create production batches
    batches = manager.create_production_batches()
    
    # 2. Create automation scripts  
    scripts = manager.create_production_automation_scripts()
    
    # 3. Create production dashboard
    dashboard = manager.create_production_dashboard()
    
    # 4. Finalize complete system
    master_controller = manager.finalize_mass_production_system()
    
    print("\n" + "=" * 60)
    print("SISTEMA DE PRODUCAO EM MASSA COMPLETO!")
    print("=" * 60)
    print(f"Target: 64 assets Hades-Egyptian")
    print(f"Métodos: 3 diferentes (ComfyUI, Leonardo AI, Fooocus)")
    print(f"Quality Control: Automatizado")
    print(f"Dashboard: Tempo real")
    print(f"Coordenação: Sistema mestre unificado")
    print("\nPara iniciar produção:")
    print(f"cd {manager.production_dir}")
    print("python run_mass_production.py")

if __name__ == "__main__":
    main()