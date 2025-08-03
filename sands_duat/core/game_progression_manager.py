"""
Game Progression Manager for Sands of Duat

Central coordinator that integrates save system, progression rewards, achievements,
backup management, and player collection into a unified progression experience.
"""

import logging
from typing import Dict, Any, Optional, List, Set, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass

from .save_system import SaveSystem, get_save_system, SaveData, ProgressionState
from .progression_rewards import ProgressionRewardSystem, RewardBundle
from .achievements import AchievementManager, Achievement
from .backup_manager import BackupManager, get_backup_manager, BackupType
from .player_collection import PlayerCollection, CardRewardSystem


@dataclass
class GameSession:
    """Tracks current game session data."""
    session_id: str
    start_time: datetime
    player_name: str
    battles_this_session: int = 0
    xp_gained_this_session: int = 0
    cards_discovered_this_session: List[str] = None
    achievements_earned_this_session: List[str] = None
    chambers_completed_this_session: List[str] = None
    
    def __post_init__(self):
        if self.cards_discovered_this_session is None:
            self.cards_discovered_this_session = []
        if self.achievements_earned_this_session is None:
            self.achievements_earned_this_session = []
        if self.chambers_completed_this_session is None:
            self.chambers_completed_this_session = []


class GameProgressionManager:
    """
    Central manager for all progression-related systems.
    Coordinates save/load, rewards, achievements, backups, and player collection.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Core systems
        self.save_system = get_save_system()
        self.backup_manager = get_backup_manager()
        
        # Progression systems (initialized after save load)
        self.player_collection: Optional[PlayerCollection] = None
        self.reward_system: Optional[ProgressionRewardSystem] = None
        self.achievement_manager: Optional[AchievementManager] = None
        
        # Current session
        self.current_session: Optional[GameSession] = None
        
        # Event callbacks
        self.event_handlers: Dict[str, List[Callable]] = {
            "level_up": [],
            "achievement_earned": [],
            "chamber_completed": [],
            "battle_won": [],
            "battle_lost": [],
            "card_discovered": [],
            "save_completed": [],
            "backup_created": []
        }
        
        # Auto-save and backup timers
        self.last_auto_save = datetime.now()
        self.last_backup_check = datetime.now()
        self.auto_save_interval = 300  # 5 minutes
        self.backup_check_interval = 1800  # 30 minutes
        
        self.logger.info("Game progression manager initialized")
    
    def start_new_game(self, player_name: str) -> bool:
        """
        Start a new game with fresh save data.
        
        Args:
            player_name: Name for the new player
        
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Starting new game for player: {player_name}")
            
            # Create emergency backup if there's existing data
            if self.save_system.current_save:
                self.backup_manager.create_emergency_backup("Before new game")
            
            # Create new save data
            save_data = self.save_system.create_new_save(player_name)
            
            # Initialize progression systems
            self._initialize_progression_systems(save_data)
            
            # Create initial backup
            self.backup_manager.create_backup(BackupType.SESSION_START, description="New game started")
            
            # Start session tracking
            self._start_new_session(player_name)
            
            # Save initial state
            self.save_system.save_game()
            
            self.logger.info("New game started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start new game: {e}")
            return False
    
    def load_game(self, slot_name: str = "quicksave") -> bool:
        """
        Load an existing game.
        
        Args:
            slot_name: Save slot to load from
        
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Loading game from slot: {slot_name}")
            
            # Load save data
            save_data = self.save_system.load_save(slot_name)
            if not save_data:
                self.logger.error(f"Failed to load save data from slot: {slot_name}")
                return False
            
            # Initialize progression systems with loaded data
            self._initialize_progression_systems(save_data)
            
            # Start session tracking
            self._start_new_session(save_data.player_profile.name)
            
            # Create session backup
            self.backup_manager.create_backup(BackupType.SESSION_START, description="Game loaded")
            
            self.logger.info(f"Game loaded successfully for player: {save_data.player_profile.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load game: {e}")
            return False
    
    def save_game(self, slot_name: str = "quicksave", create_backup: bool = True) -> bool:
        """
        Save current game state.
        
        Args:
            slot_name: Save slot to save to
            create_backup: Whether to create a backup
        
        Returns:
            True if successful
        """
        try:
            # Update save data with current progression state
            self._update_save_data_from_progression_systems()
            
            # Save game
            success = self.save_system.save_game(slot_name)
            
            if success:
                # Create backup if requested
                if create_backup:
                    self.backup_manager.create_backup(BackupType.MANUAL, description="Manual save")
                
                # Trigger save event
                self._trigger_event("save_completed", {"slot_name": slot_name, "success": True})
                
                self.logger.info(f"Game saved successfully to slot: {slot_name}")
            else:
                self.logger.error(f"Failed to save game to slot: {slot_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False
    
    def record_battle_result(self, won: bool, enemy_type: str = "unknown", 
                           damage_dealt: int = 0, damage_taken: int = 0,
                           cards_played: List[str] = None) -> Dict[str, Any]:
        """
        Record the result of a battle and handle all related progression.
        
        Args:
            won: Whether the battle was won
            enemy_type: Type of enemy fought
            damage_dealt: Total damage dealt in battle
            damage_taken: Total damage taken in battle
            cards_played: List of card IDs played during battle
        
        Returns:
            Dictionary containing all progression results
        """
        if not self.save_system.current_save:
            return {"error": "No active save"}
        
        self.logger.info(f"Recording battle result: {'Victory' if won else 'Defeat'} vs {enemy_type}")
        
        # Update session tracking
        if self.current_session:
            self.current_session.battles_this_session += 1
        
        # Record battle in save system
        battle_result = self.save_system.record_battle_result(won, enemy_type)
        
        # Update achievement statistics
        if self.achievement_manager:
            stats_updates = {
                "total_wins" if won else "total_losses": 1,
                "battles_fought": 1,
                "damage_dealt": damage_dealt,
                "damage_taken": damage_taken
            }
            
            if won:
                stats_updates["current_win_streak"] = self.save_system.current_save.player_profile.win_streak
                stats_updates["best_win_streak"] = self.save_system.current_save.player_profile.best_win_streak
            
            if cards_played:
                stats_updates["total_cards_played"] = len(cards_played)
            
            # Update stats and check for achievements
            newly_completed = set()
            for stat, value in stats_updates.items():
                completed = self.achievement_manager.update_stat(stat, value, increment=True)
                newly_completed.update(completed)
            
            # Process newly completed achievements
            achievement_rewards = []
            for achievement_id in newly_completed:
                reward_bundle = self.achievement_manager.get_achievement_rewards(achievement_id)
                achievement_rewards.append(reward_bundle)
                
                if self.current_session:
                    self.current_session.achievements_earned_this_session.append(achievement_id)
                
                self._trigger_event("achievement_earned", {
                    "achievement_id": achievement_id,
                    "rewards": reward_bundle
                })
        
        # Generate battle rewards if won
        battle_rewards = None
        if won and self.reward_system:
            win_streak = self.save_system.current_save.player_profile.win_streak
            daily_wins = self.save_system.current_save.progression.daily_wins
            
            battle_rewards = self.reward_system.generate_combat_victory_rewards(
                enemy_difficulty=1,  # Would be determined by enemy type
                win_streak=win_streak,
                daily_wins=daily_wins,
                chamber_type="normal"
            )
            
            # Award card rewards to collection
            if self.player_collection and battle_rewards.get_cards():
                for card_id in battle_rewards.get_cards():
                    self.player_collection.add_card(card_id)
                    
                    if self.current_session:
                        self.current_session.cards_discovered_this_session.append(card_id)
                    
                    self._trigger_event("card_discovered", {"card_id": card_id})
        
        # Check for level up
        level_up_result = None
        if battle_result.get("xp_result", {}).get("level_up", False):
            if self.current_session:
                self.current_session.xp_gained_this_session += battle_result["xp_result"]["xp_gained"]
            
            level_up_result = self.reward_system.generate_level_up_rewards(
                battle_result["xp_result"]["new_level"]
            ) if self.reward_system else None
            
            self._trigger_event("level_up", {
                "old_level": battle_result["xp_result"]["old_level"],
                "new_level": battle_result["xp_result"]["new_level"],
                "rewards": level_up_result
            })
        
        # Trigger battle event
        self._trigger_event("battle_won" if won else "battle_lost", {
            "enemy_type": enemy_type,
            "battle_result": battle_result,
            "rewards": battle_rewards
        })
        
        # Auto-save after significant events
        self._check_auto_save()
        
        return {
            "battle_result": battle_result,
            "battle_rewards": battle_rewards,
            "level_up_result": level_up_result,
            "achievements_earned": list(newly_completed) if 'newly_completed' in locals() else [],
            "session_stats": self._get_session_stats()
        }
    
    def complete_chamber(self, chamber_id: str, completion_time: float = 0.0) -> Dict[str, Any]:
        """
        Record chamber completion and handle all related progression.
        
        Args:
            chamber_id: ID of completed chamber
            completion_time: Time taken to complete in seconds
        
        Returns:
            Dictionary containing progression results
        """
        if not self.save_system.current_save:
            return {"error": "No active save"}
        
        self.logger.info(f"Recording chamber completion: {chamber_id}")
        
        # Record completion in save system
        completion_result = self.save_system.complete_chamber(chamber_id)
        
        # Update session tracking
        if self.current_session:
            self.current_session.chambers_completed_this_session.append(chamber_id)
        
        # Generate chamber rewards
        chamber_rewards = None
        if self.reward_system:
            chamber_rewards = self.reward_system.generate_chamber_completion_rewards(
                chamber_id, 
                first_completion=not completion_result.get("already_completed", False)
            )
            
            # Award rewards to collection
            if self.player_collection and chamber_rewards.get_cards():
                for card_id in chamber_rewards.get_cards():
                    self.player_collection.add_card(card_id)
                    self._trigger_event("card_discovered", {"card_id": card_id})
        
        # Update achievement progress
        if self.achievement_manager:
            completed_achievements = self.achievement_manager.update_stat(
                "chambers_completed", 
                self.save_system.current_save.progression.chambers_completed
            )
            
            # Check for speed run achievements
            if completion_time > 0:
                self.achievement_manager.update_stat("completion_time", completion_time)
        
        # Create progression backup
        self.backup_manager.create_backup(
            BackupType.PROGRESSION, 
            description=f"Chamber {chamber_id} completed"
        )
        
        # Trigger chamber completion event
        self._trigger_event("chamber_completed", {
            "chamber_id": chamber_id,
            "completion_result": completion_result,
            "rewards": chamber_rewards,
            "completion_time": completion_time
        })
        
        # Auto-save
        self._check_auto_save()
        
        return {
            "completion_result": completion_result,
            "chamber_rewards": chamber_rewards,
            "session_stats": self._get_session_stats()
        }
    
    def update(self, delta_time: float) -> None:
        """
        Update progression manager (called each frame).
        
        Args:
            delta_time: Time since last update in seconds
        """
        # Check for auto-save
        self._check_auto_save()
        
        # Check for backup maintenance
        self._check_backup_maintenance()
        
        # Update playtime
        if self.save_system.current_save:
            self.save_system.current_save.player_profile.playtime_hours += delta_time / 3600
    
    def get_progression_summary(self) -> Dict[str, Any]:
        """Get comprehensive progression summary for UI display."""
        if not self.save_system.current_save:
            return {"error": "No active save"}
        
        summary = self.save_system.get_save_summary()
        
        # Add achievement summary
        if self.achievement_manager:
            summary["achievements"] = self.achievement_manager.get_achievement_summary()
        
        # Add collection summary
        if self.player_collection:
            summary["collection"] = self.player_collection.get_collection_stats()
        
        # Add backup summary
        summary["backups"] = self.backup_manager.get_backup_summary()
        
        # Add session summary
        if self.current_session:
            summary["current_session"] = self._get_session_stats()
        
        return summary
    
    def _initialize_progression_systems(self, save_data: SaveData) -> None:
        """Initialize all progression systems with save data."""
        # Initialize player collection
        if "card_collection" in save_data.__dict__:
            self.player_collection = PlayerCollection.from_dict(save_data.card_collection.__dict__)
        else:
            self.player_collection = PlayerCollection()
        
        # Initialize reward system
        self.reward_system = ProgressionRewardSystem(self.player_collection)
        
        # Initialize achievement manager
        self.achievement_manager = AchievementManager(self.reward_system)
        
        # Load achievement progress if available
        if hasattr(save_data.progression, 'achievement_data'):
            self.achievement_manager = AchievementManager.from_dict(
                save_data.progression.achievement_data, 
                self.reward_system
            )
        
        self.logger.info("Progression systems initialized")
    
    def _start_new_session(self, player_name: str) -> None:
        """Start tracking a new game session."""
        self.current_session = GameSession(
            session_id=f"{player_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            start_time=datetime.now(),
            player_name=player_name
        )
        
        self.logger.info(f"Started new session: {self.current_session.session_id}")
    
    def _update_save_data_from_progression_systems(self) -> None:
        """Update save data with current state from progression systems."""
        if not self.save_system.current_save:
            return
        
        # Update player collection
        if self.player_collection:
            collection_dict = self.player_collection.to_dict()
            for key, value in collection_dict.items():
                if hasattr(self.save_system.current_save.card_collection, key):
                    setattr(self.save_system.current_save.card_collection, key, value)
        
        # Update achievement data
        if self.achievement_manager:
            achievement_dict = self.achievement_manager.to_dict()
            self.save_system.current_save.progression.__dict__["achievement_data"] = achievement_dict
    
    def _check_auto_save(self) -> None:
        """Check if auto-save should be performed."""
        now = datetime.now()
        time_since_save = (now - self.last_auto_save).total_seconds()
        
        if time_since_save >= self.auto_save_interval:
            if self.save_system.auto_save():
                self.last_auto_save = now
                self._trigger_event("save_completed", {"type": "auto_save", "success": True})
    
    def _check_backup_maintenance(self) -> None:
        """Check if backup maintenance should be performed."""
        now = datetime.now()
        time_since_check = (now - self.last_backup_check).total_seconds()
        
        if time_since_check >= self.backup_check_interval:
            # This could trigger cleanup, create scheduled backups, etc.
            self.last_backup_check = now
    
    def _get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics."""
        if not self.current_session:
            return {}
        
        session_duration = datetime.now() - self.current_session.start_time
        
        return {
            "session_id": self.current_session.session_id,
            "duration_minutes": session_duration.total_seconds() / 60,
            "battles_fought": self.current_session.battles_this_session,
            "xp_gained": self.current_session.xp_gained_this_session,
            "cards_discovered": len(self.current_session.cards_discovered_this_session),
            "achievements_earned": len(self.current_session.achievements_earned_this_session),
            "chambers_completed": len(self.current_session.chambers_completed_this_session)
        }
    
    def _trigger_event(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Trigger an event to registered handlers."""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    handler(event_data)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_name}: {e}")
    
    def add_event_handler(self, event_name: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Add an event handler."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)
    
    def remove_event_handler(self, event_name: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Remove an event handler."""
        if event_name in self.event_handlers and handler in self.event_handlers[event_name]:
            self.event_handlers[event_name].remove(handler)


# Global progression manager instance
_progression_manager: Optional[GameProgressionManager] = None


def get_progression_manager() -> GameProgressionManager:
    """Get the global progression manager instance."""
    global _progression_manager
    if _progression_manager is None:
        _progression_manager = GameProgressionManager()
    return _progression_manager


def init_progression_manager() -> GameProgressionManager:
    """Initialize the global progression manager."""
    global _progression_manager
    _progression_manager = GameProgressionManager()
    return _progression_manager