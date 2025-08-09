
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
            self.status = {
                "phase": "planning",
                "total_assets": 64,
                "completed": 0,
                "approved": 0, 
                "rejected": 0,
                "in_review": 0,
                "current_batch": None,
                "start_time": None,
                "estimated_completion": None
            }
    
    def save_status(self):
        """Save current status to file."""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)
    
    def show_main_menu(self):
        """Display main coordination menu."""
        print("MASTER GENERATION COORDINATOR")
        print("=" * 30)
        print(f"Status: {self.status['phase'].upper()}")
        print(f"Progress: {self.status['completed']}/{self.status['total_assets']} assets")
        print(f"Approved: {self.status['approved']}")
        print(f"Rejected: {self.status['rejected']}")
        print(f"In Review: {self.status['in_review']}")
        print()
        print("ACTIONS:")
        print("1. Start generation process")
        print("2. Check generation status") 
        print("3. Run quality control")
        print("4. Generate final report")
        print("5. Show generation guides")
        print("0. Exit")
        
        return input("\nSelect action: ").strip()
    
    def start_generation_process(self):
        """Start the generation process."""
        print("\nSTARTING GENERATION PROCESS")
        print("=" * 28)
        
        # Update status
        self.status["phase"] = "generating"
        self.status["start_time"] = datetime.now().isoformat()
        self.save_status()
        
        print("Generation process initiated!")
        print("\nAVAILABLE METHODS:")
        print("1. ComfyUI (Recommended for batch)")
        print("2. Automatic1111 (Good for customization)")
        print("3. Fooocus (Easiest to use)")
        print("4. Online Services (Leonardo AI, Midjourney, etc.)")
        
        method = input("\nSelect method (1-4): ").strip()
        
        if method == "1":
            print("\nComfyUI Guide:")
            print("1. Open ComfyUI")
            print("2. Load the batch script: comfyui_batch_generation.py")
            print("3. Execute batch generation")
            print("4. Images will be saved automatically")
        
        elif method == "2":
            print("\nAutomatic1111 Guide:")
            print("1. Start A1111 with --api flag")
            print("2. Run: python automatic1111_batch.py")
            print("3. Or use run_automatic1111_batch.bat")
        
        elif method == "3":
            print("\nFooocus Guide:")
            print("1. Open fooocus_generation_guide.md")
            print("2. Follow step-by-step instructions")
            print("3. Generate images manually with provided prompts")
        
        elif method == "4":
            print("\nOnline Services Guide:")
            print("1. Open online_services_guide.md")
            print("2. Choose your preferred service")
            print("3. Use provided prompts for batch generation")
        
        print("\nAfter generation, run quality control to validate assets!")
        
    def check_generation_status(self):
        """Check current generation status."""
        print("\nGENERATION STATUS")
        print("=" * 17)
        
        # Scan for generated images
        generated_count = 0
        for img_dir in self.base_dir.rglob("*.png"):
            if "hades" in img_dir.name.lower() or "egyptian" in img_dir.name.lower():
                generated_count += 1
        
        self.status["completed"] = generated_count
        self.save_status()
        
        print(f"Phase: {self.status['phase'].upper()}")
        print(f"Total Target: {self.status['total_assets']} assets")
        print(f"Generated: {generated_count} images found")
        print(f"Progress: {(generated_count/self.status['total_assets']*100):.1f}%")
        
        if self.status["start_time"]:
            start = datetime.fromisoformat(self.status["start_time"])
            elapsed = (datetime.now() - start).total_seconds() / 3600
            print(f"Time Elapsed: {elapsed:.1f} hours")
            
            if generated_count > 0:
                rate = generated_count / elapsed
                remaining = self.status['total_assets'] - generated_count
                eta = remaining / rate if rate > 0 else 0
                print(f"ETA: {eta:.1f} hours remaining")
        
        print(f"Quality Status:")
        print(f"  Approved: {self.status['approved']}")
        print(f"  Rejected: {self.status['rejected']}")
        print(f"  In Review: {self.status['in_review']}")
    
    def run_quality_control(self):
        """Run quality control on generated images."""
        print("\nRUNNING QUALITY CONTROL")
        print("=" * 23)
        
        # This would integrate with quality_control_system.py
        print("Execute: python quality_control_system.py")
        print("Or run automated scan of generated_assets/ directory")
        
        # Update status based on QC results
        self.status["phase"] = "quality_control"
        self.save_status()
    
    def generate_final_report(self):
        """Generate final comprehensive report."""
        print("\nGENERATING FINAL REPORT")
        print("=" * 22)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": "Hades-Egyptian Asset Generation",
            "phase": "FASE 4 - Sistema Geração Inteligente",
            "status": self.status,
            "summary": {
                "total_planned": self.status["total_assets"],
                "total_generated": self.status["completed"],
                "completion_rate": self.status["completed"] / self.status["total_assets"] * 100,
                "quality_rate": self.status["approved"] / max(self.status["completed"], 1) * 100
            }
        }
        
        report_file = self.base_dir / "final_generation_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Final report generated: {report_file}")
        
        # Generate human-readable summary
        summary = f"""
FINAL GENERATION REPORT - HADES EGYPTIAN ASSETS
===============================================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PROJECT STATUS:
- Phase: {report["phase"]}
- Total Planned: {report["summary"]["total_planned"]} assets
- Total Generated: {report["summary"]["total_generated"]} assets  
- Completion Rate: {report["summary"]["completion_rate"]:.1f}%
- Quality Rate: {report["summary"]["quality_rate"]:.1f}%

ASSET BREAKDOWN:
- Legendary (Deities): 5 characters × 4 variations = 20 assets
- Epic (Heroes): 3 characters × 4 variations = 12 assets
- Epic (Environments): 3 scenes × 4 variations = 12 assets  
- Rare (Creatures): 4 creatures × 4 variations = 16 assets
- Common (UI): 1 element × 4 variations = 4 assets

QUALITY CONTROL:
- Approved: {self.status["approved"]} assets
- Rejected: {self.status["rejected"]} assets
- In Review: {self.status["in_review"]} assets

NEXT STEPS:
- Complete any remaining generation
- Finalize quality control
- Prepare for FASE 5 (Production)
"""
        
        summary_file = self.base_dir / "generation_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(summary)
        print(f"Summary saved: {summary_file}")
    
    def show_generation_guides(self):
        """Show available generation guides."""
        print("\nGENERATION GUIDES")
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
            print(f"{exists} {name}: {filename}")
    
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
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    coordinator = MasterCoordinator()
    coordinator.run()
