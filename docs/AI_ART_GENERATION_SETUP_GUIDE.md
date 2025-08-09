# SANDS OF DUAT - AI ART GENERATION SETUP GUIDE
## RTX 5070 + 32GB RAM Optimization

Your hardware configuration is **excellent** for local AI art generation! Here's the optimal setup:

## Hardware Analysis ✅

- **RTX 5070**: 12GB VRAM - Perfect for SDXL and Flux models
- **32GB RAM**: Excellent for model loading and batch processing
- **7800X3D**: Fast CPU for preprocessing and post-processing

## Recommended AI Art Generation Stack

### Option 1: ComfyUI (Recommended)
**Best for:** Maximum control, custom workflows, batch processing

```bash
# Installation
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

**Optimal Settings for RTX 5070:**
- Model: SDXL Base (6.94GB VRAM usage)
- Resolution: 1024x1024 or 768x1024 for cards
- Batch Size: 2-4 (with 32GB RAM)
- Steps: 25-35 for quality
- CFG Scale: 7-9

### Option 2: Automatic1111 WebUI
**Best for:** User-friendly interface, extensive extension ecosystem

```bash
# Installation
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
# Run webui-user.bat on Windows
```

**Optimal Settings:**
- `--medvram` flag (not needed with 12GB VRAM)
- `--xformers` for memory efficiency
- Batch count: 4-6 simultaneously

### Option 3: Fooocus (Easiest Setup)
**Best for:** Plug-and-play, minimal configuration

```bash
# Installation
git clone https://github.com/lllyasviel/Fooocus.git
cd Fooocus
python launch.py
```

## Recommended Models for Egyptian Art

### 1. SDXL Base + LoRA Training
```
Base Model: stabilityai/stable-diffusion-xl-base-1.0
+ Your custom LoRA trained on the 75 Egyptian images
Estimated Generation Time: 15-30 seconds per image
```

### 2. Flux.1 Dev (Cutting Edge)
```
Model: black-forest-labs/FLUX.1-dev
VRAM Usage: ~10GB
Quality: Exceptional detail and prompt adherence
Generation Time: 45-60 seconds per image
```

### 3. RealVisXL V4.0
```
Specialized for: Photorealistic artwork
Perfect for: Egyptian god portraits, artifacts
VRAM Usage: ~7GB
```

## Local LoRA Training Setup

With your hardware, you can train custom LoRAs:

```bash
# Install Kohya_ss for LoRA training
git clone https://github.com/bmaltais/kohya_ss.git
cd kohya_ss
pip install -r requirements.txt

# Training parameters for RTX 5070:
# - Learning rate: 1e-4
# - Batch size: 2-4
# - Epochs: 10-20
# - Resolution: 768x768 or 1024x1024
```

## Integration with Sands of Duat

Update the AI generation pipeline to use local models:

```python
# In ai_generation_pipeline.py
class LocalSDXLGenerator:
    def __init__(self):
        self.api_base = "http://127.0.0.1:7860"  # A1111 WebUI
        # or
        self.comfy_api = "http://127.0.0.1:8188"  # ComfyUI
        
    def generate_with_local_model(self, prompt, negative_prompt, 
                                 width=768, height=1024):
        """Generate using local SDXL + custom LoRA"""
        
        payload = {
            "prompt": f"<lora:sands_of_duat:1.0> {prompt}",
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": 30,
            "cfg_scale": 7.5,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1
        }
        
        # Send to local API
        response = requests.post(f"{self.api_base}/sdapi/v1/txt2img", 
                               json=payload)
        return response.json()
```

## Optimal Generation Workflow

### 1. Batch Processing Strategy
```python
# Generate in batches to maximize GPU utilization
batch_configs = [
    {"size": (768, 1024), "type": "card_art", "batch_size": 3},
    {"size": (1920, 1080), "type": "backgrounds", "batch_size": 2},
    {"size": (512, 512), "type": "ui_elements", "batch_size": 4}
]
```

### 2. Quality Control Pipeline
```python
def quality_assessment(image_path):
    """Automated quality scoring"""
    # Check for:
    # - Egyptian style consistency
    # - Detail level
    # - Color palette adherence
    # - Composition quality
    return quality_score
```

### 3. Performance Optimization
- **Pre-load models** to avoid reload time
- **Use VRAM-optimized settings** for continuous generation
- **Implement queue system** for batch processing
- **Auto-save intermediate results**

## Expected Performance

With RTX 5070 + 32GB RAM:

| Model | Resolution | Time per Image | Batch Size |
|-------|------------|----------------|------------|
| SDXL Base | 1024x1024 | 20-25s | 2-3 |
| SDXL + LoRA | 768x1024 | 15-20s | 3-4 |
| Flux.1 Dev | 1024x1024 | 45-60s | 1-2 |
| RealVisXL | 768x768 | 12-18s | 4-6 |

**Daily Generation Capacity:** 500-800 high-quality images

## Next Steps

1. **Choose your preferred interface** (ComfyUI recommended for power users)
2. **Download base models** (~6GB each)
3. **Train custom LoRA** using your 75 Egyptian training images
4. **Test generation pipeline** with sample cards
5. **Integrate with game asset system**

Your hardware is perfectly suited for professional AI art generation at scale! 🚀