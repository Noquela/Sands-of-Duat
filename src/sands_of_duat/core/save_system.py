"""
Save System - SPRINT 8: Complete Game State Persistence
Professional save system with progression tracking and Egyptian theming.
"""

import json
import os
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum, auto

class SaveType(Enum):
    """Types of save data."""
    QUICK_SAVE = auto()
    MANUAL_SAVE = auto()
    AUTO_SAVE = auto()
    CHECKPOINT = auto()

class DifficultyLevel(Enum):
    """Game difficulty levels."""
    APPRENTICE = auto()    # Easy mode
    SCRIBE = auto()        # Normal mode  
    PHARAOH = auto()       # Hard mode
    GOD_KING = auto()      # Expert mode

@dataclass
class PlayerStats:
    """Player statistics and achievements."""
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    total_damage_dealt: int = 0
    total_damage_taken: int = 0
    cards_played: int = 0
    favorite_cards: List[str] = None
    longest_game_duration: float = 0.0
    shortest_victory_time: float = float('inf')
    win_streak: int = 0
    current_win_streak: int = 0
    
    def __post_init__(self):
        if self.favorite_cards is None:
            self.favorite_cards = []

@dataclass
class GameProgress:
    """Game progression data."""
    current_level: int = 1
    experience_points: int = 0
    unlocked_cards: List[str] = None
    unlocked_enemies: List[str] = None
    completed_challenges: List[str] = None
    achievements: List[str] = None
    deck_collection: Dict[str, List[str]] = None
    
    def __post_init__(self):
        if self.unlocked_cards is None:
            self.unlocked_cards = ["Ra", "Anubis", "Isis", "Bastet"]  # Starting cards
        if self.unlocked_enemies is None:
            self.unlocked_enemies = ["Desert Scorpion"]
        if self.completed_challenges is None:
            self.completed_challenges = []
        if self.achievements is None:
            self.achievements = []
        if self.deck_collection is None:
            self.deck_collection = {"Starter Deck": ["Ra", "Anubis", "Isis", "Bastet"]}

@dataclass
class GameState:
    """Current game state for save/load."""
    player_health: int = 30
    enemy_health: int = 30
    player_mana: int = 1
    enemy_mana: int = 1
    turn_count: int = 1
    player_deck: List[str] = None
    player_hand: List[str] = None
    enemy_hand: List[str] = None
    battlefield_state: Dict[str, Any] = None
    current_difficulty: DifficultyLevel = DifficultyLevel.SCRIBE
    
    def __post_init__(self):
        if self.player_deck is None:
            self.player_deck = []
        if self.player_hand is None:
            self.player_hand = []
        if self.enemy_hand is None:
            self.enemy_hand = []
        if self.battlefield_state is None:
            self.battlefield_state = {}

@dataclass
class SaveData:
    """Complete save file structure."""
    save_name: str
    save_type: SaveType
    timestamp: float
    game_version: str = "1.0.0"
    player_stats: PlayerStats = None
    game_progress: GameProgress = None
    current_game_state: Optional[GameState] = None
    settings_snapshot: Dict[str, Any] = None
    checksum: str = ""
    
    def __post_init__(self):
        if self.player_stats is None:
            self.player_stats = PlayerStats()
        if self.game_progress is None:
            self.game_progress = GameProgress()
        if self.settings_snapshot is None:
            self.settings_snapshot = {}

class SaveSystem:
    """
    Professional save system for Sands of Duat.
    Handles game state persistence, progression, and achievements.
    """
    
    def __init__(self):
        """Initialize the save system."""
        # Save directory
        self.save_dir = Path.home() / ".sands_of_duat" / "saves"
        self.backup_dir = self.save_dir / "backups"
        
        # Create directories
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Save metadata
        self.current_save: Optional[SaveData] = None
        self.auto_save_enabled = True
        self.auto_save_interval = 300.0  # 5 minutes
        self.last_auto_save = 0.0
        
        # Quick save slot
        self.quick_save_file = self.save_dir / "quicksave.json"
        
        print("Save System initialized - Hall of Eternity ready")
    
    def create_new_save(self, save_name: str, save_type: SaveType = SaveType.MANUAL_SAVE) -> SaveData:
        """Create a new save file."""
        save_data = SaveData(
            save_name=save_name,
            save_type=save_type,
            timestamp=time.time()
        )
        
        # Generate checksum for integrity
        save_data.checksum = self._generate_checksum(save_data)
        
        self.current_save = save_data
        return save_data
    
    def save_game(self, save_data: SaveData, filename: Optional[str] = None) -> bool:
        """Save game data to file."""
        try:
            if filename is None:
                # Generate filename from save name and timestamp
                safe_name = "".join(c for c in save_data.save_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                timestamp = datetime.fromtimestamp(save_data.timestamp).strftime("%Y%m%d_%H%M%S")
                filename = f"{safe_name}_{timestamp}.json"
            
            save_file = self.save_dir / filename
            
            # Update timestamp and checksum
            save_data.timestamp = time.time()
            save_data.checksum = self._generate_checksum(save_data)
            
            # Convert to dictionary for JSON serialization
            save_dict = self._save_data_to_dict(save_data)
            
            # Write to file with backup
            if save_file.exists():
                backup_file = self.backup_dir / f"{filename}.backup"
                save_file.replace(backup_file)
            
            with open(save_file, 'w') as f:
                json.dump(save_dict, f, indent=2)
            
            print(f"Game saved: {save_file.name}")
            return True
            
        except Exception as e:
            print(f"Failed to save game: {e}")
            return False
    
    def load_game(self, filename: str) -> Optional[SaveData]:
        """Load game data from file."""
        try:
            save_file = self.save_dir / filename
            
            if not save_file.exists():
                print(f"Save file not found: {filename}")
                return None
            
            with open(save_file, 'r') as f:
                save_dict = json.load(f)
            
            # Convert back to SaveData object
            save_data = self._dict_to_save_data(save_dict)
            
            # Verify checksum integrity
            expected_checksum = self._generate_checksum(save_data)
            if save_data.checksum != expected_checksum:
                print(f"Warning: Save file checksum mismatch for {filename}")
                # Continue loading but mark as potentially corrupted
            
            self.current_save = save_data
            print(f"Game loaded: {filename}")
            return save_data
            
        except Exception as e:
            print(f"Failed to load game: {e}")
            return None
    
    def quick_save(self, game_state: GameState) -> bool:
        """Perform a quick save."""
        if not self.current_save:
            self.current_save = self.create_new_save("QuickSave", SaveType.QUICK_SAVE)
        
        self.current_save.current_game_state = game_state
        self.current_save.save_type = SaveType.QUICK_SAVE
        
        try:
            save_dict = self._save_data_to_dict(self.current_save)
            
            with open(self.quick_save_file, 'w') as f:
                json.dump(save_dict, f, indent=2)
            
            print("Quick save complete")
            return True
            
        except Exception as e:
            print(f"Quick save failed: {e}")
            return False
    
    def quick_load(self) -> Optional[SaveData]:
        """Load the quick save."""
        if not self.quick_save_file.exists():
            print("No quick save found")
            return None
        
        try:
            with open(self.quick_save_file, 'r') as f:
                save_dict = json.load(f)
            
            save_data = self._dict_to_save_data(save_dict)
            self.current_save = save_data
            print("Quick load complete")
            return save_data
            
        except Exception as e:
            print(f"Quick load failed: {e}")
            return None
    
    def auto_save(self, game_state: GameState) -> bool:
        """Perform an auto save if enough time has passed."""
        if not self.auto_save_enabled:
            return False
        
        current_time = time.time()
        if current_time - self.last_auto_save < self.auto_save_interval:
            return False
        
        if not self.current_save:
            self.current_save = self.create_new_save("AutoSave", SaveType.AUTO_SAVE)
        
        self.current_save.current_game_state = game_state
        self.current_save.save_type = SaveType.AUTO_SAVE
        
        auto_save_file = self.save_dir / "autosave.json"
        
        try:
            save_dict = self._save_data_to_dict(self.current_save)
            
            with open(auto_save_file, 'w') as f:
                json.dump(save_dict, f, indent=2)
            
            self.last_auto_save = current_time
            print("Auto save complete")
            return True
            
        except Exception as e:
            print(f"Auto save failed: {e}")
            return False
    
    def get_save_files(self) -> List[Dict[str, Any]]:
        """Get list of available save files."""
        save_files = []
        
        for save_file in self.save_dir.glob("*.json"):
            if save_file.name in ["quicksave.json", "autosave.json"]:
                continue
            
            try:
                with open(save_file, 'r') as f:
                    save_dict = json.load(f)
                
                save_info = {
                    "filename": save_file.name,
                    "save_name": save_dict.get("save_name", "Unknown"),
                    "timestamp": save_dict.get("timestamp", 0),
                    "save_type": save_dict.get("save_type", "MANUAL_SAVE"),
                    "game_version": save_dict.get("game_version", "Unknown"),
                    "level": save_dict.get("game_progress", {}).get("current_level", 1),
                    "games_won": save_dict.get("player_stats", {}).get("games_won", 0)
                }
                
                save_files.append(save_info)
                
            except Exception as e:
                print(f"Error reading save file {save_file.name}: {e}")
        
        # Sort by timestamp (newest first)
        save_files.sort(key=lambda x: x["timestamp"], reverse=True)
        return save_files
    
    def delete_save(self, filename: str) -> bool:
        """Delete a save file."""
        try:
            save_file = self.save_dir / filename
            if save_file.exists():
                # Move to backup before deletion
                backup_file = self.backup_dir / f"deleted_{filename}"
                save_file.replace(backup_file)
                print(f"Save file deleted: {filename}")
                return True
            else:
                print(f"Save file not found: {filename}")
                return False
                
        except Exception as e:
            print(f"Failed to delete save file: {e}")
            return False
    
    def update_player_stats(self, stats_update: Dict[str, Any]):
        """Update player statistics."""
        if not self.current_save:
            self.current_save = self.create_new_save("Current Game")
        
        stats = self.current_save.player_stats
        
        for key, value in stats_update.items():
            if hasattr(stats, key):
                if isinstance(value, (int, float)):
                    # Add to existing value
                    current_value = getattr(stats, key)
                    if isinstance(current_value, (int, float)):
                        setattr(stats, key, current_value + value)
                    else:
                        setattr(stats, key, value)
                else:
                    setattr(stats, key, value)
    
    def update_progress(self, progress_update: Dict[str, Any]):
        """Update game progress."""
        if not self.current_save:
            self.current_save = self.create_new_save("Current Game")
        
        progress = self.current_save.game_progress
        
        for key, value in progress_update.items():
            if hasattr(progress, key):
                if key in ["unlocked_cards", "unlocked_enemies", "completed_challenges", "achievements"]:
                    # Add to list if not already present
                    current_list = getattr(progress, key)
                    if isinstance(value, list):
                        for item in value:
                            if item not in current_list:
                                current_list.append(item)
                    elif value not in current_list:
                        current_list.append(value)
                else:
                    setattr(progress, key, value)
    
    def _generate_checksum(self, save_data: SaveData) -> str:
        """Generate checksum for save data integrity."""
        # Create a copy without the checksum field
        data_copy = asdict(save_data)
        data_copy.pop('checksum', None)
        
        # Convert to JSON string and hash
        json_str = json.dumps(data_copy, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def _save_data_to_dict(self, save_data: SaveData) -> Dict[str, Any]:
        """Convert SaveData to dictionary for JSON serialization."""
        save_dict = asdict(save_data)
        
        # Convert enums to strings
        save_dict["save_type"] = save_data.save_type.name
        if save_data.current_game_state:
            save_dict["current_game_state"]["current_difficulty"] = save_data.current_game_state.current_difficulty.name
        
        return save_dict
    
    def _dict_to_save_data(self, save_dict: Dict[str, Any]) -> SaveData:
        """Convert dictionary back to SaveData object."""
        # Convert enum strings back to enums
        save_type = SaveType[save_dict["save_type"]]
        
        # Create SaveData object
        save_data = SaveData(
            save_name=save_dict["save_name"],
            save_type=save_type,
            timestamp=save_dict["timestamp"],
            game_version=save_dict.get("game_version", "1.0.0"),
            checksum=save_dict.get("checksum", "")
        )
        
        # Populate player stats
        if "player_stats" in save_dict:
            stats_dict = save_dict["player_stats"]
            save_data.player_stats = PlayerStats(**stats_dict)
        
        # Populate game progress
        if "game_progress" in save_dict:
            progress_dict = save_dict["game_progress"]
            save_data.game_progress = GameProgress(**progress_dict)
        
        # Populate current game state
        if "current_game_state" in save_dict and save_dict["current_game_state"]:
            state_dict = save_dict["current_game_state"]
            # Convert difficulty enum
            if "current_difficulty" in state_dict:
                state_dict["current_difficulty"] = DifficultyLevel[state_dict["current_difficulty"]]
            save_data.current_game_state = GameState(**state_dict)
        
        # Settings snapshot
        save_data.settings_snapshot = save_dict.get("settings_snapshot", {})
        
        return save_data
    
    def get_achievements(self) -> List[str]:
        """Get current achievements."""
        if self.current_save:
            return self.current_save.game_progress.achievements
        return []
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock a new achievement."""
        if not self.current_save:
            self.current_save = self.create_new_save("Current Game")
        
        achievements = self.current_save.game_progress.achievements
        if achievement_id not in achievements:
            achievements.append(achievement_id)
            print(f"Achievement unlocked: {achievement_id}")
            return True
        return False
    
    def get_win_rate(self) -> float:
        """Calculate win rate percentage."""
        if not self.current_save or not self.current_save.player_stats.games_played:
            return 0.0
        
        stats = self.current_save.player_stats
        return (stats.games_won / stats.games_played) * 100.0
    
    def cleanup_old_saves(self, max_saves: int = 10):
        """Clean up old save files, keeping only the most recent ones."""
        save_files = self.get_save_files()
        
        if len(save_files) <= max_saves:
            return
        
        # Delete oldest saves beyond the limit
        for save_info in save_files[max_saves:]:
            self.delete_save(save_info["filename"])
        
        print(f"Cleaned up {len(save_files) - max_saves} old save files")

# Global save system instance
save_system = SaveSystem()