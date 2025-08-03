"""
Advanced Save System for Sands of Duat

Comprehensive save/load system with structured data, progression tracking,
and robust integrity checking. Integrates with existing player collection
and progression systems.
"""

import json
import gzip
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import logging
from enum import Enum

from ..services.save_load import SaveLoadManager, get_save_manager
from .player_collection import PlayerCollection


class ProgressionState(Enum):
    """Player progression states in the game."""
    NEW_PLAYER = "new_player"
    TUTORIAL_COMPLETE = "tutorial_complete"
    DECK_BUILDER_UNLOCKED = "deck_builder_unlocked"
    COMBAT_READY = "combat_ready"
    CHAMBER_EXPLORER = "chamber_explorer"
    TEMPLE_MASTER = "temple_master"
    PHARAOH_CHALLENGER = "pharaoh_challenger"
    PHARAOH_VICTOR = "pharaoh_victor"


@dataclass
class PlayerProfile:
    """Complete player profile data."""
    name: str = "Unknown Adventurer"
    level: int = 1
    xp: int = 0
    total_wins: int = 0
    total_losses: int = 0
    win_streak: int = 0
    best_win_streak: int = 0
    playtime_hours: float = 0.0
    current_chamber: str = "entrance"
    unlocked_chambers: Set[str] = field(default_factory=lambda: {"entrance"})
    progression_state: ProgressionState = ProgressionState.NEW_PLAYER
    created_at: str = ""
    last_played: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.last_played = datetime.now().isoformat()


@dataclass
class CardCollectionData:
    """Player's card collection and deck data."""
    owned_cards: Dict[str, int] = field(default_factory=dict)  # card_id -> count
    favorite_cards: Set[str] = field(default_factory=set)
    discovered_cards: Set[str] = field(default_factory=set)
    upgrade_levels: Dict[str, int] = field(default_factory=dict)  # Future: card upgrades
    unlocked_card_pools: Set[str] = field(default_factory=set)
    
    # Deck management
    saved_decks: Dict[str, List[str]] = field(default_factory=dict)  # deck_name -> card_ids
    active_deck: str = "starter_deck"
    deck_wins: Dict[str, int] = field(default_factory=dict)  # deck performance tracking
    deck_losses: Dict[str, int] = field(default_factory=dict)


@dataclass
class ProgressionData:
    """Player progression and achievements data."""
    chambers_completed: Set[str] = field(default_factory=set)
    chamber_completion_times: Dict[str, str] = field(default_factory=dict)  # chamber -> timestamp
    boss_defeats: Dict[str, int] = field(default_factory=dict)  # boss_id -> times defeated
    achievements: Set[str] = field(default_factory=set)
    achievement_progress: Dict[str, int] = field(default_factory=dict)  # achievement_id -> progress
    
    # Statistics
    battles_won: int = 0
    battles_lost: int = 0
    cards_played: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    special_abilities_used: int = 0
    
    # Daily/Weekly tracking
    daily_wins: int = 0
    weekly_wins: int = 0
    last_daily_reset: str = ""
    last_weekly_reset: str = ""


@dataclass
class GameSettings:
    """Player's game settings and preferences."""
    audio_volume: float = 0.8
    music_volume: float = 0.6
    sfx_volume: float = 0.8
    display_mode: str = "windowed"  # windowed, fullscreen, borderless
    resolution: str = "1280x720"
    vsync: bool = True
    
    # Gameplay settings
    auto_save: bool = True
    auto_save_frequency: int = 300  # seconds
    combat_speed: str = "normal"  # slow, normal, fast
    animation_quality: str = "high"  # low, medium, high
    
    # UI preferences
    ui_scale: float = 1.0
    show_card_tooltips: bool = True
    confirm_card_plays: bool = False
    
    # Key bindings
    key_bindings: Dict[str, str] = field(default_factory=lambda: {
        "deck_builder": "d",
        "collection": "c",
        "pause": "escape",
        "confirm": "return",
        "cancel": "escape"
    })


@dataclass
class SaveData:
    """Complete save data structure."""
    # Core data
    player_profile: PlayerProfile = field(default_factory=PlayerProfile)
    card_collection: CardCollectionData = field(default_factory=CardCollectionData)
    progression: ProgressionData = field(default_factory=ProgressionData)
    settings: GameSettings = field(default_factory=GameSettings)
    
    # Session data
    session_start_time: str = ""
    last_auto_save: str = ""
    game_version: str = "1.0.0"
    save_version: str = "1.0.0"
    
    def __post_init__(self):
        if not self.session_start_time:
            self.session_start_time = datetime.now().isoformat()


class SaveSystem:
    """
    Advanced save system managing player data, progression, and settings.
    """
    
    def __init__(self, save_manager: Optional[SaveLoadManager] = None):
        self.logger = logging.getLogger(__name__)
        self.save_manager = save_manager or get_save_manager()
        
        # Current session data
        self.current_save: Optional[SaveData] = None
        self.session_start_time = datetime.now()
        self.last_auto_save = datetime.now()
        self.auto_save_enabled = True
        self.auto_save_interval = 300  # 5 minutes
        
        # Change tracking for optimized saves
        self.data_changed = False
        self.last_change_time = datetime.now()
        
        self.logger.info("Advanced save system initialized")
    
    def create_new_save(self, player_name: str = "Unknown Adventurer") -> SaveData:
        """Create a new save file with default data."""
        self.logger.info(f"Creating new save for player: {player_name}")
        
        save_data = SaveData()
        save_data.player_profile.name = player_name
        
        # Initialize with starter collection
        collection_data = self._create_starter_collection()
        save_data.card_collection = collection_data
        
        # Set up initial progression
        save_data.progression.last_daily_reset = datetime.now().isoformat()
        save_data.progression.last_weekly_reset = datetime.now().isoformat()
        
        self.current_save = save_data
        self.data_changed = True
        
        return save_data
    
    def load_save(self, slot_name: str = "quicksave") -> Optional[SaveData]:
        """Load save data from file."""
        self.logger.info(f"Loading save from slot: {slot_name}")
        
        # Load raw save data
        raw_data = self.save_manager.load_game(slot_name)
        if not raw_data:
            self.logger.warning(f"No save data found for slot: {slot_name}")
            return None
        
        try:
            # Convert to structured save data
            save_data = self._deserialize_save_data(raw_data)
            
            # Validate and migrate if necessary
            save_data = self._validate_and_migrate_save(save_data)
            
            # Update session tracking
            save_data.session_start_time = datetime.now().isoformat()
            save_data.player_profile.last_played = datetime.now().isoformat()
            
            self.current_save = save_data
            self.data_changed = False
            
            self.logger.info(f"Successfully loaded save for player: {save_data.player_profile.name}")
            return save_data
            
        except Exception as e:
            self.logger.error(f"Failed to parse save data: {e}")
            return None
    
    def save_game(self, slot_name: str = "quicksave", force: bool = False) -> bool:
        """Save current game state."""
        if not self.current_save:
            self.logger.warning("No save data to save")
            return False
        
        if not force and not self.data_changed:
            self.logger.debug("No changes to save")
            return True
        
        try:
            # Update save metadata
            self._update_save_metadata()
            
            # Serialize to dictionary format
            save_dict = self._serialize_save_data(self.current_save)
            
            # Save using existing save manager
            success = self.save_manager.save_game(save_dict, slot_name)
            
            if success:
                self.data_changed = False
                self.last_auto_save = datetime.now()
                self.logger.info(f"Game saved successfully to slot: {slot_name}")
            else:
                self.logger.error(f"Failed to save game to slot: {slot_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False
    
    def auto_save(self) -> bool:
        """Perform automatic save if conditions are met."""
        if not self.auto_save_enabled or not self.current_save:
            return False
        
        # Check if enough time has passed and there are changes
        time_since_last_save = (datetime.now() - self.last_auto_save).total_seconds()
        
        if time_since_last_save >= self.auto_save_interval and self.data_changed:
            self.logger.info("Performing auto-save")
            return self.save_game("auto_save")
        
        return False
    
    def mark_data_changed(self) -> None:
        """Mark that save data has changed."""
        self.data_changed = True
        self.last_change_time = datetime.now()
    
    def update_player_progress(self, **kwargs) -> None:
        """Update player progression data."""
        if not self.current_save:
            return
        
        profile = self.current_save.player_profile
        progression = self.current_save.progression
        
        # Update profile data
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
            elif hasattr(progression, key):
                setattr(progression, key, value)
        
        # Update playtime
        session_time = (datetime.now() - self.session_start_time).total_seconds() / 3600
        profile.playtime_hours += session_time
        self.session_start_time = datetime.now()  # Reset for next update
        
        self.mark_data_changed()
    
    def award_xp(self, amount: int, source: str = "unknown") -> Dict[str, Any]:
        """Award XP and handle level ups."""
        if not self.current_save:
            return {}
        
        profile = self.current_save.player_profile
        old_level = profile.level
        old_xp = profile.xp
        
        # Award XP
        profile.xp += amount
        
        # Calculate level ups (Egyptian themed levels)
        xp_per_level = 1000
        new_level = 1 + (profile.xp // xp_per_level)
        
        level_up_rewards = {}
        if new_level > old_level:
            profile.level = new_level
            levels_gained = new_level - old_level
            
            # Generate level up rewards
            level_up_rewards = self._generate_level_up_rewards(new_level, levels_gained)
            
            self.logger.info(f"Player leveled up: {old_level} -> {new_level} (gained {amount} XP from {source})")
        
        self.mark_data_changed()
        
        return {
            "xp_gained": amount,
            "old_xp": old_xp,
            "new_xp": profile.xp,
            "old_level": old_level,
            "new_level": profile.level,
            "level_up": new_level > old_level,
            "rewards": level_up_rewards
        }
    
    def complete_chamber(self, chamber_id: str) -> Dict[str, Any]:
        """Mark chamber as completed and award rewards."""
        if not self.current_save:
            return {}
        
        progression = self.current_save.progression
        
        # Check if already completed
        if chamber_id in progression.chambers_completed:
            self.logger.info(f"Chamber {chamber_id} already completed")
            return {"already_completed": True}
        
        # Mark as completed
        progression.chambers_completed.add(chamber_id)
        progression.chamber_completion_times[chamber_id] = datetime.now().isoformat()
        
        # Unlock next chambers and award XP
        chamber_rewards = self._generate_chamber_completion_rewards(chamber_id)
        
        # Award XP for completion
        xp_reward = chamber_rewards.get("xp", 100)
        xp_result = self.award_xp(xp_reward, f"chamber_completion_{chamber_id}")
        
        self.mark_data_changed()
        
        self.logger.info(f"Chamber {chamber_id} completed! Rewards: {chamber_rewards}")
        
        return {
            "chamber_id": chamber_id,
            "rewards": chamber_rewards,
            "xp_result": xp_result,
            "completion_time": progression.chamber_completion_times[chamber_id]
        }
    
    def record_battle_result(self, won: bool, enemy_type: str = "unknown", deck_used: str = "") -> Dict[str, Any]:
        """Record battle result and update statistics."""
        if not self.current_save:
            return {}
        
        profile = self.current_save.player_profile
        progression = self.current_save.progression
        
        if won:
            profile.total_wins += 1
            profile.win_streak += 1
            progression.battles_won += 1
            progression.daily_wins += 1
            progression.weekly_wins += 1
            
            if profile.win_streak > profile.best_win_streak:
                profile.best_win_streak = profile.win_streak
            
            # Award XP for wins
            base_xp = 50
            streak_bonus = min(profile.win_streak * 5, 100)  # Max 100 bonus
            total_xp = base_xp + streak_bonus
            
            xp_result = self.award_xp(total_xp, f"battle_win_{enemy_type}")
            
        else:
            profile.total_losses += 1
            profile.win_streak = 0
            progression.battles_lost += 1
            
            # Small XP for participation
            xp_result = self.award_xp(10, f"battle_participation_{enemy_type}")
        
        # Update deck statistics
        if deck_used and deck_used in self.current_save.card_collection.saved_decks:
            if won:
                self.current_save.card_collection.deck_wins[deck_used] = \
                    self.current_save.card_collection.deck_wins.get(deck_used, 0) + 1
            else:
                self.current_save.card_collection.deck_losses[deck_used] = \
                    self.current_save.card_collection.deck_losses.get(deck_used, 0) + 1
        
        self.mark_data_changed()
        
        result = {
            "won": won,
            "enemy_type": enemy_type,
            "win_streak": profile.win_streak,
            "total_wins": profile.total_wins,
            "total_losses": profile.total_losses,
            "xp_result": xp_result
        }
        
        self.logger.info(f"Battle result recorded: {result}")
        return result
    
    def get_save_summary(self) -> Dict[str, Any]:
        """Get summary of current save for UI display."""
        if not self.current_save:
            return {}
        
        profile = self.current_save.player_profile
        progression = self.current_save.progression
        collection = self.current_save.card_collection
        
        return {
            "player_name": profile.name,
            "level": profile.level,
            "xp": profile.xp,
            "playtime_hours": round(profile.playtime_hours, 1),
            "win_rate": (profile.total_wins / max(1, profile.total_wins + profile.total_losses)) * 100,
            "current_streak": profile.win_streak,
            "best_streak": profile.best_win_streak,
            "chambers_completed": len(progression.chambers_completed),
            "unique_cards": len(collection.owned_cards),
            "total_cards": sum(collection.owned_cards.values()),
            "achievements": len(progression.achievements),
            "last_played": profile.last_played,
            "progression_state": profile.progression_state.value
        }
    
    def _create_starter_collection(self) -> CardCollectionData:
        """Create starter card collection."""
        collection = CardCollectionData()
        
        # Add starter cards
        starter_cards = {
            "whisper_of_thoth": 3,
            "anubis_judgment": 3,
            "isis_protection": 3,
            "desert_meditation": 3,
            "ra_solar_flare": 2,
            "mummification_ritual": 2
        }
        
        collection.owned_cards = starter_cards
        collection.discovered_cards = set(starter_cards.keys())
        
        # Create starter deck
        starter_deck = []
        for card_id, count in starter_cards.items():
            starter_deck.extend([card_id] * count)
        
        collection.saved_decks["starter_deck"] = starter_deck
        collection.active_deck = "starter_deck"
        
        return collection
    
    def _serialize_save_data(self, save_data: SaveData) -> Dict[str, Any]:
        """Convert SaveData to dictionary for saving."""
        def convert_sets_to_lists(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, dict):
                return {k: convert_sets_to_lists(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets_to_lists(item) for item in obj]
            elif hasattr(obj, '__dict__'):
                return convert_sets_to_lists(asdict(obj))
            else:
                return obj
        
        # Convert SaveData to dict and handle sets/enums
        save_dict = asdict(save_data)
        
        # Convert enums to strings
        save_dict["player_profile"]["progression_state"] = save_data.player_profile.progression_state.value
        
        # Convert sets to lists for JSON serialization
        return convert_sets_to_lists(save_dict)
    
    def _deserialize_save_data(self, save_dict: Dict[str, Any]) -> SaveData:
        """Convert dictionary back to SaveData."""
        def convert_lists_to_sets(obj, field_name=""):
            # Fields that should be sets
            set_fields = {
                "unlocked_chambers", "favorite_cards", "discovered_cards", 
                "unlocked_card_pools", "chambers_completed", "achievements"
            }
            
            if field_name in set_fields and isinstance(obj, list):
                return set(obj)
            elif isinstance(obj, dict):
                return {k: convert_lists_to_sets(v, k) for k, v in obj.items()}
            elif isinstance(obj, list) and field_name not in set_fields:
                return [convert_lists_to_sets(item) for item in obj]
            else:
                return obj
        
        # Convert lists back to sets where appropriate
        converted_dict = convert_lists_to_sets(save_dict)
        
        # Handle enum conversion
        if "player_profile" in converted_dict and "progression_state" in converted_dict["player_profile"]:
            state_value = converted_dict["player_profile"]["progression_state"]
            converted_dict["player_profile"]["progression_state"] = ProgressionState(state_value)
        
        # Create SaveData object
        save_data = SaveData()
        
        # Populate fields
        if "player_profile" in converted_dict:
            save_data.player_profile = PlayerProfile(**converted_dict["player_profile"])
        if "card_collection" in converted_dict:
            save_data.card_collection = CardCollectionData(**converted_dict["card_collection"])
        if "progression" in converted_dict:
            save_data.progression = ProgressionData(**converted_dict["progression"])
        if "settings" in converted_dict:
            save_data.settings = GameSettings(**converted_dict["settings"])
        
        # Copy remaining fields
        for field in ["session_start_time", "last_auto_save", "game_version", "save_version"]:
            if field in converted_dict:
                setattr(save_data, field, converted_dict[field])
        
        return save_data
    
    def _validate_and_migrate_save(self, save_data: SaveData) -> SaveData:
        """Validate save data and perform migrations if needed."""
        # Reset daily/weekly progress if needed
        now = datetime.now()
        
        # Check daily reset
        if save_data.progression.last_daily_reset:
            last_daily = datetime.fromisoformat(save_data.progression.last_daily_reset)
            if now.date() > last_daily.date():
                save_data.progression.daily_wins = 0
                save_data.progression.last_daily_reset = now.isoformat()
        
        # Check weekly reset (Monday)
        if save_data.progression.last_weekly_reset:
            last_weekly = datetime.fromisoformat(save_data.progression.last_weekly_reset)
            current_week = now.isocalendar()[1]
            last_week = last_weekly.isocalendar()[1]
            if current_week != last_week:
                save_data.progression.weekly_wins = 0
                save_data.progression.last_weekly_reset = now.isoformat()
        
        return save_data
    
    def _update_save_metadata(self) -> None:
        """Update save metadata before saving."""
        if not self.current_save:
            return
        
        self.current_save.last_auto_save = datetime.now().isoformat()
        self.current_save.player_profile.last_played = datetime.now().isoformat()
    
    def _generate_level_up_rewards(self, new_level: int, levels_gained: int) -> Dict[str, Any]:
        """Generate rewards for leveling up."""
        rewards = {
            "cards": [],
            "card_packs": 0,
            "unlocks": []
        }
        
        # Every 5 levels, unlock new card pool
        if new_level % 5 == 0:
            rewards["card_packs"] = 2
            rewards["unlocks"].append(f"level_{new_level}_pool")
        
        # Every 10 levels, special reward
        if new_level % 10 == 0:
            rewards["unlocks"].append("special_chamber")
        
        return rewards
    
    def _generate_chamber_completion_rewards(self, chamber_id: str) -> Dict[str, Any]:
        """Generate rewards for completing a chamber."""
        chamber_rewards = {
            "entrance": {"xp": 100, "cards": ["whisper_of_thoth"], "unlocks": ["antechamber"]},
            "antechamber": {"xp": 150, "cards": ["ra_solar_flare"], "unlocks": ["first_trial"]},
            "first_trial": {"xp": 200, "cards": ["anubis_judgment"], "unlocks": ["chamber_of_isis", "chamber_of_horus"]},
            "chamber_of_isis": {"xp": 300, "cards": ["isis_protection"], "unlocks": ["hall_of_truth"]},
            "chamber_of_horus": {"xp": 300, "cards": ["horus_sight"], "unlocks": ["hall_of_truth"]},
            "hall_of_truth": {"xp": 500, "cards": ["maat_judgment"], "unlocks": ["pharaoh_tomb"]},
            "pharaoh_tomb": {"xp": 1000, "cards": ["pharaoh_crown"], "unlocks": []}
        }
        
        return chamber_rewards.get(chamber_id, {"xp": 100, "cards": [], "unlocks": []})


# Global save system instance
_save_system: Optional[SaveSystem] = None


def get_save_system() -> SaveSystem:
    """Get the global save system instance."""
    global _save_system
    if _save_system is None:
        _save_system = SaveSystem()
    return _save_system


def init_save_system(save_manager: Optional[SaveLoadManager] = None) -> SaveSystem:
    """Initialize the global save system."""
    global _save_system
    _save_system = SaveSystem(save_manager)
    return _save_system