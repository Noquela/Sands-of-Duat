"""
Backup Manager for Sands of Duat

Comprehensive backup system with automatic saves, multiple backup slots,
cloud preparation, and recovery mechanisms to ensure player data is never lost.
"""

import os
import json
import gzip
import shutil
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import threading
import time

from ..services.save_load import SaveLoadManager, get_save_manager


class BackupType(Enum):
    """Types of backups."""
    AUTO_SAVE = "auto_save"
    MANUAL = "manual"
    SESSION_START = "session_start"
    PROGRESSION = "progression"
    EMERGENCY = "emergency"
    DAILY = "daily"
    WEEKLY = "weekly"


class BackupStatus(Enum):
    """Backup operation status."""
    SUCCESS = "success"
    FAILED = "failed"
    CORRUPTED = "corrupted"
    PARTIAL = "partial"
    IN_PROGRESS = "in_progress"


@dataclass
class BackupMetadata:
    """Metadata for backup files."""
    backup_id: str
    backup_type: BackupType
    created_at: str
    file_size_bytes: int
    checksum: str
    game_version: str
    player_name: str
    player_level: int
    playtime_hours: float
    chambers_completed: int
    total_cards: int
    status: BackupStatus = BackupStatus.SUCCESS
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "backup_id": self.backup_id,
            "backup_type": self.backup_type.value,
            "created_at": self.created_at,
            "file_size_bytes": self.file_size_bytes,
            "checksum": self.checksum,
            "game_version": self.game_version,
            "player_name": self.player_name,
            "player_level": self.player_level,
            "playtime_hours": self.playtime_hours,
            "chambers_completed": self.chambers_completed,
            "total_cards": self.total_cards,
            "status": self.status.value,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupMetadata':
        """Create from dictionary."""
        return cls(
            backup_id=data["backup_id"],
            backup_type=BackupType(data["backup_type"]),
            created_at=data["created_at"],
            file_size_bytes=data["file_size_bytes"],
            checksum=data["checksum"],
            game_version=data["game_version"],
            player_name=data["player_name"],
            player_level=data["player_level"],
            playtime_hours=data["playtime_hours"],
            chambers_completed=data["chambers_completed"],
            total_cards=data["total_cards"],
            status=BackupStatus(data.get("status", "success")),
            description=data.get("description", "")
        )


class BackupManager:
    """
    Comprehensive backup management system for player data.
    """
    
    def __init__(self, save_manager: Optional[SaveLoadManager] = None, backup_dir: Path = Path("backups")):
        self.logger = logging.getLogger(__name__)
        self.save_manager = save_manager or get_save_manager()
        
        # Backup directories
        self.backup_dir = backup_dir
        self.auto_backup_dir = backup_dir / "auto"
        self.manual_backup_dir = backup_dir / "manual"
        self.emergency_backup_dir = backup_dir / "emergency"
        self.daily_backup_dir = backup_dir / "daily"
        self.weekly_backup_dir = backup_dir / "weekly"
        
        # Create directories
        for directory in [self.backup_dir, self.auto_backup_dir, self.manual_backup_dir, 
                         self.emergency_backup_dir, self.daily_backup_dir, self.weekly_backup_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Backup settings
        self.max_auto_backups = 10
        self.max_manual_backups = 20
        self.max_daily_backups = 7
        self.max_weekly_backups = 4
        self.max_emergency_backups = 5
        
        # Auto-backup settings
        self.auto_backup_enabled = True
        self.auto_backup_interval = 300  # 5 minutes
        self.last_auto_backup = datetime.now()
        
        # Background backup thread
        self.backup_thread = None
        self.backup_thread_running = False
        
        # Backup metadata tracking
        self.backup_metadata: Dict[str, BackupMetadata] = {}
        self.metadata_file = self.backup_dir / "backup_metadata.json"
        
        # Load existing metadata
        self._load_backup_metadata()
        
        # Start background backup service
        self.start_backup_service()
        
        self.logger.info(f"Backup manager initialized - Directory: {backup_dir}")
    
    def start_backup_service(self) -> None:
        """Start the background backup service."""
        if self.backup_thread_running:
            return
        
        self.backup_thread_running = True
        self.backup_thread = threading.Thread(target=self._backup_service_loop, daemon=True)
        self.backup_thread.start()
        
        self.logger.info("Background backup service started")
    
    def stop_backup_service(self) -> None:
        """Stop the background backup service."""
        self.backup_thread_running = False
        if self.backup_thread:
            self.backup_thread.join(timeout=5.0)
        
        self.logger.info("Background backup service stopped")
    
    def _backup_service_loop(self) -> None:
        """Background service loop for automatic backups."""
        while self.backup_thread_running:
            try:
                # Check if auto-backup is needed
                if self.auto_backup_enabled:
                    time_since_backup = (datetime.now() - self.last_auto_backup).total_seconds()
                    
                    if time_since_backup >= self.auto_backup_interval:
                        self.create_auto_backup()
                
                # Check for daily/weekly backups
                self._check_scheduled_backups()
                
                # Sleep for 60 seconds before next check
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Error in backup service loop: {e}")
                time.sleep(60)  # Continue after error
    
    def create_backup(self, 
                     backup_type: BackupType, 
                     slot_name: str = "quicksave",
                     description: str = "") -> Optional[BackupMetadata]:
        """
        Create a backup of the specified save slot.
        
        Args:
            backup_type: Type of backup to create
            slot_name: Save slot to backup
            description: Optional description for the backup
        
        Returns:
            BackupMetadata if successful, None otherwise
        """
        try:
            # Load save data to backup
            save_data = self.save_manager.load_game(slot_name)
            if not save_data:
                self.logger.warning(f"No save data found for slot: {slot_name}")
                return None
            
            # Generate backup ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_id = f"{backup_type.value}_{timestamp}"
            
            # Determine backup directory
            backup_dir = self._get_backup_directory(backup_type)
            backup_file = backup_dir / f"{backup_id}.bak"
            
            # Create backup metadata
            metadata = self._create_backup_metadata(backup_id, backup_type, save_data, description)
            
            # Write backup file (compressed)
            backup_content = {
                "metadata": metadata.to_dict(),
                "save_data": save_data
            }
            
            json_data = json.dumps(backup_content, indent=2, default=str)
            
            # Calculate checksum
            checksum = hashlib.sha256(json_data.encode()).hexdigest()
            metadata.checksum = checksum
            backup_content["metadata"]["checksum"] = checksum
            
            # Write compressed backup
            final_json = json.dumps(backup_content, indent=2, default=str)
            with gzip.open(backup_file, 'wt', encoding='utf-8') as f:
                f.write(final_json)
            
            # Update file size
            metadata.file_size_bytes = backup_file.stat().st_size
            
            # Store metadata
            self.backup_metadata[backup_id] = metadata
            self._save_backup_metadata()
            
            # Cleanup old backups
            self._cleanup_old_backups(backup_type)
            
            self.logger.info(f"Created backup: {backup_id} ({metadata.file_size_bytes} bytes)")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def create_auto_backup(self) -> Optional[BackupMetadata]:
        """Create an automatic backup."""
        backup = self.create_backup(BackupType.AUTO_SAVE, description="Automatic backup")
        if backup:
            self.last_auto_backup = datetime.now()
        return backup
    
    def create_manual_backup(self, description: str = "") -> Optional[BackupMetadata]:
        """Create a manual backup."""
        return self.create_backup(BackupType.MANUAL, description=description or "Manual backup")
    
    def create_emergency_backup(self, description: str = "Emergency backup") -> Optional[BackupMetadata]:
        """Create an emergency backup (e.g., before risky operations)."""
        return self.create_backup(BackupType.EMERGENCY, description=description)
    
    def restore_backup(self, backup_id: str, target_slot: str = "quicksave") -> bool:
        """
        Restore a backup to a save slot.
        
        Args:
            backup_id: ID of backup to restore
            target_slot: Save slot to restore to
        
        Returns:
            True if restoration successful
        """
        try:
            if backup_id not in self.backup_metadata:
                self.logger.error(f"Backup not found: {backup_id}")
                return False
            
            metadata = self.backup_metadata[backup_id]
            backup_dir = self._get_backup_directory(metadata.backup_type)
            backup_file = backup_dir / f"{backup_id}.bak"
            
            if not backup_file.exists():
                self.logger.error(f"Backup file not found: {backup_file}")
                return False
            
            # Create emergency backup before restoration
            self.create_emergency_backup(f"Before restoring {backup_id}")
            
            # Load and verify backup
            with gzip.open(backup_file, 'rt', encoding='utf-8') as f:
                backup_content = json.load(f)
            
            # Verify integrity
            if not self._verify_backup_integrity(backup_content):
                self.logger.error(f"Backup integrity check failed: {backup_id}")
                return False
            
            # Extract save data
            save_data = backup_content["save_data"]
            
            # Restore to save slot
            success = self.save_manager.save_game(save_data, target_slot)
            
            if success:
                self.logger.info(f"Successfully restored backup {backup_id} to slot {target_slot}")
            else:
                self.logger.error(f"Failed to restore backup {backup_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error restoring backup {backup_id}: {e}")
            return False
    
    def list_backups(self, backup_type: Optional[BackupType] = None) -> List[BackupMetadata]:
        """
        List available backups, optionally filtered by type.
        
        Args:
            backup_type: Filter by backup type, or None for all
        
        Returns:
            List of backup metadata, sorted by creation date (newest first)
        """
        backups = []
        
        for backup_id, metadata in self.backup_metadata.items():
            if backup_type is None or metadata.backup_type == backup_type:
                backups.append(metadata)
        
        # Sort by creation date (newest first)
        backups.sort(key=lambda x: x.created_at, reverse=True)
        
        return backups
    
    def delete_backup(self, backup_id: str) -> bool:
        """
        Delete a specific backup.
        
        Args:
            backup_id: ID of backup to delete
        
        Returns:
            True if deletion successful
        """
        try:
            if backup_id not in self.backup_metadata:
                self.logger.warning(f"Backup not found: {backup_id}")
                return False
            
            metadata = self.backup_metadata[backup_id]
            backup_dir = self._get_backup_directory(metadata.backup_type)
            backup_file = backup_dir / f"{backup_id}.bak"
            
            # Delete file if it exists
            if backup_file.exists():
                backup_file.unlink()
            
            # Remove from metadata
            del self.backup_metadata[backup_id]
            self._save_backup_metadata()
            
            self.logger.info(f"Deleted backup: {backup_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting backup {backup_id}: {e}")
            return False
    
    def get_backup_summary(self) -> Dict[str, Any]:
        """Get comprehensive backup statistics."""
        total_backups = len(self.backup_metadata)
        total_size = sum(m.file_size_bytes for m in self.backup_metadata.values())
        
        # Count by type
        type_counts = {}
        type_sizes = {}
        for backup_type in BackupType:
            type_backups = [m for m in self.backup_metadata.values() if m.backup_type == backup_type]
            type_counts[backup_type.value] = len(type_backups)
            type_sizes[backup_type.value] = sum(m.file_size_bytes for m in type_backups)
        
        # Recent backups
        recent_backups = sorted(
            self.backup_metadata.values(),
            key=lambda x: x.created_at,
            reverse=True
        )[:5]
        
        # Status summary
        status_counts = {}
        for status in BackupStatus:
            status_counts[status.value] = sum(
                1 for m in self.backup_metadata.values() if m.status == status
            )
        
        return {
            "total_backups": total_backups,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "type_counts": type_counts,
            "type_sizes_mb": {k: round(v / (1024 * 1024), 2) for k, v in type_sizes.items()},
            "recent_backups": [m.to_dict() for m in recent_backups],
            "status_counts": status_counts,
            "auto_backup_enabled": self.auto_backup_enabled,
            "last_auto_backup": self.last_auto_backup.isoformat(),
            "auto_backup_interval_minutes": self.auto_backup_interval // 60
        }
    
    def export_backup(self, backup_id: str, export_path: Path) -> bool:
        """
        Export a backup to an external location.
        
        Args:
            backup_id: ID of backup to export
            export_path: Path where to export the backup
        
        Returns:
            True if export successful
        """
        try:
            if backup_id not in self.backup_metadata:
                self.logger.error(f"Backup not found: {backup_id}")
                return False
            
            metadata = self.backup_metadata[backup_id]
            backup_dir = self._get_backup_directory(metadata.backup_type)
            backup_file = backup_dir / f"{backup_id}.bak"
            
            if not backup_file.exists():
                self.logger.error(f"Backup file not found: {backup_file}")
                return False
            
            # Copy backup file to export location
            shutil.copy2(backup_file, export_path)
            
            self.logger.info(f"Exported backup {backup_id} to {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting backup {backup_id}: {e}")
            return False
    
    def import_backup(self, import_path: Path) -> Optional[BackupMetadata]:
        """
        Import a backup from an external location.
        
        Args:
            import_path: Path to backup file to import
        
        Returns:
            BackupMetadata if import successful, None otherwise
        """
        try:
            if not import_path.exists():
                self.logger.error(f"Import file not found: {import_path}")
                return None
            
            # Load and verify backup
            with gzip.open(import_path, 'rt', encoding='utf-8') as f:
                backup_content = json.load(f)
            
            if not self._verify_backup_integrity(backup_content):
                self.logger.error(f"Invalid backup file: {import_path}")
                return None
            
            # Extract metadata
            metadata_dict = backup_content["metadata"]
            metadata = BackupMetadata.from_dict(metadata_dict)
            
            # Generate new backup ID to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_backup_id = f"imported_{timestamp}"
            metadata.backup_id = new_backup_id
            metadata.backup_type = BackupType.MANUAL
            metadata.description = f"Imported from {import_path.name}"
            
            # Copy to manual backup directory
            backup_dir = self.manual_backup_dir
            backup_file = backup_dir / f"{new_backup_id}.bak"
            shutil.copy2(import_path, backup_file)
            
            # Update metadata
            metadata.file_size_bytes = backup_file.stat().st_size
            self.backup_metadata[new_backup_id] = metadata
            self._save_backup_metadata()
            
            self.logger.info(f"Imported backup as {new_backup_id}")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error importing backup from {import_path}: {e}")
            return None
    
    def _get_backup_directory(self, backup_type: BackupType) -> Path:
        """Get the directory for a specific backup type."""
        backup_dirs = {
            BackupType.AUTO_SAVE: self.auto_backup_dir,
            BackupType.MANUAL: self.manual_backup_dir,
            BackupType.SESSION_START: self.auto_backup_dir,
            BackupType.PROGRESSION: self.auto_backup_dir,
            BackupType.EMERGENCY: self.emergency_backup_dir,
            BackupType.DAILY: self.daily_backup_dir,
            BackupType.WEEKLY: self.weekly_backup_dir
        }
        
        return backup_dirs.get(backup_type, self.backup_dir)
    
    def _create_backup_metadata(self, 
                              backup_id: str, 
                              backup_type: BackupType, 
                              save_data: Dict[str, Any],
                              description: str) -> BackupMetadata:
        """Create backup metadata from save data."""
        # Extract player information
        player_profile = save_data.get("player_profile", {})
        card_collection = save_data.get("card_collection", {})
        progression = save_data.get("progression", {})
        
        return BackupMetadata(
            backup_id=backup_id,
            backup_type=backup_type,
            created_at=datetime.now().isoformat(),
            file_size_bytes=0,  # Will be updated after file creation
            checksum="",  # Will be calculated
            game_version=save_data.get("game_version", "unknown"),
            player_name=player_profile.get("name", "Unknown"),
            player_level=player_profile.get("level", 1),
            playtime_hours=player_profile.get("playtime_hours", 0.0),
            chambers_completed=len(progression.get("chambers_completed", [])),
            total_cards=sum(card_collection.get("owned_cards", {}).values()),
            description=description
        )
    
    def _verify_backup_integrity(self, backup_content: Dict[str, Any]) -> bool:
        """Verify backup file integrity."""
        try:
            # Check required fields
            if "metadata" not in backup_content or "save_data" not in backup_content:
                return False
            
            metadata = backup_content["metadata"]
            expected_checksum = metadata.get("checksum")
            
            if not expected_checksum:
                return True  # Allow backups without checksum
            
            # Recalculate checksum
            metadata_copy = metadata.copy()
            metadata_copy["checksum"] = ""
            
            temp_content = {
                "metadata": metadata_copy,
                "save_data": backup_content["save_data"]
            }
            
            json_data = json.dumps(temp_content, indent=2, default=str)
            calculated_checksum = hashlib.sha256(json_data.encode()).hexdigest()
            
            return calculated_checksum == expected_checksum
            
        except Exception as e:
            self.logger.error(f"Error verifying backup integrity: {e}")
            return False
    
    def _cleanup_old_backups(self, backup_type: BackupType) -> None:
        """Remove old backups beyond the maximum count."""
        max_counts = {
            BackupType.AUTO_SAVE: self.max_auto_backups,
            BackupType.MANUAL: self.max_manual_backups,
            BackupType.DAILY: self.max_daily_backups,
            BackupType.WEEKLY: self.max_weekly_backups,
            BackupType.EMERGENCY: self.max_emergency_backups,
            BackupType.SESSION_START: self.max_auto_backups,
            BackupType.PROGRESSION: self.max_auto_backups
        }
        
        max_count = max_counts.get(backup_type, 10)
        
        # Get backups of this type, sorted by creation date
        type_backups = [
            (backup_id, metadata) for backup_id, metadata in self.backup_metadata.items()
            if metadata.backup_type == backup_type
        ]
        
        type_backups.sort(key=lambda x: x[1].created_at, reverse=True)
        
        # Remove excess backups
        for backup_id, metadata in type_backups[max_count:]:
            self.delete_backup(backup_id)
    
    def _check_scheduled_backups(self) -> None:
        """Check if daily or weekly backups are needed."""
        now = datetime.now()
        
        # Check daily backup
        daily_backups = [m for m in self.backup_metadata.values() if m.backup_type == BackupType.DAILY]
        
        if daily_backups:
            latest_daily = max(daily_backups, key=lambda x: x.created_at)
            latest_date = datetime.fromisoformat(latest_daily.created_at).date()
            
            if now.date() > latest_date:
                self.create_backup(BackupType.DAILY, description="Daily scheduled backup")
        else:
            # No daily backups exist, create first one
            self.create_backup(BackupType.DAILY, description="First daily backup")
        
        # Check weekly backup (Sundays)
        if now.weekday() == 6:  # Sunday
            weekly_backups = [m for m in self.backup_metadata.values() if m.backup_type == BackupType.WEEKLY]
            
            if weekly_backups:
                latest_weekly = max(weekly_backups, key=lambda x: x.created_at)
                latest_date = datetime.fromisoformat(latest_weekly.created_at).date()
                
                # Check if it's been at least a week
                if (now.date() - latest_date).days >= 7:
                    self.create_backup(BackupType.WEEKLY, description="Weekly scheduled backup")
            else:
                # No weekly backups exist, create first one
                self.create_backup(BackupType.WEEKLY, description="First weekly backup")
    
    def _load_backup_metadata(self) -> None:
        """Load backup metadata from file."""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    metadata_dict = json.load(f)
                
                self.backup_metadata = {
                    backup_id: BackupMetadata.from_dict(data)
                    for backup_id, data in metadata_dict.items()
                }
                
                self.logger.info(f"Loaded metadata for {len(self.backup_metadata)} backups")
        except Exception as e:
            self.logger.error(f"Error loading backup metadata: {e}")
            self.backup_metadata = {}
    
    def _save_backup_metadata(self) -> None:
        """Save backup metadata to file."""
        try:
            metadata_dict = {
                backup_id: metadata.to_dict()
                for backup_id, metadata in self.backup_metadata.items()
            }
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata_dict, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving backup metadata: {e}")


# Global backup manager instance
_backup_manager: Optional[BackupManager] = None


def get_backup_manager() -> BackupManager:
    """Get the global backup manager instance."""
    global _backup_manager
    if _backup_manager is None:
        _backup_manager = BackupManager()
    return _backup_manager


def init_backup_manager(save_manager: Optional[SaveLoadManager] = None, 
                       backup_dir: Path = Path("backups")) -> BackupManager:
    """Initialize the global backup manager."""
    global _backup_manager
    _backup_manager = BackupManager(save_manager, backup_dir)
    return _backup_manager