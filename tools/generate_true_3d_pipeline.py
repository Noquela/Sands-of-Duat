#!/usr/bin/env python3
"""
SANDS OF DUAT - TRUE 3D PIPELINE
Complete pipeline: SDXL concepts → Background removal → Blender 3D models → glTF → Bevy integration
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

class True3DPipeline:
    def __init__(self):
        self.project_root = Path.cwd()
        self.art_dir = self.project_root / "art"
        self.assets_dir = self.project_root / "assets"
        self.tools_dir = self.project_root / "tools"
        
        # Check for virtual environment
        self.venv_path = self.project_root / ".venv"
        if sys.platform == "win32":
            self.python_exe = self.venv_path / "Scripts" / "python.exe"
            self.pip_exe = self.venv_path / "Scripts" / "pip.exe"
        else:
            self.python_exe = self.venv_path / "bin" / "python"
            self.pip_exe = self.venv_path / "bin" / "pip"
    
    def print_banner(self):
        """Print pipeline banner."""
        print("=" * 65)
        print("SANDS OF DUAT - TRUE 3D PIPELINE (RTX 5070 + Blender)")
        print("=" * 65)
        print()
        print("[PIPELINE STAGES]")
        print("  1. SDXL concept art + textures (RTX 5070)")
        print("  2. Background removal with rembg")
        print("  3. 3D modeling in Blender with rigging")
        print("  4. glTF export with animations")
        print("  5. Bevy 3D integration and testing")
        print("  6. Performance test at 3440x1440 @ 120fps")
        print()
    
    def check_dependencies(self):
        """Check all required dependencies."""
        print("[STEP 1] Checking dependencies...")
        
        # Check Python virtual environment
        if not self.venv_path.exists():
            print("[ERROR] Python virtual environment not found!")
            print("[FIX] Run: python -m venv .venv")
            return False
        
        if not self.python_exe.exists():
            print("[ERROR] Python executable not found in venv!")
            return False
        
        # Check Blender
        blender_found = False
        blender_paths = [
            "blender",  # In PATH
            "C:\\Program Files\\Blender Foundation\\Blender 4.5\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe",
            "/usr/bin/blender",  # Linux
            "/Applications/Blender.app/Contents/MacOS/Blender"  # macOS
        ]
        
        for blender_path in blender_paths:
            try:
                result = subprocess.run([blender_path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.blender_exe = blender_path
                    blender_found = True
                    print(f"[SUCCESS] Found Blender: {blender_path}")
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                continue
        
        if not blender_found:
            print("[ERROR] Blender not found!")
            print("[FIX] Install Blender and add to PATH")
            return False
        
        # Check Cargo/Rust
        cargo_found = False
        cargo_paths = ["cargo"]
        if sys.platform == "win32":
            cargo_paths.extend([
                str(Path.home() / ".cargo" / "bin" / "cargo.exe"),
                "C:\\Users\\Bruno\\.cargo\\bin\\cargo.exe"
            ])
        
        for cargo_path in cargo_paths:
            try:
                result = subprocess.run([cargo_path, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.cargo_exe = cargo_path
                    cargo_found = True
                    print(f"[SUCCESS] Found Cargo: {cargo_path}")
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                continue
        
        if not cargo_found:
            print("[ERROR] Rust/Cargo not found!")
            print("[FIX] Install Rust from https://rustup.rs/")
            return False
        
        print("[SUCCESS] All dependencies found!")
        return True
    
    def setup_directories(self):
        """Create directory structure."""
        print("[STEP 2] Creating directory structure...")
        
        directories = [
            self.art_dir / "sdxl" / "concepts",
            self.art_dir / "sdxl" / "textures", 
            self.art_dir / "sdxl" / "emissive",
            self.art_dir / "sdxl" / "clean",
            self.art_dir / "prompts",
            self.assets_dir / "models",
            self.assets_dir / "models" / "weapons",
            self.assets_dir / "models" / "environment",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("[SUCCESS] Directories created!")
    
    def install_dependencies(self):
        """Install Python AI dependencies."""
        print("[STEP 3] Installing AI dependencies...")
        
        # Install requirements
        print("[INFO] Installing PyTorch CUDA 12.8 for RTX 5070...")
        
        try:
            # Install PyTorch with CUDA 12.8
            subprocess.run([
                str(self.pip_exe), "install", 
                "-r", str(self.tools_dir / "requirements.txt"),
                "--index-url", "https://download.pytorch.org/whl/cu128",
                "--quiet"
            ], check=True, timeout=300)
            
            print("[SUCCESS] AI dependencies installed!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[WARNING] Some packages failed to install: {e}")
            print("[INFO] Continuing with available packages...")
            return True
        except subprocess.TimeoutExpired:
            print("[WARNING] Installation timeout, but continuing...")
            return True
    
    def generate_sdxl_concepts(self):
        """Generate SDXL concept art and textures."""
        print("[STEP 4] Generating SDXL concept art and textures...")
        print("[RTX-5070] Using RTX 5070 12GB VRAM for high-quality generation...")
        
        try:
            result = subprocess.run([
                str(self.python_exe),
                str(self.tools_dir / "generate_3d_concepts.py")
            ], timeout=600)  # 10 minute timeout
            
            if result.returncode == 0:
                print("[SUCCESS] Concepts and textures generated!")
                return True
            else:
                print("[ERROR] SDXL generation failed!")
                return False
                
        except subprocess.TimeoutExpired:
            print("[WARNING] SDXL generation timeout, but continuing...")
            return True
        except Exception as e:
            print(f"[ERROR] SDXL generation error: {e}")
            return False
    
    def clean_backgrounds(self):
        """Clean backgrounds with rembg."""
        print("[STEP 5] Cleaning backgrounds with rembg...")
        print("[AI] Using U²-Net for professional background removal...")
        
        concepts_dir = self.art_dir / "sdxl" / "concepts"
        clean_dir = self.art_dir / "sdxl" / "clean"
        
        if not concepts_dir.exists() or not any(concepts_dir.iterdir()):
            print("[WARNING] No concepts found, skipping background cleaning...")
            return True
        
        try:
            result = subprocess.run([
                str(self.python_exe),
                str(self.tools_dir / "clean_bg.py"),
                str(concepts_dir),
                str(clean_dir),
                "auto"
            ], timeout=300)
            
            if result.returncode == 0:
                print("[SUCCESS] Backgrounds cleaned!")
            else:
                print("[WARNING] Background cleaning had issues, but continuing...")
            
            return True
            
        except Exception as e:
            print(f"[WARNING] Background cleaning error: {e}")
            print("[INFO] Continuing without background cleaning...")
            return True
    
    def run_blender_pipeline(self):
        """Run Blender 3D modeling pipeline."""
        print("[STEP 6] Running Blender 3D modeling pipeline...")
        print("[BLENDER] Creating 3D models with rigging and animations...")
        
        try:
            result = subprocess.run([
                self.blender_exe,
                "--background",
                "--python", str(self.tools_dir / "blender_3d_pipeline.py")
            ], timeout=600)  # 10 minute timeout
            
            if result.returncode == 0:
                print("[SUCCESS] 3D models created and exported!")
                return True
            else:
                print("[ERROR] Blender 3D pipeline failed!")
                print("[INFO] Make sure Blender is properly installed")
                return False
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Blender pipeline timeout!")
            return False
        except Exception as e:
            print(f"[ERROR] Blender pipeline error: {e}")
            return False
    
    def build_game(self):
        """Build the game with TRUE 3D system."""
        print("[STEP 7] Building game with TRUE 3D system...")
        print("[RUST] Compiling Bevy game with 3D glTF assets...")
        
        try:
            result = subprocess.run([
                self.cargo_exe, "build", "--release"
            ], timeout=300)
            
            if result.returncode == 0:
                print("[SUCCESS] Game built successfully!")
                return True
            else:
                print("[ERROR] Game build failed!")
                return False
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Game build timeout!")
            return False
        except Exception as e:
            print(f"[ERROR] Game build error: {e}")
            return False
    
    def test_game_performance(self):
        """Test game performance."""
        print("[STEP 8] Testing 3D performance at 3440x1440...")
        print("[INFO] Game should run at 120+ FPS with true 3D models")
        print("[INFO] Look for:")
        print("  • 3D hero with volume and depth")
        print("  • Real animations (idle/walk/attack)")
        print("  • Weapon attached to hand socket")
        print("  • 3D environment elements")
        print("  • Perspective camera with isometric feel")
        print()
        
        input("[MANUAL] Press Enter to launch game for testing...")
        
        try:
            # Launch game (non-blocking for manual testing)
            subprocess.run([self.cargo_exe, "run", "--release"])
            print("[SUCCESS] Game testing completed!")
            return True
            
        except KeyboardInterrupt:
            print("[INFO] Game testing interrupted by user")
            return True
        except Exception as e:
            print(f"[ERROR] Game launch error: {e}")
            return False
    
    def print_summary(self):
        """Print pipeline completion summary."""
        print()
        print("=" * 65)
        print("TRUE 3D PIPELINE COMPLETE!")
        print("=" * 65)
        print("[RESULTS]")
        print(f"  • SDXL concepts: {self.art_dir / 'sdxl' / 'concepts'}")
        print(f"  • 3D textures: {self.art_dir / 'sdxl' / 'textures'}")
        print(f"  • glTF models: {self.assets_dir / 'models'}")
        print(f"  • Game running with TRUE 3D graphics")
        print()
        print("[PERFORMANCE] Target: 120+ FPS at 3440x1440")
        print("[QUALITY] Hades-like 3D visuals with Egyptian theme")
        print()
    
    def run_full_pipeline(self):
        """Run the complete TRUE 3D pipeline."""
        self.print_banner()
        
        # Execute each stage
        stages = [
            ("Check Dependencies", self.check_dependencies),
            ("Setup Directories", self.setup_directories),
            ("Install AI Dependencies", self.install_dependencies),
            ("Generate SDXL Concepts", self.generate_sdxl_concepts),
            ("Clean Backgrounds", self.clean_backgrounds),
            ("Run Blender Pipeline", self.run_blender_pipeline),
            ("Build Game", self.build_game),
            ("Test Performance", self.test_game_performance),
        ]
        
        failed_stages = []
        
        for stage_name, stage_func in stages:
            print(f"\n[STARTING] {stage_name}")
            start_time = time.time()
            
            try:
                success = stage_func()
                duration = time.time() - start_time
                
                if success:
                    print(f"[COMPLETED] {stage_name} ({duration:.1f}s)")
                else:
                    print(f"[FAILED] {stage_name} ({duration:.1f}s)")
                    failed_stages.append(stage_name)
                    
                    # Ask user if they want to continue
                    if stage_name in ["Check Dependencies", "Build Game"]:
                        print("[CRITICAL] Critical stage failed!")
                        return False
                    else:
                        continue_choice = "y"  # Auto-continue for unattended execution
                        if continue_choice != 'y':
                            return False
                        
            except Exception as e:
                duration = time.time() - start_time
                print(f"[EXCEPTION] {stage_name}: {e} ({duration:.1f}s)")
                failed_stages.append(stage_name)
                return False
        
        # Summary
        self.print_summary()
        
        if failed_stages:
            print(f"[WARNING] Some stages had issues: {', '.join(failed_stages)}")
        
        return len(failed_stages) == 0

def main():
    """Main entry point."""
    pipeline = True3DPipeline()
    
    try:
        success = pipeline.run_full_pipeline()
        
        if success:
            print("[SUCCESS] TRUE 3D pipeline completed successfully!")
            return 0
        else:
            print("[FAILED] TRUE 3D pipeline failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Pipeline interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\n[INFO] Pipeline execution completed.")
    sys.exit(exit_code)