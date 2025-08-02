"""
Content Validation Tool

Validates YAML content files for the Sands of Duat project,
ensuring data integrity and catching configuration errors.

Key Features:
- YAML schema validation
- Content cross-reference checking
- Balance validation for game mechanics
- Automated testing integration
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    level: ValidationLevel
    message: str
    file_path: Optional[Path] = None
    item_id: Optional[str] = None
    field: Optional[str] = None


class ContentValidator:
    """
    Validates YAML content files for game data integrity.
    
    Ensures that all content meets the required schemas and
    maintains consistency across the game's data files.
    """
    
    def __init__(self, content_root: Optional[Path] = None):
        self.content_root = content_root or Path(__file__).parent.parent / "content"
        self.logger = logging.getLogger(__name__)
        self.results: List[ValidationResult] = []
    
    def validate_all_content(self) -> List[ValidationResult]:
        """Validate all content in the content directory."""
        self.results.clear()
        
        # Validate each content type
        self.validate_cards()
        self.validate_enemies() 
        self.validate_events()
        self.validate_decks()
        
        # Cross-reference validation
        self.validate_cross_references()
        
        return self.results
    
    def validate_cards(self) -> None:
        """Validate all card definitions."""
        cards_dir = self.content_root / "cards"
        if not cards_dir.exists():
            self._add_result(ValidationLevel.WARNING, "Cards directory not found", cards_dir)
            return
        
        for yaml_file in cards_dir.glob("*.yaml"):
            self._validate_yaml_file(yaml_file, self._validate_card_data)
    
    def validate_enemies(self) -> None:
        """Validate all enemy definitions."""
        enemies_dir = self.content_root / "enemies"
        if not enemies_dir.exists():
            self._add_result(ValidationLevel.WARNING, "Enemies directory not found", enemies_dir)
            return
        
        for yaml_file in enemies_dir.glob("*.yaml"):
            self._validate_yaml_file(yaml_file, self._validate_enemy_data)
    
    def validate_events(self) -> None:
        """Validate all event definitions."""
        events_dir = self.content_root / "events"
        if not events_dir.exists():
            self._add_result(ValidationLevel.WARNING, "Events directory not found", events_dir)
            return
        
        for yaml_file in events_dir.glob("*.yaml"):
            self._validate_yaml_file(yaml_file, self._validate_event_data)
    
    def validate_decks(self) -> None:
        """Validate all deck definitions."""
        decks_dir = self.content_root / "decks"
        if not decks_dir.exists():
            self._add_result(ValidationLevel.WARNING, "Decks directory not found", decks_dir)
            return
        
        for yaml_file in decks_dir.glob("*.yaml"):
            self._validate_yaml_file(yaml_file, self._validate_deck_data)
    
    def _validate_yaml_file(self, file_path: Path, validator_func) -> None:
        """Validate a single YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                self._add_result(ValidationLevel.WARNING, "Empty YAML file", file_path)
                return
            
            for item_id, item_data in data.items():
                validator_func(item_id, item_data, file_path)
        
        except yaml.YAMLError as e:
            self._add_result(ValidationLevel.ERROR, f"YAML parsing error: {e}", file_path)
        except Exception as e:
            self._add_result(ValidationLevel.ERROR, f"Unexpected error: {e}", file_path)
    
    def _validate_card_data(self, card_id: str, card_data: Dict[str, Any], file_path: Path) -> None:
        """Validate a single card definition."""
        required_fields = ['id', 'name', 'description', 'sand_cost', 'card_type']
        
        # Check required fields
        for field in required_fields:
            if field not in card_data:
                self._add_result(
                    ValidationLevel.ERROR,
                    f"Missing required field: {field}",
                    file_path, card_id, field
                )
        
        # Validate sand cost
        sand_cost = card_data.get('sand_cost')
        if sand_cost is not None:
            if not isinstance(sand_cost, int) or not 0 <= sand_cost <= 6:
                self._add_result(
                    ValidationLevel.ERROR,
                    f"Invalid sand_cost: {sand_cost}. Must be integer 0-6",
                    file_path, card_id, 'sand_cost'
                )
        
        # Validate card type
        valid_types = ['attack', 'skill', 'power', 'curse', 'status']
        card_type = card_data.get('card_type')
        if card_type and card_type not in valid_types:
            self._add_result(
                ValidationLevel.ERROR,
                f"Invalid card_type: {card_type}. Must be one of {valid_types}",
                file_path, card_id, 'card_type'
            )
        
        # Validate rarity
        valid_rarities = ['common', 'uncommon', 'rare', 'legendary']
        rarity = card_data.get('rarity')
        if rarity and rarity not in valid_rarities:
            self._add_result(
                ValidationLevel.WARNING,
                f"Invalid rarity: {rarity}. Should be one of {valid_rarities}",
                file_path, card_id, 'rarity'
            )
        
        # Validate effects
        effects = card_data.get('effects', [])
        if isinstance(effects, list):
            for i, effect in enumerate(effects):
                self._validate_card_effect(effect, file_path, card_id, f'effects[{i}]')
    
    def _validate_card_effect(self, effect: Dict[str, Any], file_path: Path, 
                             card_id: str, field_path: str) -> None:
        """Validate a card effect definition."""
        if not isinstance(effect, dict):
            self._add_result(
                ValidationLevel.ERROR,
                "Effect must be a dictionary",
                file_path, card_id, field_path
            )
            return
        
        # Required effect fields
        if 'effect_type' not in effect:
            self._add_result(
                ValidationLevel.ERROR,
                "Effect missing effect_type",
                file_path, card_id, f'{field_path}.effect_type'
            )
        
        # Validate effect types
        valid_effect_types = [
            'damage', 'heal', 'block', 'draw_cards', 'gain_sand', 
            'buff', 'debuff', 'transform', 'discover'
        ]
        effect_type = effect.get('effect_type')
        if effect_type and effect_type not in valid_effect_types:
            self._add_result(
                ValidationLevel.ERROR,
                f"Invalid effect_type: {effect_type}",
                file_path, card_id, f'{field_path}.effect_type'
            )
    
    def _validate_enemy_data(self, enemy_id: str, enemy_data: Dict[str, Any], file_path: Path) -> None:
        """Validate a single enemy definition."""
        required_fields = ['id', 'name', 'health', 'max_sand']
        
        # Check required fields
        for field in required_fields:
            if field not in enemy_data:
                self._add_result(
                    ValidationLevel.ERROR,
                    f"Missing required field: {field}",
                    file_path, enemy_id, field
                )
        
        # Validate health
        health = enemy_data.get('health')
        if health is not None and (not isinstance(health, int) or health <= 0):
            self._add_result(
                ValidationLevel.ERROR,
                f"Invalid health: {health}. Must be positive integer",
                file_path, enemy_id, 'health'
            )
        
        # Validate max_sand
        max_sand = enemy_data.get('max_sand')
        if max_sand is not None and (not isinstance(max_sand, int) or not 1 <= max_sand <= 6):
            self._add_result(
                ValidationLevel.ERROR,
                f"Invalid max_sand: {max_sand}. Must be integer 1-6",
                file_path, enemy_id, 'max_sand'
            )
        
        # Validate abilities
        abilities = enemy_data.get('abilities', [])
        if isinstance(abilities, list):
            for i, ability in enumerate(abilities):
                self._validate_enemy_ability(ability, file_path, enemy_id, f'abilities[{i}]')
    
    def _validate_enemy_ability(self, ability: Dict[str, Any], file_path: Path,
                               enemy_id: str, field_path: str) -> None:
        """Validate an enemy ability definition."""
        if not isinstance(ability, dict):
            self._add_result(
                ValidationLevel.ERROR,
                "Ability must be a dictionary",
                file_path, enemy_id, field_path
            )
            return
        
        required_fields = ['name', 'sand_cost']
        for field in required_fields:
            if field not in ability:
                self._add_result(
                    ValidationLevel.ERROR,
                    f"Ability missing {field}",
                    file_path, enemy_id, f'{field_path}.{field}'
                )
    
    def _validate_event_data(self, event_id: str, event_data: Dict[str, Any], file_path: Path) -> None:
        """Validate a single event definition."""
        required_fields = ['id', 'name', 'description', 'options']
        
        for field in required_fields:
            if field not in event_data:
                self._add_result(
                    ValidationLevel.ERROR,
                    f"Missing required field: {field}",
                    file_path, event_id, field
                )
        
        # Validate options
        options = event_data.get('options', [])
        if not isinstance(options, list) or len(options) == 0:
            self._add_result(
                ValidationLevel.ERROR,
                "Event must have at least one option",
                file_path, event_id, 'options'
            )
    
    def _validate_deck_data(self, deck_id: str, deck_data: Dict[str, Any], file_path: Path) -> None:
        """Validate a single deck definition."""
        required_fields = ['id', 'name', 'cards']
        
        for field in required_fields:
            if field not in deck_data:
                self._add_result(
                    ValidationLevel.ERROR,
                    f"Missing required field: {field}",
                    file_path, deck_id, field
                )
        
        # Validate cards list
        cards = deck_data.get('cards', [])
        if not isinstance(cards, list) or len(cards) == 0:
            self._add_result(
                ValidationLevel.ERROR,
                "Deck must have at least one card",
                file_path, deck_id, 'cards'
            )
        
        # Validate individual card entries
        for i, card_entry in enumerate(cards):
            if isinstance(card_entry, dict):
                if 'card_id' not in card_entry:
                    self._add_result(
                        ValidationLevel.ERROR,
                        "Card entry missing card_id",
                        file_path, deck_id, f'cards[{i}].card_id'
                    )
    
    def validate_cross_references(self) -> None:
        """Validate cross-references between content types."""
        # Load all content for cross-reference checking
        all_cards = self._load_all_content("cards")
        all_decks = self._load_all_content("decks")
        
        # Check that deck cards reference valid card IDs
        for deck_file, decks in all_decks.items():
            for deck_id, deck_data in decks.items():
                cards = deck_data.get('cards', [])
                for card_entry in cards:
                    if isinstance(card_entry, dict):
                        card_id = card_entry.get('card_id')
                        if card_id and not self._card_exists(card_id, all_cards):
                            self._add_result(
                                ValidationLevel.ERROR,
                                f"Deck references non-existent card: {card_id}",
                                deck_file, deck_id
                            )
    
    def _load_all_content(self, content_type: str) -> Dict[Path, Dict[str, Any]]:
        """Load all content of a specific type."""
        content_dir = self.content_root / content_type
        all_content = {}
        
        if content_dir.exists():
            for yaml_file in content_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            all_content[yaml_file] = data
                except Exception as e:
                    self.logger.error(f"Error loading {yaml_file}: {e}")
        
        return all_content
    
    def _card_exists(self, card_id: str, all_cards: Dict[Path, Dict[str, Any]]) -> bool:
        """Check if a card ID exists in the loaded cards."""
        for cards_data in all_cards.values():
            if card_id in cards_data:
                return True
        return False
    
    def _add_result(self, level: ValidationLevel, message: str, 
                   file_path: Optional[Path] = None, item_id: Optional[str] = None,
                   field: Optional[str] = None) -> None:
        """Add a validation result."""
        result = ValidationResult(
            level=level,
            message=message,
            file_path=file_path,
            item_id=item_id,
            field=field
        )
        self.results.append(result)
    
    def get_error_count(self) -> int:
        """Get the number of validation errors."""
        return len([r for r in self.results if r.level == ValidationLevel.ERROR])
    
    def get_warning_count(self) -> int:
        """Get the number of validation warnings."""
        return len([r for r in self.results if r.level == ValidationLevel.WARNING])
    
    def print_results(self) -> None:
        """Print validation results to console."""
        errors = [r for r in self.results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in self.results if r.level == ValidationLevel.WARNING]
        
        if errors:
            print(f"\n❌ {len(errors)} Errors found:")
            for result in errors:
                print(f"  {self._format_result(result)}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} Warnings found:")
            for result in warnings:
                print(f"  {self._format_result(result)}")
        
        if not errors and not warnings:
            print("✅ All content validation passed!")
    
    def _format_result(self, result: ValidationResult) -> str:
        """Format a validation result for display."""
        parts = [result.message]
        
        if result.file_path:
            parts.append(f"in {result.file_path.name}")
        
        if result.item_id:
            parts.append(f"({result.item_id})")
        
        if result.field:
            parts.append(f"field: {result.field}")
        
        return " ".join(parts)


# CLI interface for content validation
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate content for Sands of Duat")
    parser.add_argument("--content-dir", type=Path, help="Content directory to validate")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    validator = ContentValidator(args.content_dir)
    results = validator.validate_all_content()
    
    if args.json:
        # Output as JSON for CI/CD integration
        json_results = []
        for result in results:
            json_results.append({
                "level": result.level.value,
                "message": result.message,
                "file": str(result.file_path) if result.file_path else None,
                "item_id": result.item_id,
                "field": result.field
            })
        print(json.dumps(json_results, indent=2))
    else:
        # Human-readable output
        validator.print_results()
    
    # Exit with error code if validation failed
    if validator.get_error_count() > 0:
        exit(1)