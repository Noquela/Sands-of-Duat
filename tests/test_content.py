"""
Content Validation Tests

Tests for YAML content loading, validation, and hot-reload functionality.
"""

import unittest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, Mock

from content.loader import ContentLoader, ContentType
from content.validator import ContentValidator
from content.hot_reload import HotReloadManager


class ContentLoaderTestCase(unittest.TestCase):
    """Test cases for content loading functionality."""
    
    def setUp(self):
        """Set up test fixtures with temporary directories."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.content_root = Path(self.temp_dir.name)
        self.loader = ContentLoader(self.content_root)
        
        # Create content subdirectories
        for content_type in ContentType:
            (self.content_root / content_type.value).mkdir(exist_ok=True)
    
    def tearDown(self):
        """Clean up temporary directories."""
        self.temp_dir.cleanup()
    
    def test_load_yaml_file(self):
        """Test loading individual YAML files."""
        # Create test YAML file
        test_data = {
            "test_card": {
                "id": "test_card",
                "name": "Test Card",
                "sand_cost": 2,
                "card_type": "attack"
            }
        }
        
        yaml_file = self.content_root / "test.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(test_data, f)
        
        # Load the file
        loaded_data = self.loader.load_yaml_file(yaml_file)
        self.assertEqual(loaded_data, test_data)
    
    def test_load_invalid_yaml(self):
        """Test handling of invalid YAML files."""
        # Create invalid YAML file
        yaml_file = self.content_root / "invalid.yaml"
        with open(yaml_file, 'w') as f:
            f.write("invalid: yaml: content: {\n")  # Malformed YAML
        
        # Should return None for invalid YAML
        loaded_data = self.loader.load_yaml_file(yaml_file)
        self.assertIsNone(loaded_data)
    
    def test_load_nonexistent_file(self):
        """Test handling of nonexistent files."""
        nonexistent = self.content_root / "nonexistent.yaml"
        loaded_data = self.loader.load_yaml_file(nonexistent)
        self.assertIsNone(loaded_data)
    
    def test_load_content_directory(self):
        """Test loading all content from a directory."""
        cards_dir = self.content_root / "cards"
        
        # Create test card files
        card1_data = {
            "card1": {
                "id": "card1",
                "name": "First Card",
                "sand_cost": 1
            }
        }
        
        card2_data = {
            "card2": {
                "id": "card2", 
                "name": "Second Card",
                "sand_cost": 2
            }
        }
        
        with open(cards_dir / "basic_cards.yaml", 'w') as f:
            yaml.dump(card1_data, f)
        
        with open(cards_dir / "advanced_cards.yml", 'w') as f:
            yaml.dump(card2_data, f)
        
        # Load directory content
        content = self.loader.load_content_directory(ContentType.CARDS)
        
        self.assertIn("basic_cards", content)
        self.assertIn("advanced_cards", content)
        self.assertEqual(content["basic_cards"], card1_data)
        self.assertEqual(content["advanced_cards"], card2_data)
    
    def test_get_content_with_caching(self):
        """Test content retrieval with caching."""
        cards_dir = self.content_root / "cards"
        test_data = {"test": {"id": "test"}}
        
        with open(cards_dir / "test.yaml", 'w') as f:
            yaml.dump(test_data, f)
        
        # First call should load from disk
        content1 = self.loader.get_content(ContentType.CARDS)
        
        # Second call should use cache
        content2 = self.loader.get_content(ContentType.CARDS)
        
        self.assertEqual(content1, content2)
        self.assertIs(content1, content2)  # Same object reference
    
    def test_reload_content(self):
        """Test content reloading."""
        cards_dir = self.content_root / "cards"
        test_file = cards_dir / "test.yaml"
        
        # Create initial content
        initial_data = {"test": {"value": "initial"}}
        with open(test_file, 'w') as f:
            yaml.dump(initial_data, f)
        
        content = self.loader.get_content(ContentType.CARDS)
        self.assertEqual(content["test"]["test"]["value"], "initial")
        
        # Modify content
        modified_data = {"test": {"value": "modified"}}
        with open(test_file, 'w') as f:
            yaml.dump(modified_data, f)
        
        # Reload should get new content
        content = self.loader.get_content(ContentType.CARDS, reload=True)
        self.assertEqual(content["test"]["test"]["value"], "modified")
    
    def test_get_content_item(self):
        """Test retrieving specific content items."""
        cards_dir = self.content_root / "cards"
        test_data = {
            "fireball": {"id": "fireball", "name": "Fireball"},
            "heal": {"id": "heal", "name": "Heal"}
        }
        
        with open(cards_dir / "spells.yaml", 'w') as f:
            yaml.dump(test_data, f)
        
        # Get specific item
        fireball = self.loader.get_content_item(ContentType.CARDS, "fireball")
        self.assertIsNotNone(fireball)
        self.assertEqual(fireball["id"], "fireball")
        
        # Get nonexistent item
        nonexistent = self.loader.get_content_item(ContentType.CARDS, "nonexistent")
        self.assertIsNone(nonexistent)


class ContentValidatorTestCase(unittest.TestCase):
    """Test cases for content validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.content_root = Path(self.temp_dir.name)
        self.validator = ContentValidator(self.content_root)
        
        # Create content subdirectories
        for content_type in ContentType:
            (self.content_root / content_type.value).mkdir(exist_ok=True)
    
    def tearDown(self):
        """Clean up temporary directories."""
        self.temp_dir.cleanup()
    
    def test_validate_valid_card(self):
        """Test validation of valid card data."""
        valid_card = {
            "id": "fireball",
            "name": "Fireball",
            "description": "Deal damage to an enemy",
            "sand_cost": 3,
            "card_type": "attack",
            "rarity": "common",
            "effects": [
                {
                    "effect_type": "damage",
                    "value": 12,
                    "target": "enemy"
                }
            ]
        }
        
        # Should pass validation
        result = self.validator._validate_card_data("fireball", valid_card, Path("test.yaml"))
        
        # Check that no errors were added
        errors = [r for r in self.validator.results if r.level.value == "error"]
        self.assertEqual(len(errors), 0)
    
    def test_validate_invalid_card(self):
        """Test validation of invalid card data."""
        invalid_card = {
            "name": "Invalid Card",
            # Missing required fields: id, description, sand_cost, card_type
            "sand_cost": 10,  # Invalid range
            "card_type": "invalid_type",  # Invalid type
            "rarity": "invalid_rarity"  # Invalid rarity
        }
        
        self.validator.results.clear()
        self.validator._validate_card_data("invalid", invalid_card, Path("test.yaml"))
        
        # Should have multiple errors
        errors = [r for r in self.validator.results if r.level.value == "error"]
        self.assertGreater(len(errors), 0)
        
        # Check for specific error types
        error_messages = [r.message for r in errors]
        self.assertTrue(any("Missing required field: id" in msg for msg in error_messages))
        self.assertTrue(any("Invalid sand_cost" in msg for msg in error_messages))
    
    def test_validate_enemy_data(self):
        """Test enemy data validation."""
        valid_enemy = {
            "id": "goblin",
            "name": "Goblin",
            "health": 30,
            "max_sand": 4,
            "abilities": [
                {
                    "name": "Strike",
                    "sand_cost": 1,
                    "effects": []
                }
            ]
        }
        
        self.validator.results.clear()
        self.validator._validate_enemy_data("goblin", valid_enemy, Path("test.yaml"))
        
        errors = [r for r in self.validator.results if r.level.value == "error"]
        self.assertEqual(len(errors), 0)
    
    def test_validate_event_data(self):
        """Test event data validation."""
        valid_event = {
            "id": "shrine",
            "name": "Ancient Shrine",
            "description": "You find an ancient shrine",
            "options": [
                {
                    "text": "Pray at the shrine",
                    "effects": []
                }
            ]
        }
        
        self.validator.results.clear()
        self.validator._validate_event_data("shrine", valid_event, Path("test.yaml"))
        
        errors = [r for r in self.validator.results if r.level.value == "error"]
        self.assertEqual(len(errors), 0)
    
    def test_validate_deck_data(self):
        """Test deck data validation."""
        valid_deck = {
            "id": "starter",
            "name": "Starter Deck",
            "cards": [
                {"card_id": "strike", "count": 4},
                {"card_id": "defend", "count": 3}
            ]
        }
        
        self.validator.results.clear()
        self.validator._validate_deck_data("starter", valid_deck, Path("test.yaml"))
        
        errors = [r for r in self.validator.results if r.level.value == "error"]
        self.assertEqual(len(errors), 0)
    
    def test_cross_reference_validation(self):
        """Test cross-reference validation between content types."""
        # Create card content
        cards_dir = self.content_root / "cards"
        card_data = {
            "strike": {
                "id": "strike",
                "name": "Strike",
                "description": "Basic attack",
                "sand_cost": 1,
                "card_type": "attack"
            }
        }
        with open(cards_dir / "basic.yaml", 'w') as f:
            yaml.dump(card_data, f)
        
        # Create deck content that references cards
        decks_dir = self.content_root / "decks"
        deck_data = {
            "starter": {
                "id": "starter",
                "name": "Starter Deck",
                "cards": [
                    {"card_id": "strike", "count": 4},
                    {"card_id": "nonexistent", "count": 2}  # Invalid reference
                ]
            }
        }
        with open(decks_dir / "starter.yaml", 'w') as f:
            yaml.dump(deck_data, f)
        
        # Run validation
        results = self.validator.validate_all_content()
        
        # Should have error for nonexistent card reference
        errors = [r for r in results if r.level.value == "error"]
        error_messages = [r.message for r in errors]
        self.assertTrue(any("references non-existent card: nonexistent" in msg for msg in error_messages))
    
    def test_validation_result_counts(self):
        """Test validation result counting."""
        # Add some mock results
        from content.validator import ValidationResult, ValidationLevel
        
        self.validator.results = [
            ValidationResult(ValidationLevel.ERROR, "Test error 1"),
            ValidationResult(ValidationLevel.ERROR, "Test error 2"),
            ValidationResult(ValidationLevel.WARNING, "Test warning 1"),
            ValidationResult(ValidationLevel.INFO, "Test info 1")
        ]
        
        self.assertEqual(self.validator.get_error_count(), 2)
        self.assertEqual(self.validator.get_warning_count(), 1)


class HotReloadTestCase(unittest.TestCase):
    """Test cases for hot reload functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.content_root = Path(self.temp_dir.name)
        
        # Create mock content loader
        self.loader = Mock()
        self.loader.content_root = self.content_root
        
        self.hot_reload = HotReloadManager(self.loader)
        
        # Create content subdirectories
        for content_type in ContentType:
            (self.content_root / content_type.value).mkdir(exist_ok=True)
    
    def tearDown(self):
        """Clean up temporary directories."""
        if self.hot_reload.is_watching:
            self.hot_reload.stop_watching()
        self.temp_dir.cleanup()
    
    def test_callback_registration(self):
        """Test registering and unregistering callbacks."""
        callback = Mock()
        
        self.hot_reload.register_reload_callback("test", callback)
        self.assertIn("test", self.hot_reload.reload_callbacks)
        
        self.hot_reload.unregister_reload_callback("test")
        self.assertNotIn("test", self.hot_reload.reload_callbacks)
    
    def test_content_type_detection(self):
        """Test detecting content type from file path."""
        cards_file = self.content_root / "cards" / "test.yaml"
        enemies_file = self.content_root / "enemies" / "test.yaml"
        
        cards_type = self.hot_reload._get_content_type_from_path(cards_file)
        enemies_type = self.hot_reload._get_content_type_from_path(enemies_file)
        
        self.assertEqual(cards_type, ContentType.CARDS)
        self.assertEqual(enemies_type, ContentType.ENEMIES)
        
        # Non-content file should return None
        other_file = self.content_root / "other" / "test.yaml"
        other_type = self.hot_reload._get_content_type_from_path(other_file)
        self.assertIsNone(other_type)
    
    @patch('content.hot_reload.Observer')
    def test_start_stop_watching(self, mock_observer):
        """Test starting and stopping file watching."""
        mock_observer_instance = Mock()
        mock_observer.return_value = mock_observer_instance
        
        # Create new manager with mocked observer
        hot_reload = HotReloadManager(self.loader)
        hot_reload.observer = mock_observer_instance
        
        # Test starting
        hot_reload.start_watching()
        self.assertTrue(hot_reload.is_watching)
        mock_observer_instance.start.assert_called_once()
        
        # Test stopping
        hot_reload.stop_watching()
        self.assertFalse(hot_reload.is_watching)
        mock_observer_instance.stop.assert_called_once()
        mock_observer_instance.join.assert_called_once()
    
    def test_file_change_handling(self):
        """Test handling file change events."""
        callback = Mock()
        self.hot_reload.register_reload_callback("test", callback)
        
        # Create a test file
        cards_dir = self.content_root / "cards"
        test_file = cards_dir / "test.yaml"
        
        # Simulate file change
        self.hot_reload._on_file_changed(test_file)
        
        # Should reload content and call callback
        self.loader.load_content_directory.assert_called_once_with(ContentType.CARDS)
        callback.assert_called_once()


if __name__ == '__main__':
    unittest.main()