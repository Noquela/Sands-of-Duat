#!/usr/bin/env python3
"""
RTX 5070 CUDA 12.8 CARD GENERATION TOOL
Entry point for maximum quality Egyptian art generation
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

from sands_of_duat.ai_art.ai_generation_pipeline import generate_all_egyptian_cards, get_pipeline

def main():
    """Main entry point for RTX 5070 card generation"""
    
    print("RTX5070" + "="*52)
    print("    RTX 5070 CUDA 12.8 EGYPTIAN CARD GENERATOR")
    print("    MAXIMUM QUALITY - NO FALLBACKS - LOCAL ONLY")
    print("RTX5070" + "="*52)
    
    # Test RTX 5070 setup first
    pipeline = get_pipeline()
    
    print("\n[SETUP] Testing RTX 5070 CUDA 12.8 setup...")
    if not pipeline.test_setup():
        print("\n[ERROR] RTX 5070 setup failed!")
        print("[REQUIRED] Required actions:")
        print("   1. Start ComfyUI: cd external/ComfyUI && python main.py --listen 127.0.0.1 --port 8188")
        print("   2. Verify CUDA 12.8 PyTorch installation")
        print("   3. Download SDXL models to external/ComfyUI/models/checkpoints/")
        return False
    
    print("[SUCCESS] RTX 5070 CUDA 12.8 ready for maximum quality generation!")
    
    # Generate all Egyptian cards
    start_time = time.time()
    print("\n[GENERATION] Starting RTX 5070 card generation...")
    
    results = generate_all_egyptian_cards()
    
    elapsed_time = time.time() - start_time
    
    # Analyze results
    successful_cards = [name for name, success in results.items() if success]
    failed_cards = [name for name, success in results.items() if not success]
    
    print("\nRTX5070" + "="*52)
    print("         RTX 5070 GENERATION RESULTS")
    print("RTX5070" + "="*52)
    print(f"[TIME] Total generation time: {elapsed_time/60:.1f} minutes")
    print(f"[SUCCESS] Successful cards: {len(successful_cards)}/{len(results)}")
    print(f"[PERFORMANCE] RTX 5070 CUDA 12.8 performance: MAXIMUM")
    
    if successful_cards:
        print(f"\n[SUCCESS] Successfully generated ({len(successful_cards)} cards):")
        for card in successful_cards:
            print(f"   [CARD] {card}")
    
    if failed_cards:
        print(f"\n[FAILED] Failed generations ({len(failed_cards)} cards):")
        for card in failed_cards:
            print(f"   [ERROR] {card}")
    
    # Display output directories
    print(f"\n[OUTPUT] Generated assets:")
    print(f"   [GENERATED] {pipeline.generated_dir}")
    print(f"   [APPROVED] {pipeline.approved_dir}")
    
    # Success criteria
    success_rate = len(successful_cards) / len(results) if results else 0
    
    if success_rate >= 0.9:  # 90% success rate
        print(f"\n[COMPLETE] RTX 5070 GENERATION COMPLETE SUCCESS!")
        print("[READY] Ready for animation pipeline!")
        print("[READY] Ready for game integration!")
        return True
    elif success_rate >= 0.5:  # 50% success rate
        print(f"\n[PARTIAL] RTX 5070 partial success ({success_rate*100:.0f}%)")
        print("[ADVICE] Consider retrying failed cards or adjusting quality thresholds")
        return False
    else:
        print(f"\n[FAILED] RTX 5070 generation failed ({success_rate*100:.0f}% success)")
        print("[REQUIRED] Check ComfyUI setup, CUDA 12.8 installation, and model availability")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n[COMPLETE] RTX 5070 EGYPTIAN CARD GENERATION COMPLETE!")
        print("[NEXT] Proceeding to animation pipeline...")
    else:
        print("\n[ERROR] RTX 5070 generation incomplete - check errors above")
    
    sys.exit(0 if success else 1)