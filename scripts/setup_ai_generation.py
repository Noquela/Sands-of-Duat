"""
Setup script for local AI animation generation
Installs required dependencies for Stable Diffusion + AnimateDiff
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def check_gpu():
    """Check if CUDA is available."""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"🎮 GPU detected: {gpu_name}")
            print(f"🎮 CUDA version: {torch.version.cuda}")
            return True
        else:
            print("⚠️ No CUDA GPU detected - will use CPU (very slow)")
            return False
    except ImportError:
        print("⚠️ PyTorch not installed yet")
        return False

def install_pytorch():
    """Install PyTorch with CUDA support."""
    print("Installing PyTorch with CUDA support...")
    
    # For RTX 5070, install latest PyTorch with CUDA 12.1
    pytorch_cmd = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
    
    return run_command(pytorch_cmd, "Installing PyTorch with CUDA 12.1")

def install_diffusers():
    """Install diffusers library and dependencies."""
    diffusers_packages = [
        "diffusers[torch]",
        "transformers", 
        "accelerate",
        "xformers",  # For memory optimization
        "safetensors"
    ]
    
    for package in diffusers_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    
    return True

def install_optional_packages():
    """Install optional packages for better performance."""
    optional_packages = [
        "opencv-python",  # For video processing
        "imageio[ffmpeg]",  # For GIF creation
        "pillow-simd"  # Faster image processing
    ]
    
    for package in optional_packages:
        run_command(f"pip install {package}", f"Installing {package} (optional)")

def download_models():
    """Pre-download models to avoid delays during generation."""
    print("\n🔄 Pre-downloading AI models...")
    
    download_script = '''
import torch
from diffusers import StableDiffusionPipeline, AnimateDiffPipeline, MotionAdapter

print("Downloading Stable Diffusion v1.5...")
sd_pipeline = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    safety_checker=None,
    requires_safety_checker=False
)
print("✅ Stable Diffusion downloaded")

print("Downloading AnimateDiff motion adapter...")
adapter = MotionAdapter.from_pretrained(
    "guoyww/animatediff-motion-adapter-v1-5-2", 
    torch_dtype=torch.float16
)
print("✅ AnimateDiff adapter downloaded")

print("Models downloaded successfully!")
'''
    
    with open("temp_download.py", "w") as f:
        f.write(download_script)
    
    success = run_command("python temp_download.py", "Downloading AI models")
    
    # Cleanup
    if os.path.exists("temp_download.py"):
        os.remove("temp_download.py")
    
    return success

def main():
    """Main setup function."""
    print("🏺 Setting up Local AI Animation Generation")
    print("=" * 60)
    
    # Check current environment
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️ Not in virtual environment - recommend using venv")
    
    # Install PyTorch first
    if not install_pytorch():
        print("❌ Failed to install PyTorch - aborting setup")
        return False
    
    # Check GPU after PyTorch installation
    gpu_available = check_gpu()
    
    # Install diffusers and dependencies
    if not install_diffusers():
        print("❌ Failed to install diffusers - aborting setup")
        return False
    
    # Install optional packages
    install_optional_packages()
    
    # Pre-download models
    if gpu_available:
        print("\n🤖 Would you like to pre-download AI models? (This will take ~10GB of disk space)")
        response = input("Download models now? (y/N): ").strip().lower()
        if response == 'y':
            if download_models():
                print("✅ Models downloaded successfully!")
            else:
                print("⚠️ Model download failed - models will be downloaded during first use")
    
    # Create models directory
    models_dir = Path("models/ai")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("🎉 AI Animation Generation Setup Complete!")
    print("="*60)
    print("\nTo generate animations, run:")
    print("python src/sands_of_duat/animation/local_ai_generator.py")
    
    if gpu_available:
        print(f"\n🎮 GPU acceleration enabled - generation will be fast!")
    else:
        print(f"\n⚠️ CPU mode - generation will be very slow (consider getting a GPU)")
    
    print("\nRecommended workflow:")
    print("1. Run the AI generator to create animated cards")
    print("2. Generated animations will be saved to assets/animations/ai_generated/")
    print("3. The game will automatically use AI-generated animations when available")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        raise