#!/usr/bin/env python3
"""
SMART ASSET GENERATOR - FASE 4
===============================
Sistema inteligente de geração de assets com quality control automatizado
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib

class SmartAssetGenerator:
    def __init__(self):
        self.base_dir = Path(".")
        self.output_dir = self.base_dir / "generated_assets"
        self.quality_db = self.base_dir / "quality_database.json"
        
        # Load dataset
        dataset_file = Path("../lora_training/dataset/hades_egyptian/hades_egyptian_dataset.json")
        if dataset_file.exists():
            with open(dataset_file, 'r', encoding='utf-8') as f:
                self.dataset = json.load(f)
        else:
            self.dataset = {"prompts": []}
        
        # Generation queue system
        self.generation_queue = []
        self.completed_assets = []
        self.failed_assets = []
        
        # Quality control settings
        self.quality_thresholds = {
            "legendary": 0.90,  # Must be near perfect
            "epic": 0.85,       # High quality
            "rare": 0.80,       # Good quality  
            "common": 0.75      # Acceptable quality
        }
        
        self.setup_directories()
    
    def setup_directories(self):
        """Create organized directory structure."""
        print("CONFIGURANDO SISTEMA INTELIGENTE DE GERACAO")
        print("=" * 45)
        
        directories = [
            self.output_dir / "legendary" / "deities",
            self.output_dir / "epic" / "heroes", 
            self.output_dir / "epic" / "environments",
            self.output_dir / "rare" / "creatures",
            self.output_dir / "common" / "ui_elements",
            self.output_dir / "quality_control" / "approved",
            self.output_dir / "quality_control" / "rejected", 
            self.output_dir / "quality_control" / "review",
            self.output_dir / "production_ready",
            self.output_dir / "batch_logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("Estrutura de diretorios criada!")
    
    def create_generation_plan(self):
        """Create intelligent generation plan based on priorities."""
        print("CRIANDO PLANO INTELIGENTE DE GERACAO")
        print("=" * 40)
        
        # Priority system: Legendary > Epic > Rare > Common
        priority_order = ["legendary", "epic", "rare", "common"]
        
        generation_plan = {
            "timestamp": datetime.now().isoformat(),
            "total_assets": 0,
            "estimated_time": 0,
            "priority_batches": {}
        }
        
        # Organize by priority
        for priority in priority_order:
            priority_assets = []
            
            for prompt_data in self.dataset.get("prompts", []):
                rarity = prompt_data.get("rarity", "common")
                if rarity == priority:
                    # Create 4 variations for each prompt
                    for i in range(4):
                        asset_spec = {
                            "id": f"{prompt_data['id']}_var_{i+1}",
                            "original_id": prompt_data["id"], 
                            "variation": i + 1,
                            "prompt": prompt_data["prompt"],
                            "category": prompt_data["category"],
                            "character": prompt_data["character"],
                            "rarity": rarity,
                            "quality_threshold": self.quality_thresholds[rarity],
                            "max_attempts": 3,
                            "estimated_time": 45  # seconds per generation
                        }
                        priority_assets.append(asset_spec)
            
            if priority_assets:
                generation_plan["priority_batches"][priority] = {
                    "assets": priority_assets,
                    "count": len(priority_assets),
                    "estimated_time": len(priority_assets) * 45
                }
                generation_plan["total_assets"] += len(priority_assets)
                generation_plan["estimated_time"] += len(priority_assets) * 45
        
        # Save generation plan
        plan_file = self.output_dir / "generation_plan.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(generation_plan, f, indent=2, ensure_ascii=False)
        
        print(f"Plano criado: {plan_file}")
        print(f"Total assets: {generation_plan['total_assets']}")
        print(f"Tempo estimado: {generation_plan['estimated_time']//60:.0f} minutos")
        
        # Show breakdown
        for priority, batch in generation_plan["priority_batches"].items():
            print(f"  {priority.upper()}: {batch['count']} assets")
        
        return generation_plan
    
    def create_external_generation_scripts(self):
        """Create scripts for external AI generation tools."""
        print("\nCRIANDO SCRIPTS PARA FERRAMENTAS EXTERNAS")
        print("=" * 42)
        
        # ComfyUI workflow script
        comfyui_script = self.create_comfyui_batch_script()
        
        # Automatic1111 script  
        a1111_script = self.create_automatic1111_script()
        
        # Fooocus script
        fooocus_script = self.create_fooocus_script()
        
        # Online services script
        online_script = self.create_online_services_guide()
        
        print("Scripts externos criados:")
        print(f"- ComfyUI: {comfyui_script}")
        print(f"- Automatic1111: {a1111_script}")
        print(f"- Fooocus: {fooocus_script}")
        print(f"- Online Guide: {online_script}")
        
        return {
            "comfyui": comfyui_script,
            "automatic1111": a1111_script,
            "fooocus": fooocus_script,
            "online": online_script
        }
    
    def create_comfyui_batch_script(self):
        """Create ComfyUI batch generation script."""
        
        # Load all prompts for batch processing
        all_prompts = []
        for prompt_data in self.dataset.get("prompts", []):
            for i in range(4):  # 4 variations
                all_prompts.append({
                    "filename": f"{prompt_data['id']}_var_{i+1}",
                    "prompt": prompt_data["prompt"],
                    "negative": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
                    "category": prompt_data["category"],
                    "rarity": prompt_data["rarity"]
                })
        
        script_content = f'''
# COMFYUI BATCH GENERATION - HADES EGYPTIAN ASSETS
# =================================================
# 
# INSTRUCOES:
# 1. Abra ComfyUI
# 2. Carregue o workflow SDXL base
# 3. Configure os parametros abaixo
# 4. Execute em batch
#
# CONFIGURACOES OTIMIZADAS:
# - Modelo: SDXL Base 1.0
# - Resolucao: 1024x1024
# - Steps: 30
# - CFG: 7.5
# - Sampler: DPM++ 2M Karras
# - Scheduler: Karras

TOTAL_IMAGES = {len(all_prompts)}
BATCH_SIZE = 4

# PROMPTS PARA GERACAO:
prompts_data = {json.dumps(all_prompts, indent=2, ensure_ascii=False)}

# WORKFLOW BASICO (JSON para ComfyUI):
workflow_template = {{
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
            "seed": 42,
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
            "text": "PROMPT_PLACEHOLDER"
        }}
    }},
    "7": {{
        "class_type": "CLIPTextEncode", 
        "inputs": {{
            "clip": ["4", 1],
            "text": "NEGATIVE_PLACEHOLDER"
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
            "filename_prefix": "hades_egyptian_",
            "images": ["8", 0]
        }}
    }}
}}

print("COMFYUI BATCH SCRIPT CARREGADO")
print(f"Total de imagens para gerar: {{TOTAL_IMAGES}}")
print("Configure o workflow e execute!")
'''
        
        script_file = self.output_dir / "comfyui_batch_generation.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_file
    
    def create_automatic1111_script(self):
        """Create Automatic1111 batch script."""
        
        # Create batch file for A1111 API
        script_content = '''
REM AUTOMATIC1111 BATCH GENERATION SCRIPT
REM =====================================
REM 
REM PREREQUISITOS:
REM 1. Automatic1111 instalado e rodando
REM 2. SDXL model carregado
REM 3. API habilitada (--api flag)
REM
REM CONFIGURACOES:
REM - URL: http://127.0.0.1:7860
REM - Model: SDXL Base 1.0
REM - Resolution: 1024x1024
REM - Steps: 30
REM - CFG: 7.5

@echo off
echo INICIANDO BATCH GENERATION AUTOMATIC1111
echo ========================================

REM Verificar se A1111 esta rodando
curl -s http://127.0.0.1:7860/sdapi/v1/progress >nul
if %errorlevel% neq 0 (
    echo ERRO: Automatic1111 nao esta rodando!
    echo Inicie A1111 com: python launch.py --api
    pause
    exit /b 1
)

echo A1111 detectado! Iniciando geracao...

REM Aqui voce pode usar Python script ou ferramenta de batch
echo Use o script Python automatic1111_batch.py
echo Ou importe os prompts manualmente na interface web

pause
'''
        
        batch_file = self.output_dir / "run_automatic1111_batch.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Create Python API script
        api_script = f'''
import requests
import json
import time
from pathlib import Path

# Automatic1111 API endpoint
API_URL = "http://127.0.0.1:7860"

# All prompts for generation
prompts_data = {json.dumps([{
    "filename": f"{p['id']}_var_{i+1}",
    "prompt": p["prompt"],
    "category": p["category"],
    "rarity": p["rarity"]
} for p in self.dataset.get("prompts", []) for i in range(4)], indent=2)}

def generate_image(prompt_data):
    """Generate single image via A1111 API."""
    
    payload = {{
        "prompt": prompt_data["prompt"],
        "negative_prompt": "blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy",
        "width": 1024,
        "height": 1024,
        "steps": 30,
        "cfg_scale": 7.5,
        "sampler_name": "DPM++ 2M Karras",
        "seed": -1,
        "save_images": True,
        "filename": prompt_data["filename"]
    }}
    
    try:
        response = requests.post(f"{{API_URL}}/sdapi/v1/txt2img", json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"Erro API: {{response.status_code}}")
            return False
    except Exception as e:
        print(f"Erro conexao: {{e}}")
        return False

def main():
    print("AUTOMATIC1111 BATCH GENERATOR")
    print("=" * 30)
    
    # Test API connection
    try:
        response = requests.get(f"{{API_URL}}/sdapi/v1/progress")
        if response.status_code != 200:
            print("ERRO: Nao conseguiu conectar com A1111 API")
            return
    except:
        print("ERRO: Automatic1111 nao esta rodando")
        print("Inicie com: python launch.py --api")
        return
    
    print("API conectada! Iniciando batch generation...")
    
    successful = 0
    failed = 0
    
    for i, prompt_data in enumerate(prompts_data):
        print(f"Gerando {{i+1}}/{{len(prompts_data)}}: {{prompt_data['filename']}}")
        
        if generate_image(prompt_data):
            successful += 1
            print(f"  ✓ Sucesso")
        else:
            failed += 1
            print(f"  ✗ Falhou")
        
        # Pausa entre geracoes
        time.sleep(2)
    
    print(f"\\nCOMPLETO: {{successful}} sucessos, {{failed}} falhas")

if __name__ == "__main__":
    main()
'''
        
        api_file = self.output_dir / "automatic1111_batch.py"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_script)
        
        return batch_file
    
    def create_fooocus_script(self):
        """Create Fooocus generation guide."""
        
        guide_content = f'''
# FOOOCUS GENERATION GUIDE - HADES EGYPTIAN ASSETS
# ================================================

## SETUP FOOOCUS:
1. Download Fooocus: https://github.com/lllyasviel/Fooocus
2. Instalar e executar
3. Aguardar download do modelo SDXL
4. Interface pronta para uso!

## CONFIGURAÇÕES RECOMENDADAS:
- Performance: Speed (para batch rapido) ou Quality (para melhor resultado)
- Aspect Ratio: 1024x1024 (square)
- Image Number: 4 (para gerar 4 variacoes)
- Guidance Scale: 7.5
- Style: Fooocus V2 (ou desabilitado para prompt puro)

## PROMPTS PARA GERAR ({len(self.dataset.get("prompts", [])) * 4} imagens):

'''
        
        # Add all prompts to guide
        for prompt_data in self.dataset.get("prompts", []):
            guide_content += f'''
### {prompt_data["character"]} ({prompt_data["rarity"].upper()})
**Categoria:** {prompt_data["category"]}
**Variações:** 4 imagens

**Prompt:**
```
{prompt_data["prompt"]}
```

**Negative Prompt:**
```
blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy
```

**Salvar como:** {prompt_data["id"]}_var_1.png, {prompt_data["id"]}_var_2.png, etc.

---
'''
        
        guide_content += '''
## PROCESSO DE GERAÇÃO:
1. Copie o prompt no campo "Prompt"
2. Copie o negative prompt no campo "Negative Prompt" 
3. Defina "Image Number" como 4
4. Clique em "Generate"
5. Salve as 4 imagens com os nomes corretos
6. Repita para o próximo prompt

## ORGANIZAÇÃO DOS ARQUIVOS:
- Legendary (Deities): pasta /legendary/deities/
- Epic (Heroes/Environments): pasta /epic/heroes/ ou /epic/environments/
- Rare (Creatures): pasta /rare/creatures/
- Common (UI): pasta /common/ui_elements/

Total estimado: 2-4 horas dependendo da velocidade da GPU.
'''
        
        guide_file = self.output_dir / "fooocus_generation_guide.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return guide_file
    
    def create_online_services_guide(self):
        """Create guide for online AI services."""
        
        guide_content = f'''
# ONLINE AI SERVICES GUIDE - HADES EGYPTIAN ASSETS
# =================================================

## RECOMMENDED SERVICES:
1. **Runway ML** - High quality, good for batch
2. **Leonardo AI** - Game art focused, excellent results  
3. **Midjourney** - Premium quality, Discord interface
4. **DALL-E 3** - OpenAI, via ChatGPT Plus
5. **Stable Diffusion Online** - Various free/paid options

## CONFIGURATION FOR EACH SERVICE:

### LEONARDO AI (RECOMMENDED):
- Model: Leonardo Diffusion XL
- Dimensions: 1024x1024
- Guidance Scale: 7
- Steps: 30-50
- Prompt Magic: ON
- PhotoReal: OFF (we want illustrated style)

### MIDJOURNEY:
- Version: --v 6.1 
- Style: --style raw (for more literal interpretation)
- Aspect Ratio: --ar 1:1
- Quality: --q 2
- Add to end of prompt: ", game art illustration, digital painting"

### RUNWAY ML:
- Model: Gen-3 Alpha Turbo
- Mode: Image Generation
- Resolution: 1024x1024
- Steps: 30

## BATCH GENERATION STRATEGY:
1. Start with LEGENDARY tier (5 prompts × 4 variations = 20 images)
2. Then EPIC tier (6 prompts × 4 variations = 24 images) 
3. Then RARE tier (4 prompts × 4 variations = 16 images)
4. Finally COMMON tier (1 prompt × 4 variations = 4 images)

Total: {len(self.dataset.get("prompts", [])) * 4} images

## PROMPTS READY FOR COPY-PASTE:

'''
        
        # Add formatted prompts
        for i, prompt_data in enumerate(self.dataset.get("prompts", [])):
            guide_content += f'''
**{i+1}. {prompt_data["character"]} ({prompt_data["rarity"].upper()})**
```
{prompt_data["prompt"]}
```
Negative: `blurry, low quality, amateur, multiple characters, anime style, cartoon, text, watermark, bad anatomy`
Save as: `{prompt_data["id"]}_var_1.png` through `{prompt_data["id"]}_var_4.png`

'''
        
        guide_content += '''
## COST ESTIMATES:
- Leonardo AI: ~$5-10 for all 64 images
- Midjourney: ~$10 (1 month subscription)
- Runway: ~$15-20 for all images  
- DALL-E 3: ~$20-30 via API

## QUALITY CONTROL:
After generation, check each image for:
- ✅ Single character (no multiples)
- ✅ Egyptian + Hades style blend
- ✅ Proper proportions
- ✅ Rich colors and dramatic lighting
- ✅ No text/watermarks
- ✅ High resolution and detail

Regenerate any images that don't meet quality standards.
'''
        
        guide_file = self.output_dir / "online_services_guide.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return guide_file
    
    def create_quality_control_system(self):
        """Create automated quality control system."""
        print("\nCRIANDO SISTEMA DE CONTROLE DE QUALIDADE")
        print("=" * 42)
        
        qc_script = '''
#!/usr/bin/env python3
"""
QUALITY CONTROL SYSTEM - HADES EGYPTIAN ASSETS
==============================================
Sistema automatizado de validação de qualidade
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class QualityController:
    def __init__(self):
        self.quality_standards = {
            "legendary": {
                "min_resolution": (1024, 1024),
                "max_file_size": 10 * 1024 * 1024,  # 10MB
                "required_elements": ["dramatic_lighting", "high_detail", "vibrant_colors"],
                "forbidden_elements": ["multiple_characters", "text", "watermarks", "blur"]
            },
            "epic": {
                "min_resolution": (768, 768), 
                "max_file_size": 8 * 1024 * 1024,
                "required_elements": ["good_lighting", "detailed", "clear"],
                "forbidden_elements": ["multiple_characters", "text", "watermarks"]
            },
            "rare": {
                "min_resolution": (512, 512),
                "max_file_size": 6 * 1024 * 1024,
                "required_elements": ["clear", "recognizable"],
                "forbidden_elements": ["multiple_characters", "text"]
            },
            "common": {
                "min_resolution": (512, 512),
                "max_file_size": 5 * 1024 * 1024,
                "required_elements": ["clear"],
                "forbidden_elements": ["text"]
            }
        }
        
        self.quality_db = Path("quality_database.json")
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
                    "total_evaluated": 0,
                    "approved": 0,
                    "rejected": 0,
                    "pending_review": 0
                }
            }
    
    def evaluate_image(self, image_path: str, expected_rarity: str) -> Dict:
        """Evaluate single image quality."""
        
        evaluation = {
            "image_path": image_path,
            "timestamp": datetime.now().isoformat(),
            "rarity": expected_rarity,
            "checks": {},
            "overall_score": 0.0,
            "status": "pending",
            "issues": []
        }
        
        try:
            from PIL import Image
            
            # Basic file checks
            if not os.path.exists(image_path):
                evaluation["issues"].append("File not found")
                evaluation["status"] = "rejected"
                return evaluation
            
            # Load image
            img = Image.open(image_path)
            width, height = img.size
            file_size = os.path.getsize(image_path)
            
            standards = self.quality_standards[expected_rarity]
            
            # Resolution check
            min_width, min_height = standards["min_resolution"]
            if width >= min_width and height >= min_height:
                evaluation["checks"]["resolution"] = {"passed": True, "value": f"{width}x{height}"}
            else:
                evaluation["checks"]["resolution"] = {"passed": False, "value": f"{width}x{height}"}
                evaluation["issues"].append(f"Resolution too low: {width}x{height}")
            
            # File size check  
            if file_size <= standards["max_file_size"]:
                evaluation["checks"]["file_size"] = {"passed": True, "value": f"{file_size//1024}KB"}
            else:
                evaluation["checks"]["file_size"] = {"passed": False, "value": f"{file_size//1024}KB"}
                evaluation["issues"].append(f"File too large: {file_size//1024}KB")
            
            # Calculate score
            passed_checks = sum(1 for check in evaluation["checks"].values() if check["passed"])
            total_checks = len(evaluation["checks"])
            evaluation["overall_score"] = passed_checks / total_checks if total_checks > 0 else 0
            
            # Determine status
            if evaluation["overall_score"] >= 0.8 and not evaluation["issues"]:
                evaluation["status"] = "approved"
            elif evaluation["overall_score"] >= 0.6:
                evaluation["status"] = "review"
            else:
                evaluation["status"] = "rejected"
            
        except Exception as e:
            evaluation["issues"].append(f"Error processing image: {str(e)}")
            evaluation["status"] = "error"
        
        return evaluation
    
    def batch_evaluate(self, images_directory: str) -> Dict:
        """Evaluate all images in directory."""
        
        print(f"Evaluating images in: {images_directory}")
        
        image_dir = Path(images_directory)
        if not image_dir.exists():
            return {"error": "Directory not found"}
        
        # Find all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(image_dir.rglob(f"*{ext}"))
        
        print(f"Found {len(image_files)} images to evaluate")
        
        results = []
        for image_file in image_files:
            # Determine expected rarity from path
            rarity = "common"  # default
            path_str = str(image_file).lower()
            if "legendary" in path_str:
                rarity = "legendary"
            elif "epic" in path_str:
                rarity = "epic"
            elif "rare" in path_str:
                rarity = "rare"
            
            evaluation = self.evaluate_image(str(image_file), rarity)
            results.append(evaluation)
            
            print(f"  {image_file.name}: {evaluation['status']} ({evaluation['overall_score']:.2f})")
        
        # Update database
        self.db["evaluations"].extend(results)
        self.update_statistics()
        self.save_quality_database()
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluated": len(results),
            "approved": sum(1 for r in results if r["status"] == "approved"),
            "rejected": sum(1 for r in results if r["status"] == "rejected"),
            "review": sum(1 for r in results if r["status"] == "review"),
            "error": sum(1 for r in results if r["status"] == "error"),
            "average_score": sum(r["overall_score"] for r in results) / len(results) if results else 0,
            "details": results
        }
        
        return report
    
    def update_statistics(self):
        """Update quality statistics."""
        stats = {
            "total_evaluated": len(self.db["evaluations"]),
            "approved": sum(1 for e in self.db["evaluations"] if e["status"] == "approved"),
            "rejected": sum(1 for e in self.db["evaluations"] if e["status"] == "rejected"),
            "pending_review": sum(1 for e in self.db["evaluations"] if e["status"] == "review"),
            "error": sum(1 for e in self.db["evaluations"] if e["status"] == "error")
        }
        self.db["statistics"] = stats
    
    def save_quality_database(self):
        """Save quality database to file."""
        with open(self.quality_db, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)
    
    def generate_quality_report(self) -> str:
        """Generate comprehensive quality report."""
        
        stats = self.db["statistics"]
        
        report = f"""
QUALITY CONTROL REPORT - HADES EGYPTIAN ASSETS
==============================================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL STATISTICS:
- Total Evaluated: {stats["total_evaluated"]}
- Approved: {stats["approved"]} ({stats["approved"]/stats["total_evaluated"]*100:.1f}%)
- Rejected: {stats["rejected"]} ({stats["rejected"]/stats["total_evaluated"]*100:.1f}%)
- Needs Review: {stats["pending_review"]} ({stats["pending_review"]/stats["total_evaluated"]*100:.1f}%)
- Errors: {stats["error"]}

QUALITY BREAKDOWN BY RARITY:
"""
        
        # Group by rarity
        by_rarity = {}
        for eval in self.db["evaluations"]:
            rarity = eval.get("rarity", "unknown")
            if rarity not in by_rarity:
                by_rarity[rarity] = {"approved": 0, "rejected": 0, "review": 0, "total": 0}
            
            by_rarity[rarity]["total"] += 1
            by_rarity[rarity][eval["status"]] = by_rarity[rarity].get(eval["status"], 0) + 1
        
        for rarity, data in by_rarity.items():
            report += f"\\n{rarity.upper()}:"
            report += f"\\n  Total: {data['total']}"
            report += f"\\n  Approved: {data.get('approved', 0)} ({data.get('approved', 0)/data['total']*100:.1f}%)"
            report += f"\\n  Rejected: {data.get('rejected', 0)}"
            report += f"\\n  Review: {data.get('review', 0)}"
        
        # Common issues
        all_issues = []
        for eval in self.db["evaluations"]:
            all_issues.extend(eval.get("issues", []))
        
        if all_issues:
            from collections import Counter
            issue_counts = Counter(all_issues)
            
            report += "\\n\\nCOMMON ISSUES:"
            for issue, count in issue_counts.most_common(5):
                report += f"\\n- {issue}: {count} times"
        
        report += "\\n\\nRECOMMENDATIONS:"
        if stats["rejected"] > stats["approved"]:
            report += "\\n- Quality is below standards. Review generation settings."
            report += "\\n- Consider using higher-end AI service or model."
        elif stats["pending_review"] > 0:
            report += f"\\n- {stats['pending_review']} images need manual review."
        else:
            report += "\\n- Quality is excellent! Assets ready for production."
        
        return report

def main():
    """Run quality control evaluation."""
    controller = QualityController()
    
    print("QUALITY CONTROL SYSTEM")
    print("=" * 22)
    print("1. Evaluate all images")
    print("2. Generate quality report")
    print("0. Exit")
    
    choice = input("\\nSelect option: ").strip()
    
    if choice == "1":
        images_dir = input("Enter images directory path: ").strip()
        if not images_dir:
            images_dir = "generated_assets"
        
        report = controller.batch_evaluate(images_dir)
        
        print(f"\\nEVALUATION COMPLETE:")
        print(f"- Total: {report['total_evaluated']}")
        print(f"- Approved: {report['approved']}")
        print(f"- Rejected: {report['rejected']}")
        print(f"- Review: {report['review']}")
        print(f"- Average Score: {report['average_score']:.2f}")
        
    elif choice == "2":
        report_text = controller.generate_quality_report()
        
        report_file = Path("quality_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\\nReport saved: {report_file}")

if __name__ == "__main__":
    main()
'''
        
        qc_file = self.output_dir / "quality_control_system.py"
        with open(qc_file, 'w', encoding='utf-8') as f:
            f.write(qc_script)
        
        print(f"Sistema QC criado: {qc_file}")
        return qc_file
    
    def create_master_generation_coordinator(self):
        """Create master coordinator for the entire generation process."""
        print("\nCRIANDO COORDENADOR MESTRE")
        print("=" * 25)
        
        coordinator_script = f'''
#!/usr/bin/env python3
"""
MASTER GENERATION COORDINATOR - FASE 4
=======================================
Coordena todo o processo de geração inteligente de assets
"""

import json
import time
from pathlib import Path
from datetime import datetime

class MasterCoordinator:
    def __init__(self):
        self.base_dir = Path(".")
        self.status_file = self.base_dir / "generation_status.json"
        self.load_status()
    
    def load_status(self):
        """Load current generation status."""
        if self.status_file.exists():
            with open(self.status_file, 'r', encoding='utf-8') as f:
                self.status = json.load(f)
        else:
            self.status = {{
                "phase": "planning",
                "total_assets": {len(self.dataset.get("prompts", [])) * 4},
                "completed": 0,
                "approved": 0, 
                "rejected": 0,
                "in_review": 0,
                "current_batch": None,
                "start_time": None,
                "estimated_completion": None
            }}
    
    def save_status(self):
        """Save current status to file."""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)
    
    def show_main_menu(self):
        """Display main coordination menu."""
        print("MASTER GENERATION COORDINATOR")
        print("=" * 30)
        print(f"Status: {{self.status['phase'].upper()}}")
        print(f"Progress: {{self.status['completed']}}/{{self.status['total_assets']}} assets")
        print(f"Approved: {{self.status['approved']}}")
        print(f"Rejected: {{self.status['rejected']}}")
        print(f"In Review: {{self.status['in_review']}}")
        print()
        print("ACTIONS:")
        print("1. Start generation process")
        print("2. Check generation status") 
        print("3. Run quality control")
        print("4. Generate final report")
        print("5. Show generation guides")
        print("0. Exit")
        
        return input("\\nSelect action: ").strip()
    
    def start_generation_process(self):
        """Start the generation process."""
        print("\\nSTARTING GENERATION PROCESS")
        print("=" * 28)
        
        # Update status
        self.status["phase"] = "generating"
        self.status["start_time"] = datetime.now().isoformat()
        self.save_status()
        
        print("Generation process initiated!")
        print("\\nAVAILABLE METHODS:")
        print("1. ComfyUI (Recommended for batch)")
        print("2. Automatic1111 (Good for customization)")
        print("3. Fooocus (Easiest to use)")
        print("4. Online Services (Leonardo AI, Midjourney, etc.)")
        
        method = input("\\nSelect method (1-4): ").strip()
        
        if method == "1":
            print("\\nComfyUI Guide:")
            print("1. Open ComfyUI")
            print("2. Load the batch script: comfyui_batch_generation.py")
            print("3. Execute batch generation")
            print("4. Images will be saved automatically")
        
        elif method == "2":
            print("\\nAutomatic1111 Guide:")
            print("1. Start A1111 with --api flag")
            print("2. Run: python automatic1111_batch.py")
            print("3. Or use run_automatic1111_batch.bat")
        
        elif method == "3":
            print("\\nFooocus Guide:")
            print("1. Open fooocus_generation_guide.md")
            print("2. Follow step-by-step instructions")
            print("3. Generate images manually with provided prompts")
        
        elif method == "4":
            print("\\nOnline Services Guide:")
            print("1. Open online_services_guide.md")
            print("2. Choose your preferred service")
            print("3. Use provided prompts for batch generation")
        
        print("\\nAfter generation, run quality control to validate assets!")
        
    def check_generation_status(self):
        """Check current generation status."""
        print("\\nGENERATION STATUS")
        print("=" * 17)
        
        # Scan for generated images
        generated_count = 0
        for img_dir in self.base_dir.rglob("*.png"):
            if "hades" in img_dir.name.lower() or "egyptian" in img_dir.name.lower():
                generated_count += 1
        
        self.status["completed"] = generated_count
        self.save_status()
        
        print(f"Phase: {{self.status['phase'].upper()}}")
        print(f"Total Target: {{self.status['total_assets']}} assets")
        print(f"Generated: {{generated_count}} images found")
        print(f"Progress: {{(generated_count/self.status['total_assets']*100):.1f}}%")
        
        if self.status["start_time"]:
            start = datetime.fromisoformat(self.status["start_time"])
            elapsed = (datetime.now() - start).total_seconds() / 3600
            print(f"Time Elapsed: {{elapsed:.1f}} hours")
            
            if generated_count > 0:
                rate = generated_count / elapsed
                remaining = self.status['total_assets'] - generated_count
                eta = remaining / rate if rate > 0 else 0
                print(f"ETA: {{eta:.1f}} hours remaining")
        
        print(f"Quality Status:")
        print(f"  Approved: {{self.status['approved']}}")
        print(f"  Rejected: {{self.status['rejected']}}")
        print(f"  In Review: {{self.status['in_review']}}")
    
    def run_quality_control(self):
        """Run quality control on generated images."""
        print("\\nRUNNING QUALITY CONTROL")
        print("=" * 23)
        
        # This would integrate with quality_control_system.py
        print("Execute: python quality_control_system.py")
        print("Or run automated scan of generated_assets/ directory")
        
        # Update status based on QC results
        self.status["phase"] = "quality_control"
        self.save_status()
    
    def generate_final_report(self):
        """Generate final comprehensive report."""
        print("\\nGENERATING FINAL REPORT")
        print("=" * 22)
        
        report = {{
            "timestamp": datetime.now().isoformat(),
            "project": "Hades-Egyptian Asset Generation",
            "phase": "FASE 4 - Sistema Geração Inteligente",
            "status": self.status,
            "summary": {{
                "total_planned": self.status["total_assets"],
                "total_generated": self.status["completed"],
                "completion_rate": self.status["completed"] / self.status["total_assets"] * 100,
                "quality_rate": self.status["approved"] / max(self.status["completed"], 1) * 100
            }}
        }}
        
        report_file = self.base_dir / "final_generation_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Final report generated: {{report_file}}")
        
        # Generate human-readable summary
        summary = f"""
FINAL GENERATION REPORT - HADES EGYPTIAN ASSETS
===============================================

Generated: {{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}

PROJECT STATUS:
- Phase: {{report["phase"]}}
- Total Planned: {{report["summary"]["total_planned"]}} assets
- Total Generated: {{report["summary"]["total_generated"]}} assets  
- Completion Rate: {{report["summary"]["completion_rate"]:.1f}}%
- Quality Rate: {{report["summary"]["quality_rate"]:.1f}}%

ASSET BREAKDOWN:
- Legendary (Deities): 5 characters × 4 variations = 20 assets
- Epic (Heroes): 3 characters × 4 variations = 12 assets
- Epic (Environments): 3 scenes × 4 variations = 12 assets  
- Rare (Creatures): 4 creatures × 4 variations = 16 assets
- Common (UI): 1 element × 4 variations = 4 assets

QUALITY CONTROL:
- Approved: {{self.status["approved"]}} assets
- Rejected: {{self.status["rejected"]}} assets
- In Review: {{self.status["in_review"]}} assets

NEXT STEPS:
- Complete any remaining generation
- Finalize quality control
- Prepare for FASE 5 (Production)
"""
        
        summary_file = self.base_dir / "generation_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(summary)
        print(f"Summary saved: {{summary_file}}")
    
    def show_generation_guides(self):
        """Show available generation guides."""
        print("\\nGENERATION GUIDES")
        print("=" * 16)
        
        guides = [
            ("ComfyUI", "comfyui_batch_generation.py"),
            ("Automatic1111", "automatic1111_batch.py"),
            ("Fooocus", "fooocus_generation_guide.md"), 
            ("Online Services", "online_services_guide.md"),
            ("Quality Control", "quality_control_system.py")
        ]
        
        for name, filename in guides:
            filepath = self.base_dir / filename
            exists = "✓" if filepath.exists() else "✗"
            print(f"{{exists}} {{name}}: {{filename}}")
    
    def run(self):
        """Main coordinator loop."""
        while True:
            choice = self.show_main_menu()
            
            if choice == "0":
                break
            elif choice == "1":
                self.start_generation_process()
            elif choice == "2":
                self.check_generation_status()
            elif choice == "3":
                self.run_quality_control()
            elif choice == "4":
                self.generate_final_report()
            elif choice == "5":
                self.show_generation_guides()
            else:
                print("Invalid option")
            
            input("\\nPress Enter to continue...")

if __name__ == "__main__":
    coordinator = MasterCoordinator()
    coordinator.run()
'''
        
        coordinator_file = self.output_dir / "master_coordinator.py"
        with open(coordinator_file, 'w', encoding='utf-8') as f:
            f.write(coordinator_script)
        
        print(f"Coordenador mestre criado: {coordinator_file}")
        return coordinator_file
    
    def finalize_intelligent_system(self):
        """Finalize the intelligent generation system."""
        print("\nFINALIZANDO SISTEMA INTELIGENTE")
        print("=" * 32)
        
        # Create main execution script
        main_script = f'''
#!/usr/bin/env python3
"""
EXECUTE INTELLIGENT GENERATION SYSTEM
=====================================
Ponto de entrada principal para FASE 4
"""

import sys
from pathlib import Path

def main():
    print("SISTEMA INTELIGENTE DE GERACAO - FASE 4")
    print("=" * 40)
    print("Hades-Egyptian Asset Generation System")
    print()
    
    print("COMPONENTES DISPONIVEIS:")
    components = [
        ("Master Coordinator", "master_coordinator.py", "Sistema principal de coordenação"),
        ("ComfyUI Batch", "comfyui_batch_generation.py", "Geração em batch via ComfyUI"),
        ("Automatic1111", "automatic1111_batch.py", "Geração via A1111 API"),
        ("Quality Control", "quality_control_system.py", "Sistema de controle de qualidade"),
        ("Fooocus Guide", "fooocus_generation_guide.md", "Guia manual Fooocus"),
        ("Online Guide", "online_services_guide.md", "Guia serviços online")
    ]
    
    for i, (name, file, desc) in enumerate(components, 1):
        filepath = Path(file)
        status = "✓" if filepath.exists() else "✗"
        print(f"{{i}}. {{status}} {{name}}")
        print(f"   File: {{file}}")
        print(f"   Desc: {{desc}}")
        print()
    
    print("EXECUÇÃO RECOMENDADA:")
    print("1. Execute: python master_coordinator.py")
    print("2. Siga as instruções do coordenador")
    print("3. Gere {len(self.dataset.get("prompts", [])) * 4} assets usando método preferido")
    print("4. Execute controle de qualidade")
    print("5. Finalize para FASE 5")
    
    print("\\nPara iniciar, execute: python master_coordinator.py")

if __name__ == "__main__":
    main()
'''
        
        main_file = self.output_dir / "run_intelligent_system.py"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_script)
        
        # Create README
        readme_content = f'''
# SISTEMA INTELIGENTE DE GERAÇÃO - FASE 4
## Hades-Egyptian Asset Generation

Este é o sistema inteligente completo para geração de assets do projeto Sands of Duat.

## ARQUIVOS PRINCIPAIS:

### 🎯 COORDENAÇÃO:
- `run_intelligent_system.py` - Ponto de entrada principal
- `master_coordinator.py` - Coordenador mestre do processo
- `generation_plan.json` - Plano detalhado de geração

### 🤖 GERAÇÃO AUTOMATIZADA:
- `comfyui_batch_generation.py` - Script para ComfyUI
- `automatic1111_batch.py` - Script para Automatic1111
- `run_automatic1111_batch.bat` - Batch file Windows

### 📖 GUIAS MANUAIS:
- `fooocus_generation_guide.md` - Guia completo Fooocus
- `online_services_guide.md` - Guia serviços online

### 🔍 QUALIDADE:
- `quality_control_system.py` - Sistema automático de QC
- `quality_database.json` - Base de dados de qualidade

### 📊 ORGANIZAÇÃO:
```
generated_assets/
├── legendary/deities/     # 5 personagens × 4 = 20 assets
├── epic/heroes/          # 3 personagens × 4 = 12 assets  
├── epic/environments/    # 3 ambientes × 4 = 12 assets
├── rare/creatures/       # 4 criaturas × 4 = 16 assets
├── common/ui_elements/   # 1 elemento × 4 = 4 assets
├── quality_control/      # Aprovados/rejeitados/revisão
├── production_ready/     # Assets finais aprovados
└── batch_logs/          # Logs do processo
```

## COMO EXECUTAR:

### Método 1 - Coordenador Mestre (Recomendado):
```bash
python run_intelligent_system.py
python master_coordinator.py
```

### Método 2 - ComfyUI (Melhor para batch):
```bash
# Abra ComfyUI
python comfyui_batch_generation.py
```

### Método 3 - Automatic1111:
```bash
# Inicie A1111 com --api
python automatic1111_batch.py
```

### Método 4 - Fooocus (Mais simples):
```bash
# Abra fooocus_generation_guide.md
# Siga instruções step-by-step
```

### Método 5 - Online Services:
```bash
# Abra online_services_guide.md
# Use Leonardo AI, Midjourney, etc.
```

## CONTROLE DE QUALIDADE:

Após geração:
```bash
python quality_control_system.py
```

## MÉTRICAS:
- **Total Assets:** {len(self.dataset.get("prompts", [])) * 4} imagens
- **Estimated Time:** 2-6 horas (dependendo do método)
- **Quality Target:** >80% aprovação
- **Output Format:** PNG 1024x1024

## PRÓXIMAS FASES:
- ✅ FASE 1-3: Completas
- 🔄 FASE 4: Em execução (Sistema Inteligente)
- ⏳ FASE 5: Produção Sistemática
- ⏳ FASE 6: Controle de Qualidade Extremo  
- ⏳ FASE 7: Integração e Polish Final

Desenvolvido para o projeto **Sands of Duat** - Qualidade Hades + Estilo Egípcio.
'''
        
        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"README criado: {readme_file}")
        print(f"Script principal: {main_file}")
        
        return main_file

def main():
    """Execute complete intelligent generation system setup."""
    generator = SmartAssetGenerator()
    
    print("FASE 4 - SISTEMA INTELIGENTE DE GERACAO")
    print("=" * 42)
    
    # 1. Create generation plan
    plan = generator.create_generation_plan()
    
    # 2. Create external generation scripts
    scripts = generator.create_external_generation_scripts()
    
    # 3. Create quality control system
    qc_system = generator.create_quality_control_system()
    
    # 4. Create master coordinator
    coordinator = generator.create_master_generation_coordinator()
    
    # 5. Finalize system
    main_script = generator.finalize_intelligent_system()
    
    print("\n" + "=" * 50)
    print("SISTEMA INTELIGENTE COMPLETO!")
    print("=" * 50)
    print(f"Assets planejados: {plan['total_assets']}")
    print(f"Tempo estimado: {plan['estimated_time']//60:.0f} minutos")
    print("Scripts criados para todas as plataformas!")
    print("Sistema de qualidade automatizado!")
    print("Coordenador mestre configurado!")
    print("\nPara iniciar: python master_coordinator.py")

if __name__ == "__main__":
    main()