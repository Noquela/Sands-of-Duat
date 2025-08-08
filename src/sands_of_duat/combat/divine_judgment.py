#!/usr/bin/env python3
"""
DIVINE JUDGMENT SYSTEM
======================

Ma'at balance system based on authentic Egyptian beliefs about cosmic order,
divine justice, and moral judgment. Implements the weighing of the heart
ceremony and its effects on gameplay.
"""

import logging
import random
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class MoralAction(Enum):
    """Types of moral actions that affect divine judgment."""
    # Virtuous Actions (Positive Ma'at)
    PROTECT_INNOCENT = ("protect_innocent", 3, "Shielding the weak from harm")
    HEAL_WOUNDED = ("heal_wounded", 2, "Restoring health and vitality")
    SPEAK_TRUTH = ("speak_truth", 2, "Speaking honestly despite consequences") 
    HONOR_GODS = ("honor_gods", 2, "Showing proper respect to divine beings")
    PRESERVE_ORDER = ("preserve_order", 1, "Maintaining cosmic balance")
    SHARE_RESOURCES = ("share_resources", 1, "Giving aid to those in need")
    RESPECT_DEAD = ("respect_dead", 2, "Proper treatment of the deceased")
    UPHOLD_JUSTICE = ("uphold_justice", 3, "Ensuring fair treatment for all")
    
    # Neutral Actions (No Ma'at effect)
    SURVIVE_COMBAT = ("survive_combat", 0, "Basic survival instinct")
    CAST_SPELL = ("cast_spell", 0, "Using magical abilities")
    SUMMON_CREATURE = ("summon_creature", 0, "Calling forth allies")
    
    # Wicked Actions (Negative Ma'at)
    BETRAY_ALLY = ("betray_ally", -4, "Turning against trusted companions")
    DESECRATE_TOMB = ("desecrate_tomb", -3, "Violating sacred burial sites")
    MURDER_INNOCENT = ("murder_innocent", -5, "Killing the defenseless")
    LIE_FOR_GAIN = ("lie_for_gain", -2, "Deception for personal benefit")
    STEAL_OFFERINGS = ("steal_offerings", -2, "Taking what belongs to the gods")
    DESTROY_ORDER = ("destroy_order", -3, "Bringing chaos to stability")
    IGNORE_SUFFERING = ("ignore_suffering", -1, "Refusing to help those in need")
    BLASPHEME_GODS = ("blaspheme_gods", -4, "Showing contempt for divinity")
    
    def __init__(self, key: str, maat_value: int, description: str):
        self.key = key
        self.maat_value = maat_value  # Positive = virtuous, negative = wicked
        self.description = description

class JudgmentOutcome(Enum):
    """Possible outcomes of divine judgment."""
    PURE_HEART = ("pure_heart", "Heart lighter than Ma'at's feather")
    RIGHTEOUS = ("righteous", "Heart balanced with Ma'at's feather")
    BALANCED = ("balanced", "Heart equal to Ma'at's feather")
    TAINTED = ("tainted", "Heart heavier than Ma'at's feather")
    CORRUPT = ("corrupt", "Heart weighted with sin")
    DEVOURED = ("devoured", "Heart consumed by Ammit")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

@dataclass
class MoralRecord:
    """Record of an entity's moral actions."""
    entity_id: str
    actions: List[Tuple[MoralAction, datetime]] = field(default_factory=list)
    maat_balance: float = 0.0  # Running total of moral balance
    divine_favor: Dict[str, float] = field(default_factory=dict)  # Favor with specific gods
    judgment_history: List[Tuple[datetime, JudgmentOutcome, float]] = field(default_factory=list)
    
    def add_action(self, action: MoralAction):
        """Add a moral action to the record."""
        self.actions.append((action, datetime.now()))
        self.maat_balance += action.maat_value
        
        # Specific actions affect favor with specific gods
        if action in [MoralAction.PROTECT_INNOCENT, MoralAction.HEAL_WOUNDED]:
            self.divine_favor["Isis"] = self.divine_favor.get("Isis", 0) + 0.5
        elif action in [MoralAction.RESPECT_DEAD, MoralAction.HONOR_GODS]:
            self.divine_favor["Anubis"] = self.divine_favor.get("Anubis", 0) + 0.5
        elif action in [MoralAction.SPEAK_TRUTH, MoralAction.UPHOLD_JUSTICE]:
            self.divine_favor["Ma'at"] = self.divine_favor.get("Ma'at", 0) + 0.5
        elif action in [MoralAction.PRESERVE_ORDER]:
            self.divine_favor["Ra"] = self.divine_favor.get("Ra", 0) + 0.3
        elif action in [MoralAction.BETRAY_ALLY, MoralAction.DESTROY_ORDER]:
            self.divine_favor["Set"] = self.divine_favor.get("Set", 0) + 0.3  # Set appreciates chaos
    
    def get_recent_actions(self, minutes: int = 10) -> List[MoralAction]:
        """Get actions from the last N minutes."""
        cutoff = datetime.now()
        recent = []
        for action, timestamp in self.actions:
            if (cutoff - timestamp).total_seconds() < minutes * 60:
                recent.append(action)
        return recent
    
    def get_virtue_ratio(self) -> float:
        """Calculate ratio of virtuous to wicked actions."""
        if not self.actions:
            return 0.5  # Neutral
            
        virtuous = sum(1 for action, _ in self.actions if action.maat_value > 0)
        wicked = sum(1 for action, _ in self.actions if action.maat_value < 0)
        total = len(self.actions)
        
        return (virtuous + 0.5 * (total - virtuous - wicked)) / total

@dataclass
class JudgmentSession:
    """A divine judgment session in the Hall of Ma'at."""
    session_id: str
    judge_god: str  # Which god is conducting judgment
    entities_judged: List[str] = field(default_factory=list)
    judgments: Dict[str, JudgmentOutcome] = field(default_factory=dict)
    cosmic_balance_before: float = 0.0
    cosmic_balance_after: float = 0.0
    special_interventions: List[str] = field(default_factory=list)

class DivineJudgmentSystem:
    """
    Divine judgment system implementing Egyptian Ma'at balance.
    
    Judges entities based on their moral actions and determines cosmic
    consequences. Includes the famous weighing of the heart ceremony
    and interventions by Egyptian gods.
    """
    
    def __init__(self):
        self.moral_records: Dict[str, MoralRecord] = {}
        self.cosmic_maat_balance: float = 0.0  # Universal balance
        self.judgment_sessions: List[JudgmentSession] = []
        self.divine_judges = {
            "Ma'at": {"accuracy": 1.0, "mercy": 0.1, "specialty": "truth"},
            "Anubis": {"accuracy": 0.9, "mercy": 0.3, "specialty": "death"},
            "Osiris": {"accuracy": 0.8, "mercy": 0.5, "specialty": "resurrection"},
            "Thoth": {"accuracy": 0.95, "mercy": 0.2, "specialty": "wisdom"},
            "Ra": {"accuracy": 0.85, "mercy": 0.4, "specialty": "order"}
        }
        
        # The 42 Negative Confessions (sins to avoid in Egyptian afterlife)
        self.negative_confessions = [
            "I have not committed sin", "I have not committed robbery with violence",
            "I have not stolen", "I have not slain men and women",
            "I have not committed adultery", "I have not told lies",
            "I have not caused pain", "I have not destroyed food offerings",
            # ... (simplified list - full list has 42 items)
        ]
        
    def initialize_moral_record(self, entity_id: str) -> MoralRecord:
        """Initialize moral tracking for an entity."""
        record = MoralRecord(entity_id=entity_id)
        self.moral_records[entity_id] = record
        logger.info(f"Initialized moral record for {entity_id}")
        return record
    
    def record_action(self, entity_id: str, action: MoralAction, context: str = ""):
        """Record a moral action by an entity."""
        if entity_id not in self.moral_records:
            self.initialize_moral_record(entity_id)
        
        record = self.moral_records[entity_id]
        record.add_action(action)
        
        # Update cosmic balance
        self.cosmic_maat_balance += action.maat_value * 0.1  # Individual actions have cosmic impact
        
        logger.info(f"{entity_id} performed {action.key} (Ma'at: {action.maat_value:+}) - {context}")
        
        # Immediate consequences for extreme actions
        if action.maat_value <= -4:  # Severe wickedness
            self._trigger_immediate_consequences(entity_id, action, "divine_wrath")
        elif action.maat_value >= 3:  # Great virtue
            self._trigger_immediate_consequences(entity_id, action, "divine_blessing")
    
    def conduct_judgment(self, entity_id: str, judge_god: str = "Ma'at") -> JudgmentOutcome:
        """Conduct divine judgment of an entity."""
        if entity_id not in self.moral_records:
            # No record means neutral judgment
            return JudgmentOutcome.BALANCED
        
        record = self.moral_records[entity_id]
        judge_stats = self.divine_judges[judge_god]
        
        # Calculate base judgment score
        base_score = record.maat_balance
        
        # Apply judge-specific modifiers
        accuracy_mod = random.uniform(0.8, 1.0) if judge_stats["accuracy"] < 1.0 else 1.0
        mercy_mod = judge_stats["mercy"]
        
        # Account for divine favor
        divine_favor_bonus = record.divine_favor.get(judge_god, 0) * 2
        
        # Final judgment score
        final_score = (base_score * accuracy_mod) + divine_favor_bonus
        
        # Apply mercy for borderline cases
        if -2 <= final_score <= 2 and random.random() < mercy_mod:
            final_score += random.uniform(1, 3)  # Merciful adjustment upward
        
        # Determine judgment outcome
        outcome = self._determine_judgment_outcome(final_score, record)
        
        # Record the judgment
        record.judgment_history.append((datetime.now(), outcome, final_score))
        
        logger.info(f"{judge_god} judges {entity_id}: {outcome.description} (score: {final_score:.2f})")
        
        return outcome
    
    def _determine_judgment_outcome(self, score: float, record: MoralRecord) -> JudgmentOutcome:
        """Determine judgment outcome based on score and history."""
        # Check for special conditions first
        recent_actions = record.get_recent_actions(5)  # Last 5 minutes
        
        # Ammit's judgment - for the truly wicked
        if (score < -10 or 
            any(action in [MoralAction.MURDER_INNOCENT, MoralAction.BLASPHEME_GODS] 
                for action in recent_actions)):
            if random.random() < 0.3:  # 30% chance even for the wicked
                return JudgmentOutcome.DEVOURED
        
        # Standard judgment based on score
        if score >= 8:
            return JudgmentOutcome.PURE_HEART
        elif score >= 4:
            return JudgmentOutcome.RIGHTEOUS
        elif score >= -2:
            return JudgmentOutcome.BALANCED
        elif score >= -6:
            return JudgmentOutcome.TAINTED
        elif score >= -10:
            return JudgmentOutcome.CORRUPT
        else:
            return JudgmentOutcome.DEVOURED
    
    def mass_judgment(self, entity_ids: List[str], judge_god: str = "Ma'at") -> JudgmentSession:
        """Conduct mass judgment session (like end of combat)."""
        session = JudgmentSession(
            session_id=f"judgment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            judge_god=judge_god,
            cosmic_balance_before=self.cosmic_maat_balance
        )
        
        logger.info(f"Beginning mass judgment by {judge_god} for {len(entity_ids)} entities")
        
        for entity_id in entity_ids:
            outcome = self.conduct_judgment(entity_id, judge_god)
            session.entities_judged.append(entity_id)
            session.judgments[entity_id] = outcome
            
            # Apply immediate effects based on judgment
            self._apply_judgment_effects(entity_id, outcome)
        
        session.cosmic_balance_after = self.cosmic_maat_balance
        self.judgment_sessions.append(session)
        
        # Check for cosmic balance shifts
        balance_change = session.cosmic_balance_after - session.cosmic_balance_before
        if abs(balance_change) > 5:
            self._trigger_cosmic_event(balance_change)
        
        return session
    
    def _apply_judgment_effects(self, entity_id: str, outcome: JudgmentOutcome):
        """Apply gameplay effects based on judgment outcome."""
        effects = {
            JudgmentOutcome.PURE_HEART: {
                "divine_blessing": 2.0,
                "resurrection_chance": 0.9,
                "afterlife_destination": "Field of Reeds",
                "special_powers": ["divine_protection", "light_aura"]
            },
            JudgmentOutcome.RIGHTEOUS: {
                "divine_blessing": 1.5,
                "resurrection_chance": 0.7,
                "afterlife_destination": "Field of Reeds",
                "special_powers": ["righteous_strength"]
            },
            JudgmentOutcome.BALANCED: {
                "divine_blessing": 1.0,
                "resurrection_chance": 0.5,
                "afterlife_destination": "Peaceful Rest",
                "special_powers": []
            },
            JudgmentOutcome.TAINTED: {
                "divine_blessing": 0.7,
                "resurrection_chance": 0.3,
                "afterlife_destination": "Wandering Spirit",
                "penalties": ["reduced_power"]
            },
            JudgmentOutcome.CORRUPT: {
                "divine_blessing": 0.5,
                "resurrection_chance": 0.1,
                "afterlife_destination": "Torment",
                "penalties": ["weakness_curse", "divine_disfavor"]
            },
            JudgmentOutcome.DEVOURED: {
                "divine_blessing": 0.0,
                "resurrection_chance": 0.0,
                "afterlife_destination": "True Death",
                "penalties": ["soul_destruction", "permanent_death"]
            }
        }
        
        entity_effects = effects[outcome]
        logger.info(f"Applying judgment effects for {entity_id}: {outcome.key}")
        
        # Effects would be applied to the actual entity in the combat system
        return entity_effects
    
    def _trigger_immediate_consequences(self, entity_id: str, action: MoralAction, consequence_type: str):
        """Trigger immediate consequences for extreme actions."""
        if consequence_type == "divine_wrath":
            # Immediate punishment for severe wickedness
            consequences = [
                "Divine lightning strikes the entity",
                "Cursed with weakness until redemption",
                "Marked for judgment by Ammit",
                "All gods turn their backs on the entity"
            ]
        elif consequence_type == "divine_blessing":
            # Immediate reward for great virtue
            consequences = [
                "Bathed in divine light and strength",
                "Granted protection from the gods",
                "Blessed with enhanced abilities",
                "Marked as worthy by the gods"
            ]
        
        chosen_consequence = random.choice(consequences)
        logger.info(f"Immediate consequence for {entity_id}: {chosen_consequence}")
        
        # Update cosmic balance for extreme actions
        if consequence_type == "divine_wrath":
            self.cosmic_maat_balance -= 2  # Severe wickedness hurts cosmic order
        else:
            self.cosmic_maat_balance += 1  # Great virtue helps cosmic order
    
    def _trigger_cosmic_event(self, balance_change: float):
        """Trigger cosmic events based on major balance shifts."""
        if balance_change > 10:
            # Great increase in order
            event = "The gods smile upon the world - cosmic harmony strengthened"
            effects = ["enhanced_healing", "increased_divine_favor", "order_blessing"]
        elif balance_change < -10:
            # Great increase in chaos
            event = "The cosmic balance falters - chaos gains strength"
            effects = ["random_curses", "weakened_order", "chaos_manifestations"]
        else:
            return  # No major cosmic event
        
        logger.warning(f"COSMIC EVENT: {event}")
        logger.info(f"Cosmic effects: {', '.join(effects)}")
        
        # Effects would be applied to the game world
        return {"event": event, "effects": effects}
    
    def get_entity_moral_status(self, entity_id: str) -> Dict[str, Any]:
        """Get comprehensive moral status for an entity."""
        if entity_id not in self.moral_records:
            return {"status": "unrecorded", "maat_balance": 0, "judgment_risk": "unknown"}
        
        record = self.moral_records[entity_id]
        
        # Determine current risk level
        if record.maat_balance >= 5:
            risk_level = "divine_favor"
        elif record.maat_balance >= 0:
            risk_level = "safe"
        elif record.maat_balance >= -5:
            risk_level = "at_risk"
        elif record.maat_balance >= -10:
            risk_level = "great_danger"
        else:
            risk_level = "ammit_threat"
        
        # Recent action summary
        recent_actions = record.get_recent_actions(10)
        virtue_ratio = record.get_virtue_ratio()
        
        # Predict likely judgment outcome
        predicted_judgment = self._determine_judgment_outcome(record.maat_balance, record)
        
        return {
            "status": "recorded",
            "maat_balance": record.maat_balance,
            "virtue_ratio": virtue_ratio,
            "risk_level": risk_level,
            "recent_actions": len(recent_actions),
            "divine_favor": dict(record.divine_favor),
            "predicted_judgment": predicted_judgment.key,
            "total_actions": len(record.actions),
            "judgments_received": len(record.judgment_history)
        }
    
    def get_cosmic_status(self) -> Dict[str, Any]:
        """Get overall cosmic balance status."""
        total_entities = len(self.moral_records)
        if total_entities == 0:
            return {"status": "neutral", "balance": 0.0, "entities": 0}
        
        # Calculate balance distribution
        pure_hearts = sum(1 for r in self.moral_records.values() if r.maat_balance >= 8)
        righteous = sum(1 for r in self.moral_records.values() if 4 <= r.maat_balance < 8)
        balanced = sum(1 for r in self.moral_records.values() if -2 <= r.maat_balance < 4)
        tainted = sum(1 for r in self.moral_records.values() if -6 <= r.maat_balance < -2)
        corrupt = sum(1 for r in self.moral_records.values() if r.maat_balance < -6)
        
        # Determine cosmic status
        if self.cosmic_maat_balance > 20:
            cosmic_status = "golden_age"
        elif self.cosmic_maat_balance > 10:
            cosmic_status = "harmonious"
        elif self.cosmic_maat_balance > -10:
            cosmic_status = "balanced"
        elif self.cosmic_maat_balance > -20:
            cosmic_status = "troubled"
        else:
            cosmic_status = "chaotic_age"
        
        return {
            "status": cosmic_status,
            "balance": self.cosmic_maat_balance,
            "entities": total_entities,
            "distribution": {
                "pure_hearts": pure_hearts,
                "righteous": righteous,
                "balanced": balanced,
                "tainted": tainted,
                "corrupt": corrupt
            },
            "judgment_sessions": len(self.judgment_sessions)
        }
    
    def create_judgment_preview(self, entity_id: str, judge_god: str = "Ma'at") -> Dict[str, Any]:
        """Preview what judgment would be without actually conducting it."""
        if entity_id not in self.moral_records:
            return {"preview": "no_record", "likely_outcome": "balanced"}
        
        record = self.moral_records[entity_id]
        judge_stats = self.divine_judges[judge_god]
        
        # Simulate judgment calculation
        base_score = record.maat_balance
        divine_favor_bonus = record.divine_favor.get(judge_god, 0) * 2
        estimated_score = base_score + divine_favor_bonus
        
        # Account for judge mercy
        mercy_chance = judge_stats["mercy"]
        if -2 <= estimated_score <= 2:
            estimated_score += mercy_chance * 2  # Potential mercy boost
        
        predicted_outcome = self._determine_judgment_outcome(estimated_score, record)
        
        return {
            "preview": "available",
            "judge": judge_god,
            "base_score": base_score,
            "divine_favor_bonus": divine_favor_bonus,
            "estimated_score": estimated_score,
            "likely_outcome": predicted_outcome.key,
            "outcome_description": predicted_outcome.description,
            "mercy_chance": mercy_chance,
            "judgment_factors": {
                "recent_actions": len(record.get_recent_actions(5)),
                "total_actions": len(record.actions),
                "virtue_ratio": record.get_virtue_ratio(),
                "divine_connections": list(record.divine_favor.keys())
            }
        }