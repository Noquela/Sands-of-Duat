#!/usr/bin/env python3
"""
TEST FLUX.1 DEV GENERATION - YOUR FIRST HADES-QUALITY EGYPTIAN ART!
Generate one amazing card to test the system with your RTX 5070.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_single_legendary_card():
    """Generate Ra - Sun God (Legendary) - the most epic card!"""
    
    try:
        print("="*60)
        print("TESTING FLUX.1 DEV FOR HADES-QUALITY EGYPTIAN ART")
        print("="*60)
        print("Target: RA - SUN GOD (Legendary Card)")
        print("Hardware: RTX 5070 + 32GB RAM")
        print("Model: Flux.1 Dev (BEST available)")
        print("Expected: Supergiant Games Hades-level quality")
        print("="*60)
        
        from sands_of_duat.ai_art import get_ai_generator
        from sands_of_duat.ai_art.asset_validator import get_asset_validator
        from sands_of_duat.ai_art.asset_manager import get_asset_manager
        
        # Get systems
        ai_gen = get_ai_generator()
        validator = get_asset_validator()
        manager = get_asset_manager()
        
        print("\nGenerating RA - SUN GOD with Flux.1 Dev...")
        print("This will take 45-60 seconds for OUTSTANDING quality!")
        print()
        
        # Generate the most epic card
        result = ai_gen.generate_card_art(
            card_name="Ra - Sun God",
            card_type="god",
            rarity="legendary"
        )
        
        if result.success:
            print(f"SUCCESS: {result.image_path}")
            print(f"Generation time: {result.generation_time:.1f}s")
            print(f"Quality score: {result.quality_score:.2f}")
            print()
            
            # Validate for Hades quality
            print("Validating for Hades-level quality...")
            validation = validator.validate_asset(result.image_path)
            
            if validation.passed:
                print("HADES QUALITY ACHIEVED!")
                print(f"Overall score: {validation.overall_score:.2f}/1.00")
                
                # Register and approve
                asset_id = manager.register_generated_asset(
                    result.image_path,
                    {
                        'category': 'card_art',
                        'subcategory': 'god',
                        'model': 'flux_dev',
                        'prompt': result.request.base_prompt,
                        'card_name': 'Ra - Sun God',
                        'rarity': 'legendary'
                    },
                    validation
                )
                
                approved = manager.approve_asset_for_game(asset_id)
                if approved:
                    print("ASSET APPROVED FOR GAME!")
                
            else:
                print("Quality improvements needed:")
                for issue in validation.issues:
                    print(f"  - {issue}")
                    
            # Show memory usage
            if result.model_metadata:
                mem = result.model_metadata
                print(f"\nVRAM Usage: {mem.get('allocated_gb', 0):.1f}GB / {mem.get('total_vram_gb', 12):.1f}GB")
            
        else:
            print(f"GENERATION FAILED: {result.error_message}")
            print("This might be the first run - model download can take time!")
        
        print("\n" + "="*60)
        print("FLUX.1 DEV TEST COMPLETE")
        print("="*60)
        
        return result
        
    except Exception as e:
        print(f"ERROR: {e}")
        print("Make sure you have CUDA drivers and enough VRAM!")
        return None

if __name__ == "__main__":
    test_single_legendary_card()