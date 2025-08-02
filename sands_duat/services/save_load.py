"""
Save/Load Management Service

Handles game state persistence with versioning, compression,
and integrity checking.

Features:
- JSON-based save format with compression
- Save file versioning and migration
- Integrity checking with checksums
- Automatic backup management
- Cloud save integration ready
"""

import json
import gzip
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from dataclasses import dataclass, asdict
import shutil


@dataclass
class SaveMetadata:
    """Metadata for save files."""
    version: str
    created_at: str
    modified_at: str
    game_version: str
    checksum: str
    player_name: str
    floor: int
    playtime_seconds: float


class SaveLoadManager:
    """
    Manages game state persistence with versioning and integrity.
    """
    
    def __init__(self, save_dir: Path = Path("saves")):
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_version = "1.0.0"
        self.game_version = "0.1.0"  # Sands of Duat version
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Save manager initialized - Directory: {save_dir}")
    
    def save_game(self, 
                  game_state: Dict[str, Any], 
                  slot_name: str = "quicksave",
                  compress: bool = True) -> bool:
        """
        Save game state to file.
        
        Args:
            game_state: Complete game state dictionary
            slot_name: Save slot name
            compress: Whether to compress the save file
        
        Returns:
            True if save successful, False otherwise
        """
        try:
            save_file = self.save_dir / f"{slot_name}.sav"
            backup_file = self.save_dir / f"{slot_name}.bak"
            
            # Create backup of existing save
            if save_file.exists():
                shutil.copy2(save_file, backup_file)
            
            # Prepare save data
            save_data = {
                'metadata': self._create_metadata(game_state),
                'game_state': game_state
            }
            
            # Serialize to JSON
            json_data = json.dumps(save_data, indent=2, default=str)
            
            # Calculate checksum
            checksum = hashlib.sha256(json_data.encode()).hexdigest()
            save_data['metadata']['checksum'] = checksum
            
            # Re-serialize with checksum
            final_json = json.dumps(save_data, indent=2, default=str)
            
            # Write to file (compressed or uncompressed)
            if compress:
                with gzip.open(save_file, 'wt', encoding='utf-8') as f:
                    f.write(final_json)
            else:
                save_file.write_text(final_json, encoding='utf-8')
            
            self.logger.info(f"Game saved to {save_file} (compressed: {compress})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save game: {e}")
            
            # Restore backup if save failed
            if backup_file.exists() and save_file.exists():
                try:
                    shutil.copy2(backup_file, save_file)
                    self.logger.info("Restored backup after failed save")
                except Exception as restore_error:
                    self.logger.error(f"Failed to restore backup: {restore_error}")
            
            return False
    
    def load_game(self, slot_name: str = "quicksave") -> Optional[Dict[str, Any]]:
        """
        Load game state from file.
        
        Args:
            slot_name: Save slot name
        
        Returns:
            Game state dictionary or None if load failed
        """
        save_file = self.save_dir / f"{slot_name}.sav"
        
        if not save_file.exists():
            self.logger.warning(f"Save file not found: {save_file}")
            return None
        
        try:
            # Try to load as compressed file first
            try:
                with gzip.open(save_file, 'rt', encoding='utf-8') as f:
                    save_data = json.load(f)
            except (gzip.BadGzipFile, UnicodeDecodeError):
                # Fall back to uncompressed
                save_data = json.loads(save_file.read_text(encoding='utf-8'))
            
            # Verify integrity
            if not self._verify_integrity(save_data):
                self.logger.error("Save file integrity check failed")
                return None
            
            # Check version compatibility
            metadata = SaveMetadata(**save_data['metadata'])
            if not self._is_version_compatible(metadata.version):
                self.logger.error(f"Incompatible save version: {metadata.version}")
                return None
            
            # Migrate if necessary
            game_state = self._migrate_save_data(save_data['game_state'], metadata.version)
            
            self.logger.info(f"Game loaded from {save_file}")
            return game_state
            
        except Exception as e:
            self.logger.error(f"Failed to load game: {e}")
            return None
    
    def list_saves(self) -> List[Dict[str, Any]]:
        """
        List all available save files with metadata.
        
        Returns:
            List of save file information
        """
        saves = []
        
        for save_file in self.save_dir.glob("*.sav"):
            try:
                # Quick metadata extraction
                metadata = self._extract_metadata(save_file)
                if metadata:
                    saves.append({
                        'slot_name': save_file.stem,
                        'file_path': save_file,
                        'file_size_mb': save_file.stat().st_size / (1024 * 1024),
                        'metadata': metadata
                    })
            except Exception as e:
                self.logger.warning(f"Failed to read save metadata {save_file}: {e}")
        
        # Sort by modification time (newest first)
        saves.sort(key=lambda x: x['metadata']['modified_at'], reverse=True)
        
        return saves
    
    def delete_save(self, slot_name: str) -> bool:
        """
        Delete a save file.
        
        Args:
            slot_name: Save slot name
        
        Returns:
            True if deletion successful
        """
        save_file = self.save_dir / f"{slot_name}.sav"
        backup_file = self.save_dir / f"{slot_name}.bak"
        
        try:
            if save_file.exists():
                save_file.unlink()
                self.logger.info(f"Deleted save file: {save_file}")
            
            if backup_file.exists():
                backup_file.unlink()
                self.logger.info(f"Deleted backup file: {backup_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete save {slot_name}: {e}")
            return False
    
    def _create_metadata(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Create metadata for a save file."""
        now = datetime.now().isoformat()
        
        metadata = SaveMetadata(
            version=self.current_version,
            created_at=now,
            modified_at=now,
            game_version=self.game_version,
            checksum="",  # Will be filled later
            player_name=game_state.get('player_name', 'Unknown'),
            floor=game_state.get('floor', 1),
            playtime_seconds=game_state.get('playtime_seconds', 0.0)
        )
        
        return asdict(metadata)
    
    def _verify_integrity(self, save_data: Dict[str, Any]) -> bool:
        """Verify save file integrity using checksum."""
        try:
            metadata = save_data.get('metadata', {})
            expected_checksum = metadata.get('checksum', '')
            
            if not expected_checksum:
                self.logger.warning("No checksum found in save file")
                return True  # Allow saves without checksum (legacy)
            
            # Recreate checksum without the checksum field
            metadata_copy = metadata.copy()
            metadata_copy['checksum'] = ''
            
            temp_save_data = {
                'metadata': metadata_copy,
                'game_state': save_data['game_state']
            }
            
            json_data = json.dumps(temp_save_data, indent=2, default=str)
            calculated_checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            return calculated_checksum == expected_checksum
            
        except Exception as e:
            self.logger.error(f"Integrity verification failed: {e}")
            return False
    
    def _is_version_compatible(self, save_version: str) -> bool:
        """Check if save version is compatible with current game."""
        # Simple version compatibility check
        # In the future, this could be more sophisticated
        major_current = int(self.current_version.split('.')[0])
        major_save = int(save_version.split('.')[0])
        
        return major_current == major_save
    
    def _migrate_save_data(self, game_state: Dict[str, Any], from_version: str) -> Dict[str, Any]:
        """Migrate save data from older versions."""
        # Currently no migration needed
        # In the future, add version-specific migration logic here
        return game_state
    
    def _extract_metadata(self, save_file: Path) -> Optional[Dict[str, Any]]:
        """Extract metadata from save file without loading full game state."""
        try:
            # Try compressed first
            try:
                with gzip.open(save_file, 'rt', encoding='utf-8') as f:
                    # Read just enough to get metadata
                    partial_data = f.read(1024)  # Read first 1KB
                    f.seek(0)
                    save_data = json.load(f)
            except (gzip.BadGzipFile, UnicodeDecodeError):
                save_data = json.loads(save_file.read_text(encoding='utf-8'))
            
            return save_data.get('metadata', {})
            
        except Exception as e:
            self.logger.warning(f"Failed to extract metadata from {save_file}: {e}")
            return None
    
    def create_backup(self, slot_name: str) -> bool:
        """Create a timestamped backup of a save file."""
        save_file = self.save_dir / f"{slot_name}.sav"
        
        if not save_file.exists():
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.save_dir / f"{slot_name}_backup_{timestamp}.sav"
            shutil.copy2(save_file, backup_file)
            
            self.logger.info(f"Created backup: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def cleanup_old_backups(self, max_backups: int = 10):
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backup_files = list(self.save_dir.glob("*_backup_*.sav"))
            
            if len(backup_files) <= max_backups:
                return
            
            # Sort by modification time
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest files
            files_to_remove = backup_files[:-max_backups]
            for backup_file in files_to_remove:
                backup_file.unlink()
                self.logger.info(f"Removed old backup: {backup_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old backups: {e}")


# Global save manager instance
_save_manager: Optional[SaveLoadManager] = None


def get_save_manager() -> SaveLoadManager:
    """Get the global save manager instance."""
    global _save_manager
    if _save_manager is None:
        _save_manager = SaveLoadManager()
    return _save_manager


def init_save_manager(save_dir: Path = Path("saves")) -> SaveLoadManager:
    """Initialize the global save manager."""
    global _save_manager
    _save_manager = SaveLoadManager(save_dir)
    return _save_manager