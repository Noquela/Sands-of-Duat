"""
Egyptian-Themed Achievement System for Sands of Duat

Comprehensive achievement tracking with Egyptian mythology themes,
progress monitoring, and reward integration.
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from .progression_rewards import ProgressionRewardSystem, RewardBundle, EgyptianAchievementSystem


class AchievementCategory(Enum):
    """Categories for organizing achievements."""
    COMBAT = "combat"
    COLLECTION = "collection"
    EXPLORATION = "exploration"
    DEVOTION = "devotion"
    MASTERY = "mastery"
    SPECIAL = "special"
    HIDDEN = "hidden"


class AchievementDifficulty(Enum):
    """Difficulty levels for achievements."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIVINE = "divine"


@dataclass
class AchievementProgress:
    """Tracks progress for a specific achievement."""
    achievement_id: str
    current_value: float = 0.0
    target_value: float = 0.0
    progress_percentage: float = 0.0
    is_completed: bool = False
    completed_at: Optional[str] = None
    last_updated: str = ""
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()
    
    def update_progress(self, new_value: float) -> bool:
        """
        Update progress and return True if achievement was just completed.
        """
        old_completed = self.is_completed
        self.current_value = new_value
        self.progress_percentage = min(100.0, (self.current_value / self.target_value) * 100) if self.target_value > 0 else 0.0
        self.last_updated = datetime.now().isoformat()
        
        if not self.is_completed and self.current_value >= self.target_value:
            self.is_completed = True
            self.completed_at = datetime.now().isoformat()
            return True  # Just completed
        
        return False


@dataclass
class Achievement:
    """Egyptian-themed achievement definition."""
    id: str
    name: str
    description: str
    category: AchievementCategory
    difficulty: AchievementDifficulty
    
    # Progress tracking
    target_value: float = 1.0
    progress_type: str = "count"  # count, boolean, time, percentage
    
    # Visibility and rewards
    hidden: bool = False
    secret: bool = False  # Hidden until discovered
    repeatable: bool = False
    
    # Egyptian theming
    deity_association: str = ""  # Ra, Anubis, Isis, etc.
    hieroglyph_symbol: str = ""
    lore_text: str = ""
    
    # Rewards
    xp_reward: int = 100
    card_rewards: List[str] = field(default_factory=list)
    title_reward: str = ""
    unlock_rewards: List[str] = field(default_factory=list)
    
    # Requirements and dependencies
    prerequisites: List[str] = field(default_factory=list)
    mutually_exclusive: List[str] = field(default_factory=list)


class AchievementManager:
    """
    Manages achievement tracking, progress updates, and rewards.
    """
    
    def __init__(self, reward_system: ProgressionRewardSystem):
        self.logger = logging.getLogger(__name__)
        self.reward_system = reward_system
        self.egyptian_achievements = EgyptianAchievementSystem()
        
        # Achievement definitions
        self.achievements: Dict[str, Achievement] = {}
        self.achievement_progress: Dict[str, AchievementProgress] = {}
        
        # Event handlers for achievement triggers
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Statistics tracking
        self.player_stats: Dict[str, Any] = defaultdict(int)
        
        self._initialize_achievements()
        self.logger.info("Achievement manager initialized with Egyptian themes")
    
    def _initialize_achievements(self) -> None:
        """Initialize all Egyptian-themed achievements."""
        
        # COMBAT ACHIEVEMENTS - Warriors of the Sands
        self.add_achievement(Achievement(
            id="anubis_first_victory",
            name="Anubis' First Blessing",
            description="Win your first battle in the temple",
            category=AchievementCategory.COMBAT,
            difficulty=AchievementDifficulty.BRONZE,
            target_value=1,
            deity_association="Anubis",
            hieroglyph_symbol="𓄿",
            lore_text="Anubis, guardian of the afterlife, smiles upon your first victory.",
            xp_reward=100,
            card_rewards=["anubis_blessing"],
            title_reward="Anubis' Chosen"
        ))
        
        self.add_achievement(Achievement(
            id="ra_victory_streak",
            name="Ra's Eternal Flame",
            description="Achieve a 10-win streak like the eternal sun",
            category=AchievementCategory.COMBAT,
            difficulty=AchievementDifficulty.SILVER,
            target_value=10,
            progress_type="streak",
            deity_association="Ra",
            hieroglyph_symbol="☉",
            lore_text="Like Ra's journey across the sky, your victories shine without end.",
            xp_reward=500,
            card_rewards=["ra_eternal_flame", "solar_victory"],
            title_reward="Sun Warrior"
        ))
        
        self.add_achievement(Achievement(
            id="horus_champion",
            name="Horus the Avenger",
            description="Defeat 100 enemies with the eye of Horus watching",
            category=AchievementCategory.COMBAT,
            difficulty=AchievementDifficulty.GOLD,
            target_value=100,
            deity_association="Horus",
            hieroglyph_symbol="𓅃",
            lore_text="Horus grants you his divine sight to see victory in every battle.",
            xp_reward=1000,
            card_rewards=["horus_eye", "divine_sight", "victory_falcon"],
            title_reward="Eye of Horus"
        ))
        
        self.add_achievement(Achievement(
            id="pharaoh_slayer",
            name="Usurper of the Divine Throne",
            description="Defeat the Pharaoh in final combat",
            category=AchievementCategory.COMBAT,
            difficulty=AchievementDifficulty.DIVINE,
            target_value=1,
            progress_type="boss_defeat",
            deity_association="Pharaoh",
            hieroglyph_symbol="👑",
            lore_text="You have challenged the gods themselves and emerged victorious.",
            xp_reward=2000,
            card_rewards=["pharaoh_crown", "divine_authority", "usurper_seal"],
            title_reward="God-Slayer",
            prerequisites=["horus_champion"]
        ))
        
        # COLLECTION ACHIEVEMENTS - Keepers of Ancient Wisdom
        self.add_achievement(Achievement(
            id="thoth_scribe",
            name="Thoth's Sacred Scribe",
            description="Collect 50 unique cards, recording ancient wisdom",
            category=AchievementCategory.COLLECTION,
            difficulty=AchievementDifficulty.BRONZE,
            target_value=50,
            progress_type="unique_cards",
            deity_association="Thoth",
            hieroglyph_symbol="𓁟",
            lore_text="Thoth, keeper of divine knowledge, entrusts you with sacred wisdom.",
            xp_reward=300,
            card_rewards=["thoth_wisdom", "scribe_tools"],
            title_reward="Sacred Scribe"
        ))
        
        self.add_achievement(Achievement(
            id="isis_collector",
            name="Isis' Complete Magic",
            description="Collect all cards of each rarity tier",
            category=AchievementCategory.COLLECTION,
            difficulty=AchievementDifficulty.GOLD,
            target_value=100,  # All cards
            progress_type="collection_complete",
            deity_association="Isis",
            hieroglyph_symbol="𓅿",
            lore_text="Isis, mistress of magic, recognizes your mastery over all forms of power.",
            xp_reward=1500,
            card_rewards=["isis_complete_magic", "magical_mastery"],
            title_reward="Master of All Magic"
        ))
        
        self.add_achievement(Achievement(
            id="legendary_guardian",
            name="Guardian of Legendary Artifacts",
            description="Collect all legendary cards",
            category=AchievementCategory.COLLECTION,
            difficulty=AchievementDifficulty.PLATINUM,
            target_value=1,
            progress_type="legendary_complete",
            deity_association="Ptah",
            hieroglyph_symbol="𓊪",
            lore_text="Ptah, creator of all things, entrusts you with the most powerful artifacts.",
            xp_reward=2500,
            card_rewards=["legendary_vault", "ptah_creation"],
            title_reward="Legendary Guardian"
        ))
        
        # EXPLORATION ACHIEVEMENTS - Masters of the Temple
        self.add_achievement(Achievement(
            id="temple_initiate",
            name="Temple Initiate",
            description="Complete the entrance chamber",
            category=AchievementCategory.EXPLORATION,
            difficulty=AchievementDifficulty.BRONZE,
            target_value=1,
            progress_type="chamber_complete",
            hieroglyph_symbol="🏛️",
            lore_text="You have taken your first steps into the sacred temple.",
            xp_reward=100,
            card_rewards=["temple_blessing"],
            title_reward="Temple Seeker"
        ))
        
        self.add_achievement(Achievement(
            id="osiris_journey",
            name="Osiris' Sacred Journey",
            description="Complete all temple chambers",
            category=AchievementCategory.EXPLORATION,
            difficulty=AchievementDifficulty.GOLD,
            target_value=7,  # All chambers
            progress_type="chambers_complete",
            deity_association="Osiris",
            hieroglyph_symbol="𓁹",
            lore_text="Like Osiris through death and rebirth, you have journeyed through all trials.",
            xp_reward=1000,
            card_rewards=["osiris_journey", "sacred_path", "temple_mastery"],
            title_reward="Temple Master",
            prerequisites=["temple_initiate"]
        ))
        
        self.add_achievement(Achievement(
            id="speed_of_mercury",
            name="Swift as Thoth's Ibis",
            description="Complete the temple in under 2 hours",
            category=AchievementCategory.EXPLORATION,
            difficulty=AchievementDifficulty.PLATINUM,
            target_value=7200,  # 2 hours in seconds
            progress_type="completion_time",
            hidden=True,
            deity_association="Thoth",
            hieroglyph_symbol="𓅞",
            lore_text="With the speed of Thoth's sacred ibis, you have mastered time itself.",
            xp_reward=2000,
            card_rewards=["time_mastery", "swift_victory"],
            title_reward="Master of Time"
        ))
        
        # DEVOTION ACHIEVEMENTS - Faithful Servants
        self.add_achievement(Achievement(
            id="daily_devotion",
            name="Daily Devotion to the Gods",
            description="Play for 7 consecutive days",
            category=AchievementCategory.DEVOTION,
            difficulty=AchievementDifficulty.SILVER,
            target_value=7,
            progress_type="consecutive_days",
            hieroglyph_symbol="🌅",
            lore_text="Your daily prayers to the gods have not gone unnoticed.",
            xp_reward=500,
            card_rewards=["devotion_blessing", "daily_prayer"],
            title_reward="Devoted Servant"
        ))
        
        self.add_achievement(Achievement(
            id="eternal_guardian",
            name="Eternal Guardian of the Sands",
            description="Play for 100 total hours",
            category=AchievementCategory.DEVOTION,
            difficulty=AchievementDifficulty.PLATINUM,
            target_value=100,
            progress_type="playtime_hours",
            hieroglyph_symbol="⏳",
            lore_text="You have become one with the eternal sands, a guardian for all time.",
            xp_reward=3000,
            card_rewards=["eternal_blessing", "sand_mastery", "guardian_power"],
            title_reward="Eternal Guardian"
        ))
        
        # MASTERY ACHIEVEMENTS - Divine Skills
        self.add_achievement(Achievement(
            id="deck_architect",
            name="Master Deck Architect",
            description="Create 15 different deck configurations",
            category=AchievementCategory.MASTERY,
            difficulty=AchievementDifficulty.SILVER,
            target_value=15,
            progress_type="decks_created",
            hieroglyph_symbol="📜",
            lore_text="Your architectural skill rivals the builders of the great pyramids.",
            xp_reward=800,
            card_rewards=["architect_tools", "deck_mastery"],
            title_reward="Deck Architect"
        ))
        
        self.add_achievement(Achievement(
            id="perfect_balance",
            name="Ma'at's Perfect Balance",
            description="Win 100 battles with exactly 1 health remaining",
            category=AchievementCategory.MASTERY,
            difficulty=AchievementDifficulty.GOLD,
            target_value=100,
            progress_type="narrow_victories",
            hidden=True,
            deity_association="Ma'at",
            hieroglyph_symbol="⚖️",
            lore_text="Ma'at recognizes your perfect balance between life and death.",
            xp_reward=1500,
            card_rewards=["perfect_balance", "maat_feather"],
            title_reward="Master of Balance"
        ))
        
        # SPECIAL ACHIEVEMENTS - Legendary Feats
        self.add_achievement(Achievement(
            id="perfectionist",
            name="Divine Perfection",
            description="Complete the temple without losing a single battle",
            category=AchievementCategory.SPECIAL,
            difficulty=AchievementDifficulty.DIVINE,
            target_value=1,
            progress_type="perfect_run",
            secret=True,
            hieroglyph_symbol="✨",
            lore_text="You have achieved perfection worthy of the gods themselves.",
            xp_reward=5000,
            card_rewards=["divine_perfection", "flawless_victory", "god_blessing"],
            title_reward="Divine Perfectionist"
        ))
        
        self.add_achievement(Achievement(
            id="card_master",
            name="Supreme Card Master",
            description="Play 10,000 cards in total",
            category=AchievementCategory.SPECIAL,
            difficulty=AchievementDifficulty.PLATINUM,
            target_value=10000,
            progress_type="cards_played",
            repeatable=True,
            hieroglyph_symbol="🃏",
            lore_text="Your mastery over the ancient cards is unparalleled.",
            xp_reward=2000,
            card_rewards=["card_mastery", "supreme_power"],
            title_reward="Supreme Card Master"
        ))
        
        # HIDDEN ACHIEVEMENTS - Secrets of the Temple
        self.add_achievement(Achievement(
            id="secret_chamber",
            name="Discoverer of Hidden Truths",
            description="Find and complete the secret chamber",
            category=AchievementCategory.HIDDEN,
            difficulty=AchievementDifficulty.DIVINE,
            target_value=1,
            progress_type="secret_found",
            secret=True,
            hidden=True,
            hieroglyph_symbol="🔍",
            lore_text="You have uncovered secrets that were meant to remain hidden.",
            xp_reward=3000,
            card_rewards=["hidden_knowledge", "secret_power"],
            title_reward="Keeper of Secrets"
        ))
    
    def add_achievement(self, achievement: Achievement) -> None:
        """Add an achievement to the system."""
        self.achievements[achievement.id] = achievement
        if achievement.id not in self.achievement_progress:
            self.achievement_progress[achievement.id] = AchievementProgress(
                achievement_id=achievement.id,
                target_value=achievement.target_value
            )
        
        self.logger.debug(f"Added achievement: {achievement.name}")
    
    def update_stat(self, stat_name: str, value: Any, increment: bool = True) -> Set[str]:
        """
        Update a player statistic and check for achievement completions.
        
        Returns:
            Set of achievement IDs that were just completed.
        """
        if increment and isinstance(value, (int, float)):
            self.player_stats[stat_name] += value
        else:
            self.player_stats[stat_name] = value
        
        # Check all achievements for completions
        newly_completed = set()
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in self.achievement_progress:
                progress = self.achievement_progress[achievement_id]
                
                if not progress.is_completed:
                    current_value = self._get_current_value_for_achievement(achievement)
                    if progress.update_progress(current_value):
                        newly_completed.add(achievement_id)
                        self.logger.info(f"Achievement completed: {achievement.name}")
        
        return newly_completed
    
    def _get_current_value_for_achievement(self, achievement: Achievement) -> float:
        """Get current progress value for an achievement."""
        progress_type = achievement.progress_type
        
        if progress_type == "count" or progress_type == "wins":
            return self.player_stats.get("total_wins", 0)
        
        elif progress_type == "streak":
            return self.player_stats.get("best_win_streak", 0)
        
        elif progress_type == "unique_cards":
            return self.player_stats.get("unique_cards_owned", 0)
        
        elif progress_type == "collection_complete":
            return self.player_stats.get("collection_completion_percentage", 0)
        
        elif progress_type == "legendary_complete":
            total_legendary = self.player_stats.get("total_legendary_cards", 10)
            owned_legendary = self.player_stats.get("legendary_cards_owned", 0)
            return 1.0 if owned_legendary >= total_legendary else 0.0
        
        elif progress_type == "chamber_complete":
            return 1.0 if achievement.id.replace("_complete", "") in self.player_stats.get("chambers_completed", set()) else 0.0
        
        elif progress_type == "chambers_complete":
            return len(self.player_stats.get("chambers_completed", set()))
        
        elif progress_type == "consecutive_days":
            return self.player_stats.get("consecutive_login_days", 0)
        
        elif progress_type == "playtime_hours":
            return self.player_stats.get("playtime_hours", 0)
        
        elif progress_type == "decks_created":
            return len(self.player_stats.get("saved_decks", {}))
        
        elif progress_type == "cards_played":
            return self.player_stats.get("total_cards_played", 0)
        
        elif progress_type == "boss_defeat":
            boss_defeats = self.player_stats.get("boss_defeats", {})
            boss_name = achievement.id.split("_")[0]  # Extract boss name from achievement ID
            return 1.0 if boss_defeats.get(boss_name, 0) > 0 else 0.0
        
        elif progress_type == "perfect_run":
            return 1.0 if self.player_stats.get("perfect_run_completed", False) else 0.0
        
        elif progress_type == "completion_time":
            best_time = self.player_stats.get("best_completion_time", float('inf'))
            return achievement.target_value - best_time if best_time <= achievement.target_value else 0.0
        
        elif progress_type == "narrow_victories":
            return self.player_stats.get("narrow_victories", 0)
        
        elif progress_type == "secret_found":
            return 1.0 if self.player_stats.get("secret_chamber_found", False) else 0.0
        
        return 0.0
    
    def get_achievement_rewards(self, achievement_id: str) -> RewardBundle:
        """Generate reward bundle for completed achievement."""
        if achievement_id not in self.achievements:
            return RewardBundle(source=f"unknown_achievement_{achievement_id}")
        
        achievement = self.achievements[achievement_id]
        return self.reward_system.generate_achievement_rewards(achievement_id)
    
    def get_achievements_by_category(self, category: AchievementCategory, include_hidden: bool = False) -> List[Achievement]:
        """Get achievements filtered by category."""
        achievements = []
        for achievement in self.achievements.values():
            if achievement.category == category:
                if include_hidden or not achievement.hidden:
                    achievements.append(achievement)
        
        return sorted(achievements, key=lambda a: a.difficulty.value)
    
    def get_completed_achievements(self) -> List[Achievement]:
        """Get all completed achievements."""
        completed = []
        for achievement_id, progress in self.achievement_progress.items():
            if progress.is_completed:
                completed.append(self.achievements[achievement_id])
        
        return sorted(completed, key=lambda a: a.completed_at or "")
    
    def get_achievement_summary(self) -> Dict[str, Any]:
        """Get comprehensive achievement statistics."""
        total_achievements = len(self.achievements)
        completed_count = sum(1 for p in self.achievement_progress.values() if p.is_completed)
        
        # Count by category
        category_stats = {}
        for category in AchievementCategory:
            category_achievements = self.get_achievements_by_category(category, include_hidden=True)
            completed_in_category = sum(
                1 for a in category_achievements 
                if self.achievement_progress[a.id].is_completed
            )
            
            category_stats[category.value] = {
                "total": len(category_achievements),
                "completed": completed_in_category,
                "percentage": (completed_in_category / len(category_achievements) * 100) if category_achievements else 0
            }
        
        # Count by difficulty
        difficulty_stats = {}
        for difficulty in AchievementDifficulty:
            difficulty_achievements = [a for a in self.achievements.values() if a.difficulty == difficulty]
            completed_in_difficulty = sum(
                1 for a in difficulty_achievements 
                if self.achievement_progress[a.id].is_completed
            )
            
            difficulty_stats[difficulty.value] = {
                "total": len(difficulty_achievements),
                "completed": completed_in_difficulty
            }
        
        # Recent completions
        recent_completions = []
        for achievement_id, progress in self.achievement_progress.items():
            if progress.is_completed and progress.completed_at:
                completion_time = datetime.fromisoformat(progress.completed_at)
                if datetime.now() - completion_time < timedelta(days=7):  # Last 7 days
                    recent_completions.append({
                        "achievement": self.achievements[achievement_id],
                        "completed_at": progress.completed_at
                    })
        
        recent_completions.sort(key=lambda x: x["completed_at"], reverse=True)
        
        return {
            "total_achievements": total_achievements,
            "completed_count": completed_count,
            "completion_percentage": (completed_count / total_achievements * 100) if total_achievements > 0 else 0,
            "category_stats": category_stats,
            "difficulty_stats": difficulty_stats,
            "recent_completions": recent_completions[:5],  # Last 5 recent completions
            "achievement_points": sum(a.xp_reward for a in self.get_completed_achievements())
        }
    
    def get_progress_for_achievement(self, achievement_id: str) -> Optional[AchievementProgress]:
        """Get progress information for a specific achievement."""
        return self.achievement_progress.get(achievement_id)
    
    def check_prerequisites(self, achievement_id: str) -> bool:
        """Check if all prerequisites for an achievement are met."""
        if achievement_id not in self.achievements:
            return False
        
        achievement = self.achievements[achievement_id]
        
        for prereq_id in achievement.prerequisites:
            if prereq_id not in self.achievement_progress:
                return False
            if not self.achievement_progress[prereq_id].is_completed:
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize achievement data for saving."""
        return {
            "achievement_progress": {
                aid: {
                    "current_value": p.current_value,
                    "is_completed": p.is_completed,
                    "completed_at": p.completed_at,
                    "last_updated": p.last_updated
                } for aid, p in self.achievement_progress.items()
            },
            "player_stats": dict(self.player_stats)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], reward_system: ProgressionRewardSystem) -> 'AchievementManager':
        """Load achievement data from save."""
        manager = cls(reward_system)
        
        # Load progress
        if "achievement_progress" in data:
            for aid, progress_data in data["achievement_progress"].items():
                if aid in manager.achievement_progress:
                    progress = manager.achievement_progress[aid]
                    progress.current_value = progress_data.get("current_value", 0.0)
                    progress.is_completed = progress_data.get("is_completed", False)
                    progress.completed_at = progress_data.get("completed_at")
                    progress.last_updated = progress_data.get("last_updated", "")
        
        # Load stats
        if "player_stats" in data:
            manager.player_stats.update(data["player_stats"])
        
        return manager