"""
Specific Enemy AI Implementations

Defines unique AI behaviors for Egyptian enemy archetypes:
- Múmia Guerreira (Mummy Warrior): Aggressive physical combat
- Anubis Sentinela (Anubis Sentinel): Defensive counter-attacks  
- Sacerdote de Ra (Ra Priest): Magic and healing focus
- Escaravelho Guardião (Scarab Guardian): Speed and poison tactics

Each enemy type has distinct decision-making patterns, preferences,
and tactical approaches that create varied and challenging gameplay.
"""

import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from .enemy_ai_enhanced import EnhancedEnemyAI, EnemyPersonality, ActionType
from ..core.combat_enhanced import EnhancedCombatAction, ActionPriority


class CombatState(Enum):
    """Combat state indicators for tactical decisions."""
    EARLY_GAME = "early_game"      # First few turns
    MID_GAME = "mid_game"          # Active combat phase  
    LATE_GAME = "late_game"        # Low health/decisive moment
    CRITICAL = "critical"          # Very low health
    DOMINATING = "dominating"      # Winning easily


@dataclass
class TacticalSituation:
    """Represents current tactical situation for decision making."""
    my_health_percent: float
    enemy_health_percent: float
    my_sand: int
    enemy_sand: int
    turns_elapsed: int
    combat_state: CombatState
    
    def is_desperate(self) -> bool:
        return self.my_health_percent < 0.3
    
    def has_advantage(self) -> bool:
        return self.my_health_percent > self.enemy_health_percent + 0.2
    
    def is_even_match(self) -> bool:
        return abs(self.my_health_percent - self.enemy_health_percent) < 0.15


class MummyWarriorAI(EnhancedEnemyAI):
    """
    Múmia Guerreira - Aggressive Physical Combat AI
    
    Characteristics:
    - Prefers direct damage attacks
    - Builds up strength over time
    - Becomes more aggressive when low on health
    - Simple but effective tactics
    """
    
    def __init__(self, enemy_id: str, **kwargs):
        super().__init__(enemy_id, EnemyPersonality.MUMMY_WARRIOR, **kwargs)
        
        # Mummy-specific behavior parameters
        self.rage_threshold = 0.4  # Health % where rage mode activates
        self.preferred_actions = {
            'direct_attack': 0.7,
            'strength_buff': 0.5,
            'healing': 0.2,
            'defensive': 0.3
        }
        
        # Combat patterns
        self.combo_counter = 0  # Track consecutive attacks
        self.rage_mode = False
        
        logging.info(f"Mummy Warrior AI initialized for {enemy_id}")
    
    def _evaluate_tactical_situation(self) -> TacticalSituation:
        """Assess current combat situation."""
        if not self.hourglass or not self.combat_engine:
            return TacticalSituation(1.0, 1.0, 0, 0, 0, CombatState.EARLY_GAME)
        
        # Get combat status
        combat_status = self.combat_engine.get_combat_status()
        turns = combat_status.get('turn_count', 0)
        
        # Estimate health percentages (would need actual health tracking)
        my_health_percent = 0.8  # Placeholder - should get from actual health
        enemy_health_percent = 0.7  # Placeholder - should get from player health
        
        # Determine combat state
        if turns < 3:
            state = CombatState.EARLY_GAME
        elif my_health_percent < 0.3 or enemy_health_percent < 0.3:
            state = CombatState.CRITICAL
        elif turns > 8:
            state = CombatState.LATE_GAME
        else:
            state = CombatState.MID_GAME
        
        return TacticalSituation(
            my_health_percent=my_health_percent,
            enemy_health_percent=enemy_health_percent,
            my_sand=self.hourglass.current_sand,
            enemy_sand=self.player_analyzer.behavior_pattern.get_average_sand_spending(),
            turns_elapsed=turns,
            combat_state=state
        )
    
    def _apply_personality_modifiers(self, evaluation, player_threat: float, 
                                   player_predictions: Dict[str, float]):
        """Apply Mummy Warrior specific modifiers."""
        evaluation = super()._apply_personality_modifiers(evaluation, player_threat, player_predictions)
        
        situation = self._evaluate_tactical_situation()
        
        # Rage mode activation
        if situation.my_health_percent < self.rage_threshold:
            self.rage_mode = True
            
        # Mummy Warrior specific logic
        if evaluation.action_type == ActionType.PLAY_CARD:
            # Boost damage-dealing actions
            evaluation.expected_value *= 1.2
            
            # Extra boost in rage mode
            if self.rage_mode:
                evaluation.expected_value *= 1.3
                evaluation.urgency *= 1.4
            
            # Combo bonus for consecutive attacks
            if self.combo_counter > 0:
                evaluation.expected_value *= (1.0 + self.combo_counter * 0.1)
        
        elif evaluation.action_type == ActionType.ABILITY:
            # Prefer abilities that buff attack power
            evaluation.expected_value *= 1.1
        
        # Reduce preference for defensive actions unless critical
        if not situation.is_desperate() and evaluation.action_type == ActionType.END_TURN:
            evaluation.expected_value *= 0.7
        
        return evaluation
    
    def _make_decision(self) -> None:
        """Mummy Warrior decision making with aggressive patterns."""
        situation = self._evaluate_tactical_situation()
        
        # Update combo counter based on last action
        if self.decision_history:
            last_action = self.decision_history[-1]
            if last_action.action_type == ActionType.PLAY_CARD:
                self.combo_counter += 1
            else:
                self.combo_counter = 0
        
        # Limit combo counter
        self.combo_counter = min(self.combo_counter, 3)
        
        # Call enhanced decision making
        super()._make_decision()
        
        logging.debug(f"Mummy Warrior {self.enemy_id}: rage_mode={self.rage_mode}, combo={self.combo_counter}")


class AnubisSentinelAI(EnhancedEnemyAI):
    """
    Anubis Sentinela - Defensive Counter-Attack AI
    
    Characteristics:
    - Focuses on blocking and counter-attacks
    - Analyzes player patterns for optimal counters
    - Patient, methodical approach
    - Strong late-game scaling
    """
    
    def __init__(self, enemy_id: str, **kwargs):
        super().__init__(enemy_id, EnemyPersonality.ANUBIS_SENTINEL, **kwargs)
        
        # Sentinel-specific parameters
        self.defense_stance = False
        self.counter_ready = False
        self.patience_stacks = 0  # Build up power over time
        
        self.preferred_actions = {
            'block': 0.8,
            'counter_attack': 0.7,
            'debuff': 0.6,
            'direct_attack': 0.3
        }
        
        # Pattern recognition for counters
        self.player_pattern_memory: List[str] = []
        
        logging.info(f"Anubis Sentinel AI initialized for {enemy_id}")
    
    def _analyze_player_pattern(self) -> str:
        """Analyze recent player actions to predict pattern."""
        if len(self.player_pattern_memory) < 3:
            return "unknown"
        
        recent = self.player_pattern_memory[-3:]
        
        # Look for common patterns
        if all(action == "attack" for action in recent):
            return "aggressive_sequence"
        elif "attack" in recent and "skill" in recent:
            return "mixed_sequence" 
        elif all(action in ["skill", "power"] for action in recent):
            return "setup_sequence"
        else:
            return "random_sequence"
    
    def observe_player_action(self, action_type: ActionType, card_name: Optional[str] = None,
                            card_type: Optional[str] = None, sand_cost: int = 0,
                            player_health: int = 100) -> None:
        """Enhanced observation for pattern recognition."""
        super().observe_player_action(action_type, card_name, card_type, sand_cost, player_health)
        
        # Track action patterns
        if card_type:
            self.player_pattern_memory.append(card_type.lower())
            if len(self.player_pattern_memory) > 10:
                self.player_pattern_memory.pop(0)
    
    def _apply_personality_modifiers(self, evaluation, player_threat: float,
                                   player_predictions: Dict[str, float]):
        """Apply Anubis Sentinel specific modifiers."""
        evaluation = super()._apply_personality_modifiers(evaluation, player_threat, player_predictions)
        
        situation = self._evaluate_tactical_situation()
        pattern = self._analyze_player_pattern()
        
        # Defensive stance bonuses
        if self.defense_stance:
            if evaluation.action_type == ActionType.ABILITY:
                # Boost counter-attack abilities
                evaluation.expected_value *= 1.4
                evaluation.threat_reduction *= 1.3
        
        # Pattern-based counter modifications
        if pattern == "aggressive_sequence" and evaluation.action_type == ActionType.ABILITY:
            # Player is being aggressive, prepare counter
            evaluation.expected_value *= 1.3
            evaluation.urgency *= 1.2
        
        elif pattern == "setup_sequence":
            # Player is setting up, be patient or disrupt
            if evaluation.action_type == ActionType.PLAY_CARD:
                evaluation.expected_value *= 1.2  # Disrupt setup
        
        # Patience stack bonuses
        patience_multiplier = 1.0 + (self.patience_stacks * 0.1)
        if evaluation.action_type == ActionType.ABILITY:
            evaluation.expected_value *= patience_multiplier
        
        # Higher threat = more defensive
        if player_threat > 0.6:
            if evaluation.action_type in [ActionType.END_TURN]:
                evaluation.expected_value *= 0.8  # Less likely to end turn during threats
        
        return evaluation
    
    def _make_decision(self) -> None:
        """Anubis Sentinel decision making with defensive patterns."""
        situation = self._evaluate_tactical_situation()
        
        # Update defense stance
        if situation.is_desperate():
            self.defense_stance = True
        elif situation.has_advantage():
            self.defense_stance = False
        
        # Build patience stacks over time
        if not self.decision_history or self.decision_history[-1].action_type == ActionType.END_TURN:
            self.patience_stacks = min(self.patience_stacks + 1, 5)
        
        # Call enhanced decision making
        super()._make_decision()
        
        logging.debug(f"Anubis Sentinel {self.enemy_id}: defense_stance={self.defense_stance}, patience={self.patience_stacks}")


class RaPriestAI(EnhancedEnemyAI):
    """
    Sacerdote de Ra - Magic and Healing Focus AI
    
    Characteristics:
    - Strategic use of magic and healing
    - Adapts to player behavior
    - Strong battlefield control
    - Complex decision trees
    """
    
    def __init__(self, enemy_id: str, **kwargs):
        super().__init__(enemy_id, EnemyPersonality.RA_PRIEST, **kwargs)
        
        # Priest-specific parameters
        self.mana_conservation = True
        self.healing_threshold = 0.5
        self.spell_combo_potential = 0
        
        self.preferred_actions = {
            'heal': 0.8,
            'magic_damage': 0.7,
            'debuff': 0.7,
            'buff_self': 0.6,
            'direct_attack': 0.3
        }
        
        # Magic system tracking
        self.spell_history: List[str] = []
        self.divine_favor = 0  # Accumulates with good decisions
        
        logging.info(f"Ra Priest AI initialized for {enemy_id}")
    
    def _calculate_healing_priority(self, situation: TacticalSituation) -> float:
        """Calculate priority for healing actions."""
        if situation.my_health_percent > 0.8:
            return 0.2  # Low priority when healthy
        elif situation.my_health_percent < 0.3:
            return 0.9  # High priority when critical
        else:
            # Scale with missing health
            return 0.4 + (0.8 - situation.my_health_percent) * 0.8
    
    def _assess_magic_opportunity(self, player_predictions: Dict[str, float]) -> float:
        """Assess opportunity for magical attacks."""
        # Magic is more effective against predictable opponents
        predictability = max(player_predictions.values())
        
        # If player often uses attacks, magic counters well
        if player_predictions.get('attack', 0) > 0.6:
            return 0.8
        elif player_predictions.get('skill', 0) > 0.5:
            return 0.6  # Skill vs skill matchup
        else:
            return 0.4
    
    def _apply_personality_modifiers(self, evaluation, player_threat: float,
                                   player_predictions: Dict[str, float]):
        """Apply Ra Priest specific modifiers."""
        evaluation = super()._apply_personality_modifiers(evaluation, player_threat, player_predictions)
        
        situation = self._evaluate_tactical_situation()
        
        # Healing priority adjustments
        if evaluation.action_type == ActionType.ABILITY:
            healing_priority = self._calculate_healing_priority(situation)
            evaluation.expected_value *= (0.5 + healing_priority)
        
        # Magic opportunity assessment
        if evaluation.action_type == ActionType.PLAY_CARD:
            magic_opportunity = self._assess_magic_opportunity(player_predictions)
            evaluation.expected_value *= (0.6 + magic_opportunity * 0.4)
        
        # Divine favor bonuses
        if self.divine_favor > 3:
            evaluation.expected_value *= 1.2
            evaluation.confidence *= 1.1
        
        # Mana conservation logic
        if self.mana_conservation and situation.my_sand < 3:
            if evaluation.sand_cost > 2:
                evaluation.expected_value *= 0.7  # Reduce high-cost action preference
        
        # Strategic patience in early game
        if situation.combat_state == CombatState.EARLY_GAME:
            if evaluation.action_type == ActionType.END_TURN:
                evaluation.expected_value *= 1.2  # More willing to pass early
        
        return evaluation
    
    def _make_decision(self) -> None:
        """Ra Priest decision making with strategic magic focus."""
        situation = self._evaluate_tactical_situation()
        
        # Update mana conservation based on situation
        if situation.is_desperate():
            self.mana_conservation = False  # Spend everything if desperate
        elif situation.has_advantage():
            self.mana_conservation = True   # Conserve when ahead
        
        # Update divine favor based on smart decisions
        if self.decision_history:
            last_decision = self.decision_history[-1]
            if last_decision.confidence > 0.8 and last_decision.get_total_score() > 0.7:
                self.divine_favor += 1
            
        self.divine_favor = min(self.divine_favor, 10)  # Cap divine favor
        
        # Call enhanced decision making
        super()._make_decision()
        
        logging.debug(f"Ra Priest {self.enemy_id}: mana_conservation={self.mana_conservation}, favor={self.divine_favor}")


class ScarabGuardianAI(EnhancedEnemyAI):
    """
    Escaravelho Guardião - Speed and Poison Tactics AI
    
    Characteristics:
    - Fast, efficient actions
    - Poison damage over time
    - Hit-and-run tactics
    - Swarm-like behavior patterns
    """
    
    def __init__(self, enemy_id: str, **kwargs):
        super().__init__(enemy_id, EnemyPersonality.SCARAB_GUARDIAN, **kwargs)
        
        # Scarab-specific parameters
        self.swarm_intensity = 0  # Build up over time
        self.poison_stacks = 0    # Track poison applied
        self.speed_bonus = 0      # Accumulated speed
        
        self.preferred_actions = {
            'poison': 0.8,
            'quick_attack': 0.7, 
            'evasion': 0.6,
            'swarm_attack': 0.6,
            'heavy_attack': 0.2
        }
        
        # Swarm coordination
        self.last_action_time = 0
        self.action_chain = 0  # Consecutive quick actions
        
        logging.info(f"Scarab Guardian AI initialized for {enemy_id}")
    
    def _calculate_poison_effectiveness(self, situation: TacticalSituation) -> float:
        """Calculate how effective poison would be."""
        # Poison is more effective in longer fights
        if situation.combat_state in [CombatState.EARLY_GAME, CombatState.MID_GAME]:
            return 0.8  # Good for sustained damage
        elif situation.combat_state == CombatState.LATE_GAME:
            return 0.6  # Still good but less time
        else:
            return 0.3  # Not great in critical moments
    
    def _assess_speed_advantage(self, player_predictions: Dict[str, float]) -> bool:
        """Determine if we have speed advantage."""
        # Check player timing patterns
        avg_turn_time = 0
        if self.player_analyzer.behavior_pattern.turn_timing:
            avg_turn_time = sum(self.player_analyzer.behavior_pattern.turn_timing) / len(self.player_analyzer.behavior_pattern.turn_timing)
        
        # Slow players can be overwhelmed with speed
        return avg_turn_time > 5.0 or self.speed_bonus > 2
    
    def _apply_personality_modifiers(self, evaluation, player_threat: float,
                                   player_predictions: Dict[str, float]):
        """Apply Scarab Guardian specific modifiers."""
        evaluation = super()._apply_personality_modifiers(evaluation, player_threat, player_predictions)
        
        situation = self._evaluate_tactical_situation()
        
        # Poison effectiveness
        if evaluation.action_type == ActionType.PLAY_CARD:
            poison_effectiveness = self._calculate_poison_effectiveness(situation)
            evaluation.expected_value *= (0.5 + poison_effectiveness * 0.5)
        
        # Speed advantage bonuses
        if self._assess_speed_advantage(player_predictions):
            evaluation.urgency *= 1.3
            evaluation.sand_efficiency *= 1.2
        
        # Action chain bonuses
        if self.action_chain > 0:
            chain_bonus = min(0.3, self.action_chain * 0.1)
            evaluation.expected_value *= (1.0 + chain_bonus)
        
        # Swarm intensity effects
        if self.swarm_intensity > 3:
            if evaluation.action_type == ActionType.PLAY_CARD:
                evaluation.expected_value *= 1.2  # More aggressive with high intensity
        
        # Low cost preference (scarabs are efficient)
        if evaluation.sand_cost <= 1:
            evaluation.sand_efficiency *= 1.3
        elif evaluation.sand_cost >= 3:
            evaluation.sand_efficiency *= 0.8
        
        return evaluation
    
    def _make_decision(self) -> None:
        """Scarab Guardian decision making with speed and poison focus."""
        current_time = time.time()
        situation = self._evaluate_tactical_situation()
        
        # Update action chain
        if self.last_action_time and (current_time - self.last_action_time) < 2.0:
            self.action_chain += 1
        else:
            self.action_chain = 0
        
        self.action_chain = min(self.action_chain, 5)  # Cap chain
        
        # Build swarm intensity over time
        if situation.combat_state != CombatState.EARLY_GAME:
            self.swarm_intensity += 1
        
        self.swarm_intensity = min(self.swarm_intensity, 10)  # Cap intensity
        
        # Update speed bonus based on quick actions
        if self.decision_history and self.decision_history[-1].sand_cost <= 1:
            self.speed_bonus += 1
        
        self.speed_bonus = min(self.speed_bonus, 5)  # Cap speed bonus
        
        # Call enhanced decision making
        super()._make_decision()
        
        self.last_action_time = current_time
        
        logging.debug(f"Scarab Guardian {self.enemy_id}: intensity={self.swarm_intensity}, chain={self.action_chain}, speed={self.speed_bonus}")


# Factory function for creating specific enemy AIs
def create_enemy_ai(enemy_id: str, enemy_type: str, hourglass, combat_engine, 
                   difficulty=None) -> EnhancedEnemyAI:
    """
    Factory function to create the appropriate AI for an enemy type.
    
    Args:
        enemy_id: Unique identifier for this enemy
        enemy_type: Type of enemy (determines AI class)
        hourglass: Hour-glass resource system
        combat_engine: Combat system reference
        difficulty: AI difficulty level
    
    Returns:
        Appropriate EnhancedEnemyAI subclass instance
    """
    
    # Map enemy types to AI classes
    ai_classes = {
        'mummified_priest': RaPriestAI,
        'mummy_warrior': MummyWarriorAI,
        'tomb_sentinel': AnubisSentinelAI,
        'anubite_guard': AnubisSentinelAI,
        'scarab_swarm': ScarabGuardianAI,
        'scarab_guardian': ScarabGuardianAI,
        'sphinx_guardian': RaPriestAI,  # Strategic like priest
        'pharaoh_lich': RaPriestAI,    # Magic focused
        'chaos_djinn': MummyWarriorAI, # Aggressive
        'sand_wraith': ScarabGuardianAI, # Fast attacks
        'serpent_of_apophis': MummyWarriorAI  # Pure aggression
    }
    
    # Get appropriate AI class or default to MummyWarriorAI
    ai_class = ai_classes.get(enemy_type, MummyWarriorAI)
    
    # Create AI instance
    ai = ai_class(enemy_id=enemy_id, difficulty=difficulty)
    ai.set_hourglass(hourglass)
    ai.set_combat_engine(combat_engine)
    
    logging.info(f"Created {ai_class.__name__} for enemy {enemy_id} ({enemy_type})")
    
    return ai