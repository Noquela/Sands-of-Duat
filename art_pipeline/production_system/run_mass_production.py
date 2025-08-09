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
    
    return input("\nSelect option: ").strip()

def show_status():
    """Show current production status."""
    print("\nCURRENT PRODUCTION STATUS")
    print("=" * 25)
    
    # Look for assets in common directories
    asset_dirs = ["assets", "generated_assets", "leonardo_assets", "comfy_output", "fooocus_output"]
    total_found = 0
    
    for dir_name in asset_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            png_count = len(list(dir_path.rglob("*.png")))
            if png_count > 0:
                print(f"{dir_name}: {png_count} PNG files")
                total_found += png_count
    
    target = 64
    completion = total_found / target * 100
    
    print(f"\nOVERALL STATUS:")
    print(f"Generated: {total_found}/{target} assets ({completion:.1f}%)")
    
    if total_found >= target:
        print("🎉 PRODUCTION COMPLETE!")
        print("Next: Run quality control")
    elif total_found > 0:
        remaining = target - total_found
        print(f"⚡ IN PROGRESS - {remaining} more needed")
    else:
        print("⏳ NOT STARTED - Choose production method")

def show_production_guide():
    """Show production guide."""
    print("\nPRODUCTION GUIDE")
    print("=" * 16)
    
    guide_text = """
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
    
    print("FASE 5 - MASS PRODUCTION SYSTEM READY!")
    print("=" * 42)
    print("64 Hades-Egyptian assets target")
    print("Multiple generation methods available")
    print("Quality control automation included")
    print()
    
    while True:
        choice = show_main_menu()
        
        if choice == "0":
            print("Production system closed.")
            break
        elif choice == "6":
            show_status()
        elif choice == "8":
            show_production_guide()
        else:
            print(f"Method {choice} ready for implementation!")
            print("Check the following files:")
            print("- comfyui_mass_production.py (automated)")
            print("- leonardo_ai_mass_production.py (premium)")  
            print("- fooocus_mass_production_guide.md (manual)")
            print("- mass_production_qc.py (quality control)")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()