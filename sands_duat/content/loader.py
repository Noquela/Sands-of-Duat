"""
Content Loader

Handles loading and parsing of YAML content files with validation
and error handling for the game's data-driven content pipeline.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import logging


class ContentType(Enum):
    """Types of content that can be loaded."""
    CARDS = "cards"
    ENEMIES = "enemies"
    EVENTS = "events"
    DECKS = "decks"


class ContentLoader:
    """
    Loads and manages YAML-based game content.
    
    Provides methods to load content from files and directories,
    with built-in validation and error handling.
    """
    
    def __init__(self, content_root: Optional[Path] = None):
        self.content_root = content_root or Path(__file__).parent
        self.logger = logging.getLogger(__name__)
        self._content_cache: Dict[ContentType, Dict[str, Any]] = {}
    
    def load_yaml_file(self, file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Load a single YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            self.logger.error(f"Content file not found: {file_path}")
            return None
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error in {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error loading {file_path}: {e}")
            return None
    
    def load_content_directory(self, content_type: ContentType) -> Dict[str, Any]:
        """Load all YAML files from a content directory."""
        directory = self.content_root / content_type.value
        content = {}
        
        if not directory.exists():
            self.logger.warning(f"Content directory does not exist: {directory}")
            return content
        
        for file_path in directory.glob("*.yaml"):
            file_content = self.load_yaml_file(file_path)
            if file_content:
                file_key = file_path.stem
                content[file_key] = file_content
                self.logger.info(f"Loaded {content_type.value}: {file_key}")
        
        for file_path in directory.glob("*.yml"):
            file_content = self.load_yaml_file(file_path)
            if file_content:
                file_key = file_path.stem
                content[file_key] = file_content
                self.logger.info(f"Loaded {content_type.value}: {file_key}")
        
        self._content_cache[content_type] = content
        return content
    
    def get_content(self, content_type: ContentType, reload: bool = False) -> Dict[str, Any]:
        """Get content by type, optionally reloading from disk."""
        if reload or content_type not in self._content_cache:
            return self.load_content_directory(content_type)
        return self._content_cache[content_type]
    
    def get_content_item(self, content_type: ContentType, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific content item by ID."""
        content = self.get_content(content_type)
        return content.get(item_id)
    
    def reload_all_content(self) -> None:
        """Reload all cached content from disk."""
        for content_type in ContentType:
            self.load_content_directory(content_type)
    
    def clear_cache(self) -> None:
        """Clear the content cache."""
        self._content_cache.clear()