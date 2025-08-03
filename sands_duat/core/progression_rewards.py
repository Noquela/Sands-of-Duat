"""
Progression Rewards System for Sands of Duat

Manages player rewards, XP progression, card unlocks, and Egyptian-themed
achievements. Integrates with the save system and player collection.
"""

import random
import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from .cards import Card, CardLibrary, CardRarity, CardType
from .player_collection import PlayerCollection, CardRewardSystem


class RewardType(Enum):
    """Types of rewards that can be awarded."""
    XP = "xp"
    CARDS = "cards"
    CARD_PACK = "card_pack"
    DECK_SLOT = "deck_slot"
    CHAMBER_UNLOCK = "chamber_unlock"
    CARD_POOL_UNLOCK = "card_pool_unlock"
    ACHIEVEMENT = "achievement"
    TITLE = "title"
    COSMETIC = "cosmetic"


class RewardRarity(Enum):
    """Rarity levels for rewards."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class Reward:
    """Individual reward item."""
    type: RewardType
    rarity: RewardRarity
    value: Any  # XP amount, card ID, unlock name, etc.
    quantity: int = 1
    display_name: str = ""
    description: str = ""
    icon: str = ""
    
    def __post_init__(self):
        if not self.display_name:
            self.display_name = self._generate_display_name()
    
    def _generate_display_name(self) -> str:
        """Generate display name based on reward type."""
        if self.type == RewardType.XP:
            return f"{self.value} XP"
        elif self.type == RewardType.CARDS:
            return f"{self.quantity}x {self.value}"
        elif self.type == RewardType.CARD_PACK:
            return f"{self.value} Card Pack"
        elif self.type == RewardType.CHAMBER_UNLOCK:
            return f"Unlocked: {self.value}"
        else:
            return str(self.value)


@dataclass
class RewardBundle:
    """Collection of rewards for a specific event."""
    source: str  # What triggered this reward
    rewards: List[Reward] = field(default_factory=list)
    timestamp: str = ""
    bonus_multiplier: float = 1.0
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def get_total_xp(self) -> int:
        """Get total XP from this bundle."""
        total = 0
        for reward in self.rewards:
            if reward.type == RewardType.XP:
                total += int(reward.value * self.bonus_multiplier)
        return total
    
    def get_cards(self) -> List[str]:
        """Get all card IDs from this bundle."""
        cards = []
        for reward in self.rewards:
            if reward.type == RewardType.CARDS:
                cards.extend([reward.value] * reward.quantity)
        return cards


class ProgressionRewardSystem:
    """
    Manages player progression rewards and XP system.
    """
    
    def __init__(self, player_collection: PlayerCollection):
        self.logger = logging.getLogger(__name__)
        self.player_collection = player_collection
        self.card_reward_system = CardRewardSystem(player_collection)
        
        # XP and leveling configuration
        self.base_xp_per_level = 1000
        self.xp_scaling_factor = 1.15  # Each level requires 15% more XP
        self.max_level = 100
        
        # Reward multipliers
        self.streak_multipliers = {
            5: 1.2,   # 20% bonus at 5 wins
            10: 1.5,  # 50% bonus at 10 wins
            15: 2.0,  # 100% bonus at 15 wins
            25: 3.0   # 200% bonus at 25 wins
        }
        
        # Daily/weekly bonuses
        self.daily_win_bonus = {
            1: 1.1, 3: 1.2, 5: 1.3, 10: 1.5
        }
        
        self.logger.info("Progression reward system initialized")
    
    def calculate_xp_for_level(self, level: int) -> int:
        """Calculate total XP required to reach a specific level."""
        if level <= 1:
            return 0
        
        total_xp = 0
        for lvl in range(2, level + 1):
            level_xp = int(self.base_xp_per_level * (self.xp_scaling_factor ** (lvl - 2)))
            total_xp += level_xp
        
        return total_xp
    
    def calculate_level_from_xp(self, xp: int) -> Tuple[int, int, int]:
        """
        Calculate level, current level XP, and XP needed for next level.
        
        Returns:
            (current_level, xp_in_current_level, xp_needed_for_next)
        """
        level = 1
        total_xp_for_level = 0
        
        while level < self.max_level:
            next_level_xp = self.calculate_xp_for_level(level + 1)
            if xp < next_level_xp:
                break
            level += 1
            total_xp_for_level = next_level_xp
        
        # Calculate XP within current level
        xp_in_level = xp - total_xp_for_level
        xp_for_next_level = self.calculate_xp_for_level(level + 1) - total_xp_for_level
        xp_needed = xp_for_next_level - xp_in_level
        
        return level, xp_in_level, xp_needed
    
    def generate_combat_victory_rewards(self, 
                                      enemy_difficulty: int = 1,
                                      win_streak: int = 0,
                                      daily_wins: int = 0,
                                      chamber_type: str = "normal") -> RewardBundle:
        """Generate rewards for winning a combat."""
        bundle = RewardBundle(source=f"combat_victory_{chamber_type}")
        
        # Base XP reward
        base_xp = self._get_base_combat_xp(enemy_difficulty, chamber_type)
        
        # Apply multipliers
        multiplier = 1.0
        
        # Win streak bonus
        for streak_threshold in sorted(self.streak_multipliers.keys()):
            if win_streak >= streak_threshold:
                multiplier = self.streak_multipliers[streak_threshold]
        
        # Daily wins bonus
        for wins_threshold in sorted(self.daily_win_bonus.keys()):
            if daily_wins >= wins_threshold:
                multiplier *= self.daily_win_bonus[wins_threshold]
        
        bundle.bonus_multiplier = multiplier
        final_xp = int(base_xp * multiplier)
        
        # Add XP reward
        bundle.rewards.append(Reward(
            type=RewardType.XP,
            rarity=RewardRarity.COMMON,
            value=final_xp,
            description=f"Victory XP (x{multiplier:.1f} bonus)"
        ))
        
        # Generate card rewards
        card_rewards = self._generate_combat_card_rewards(enemy_difficulty, chamber_type)
        for card_id in card_rewards:
            bundle.rewards.append(Reward(
                type=RewardType.CARDS,
                rarity=self._get_card_rarity_enum(card_id),
                value=card_id,
                quantity=1,
                description="Victory spoils"
            ))
        
        # Chance for bonus rewards
        self._add_bonus_combat_rewards(bundle, win_streak, enemy_difficulty)
        
        self.logger.info(f"Generated combat victory rewards: {len(bundle.rewards)} items, {final_xp} XP")
        return bundle
    
    def generate_chamber_completion_rewards(self, chamber_id: str, first_completion: bool = True) -> RewardBundle:
        """Generate rewards for completing a chamber."""
        bundle = RewardBundle(source=f"chamber_completion_{chamber_id}")
        
        # Chamber-specific rewards
        chamber_data = self._get_chamber_reward_data(chamber_id)
        
        # XP reward
        xp_reward = chamber_data.get("xp", 200)
        if first_completion:
            xp_reward = int(xp_reward * 2)  # Double XP for first completion
        
        bundle.rewards.append(Reward(
            type=RewardType.XP,
            rarity=RewardRarity.UNCOMMON,
            value=xp_reward,
            description="Chamber mastery XP" if first_completion else "Chamber completion XP"
        ))
        
        # Guaranteed chamber cards
        guaranteed_cards = chamber_data.get("guaranteed_cards", [])
        for card_id in guaranteed_cards:
            bundle.rewards.append(Reward(
                type=RewardType.CARDS,
                rarity=self._get_card_rarity_enum(card_id),
                value=card_id,
                quantity=1,
                description="Chamber treasure"
            ))
        
        # Unlock rewards
        unlocks = chamber_data.get("unlocks", [])
        for unlock in unlocks:
            if unlock.startswith("chamber_"):
                bundle.rewards.append(Reward(
                    type=RewardType.CHAMBER_UNLOCK,
                    rarity=RewardRarity.RARE,
                    value=unlock,
                    description="New area discovered"
                ))
            elif unlock.startswith("pool_"):
                bundle.rewards.append(Reward(
                    type=RewardType.CARD_POOL_UNLOCK,
                    rarity=RewardRarity.EPIC,
                    value=unlock,
                    description="New cards available"
                ))
        
        # First completion bonus
        if first_completion:
            self._add_first_completion_bonus(bundle, chamber_id)
        
        self.logger.info(f"Generated chamber completion rewards for {chamber_id}: {len(bundle.rewards)} items")
        return bundle
    
    def generate_achievement_rewards(self, achievement_id: str) -> RewardBundle:
        """Generate rewards for earning an achievement."""
        bundle = RewardBundle(source=f"achievement_{achievement_id}")
        
        achievement_data = self._get_achievement_reward_data(achievement_id)
        
        # XP reward
        xp_reward = achievement_data.get("xp", 500)
        bundle.rewards.append(Reward(
            type=RewardType.XP,
            rarity=RewardRarity.RARE,
            value=xp_reward,
            description="Achievement mastery"
        ))
        
        # Special cards
        special_cards = achievement_data.get("cards", [])
        for card_id in special_cards:
            bundle.rewards.append(Reward(
                type=RewardType.CARDS,
                rarity=RewardRarity.LEGENDARY,
                value=card_id,
                quantity=1,
                description="Achievement reward"
            ))
        
        # Title unlock
        title = achievement_data.get("title")
        if title:
            bundle.rewards.append(Reward(
                type=RewardType.TITLE,
                rarity=RewardRarity.EPIC,
                value=title,
                description="Honorary title"
            ))
        
        self.logger.info(f"Generated achievement rewards for {achievement_id}")
        return bundle
    
    def generate_level_up_rewards(self, new_level: int) -> RewardBundle:
        """Generate rewards for leveling up."""
        bundle = RewardBundle(source=f"level_up_{new_level}")
        
        # Base level up rewards
        if new_level % 5 == 0:  # Every 5 levels
            # Card pack reward
            pack_rarity = "rare" if new_level % 10 == 0 else "uncommon"
            bundle.rewards.append(Reward(
                type=RewardType.CARD_PACK,
                rarity=RewardRarity.RARE if pack_rarity == "rare" else RewardRarity.UNCOMMON,
                value=f"egyptian_{pack_rarity}_pack",
                quantity=1,
                description=f"Level {new_level} reward pack"
            ))
        
        if new_level % 10 == 0:  # Every 10 levels
            # Unlock new card pool
            pool_name = f"level_{new_level}_pool"
            bundle.rewards.append(Reward(
                type=RewardType.CARD_POOL_UNLOCK,
                rarity=RewardRarity.EPIC,
                value=pool_name,
                description="Advanced cards unlocked"
            ))
        
        if new_level % 25 == 0:  # Every 25 levels
            # Special milestone rewards
            bundle.rewards.append(Reward(
                type=RewardType.DECK_SLOT,
                rarity=RewardRarity.LEGENDARY,
                value=1,
                description="Additional deck slot"
            ))
        
        # Egyptian level titles
        title = self._get_egyptian_level_title(new_level)
        if title:
            bundle.rewards.append(Reward(
                type=RewardType.TITLE,
                rarity=RewardRarity.UNCOMMON,
                value=title,
                description="Level milestone title"
            ))
        
        self.logger.info(f"Generated level up rewards for level {new_level}")
        return bundle
    
    def generate_daily_bonus_rewards(self, consecutive_days: int) -> RewardBundle:
        """Generate daily login bonus rewards."""
        bundle = RewardBundle(source=f"daily_bonus_day_{consecutive_days}")
        
        # Base daily XP
        base_xp = 100 + (consecutive_days * 10)
        bundle.rewards.append(Reward(
            type=RewardType.XP,
            rarity=RewardRarity.COMMON,
            value=base_xp,
            description="Daily devotion bonus"
        ))
        
        # Escalating rewards for consecutive days
        if consecutive_days % 7 == 0:  # Weekly milestone
            bundle.rewards.append(Reward(
                type=RewardType.CARD_PACK,
                rarity=RewardRarity.UNCOMMON,
                value="egyptian_common_pack",
                quantity=1,
                description="Weekly devotion reward"
            ))
        
        if consecutive_days % 30 == 0:  # Monthly milestone
            bundle.rewards.append(Reward(
                type=RewardType.CARDS,
                rarity=RewardRarity.LEGENDARY,
                value="pharaoh_blessing",
                quantity=1,
                description="Monthly devotion blessing"
            ))
        
        return bundle
    
    def _get_base_combat_xp(self, difficulty: int, chamber_type: str) -> int:
        """Calculate base XP for combat victory."""
        base_xp = {
            "tutorial": 25,
            "normal": 50,
            "elite": 75,
            "boss": 150,
            "final_boss": 300
        }
        
        return base_xp.get(chamber_type, 50) + (difficulty * 10)
    
    def _generate_combat_card_rewards(self, difficulty: int, chamber_type: str) -> List[str]:
        """Generate card rewards for combat victory."""
        reward_count = 1
        if chamber_type in ["boss", "final_boss"]:
            reward_count = 2
        if difficulty > 3:
            reward_count += 1
        
        return self.card_reward_system.generate_combat_rewards(difficulty, reward_count)
    
    def _get_card_rarity_enum(self, card_id: str) -> RewardRarity:
        """Get reward rarity enum for a card."""
        card_library = CardLibrary()
        card = card_library.get_card_by_id(card_id)
        
        if not card:
            return RewardRarity.COMMON
        
        rarity_map = {
            CardRarity.COMMON: RewardRarity.COMMON,
            CardRarity.UNCOMMON: RewardRarity.UNCOMMON,
            CardRarity.RARE: RewardRarity.RARE,
            CardRarity.LEGENDARY: RewardRarity.LEGENDARY
        }
        
        return rarity_map.get(card.rarity, RewardRarity.COMMON)
    
    def _add_bonus_combat_rewards(self, bundle: RewardBundle, win_streak: int, difficulty: int) -> None:
        """Add bonus rewards for exceptional performance."""
        # High streak bonus
        if win_streak >= 20:
            bundle.rewards.append(Reward(
                type=RewardType.CARD_PACK,
                rarity=RewardRarity.RARE,
                value="egyptian_rare_pack",
                quantity=1,
                description="Legendary streak bonus"
            ))
        
        # High difficulty bonus
        if difficulty >= 5:
            bundle.rewards.append(Reward(
                type=RewardType.CARDS,
                rarity=RewardRarity.RARE,
                value="legendary_artifact",
                quantity=1,
                description="Champion's prize"
            ))
    
    def _add_first_completion_bonus(self, bundle: RewardBundle, chamber_id: str) -> None:
        """Add bonus rewards for first chamber completion."""
        # Extra XP
        bundle.rewards.append(Reward(
            type=RewardType.XP,
            rarity=RewardRarity.RARE,
            value=100,
            description="First discovery bonus"
        ))
        
        # Chamber-specific first completion rewards
        first_completion_rewards = {
            "entrance": ["desert_map"],
            "antechamber": ["sacred_tools"],
            "first_trial": ["anubis_blessing"],
            "hall_of_truth": ["maat_feather"],
            "pharaoh_tomb": ["pharaoh_crown", "eternal_ankh"]
        }
        
        special_cards = first_completion_rewards.get(chamber_id, [])
        for card_id in special_cards:
            bundle.rewards.append(Reward(
                type=RewardType.CARDS,
                rarity=RewardRarity.LEGENDARY,
                value=card_id,
                quantity=1,
                description="First discovery treasure"
            ))
    
    def _get_chamber_reward_data(self, chamber_id: str) -> Dict[str, Any]:
        """Get reward data for a specific chamber."""
        chamber_rewards = {
            "entrance": {
                "xp": 100,
                "guaranteed_cards": ["whisper_of_thoth"],
                "unlocks": ["chamber_antechamber"]
            },
            "antechamber": {
                "xp": 150,
                "guaranteed_cards": ["ra_solar_flare"],
                "unlocks": ["chamber_first_trial", "pool_basic_spells"]
            },
            "first_trial": {
                "xp": 200,
                "guaranteed_cards": ["anubis_judgment"],
                "unlocks": ["chamber_isis", "chamber_horus"]
            },
            "chamber_of_isis": {
                "xp": 300,
                "guaranteed_cards": ["isis_protection", "healing_ankh"],
                "unlocks": ["chamber_hall_of_truth", "pool_healing_magic"]
            },
            "chamber_of_horus": {
                "xp": 300,
                "guaranteed_cards": ["horus_sight", "sky_power"],
                "unlocks": ["chamber_hall_of_truth", "pool_sky_magic"]
            },
            "hall_of_truth": {
                "xp": 500,
                "guaranteed_cards": ["maat_judgment", "truth_revelation"],
                "unlocks": ["chamber_pharaoh_tomb", "pool_divine_magic"]
            },
            "pharaoh_tomb": {
                "xp": 1000,
                "guaranteed_cards": ["pharaoh_crown", "eternal_power"],
                "unlocks": ["pool_legendary_artifacts"]
            }
        }
        
        return chamber_rewards.get(chamber_id, {"xp": 100, "guaranteed_cards": [], "unlocks": []})
    
    def _get_achievement_reward_data(self, achievement_id: str) -> Dict[str, Any]:
        """Get reward data for achievements."""
        achievement_rewards = {
            "first_victory": {
                "xp": 200,
                "cards": ["victory_scarab"],
                "title": "First Conqueror"
            },
            "pharaoh_slayer": {
                "xp": 2000,
                "cards": ["pharaoh_bane", "divine_retribution"],
                "title": "Pharaoh Slayer"
            },
            "card_collector": {
                "xp": 1000,
                "cards": ["collector_tome"],
                "title": "Master Collector"
            },
            "temple_explorer": {
                "xp": 1500,
                "cards": ["explorer_compass"],
                "title": "Temple Master"
            },
            "win_streak_master": {
                "xp": 1000,
                "cards": ["streak_crown"],
                "title": "Unstoppable Force"
            }
        }
        
        return achievement_rewards.get(achievement_id, {"xp": 100, "cards": [], "title": None})
    
    def _get_egyptian_level_title(self, level: int) -> Optional[str]:
        """Get Egyptian-themed title for reaching certain levels."""
        level_titles = {
            5: "Desert Wanderer",
            10: "Temple Acolyte",
            15: "Sand Guardian",
            20: "Pyramid Scholar",
            25: "Anubis Follower",
            30: "Isis Devotee",
            35: "Horus Champion",
            40: "Ra's Chosen",
            45: "Thoth's Scribe",
            50: "Pharaoh's Advisor",
            60: "High Priest",
            70: "Divine Oracle",
            80: "God-King",
            90: "Eternal Ruler",
            100: "Master of the Sands"
        }
        
        return level_titles.get(level)


class EgyptianAchievementSystem:
    """
    Achievement system with Egyptian themes and progression tracking.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.achievements = self._initialize_achievements()
        
    def _initialize_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all available achievements."""
        return {
            # Combat achievements
            "first_victory": {
                "name": "Dawn of Victory",
                "description": "Win your first battle",
                "category": "combat",
                "requirement": {"type": "wins", "value": 1},
                "hidden": False,
                "icon": "victory_scarab"
            },
            "pharaoh_slayer": {
                "name": "Pharaoh's Bane",
                "description": "Defeat the Pharaoh in final combat",
                "category": "combat",
                "requirement": {"type": "boss_defeat", "value": "pharaoh"},
                "hidden": False,
                "icon": "pharaoh_crown"
            },
            "unstoppable": {
                "name": "Unstoppable Force",
                "description": "Achieve a 25-win streak",
                "category": "combat",
                "requirement": {"type": "win_streak", "value": 25},
                "hidden": False,
                "icon": "streak_crown"
            },
            
            # Collection achievements
            "card_collector": {
                "name": "Keeper of Secrets",
                "description": "Collect 100 unique cards",
                "category": "collection",
                "requirement": {"type": "unique_cards", "value": 100},
                "hidden": False,
                "icon": "collector_tome"
            },
            "legendary_collector": {
                "name": "Guardian of Legends",
                "description": "Collect all legendary cards",
                "category": "collection",
                "requirement": {"type": "legendary_complete", "value": True},
                "hidden": False,
                "icon": "legendary_ankh"
            },
            
            # Exploration achievements
            "temple_explorer": {
                "name": "Master of the Temple",
                "description": "Complete all temple chambers",
                "category": "exploration",
                "requirement": {"type": "chambers_complete", "value": "all"},
                "hidden": False,
                "icon": "temple_key"
            },
            "speed_runner": {
                "name": "Swift as the Wind",
                "description": "Complete the temple in under 2 hours",
                "category": "exploration",
                "requirement": {"type": "completion_time", "value": 7200},  # 2 hours in seconds
                "hidden": True,
                "icon": "wind_scarab"
            },
            
            # Devotion achievements
            "devoted_pharaoh": {
                "name": "Devoted Pharaoh",
                "description": "Play for 7 consecutive days",
                "category": "devotion",
                "requirement": {"type": "consecutive_days", "value": 7},
                "hidden": False,
                "icon": "devotion_ankh"
            },
            "eternal_guardian": {
                "name": "Eternal Guardian",
                "description": "Play for 100 total hours",
                "category": "devotion",
                "requirement": {"type": "playtime_hours", "value": 100},
                "hidden": False,
                "icon": "eternal_hourglass"
            },
            
            # Special achievements
            "perfectionist": {
                "name": "Divine Perfection",
                "description": "Complete the temple without losing a single battle",
                "category": "special",
                "requirement": {"type": "perfect_run", "value": True},
                "hidden": True,
                "icon": "perfect_ankh"
            },
            "deck_master": {
                "name": "Master Deck Builder",
                "description": "Create 20 different deck configurations",
                "category": "special",
                "requirement": {"type": "decks_created", "value": 20},
                "hidden": False,
                "icon": "deck_scroll"
            }
        }
    
    def check_achievement_progress(self, achievement_id: str, player_stats: Dict[str, Any]) -> Tuple[bool, float]:
        """
        Check progress on an achievement.
        
        Returns:
            (is_completed, progress_percentage)
        """
        if achievement_id not in self.achievements:
            return False, 0.0
        
        achievement = self.achievements[achievement_id]
        requirement = achievement["requirement"]
        req_type = requirement["type"]
        req_value = requirement["value"]
        
        # Check different types of requirements
        if req_type == "wins":
            current = player_stats.get("total_wins", 0)
            return current >= req_value, min(100.0, (current / req_value) * 100)
        
        elif req_type == "win_streak":
            current = player_stats.get("best_win_streak", 0)
            return current >= req_value, min(100.0, (current / req_value) * 100)
        
        elif req_type == "unique_cards":
            current = player_stats.get("unique_cards_owned", 0)
            return current >= req_value, min(100.0, (current / req_value) * 100)
        
        elif req_type == "playtime_hours":
            current = player_stats.get("playtime_hours", 0)
            return current >= req_value, min(100.0, (current / req_value) * 100)
        
        elif req_type == "consecutive_days":
            current = player_stats.get("consecutive_login_days", 0)
            return current >= req_value, min(100.0, (current / req_value) * 100)
        
        elif req_type == "chambers_complete":
            if req_value == "all":
                total_chambers = 7  # Total number of chambers
                current = len(player_stats.get("chambers_completed", set()))
                return current >= total_chambers, min(100.0, (current / total_chambers) * 100)
        
        elif req_type == "decks_created":
            current = len(player_stats.get("saved_decks", {}))
            return current >= req_value, min(100.0, (current / req_value) * 100)
        
        elif req_type == "boss_defeat":
            boss_defeats = player_stats.get("boss_defeats", {})
            return req_value in boss_defeats and boss_defeats[req_value] > 0, 100.0 if req_value in boss_defeats else 0.0
        
        elif req_type == "legendary_complete":
            # Check if all legendary cards are collected
            legendary_cards = player_stats.get("legendary_cards_total", 10)  # Assume 10 legendary cards exist
            current = player_stats.get("legendary_cards_owned", 0)
            return current >= legendary_cards, min(100.0, (current / legendary_cards) * 100)
        
        elif req_type == "perfect_run":
            return player_stats.get("perfect_run_completed", False), 100.0 if player_stats.get("perfect_run_completed", False) else 0.0
        
        elif req_type == "completion_time":
            best_time = player_stats.get("best_completion_time", float('inf'))
            return best_time <= req_value, 100.0 if best_time <= req_value else 0.0
        
        return False, 0.0
    
    def get_achievements_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Get all achievements in a specific category."""
        return {aid: data for aid, data in self.achievements.items() if data["category"] == category}
    
    def get_visible_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Get all non-hidden achievements."""
        return {aid: data for aid, data in self.achievements.items() if not data.get("hidden", False)}
    
    def get_completed_achievements(self, player_stats: Dict[str, Any]) -> Set[str]:
        """Get set of completed achievement IDs."""
        completed = set()
        for achievement_id in self.achievements:
            is_completed, _ = self.check_achievement_progress(achievement_id, player_stats)
            if is_completed:
                completed.add(achievement_id)
        return completed