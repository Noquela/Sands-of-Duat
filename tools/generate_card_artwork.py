#!/usr/bin/env python3
"""
SANDS OF DUAT - CARD ARTWORK BATCH GENERATOR
============================================

Automated tool for generating professional artwork for all Egyptian cards.
Integrates with the AI generation pipeline to create consistent, high-quality assets.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sands_of_duat.cards.egyptian_cards import get_deck_builder, CardType, CardRarity
from sands_of_duat.ai_art import get_ai_generator, ArtCategory, AIModel, ArtStyle
from sands_of_duat.ai_art.asset_validator import get_asset_validator

class CardArtworkGenerator:
    """
    Professional card artwork generation system.
    """
    
    def __init__(self):
        self.deck_builder = get_deck_builder()
        self.ai_generator = get_ai_generator()
        self.asset_validator = get_asset_validator()
        self.all_cards = self.deck_builder.get_all_cards()
        
        print("🏺 Card Artwork Generator initialized - HADES QUALITY EGYPTIAN ART")
        print(f"📋 Found {len(self.all_cards)} cards to generate artwork for")
        print("🎨 Targeting Supergiant Games Hades-level artistic excellence")
    
    def generate_all_card_art(self):
        """Generate artwork for all Egyptian cards."""
        
        print("\n=== GENERATING ARTWORK FOR ALL CARDS ===")
        
        # Prepare card information for batch generation
        card_batch = []
        for card in self.all_cards:
            card_info = {
                'name': card.name,
                'type': card.card_type.value,
                'rarity': card.rarity.value,
                'description': card.description
            }
            card_batch.append(card_info)
        
        # Generate artwork with Hades-quality validation
        print("🎨 Generating artwork with Hades-level quality validation...")
        results = self.ai_generator.batch_generate_cards(card_batch)
        
        # Validate all generated assets for Hades-quality
        print("\n🔍 Validating assets for Hades-level artistic excellence...")
        generated_assets = [r.image_path for r in results if r.success and r.image_path]
        
        if generated_assets:
            validation_results = self.asset_validator.batch_validate_assets(generated_assets)
            validation_report = self.asset_validator.generate_validation_report(validation_results)
            
            # Enhanced results reporting
            successful_gen = sum(1 for r in results if r.success)
            failed_gen = len(results) - successful_gen
            hades_quality_passed = sum(1 for r in validation_results if r.passed)
            
            print(f"\n=== HADES-QUALITY GENERATION COMPLETE ===")
            print(f"🎨 Generated: {successful_gen}/{len(results)} ({successful_gen/len(results)*100:.1f}%)")
            print(f"✨ Hades Quality: {hades_quality_passed}/{len(validation_results)} ({validation_report['summary']['pass_rate']:.1f}%)")
            print(f"🏆 Overall Score: {validation_report['summary']['average_score']:.2f}/1.00")
            
            # Show quality breakdown
            print(f"\n📊 QUALITY BREAKDOWN:")
            for metric, score in validation_report['score_breakdown'].items():
                print(f"  {metric.replace('_', ' ').title()}: {score:.2f}")
            
            # Show common issues if any
            if validation_report['common_issues']:
                print(f"\n⚠️  COMMON ISSUES:")
                for issue, count in validation_report['common_issues'][:3]:
                    print(f"  • {issue} ({count} assets)")
        else:
            print("❌ No assets generated successfully to validate")
        
        # Export detailed report
        report_path = self.ai_generator.export_generation_report("hades_quality_card_generation.json")
        print(f"📄 Detailed report: {report_path}")
        
        return results
    
    def generate_card_by_type(self, card_type: CardType):
        """Generate artwork for cards of specific type."""
        
        type_cards = self.deck_builder.get_cards_by_type(card_type)
        
        print(f"\n=== GENERATING {card_type.value.upper()} CARD ARTWORK ===")
        print(f"Found {len(type_cards)} {card_type.value} cards")
        
        results = []
        for card in type_cards:
            print(f"\nGenerating: {card.name}")
            result = self.ai_generator.generate_card_art(
                card.name,
                card.card_type.value,
                card.rarity.value
            )
            results.append(result)
        
        successful = sum(1 for r in results if r.success)
        print(f"\n{card_type.value.title()} cards complete: {successful}/{len(results)}")
        
        return results
    
    def generate_backgrounds(self):
        """Generate all game background artwork."""
        
        print("\n=== GENERATING BACKGROUND ARTWORK ===")
        
        backgrounds = [
            "main_menu",
            "combat", 
            "deck_builder",
            "collection",
            "settings",
            "victory",
            "defeat"
        ]
        
        results = []
        for bg_type in backgrounds:
            print(f"\nGenerating background: {bg_type}")
            result = self.ai_generator.generate_background_art(bg_type)
            results.append(result)
        
        successful = sum(1 for r in results if r.success)
        print(f"\nBackground generation complete: {successful}/{len(results)}")
        
        return results
    
    def generate_priority_cards(self):
        """Generate artwork for highest priority cards first."""
        
        print("\n=== GENERATING PRIORITY CARD ARTWORK ===")
        
        # Focus on legendary and rare cards first
        legendary_cards = self.deck_builder.get_cards_by_rarity(CardRarity.LEGENDARY)
        rare_cards = self.deck_builder.get_cards_by_rarity(CardRarity.RARE)
        
        priority_cards = legendary_cards + rare_cards
        
        print(f"Generating {len(priority_cards)} priority cards")
        
        results = []
        for card in priority_cards:
            print(f"\nPriority card: {card.name} ({card.rarity.value})")
            result = self.ai_generator.generate_card_art(
                card.name,
                card.card_type.value, 
                card.rarity.value
            )
            results.append(result)
        
        successful = sum(1 for r in results if r.success)
        print(f"\nPriority generation complete: {successful}/{len(results)}")
        
        return results
    
    def show_card_catalog(self):
        """Display catalog of all available cards."""
        
        print("\n=== EGYPTIAN CARD CATALOG ===")
        
        for card_type in CardType:
            type_cards = self.deck_builder.get_cards_by_type(card_type)
            print(f"\n{card_type.value.upper()} CARDS ({len(type_cards)}):")
            
            for card in type_cards:
                rarity_symbol = {
                    CardRarity.COMMON: "⚪",
                    CardRarity.UNCOMMON: "🔵", 
                    CardRarity.RARE: "🟡",
                    CardRarity.LEGENDARY: "🔴"
                }[card.rarity]
                
                stats = ""
                if card.card_type in [CardType.GOD, CardType.CREATURE]:
                    stats = f" ({card.stats.attack}/{card.stats.health})"
                
                print(f"  {rarity_symbol} {card.name}{stats} - {card.stats.cost} cost")
        
        print(f"\nTotal cards: {len(self.all_cards)}")
    
    def test_single_card(self, card_name: str):
        """Test generation for a single card by name."""
        
        # Find the card
        target_card = None
        for card in self.all_cards:
            if card.name.lower() == card_name.lower():
                target_card = card
                break
        
        if not target_card:
            print(f"❌ Card not found: {card_name}")
            available_cards = [card.name for card in self.all_cards]
            print(f"Available cards: {available_cards}")
            return None
        
        print(f"\n=== TESTING SINGLE CARD GENERATION ===")
        print(f"Card: {target_card.name}")
        print(f"Type: {target_card.card_type.value}")
        print(f"Rarity: {target_card.rarity.value}")
        print(f"Description: {target_card.description}")
        
        result = self.ai_generator.generate_card_art(
            target_card.name,
            target_card.card_type.value,
            target_card.rarity.value
        )
        
        if result.success:
            print(f"✅ Generation successful: {result.image_path}")
            print(f"📊 Quality score: {result.quality_score:.2f}")
        else:
            print(f"❌ Generation failed: {result.error_message}")
        
        return result
    
    def validate_existing_assets(self, asset_directory: str = "assets/generated_art"):
        """Validate existing assets for Hades-quality standards."""
        
        from pathlib import Path
        
        asset_dir = Path(asset_directory)
        if not asset_dir.exists():
            print(f"❌ Asset directory not found: {asset_directory}")
            return
        
        # Find all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        asset_files = []
        
        for ext in image_extensions:
            asset_files.extend(asset_dir.glob(f"*{ext}"))
        
        if not asset_files:
            print(f"❌ No image assets found in {asset_directory}")
            return
        
        print(f"\n🔍 VALIDATING {len(asset_files)} EXISTING ASSETS FOR HADES-QUALITY")
        
        # Validate assets
        asset_paths = [str(f) for f in asset_files]
        validation_results = self.asset_validator.batch_validate_assets(asset_paths)
        validation_report = self.asset_validator.generate_validation_report(validation_results)
        
        # Show results
        print(f"\n=== VALIDATION RESULTS ===")
        print(f"✨ Hades Quality Passed: {validation_report['summary']['passed_assets']}/{validation_report['summary']['total_assets']}")
        print(f"🏆 Average Quality Score: {validation_report['summary']['average_score']:.2f}/1.00")
        print(f"📈 Pass Rate: {validation_report['summary']['pass_rate']:.1f}%")
        
        # Quality breakdown
        print(f"\n📊 QUALITY METRICS:")
        for metric, score in validation_report['score_breakdown'].items():
            status = "✅" if score >= 0.75 else "⚠️" if score >= 0.5 else "❌"
            print(f"  {status} {metric.replace('_', ' ').title()}: {score:.2f}")
        
        # Show failed assets for improvement
        failed_assets = [r for r in validation_results if not r.passed]
        if failed_assets:
            print(f"\n❌ ASSETS NEEDING IMPROVEMENT ({len(failed_assets)}):")
            for result in failed_assets[:5]:  # Show first 5
                asset_name = Path(result.asset_path).name
                print(f"  • {asset_name} (Score: {result.overall_score:.2f})")
                for issue in result.issues[:2]:  # Show top 2 issues
                    print(f"    - {issue}")
        
        return validation_results

def main():
    """Main execution function with interactive menu."""
    
    generator = CardArtworkGenerator()
    
    while True:
        print("\n" + "="*60)
        print("🏺 SANDS OF DUAT - HADES-QUALITY CARD ARTWORK GENERATOR")
        print("="*60)
        print("🎨 GENERATION:")
        print("1. Generate ALL card artwork (with validation)")
        print("2. Generate priority cards (Legendary + Rare)")
        print("3. Generate by card type")
        print("4. Generate backgrounds")
        print("5. Test single card")
        print("🔍 VALIDATION:")
        print("6. Validate existing assets")
        print("7. Show card catalog")
        print("0. Exit")
        
        choice = input("\nSelect option (0-7): ").strip()
        
        if choice == "0":
            print("🏺 Artwork generation complete!")
            break
            
        elif choice == "1":
            generator.generate_all_card_art()
            
        elif choice == "2":
            generator.generate_priority_cards()
            
        elif choice == "3":
            print("\nCard Types:")
            for i, card_type in enumerate(CardType, 1):
                print(f"{i}. {card_type.value.title()}")
            
            type_choice = input("Select type (1-5): ").strip()
            try:
                type_index = int(type_choice) - 1
                selected_type = list(CardType)[type_index]
                generator.generate_card_by_type(selected_type)
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                
        elif choice == "4":
            generator.generate_backgrounds()
            
        elif choice == "5":
            card_name = input("Enter card name: ").strip()
            generator.test_single_card(card_name)
            
        elif choice == "6":
            asset_dir = input("Enter asset directory (or press Enter for 'assets/generated_art'): ").strip()
            if not asset_dir:
                asset_dir = "assets/generated_art"
            generator.validate_existing_assets(asset_dir)
            
        elif choice == "7":
            generator.show_card_catalog()
            
        else:
            print("❌ Invalid option")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()