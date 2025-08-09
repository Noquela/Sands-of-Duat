"""
Direct Ra Card Generation Script
Generates the Ra - Sun God card with Hades-level quality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sands_of_duat.ai_art.ai_generation_pipeline import AIArtGenerator
from sands_of_duat.ai_art.asset_validator import HadesQualityValidator

def generate_ra_card():
    print("GENERATING RA - SUN GOD WITH HADES-LEVEL QUALITY")
    print("=" * 60)
    
    # Initialize systems
    try:
        generator = AIArtGenerator()
        validator = HadesQualityValidator()
        
        print("AI generator initialized")
        print("Asset validator ready")
        
        # Ra card info (hardcoded for direct generation)
        ra_card = {
            'name': 'Ra - Sun God',
            'description': 'The mighty sun deity commands solar energy to incinerate foes',
            'type': 'legendary'
        }
        
        print(f"Generating: {ra_card['name']}")
        print(f"Description: {ra_card['description']}")
        
        # Generate Ra artwork
        print("\nStarting Ra artwork generation...")
        
        # Generate using the AI generator method
        result = generator.generate_card_art(
            card_name="Ra - Sun God", 
            card_type="attack",
            rarity="legendary"
        )
        
        if result.success:
            print(f"Ra artwork generated: {result.output_path}")
            
            # Validate the generated asset
            validation_result = validator.validate_asset(result.output_path)
            
            if validation_result.passes_hades_quality:
                print("RA CARD PASSES HADES-LEVEL QUALITY!")
                print(f"Artistic Score: {validation_result.artistic_score:.2f}/1.0")
                return True
            else:
                print("Generated art needs improvement")
                print(f"Artistic Score: {validation_result.artistic_score:.2f}/1.0") 
                return False
        else:
            print(f"Generation failed: {result.error}")
            return False
            
    except Exception as e:
        print(f"Error during generation: {e}")
        return False

if __name__ == "__main__":
    success = generate_ra_card()
    if success:
        print("\nRA - SUN GOD SUCCESSFULLY GENERATED!")
    else:
        print("\nRa generation failed")