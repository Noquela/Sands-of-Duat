"""
Enhanced Enemy AI System with Intelligent Decision Making

Advanced AI that analyzes player behavior, uses different personality
strategies, and adapts tactics based on combat context.

Features:
- Personality-based decision making (Aggressive, Defensive, Strategic)
- Player card and behavior analysis
- Context-aware action selection
- Intelligent counter-play capabilities
- Egyptian enemy archetypes (Mummy Warrior, Anubis Sentinel, etc.)
"""

import logging
import random
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque

from ..core.enemy_ai import EnemyAI, ActionEvaluator, ThreatAssessment, AIDifficultyLevel
from ..core.combat_enhanced import ActionType, EnhancedCombatAction
from ..core.hourglass import HourGlass


class EnemyPersonality(Enum):
    """Enhanced enemy personality types for strategic behavior."""
    MUMMY_WARRIOR = "mummy_warrior"        # Aggressive physical combat
    ANUBIS_SENTINEL = "anubis_sentinel"    # Defensive counter-attacks  
    RA_PRIEST = "ra_priest"                # Magic and healing focus
    SCARAB_GUARDIAN = "scarab_guardian"    # Speed and poison tactics
    STRATEGIC_PHARAOH = "strategic_pharaoh" # Complex strategic play
    CHAOTIC_DJINN = "chaotic_djinn"        # Unpredictable patterns


@dataclass
class PlayerBehaviorPattern:
    """Tracks player behavior patterns for AI analysis."""
    card_play_frequency: Dict[str, int] = field(default_factory=dict)
    preferred_card_types: Dict[str, float] = field(default_factory=dict)  # Attack, Skill, Power
    sand_spending_patterns: List[int] = field(default_factory=list)
    average_cards_per_turn: float = 0.0
    defensive_tendency: float = 0.5  # 0 = aggressive, 1 = defensive
    risk_tolerance: float = 0.5  # How willing to spend all sand
    turn_timing: List[float] = field(default_factory=list)  # Time per turn
    
    def update_card_play(self, card_name: str, card_type: str, sand_cost: int) -> None:
        """Update patterns based on card played."""
        self.card_play_frequency[card_name] = self.card_play_frequency.get(card_name, 0) + 1
        self.preferred_card_types[card_type] = self.preferred_card_types.get(card_type, 0) + 1
        self.sand_spending_patterns.append(sand_cost)
        
        # Keep recent history only
        if len(self.sand_spending_patterns) > 20:
            self.sand_spending_patterns.pop(0)
    
    def get_preferred_card_type(self) -> str:
        """Get player's most preferred card type."""
        if not self.preferred_card_types:
            return "Attack"  # Default assumption
        return max(self.preferred_card_types, key=self.preferred_card_types.get)
    
    def get_average_sand_spending(self) -> float:
        """Get player's average sand spending per action."""
        if not self.sand_spending_patterns:
            return 1.5  # Default assumption
        return sum(self.sand_spending_patterns) / len(self.sand_spending_patterns)
    
    def is_player_aggressive(self) -> bool:
        """Determine if player tends to be aggressive."""
        return self.defensive_tendency < 0.4
    
    def is_player_conservative(self) -> bool:
        """Determine if player tends to be conservative."""
        return self.risk_tolerance < 0.3


class PlayerAnalyzer:
    """Analyzes player behavior to inform AI decisions."""
    
    def __init__(self):
        self.behavior_pattern = PlayerBehaviorPattern()
        self.recent_actions: deque = deque(maxlen=10)
        self.player_health_history: List[int] = []
        self.turn_start_time: Optional[float] = None
        
    def observe_player_action(self, action_type: ActionType, card_name: Optional[str] = None,
                            card_type: Optional[str] = None, sand_cost: int = 0,
                            player_health: int = 100) -> None:
        """Observe and record player action for analysis."""
        self.recent_actions.append({
            'action_type': action_type,
            'card_name': card_name,
            'card_type': card_type,
            'sand_cost': sand_cost,
            'timestamp': time.time()
        })
        
        self.player_health_history.append(player_health)
        if len(self.player_health_history) > 20:
            self.player_health_history.pop(0)
        
        if card_name and card_type:
            self.behavior_pattern.update_card_play(card_name, card_type, sand_cost)
        
        self._update_behavior_analysis()
    
    def start_turn_timing(self) -> None:
        """Start timing player's turn."""
        self.turn_start_time = time.time()
    
    def end_turn_timing(self) -> None:
        """End timing player's turn and record duration."""
        if self.turn_start_time:
            duration = time.time() - self.turn_start_time
            self.behavior_pattern.turn_timing.append(duration)
            if len(self.behavior_pattern.turn_timing) > 10:
                self.behavior_pattern.turn_timing.pop(0)
            self.turn_start_time = None
    
    def _update_behavior_analysis(self) -> None:
        """Update behavioral analysis based on recent actions."""
        if len(self.recent_actions) < 3:
            return
        
        # Analyze defensive vs aggressive tendency
        recent_card_types = [action.get('card_type') for action in self.recent_actions 
                           if action.get('card_type')]
        
        if recent_card_types:
            defensive_cards = sum(1 for card_type in recent_card_types if card_type in ['Skill', 'Power'])
            self.behavior_pattern.defensive_tendency = defensive_cards / len(recent_card_types)
        
        # Analyze risk tolerance based on sand spending
        recent_sand_costs = [action.get('sand_cost', 0) for action in self.recent_actions]
        if recent_sand_costs:
            avg_spending = sum(recent_sand_costs) / len(recent_sand_costs)
            self.behavior_pattern.risk_tolerance = min(1.0, avg_spending / 3.0)  # Normalize
    
    def predict_player_next_move(self) -> Dict[str, float]:
        """Predict what the player is likely to do next."""
        if len(self.recent_actions) < 2:
            return {'attack': 0.6, 'skill': 0.2, 'power': 0.15, 'end_turn': 0.05}
        
        # Analyze recent patterns
        recent_types = [action.get('card_type', 'Unknown') for action in self.recent_actions]
        type_counts = defaultdict(int)
        for card_type in recent_types:
            if card_type != 'Unknown':
                type_counts[card_type] += 1
        
        total = sum(type_counts.values()) or 1
        
        predictions = {
            'attack': type_counts.get('Attack', 0) / total * 0.8 + 0.1,
            'skill': type_counts.get('Skill', 0) / total * 0.8 + 0.1, 
            'power': type_counts.get('Power', 0) / total * 0.8 + 0.1,
            'end_turn': 0.1
        }
        
        # Normalize predictions
        total_prob = sum(predictions.values())
        for key in predictions:
            predictions[key] /= total_prob
            
        return predictions
    
    def get_player_threat_assessment(self) -> float:
        """Assess current threat level from player (0.0 to 1.0)."""
        threat_score = 0.0
        
        # Health-based threat (lower health = higher threat for desperate plays)
        if self.player_health_history:
            current_health = self.player_health_history[-1]
            if current_health < 30:
                threat_score += 0.4
            elif current_health < 50:
                threat_score += 0.2
        
        # Recent aggressive behavior
        if self.behavior_pattern.is_player_aggressive():
            threat_score += 0.3
        
        # High sand spending patterns
        if self.behavior_pattern.get_average_sand_spending() > 2.5:
            threat_score += 0.3
        
        return min(1.0, threat_score)


class EnhancedEnemyAI(EnemyAI):
    """
    Enhanced Enemy AI with personality-based decision making and player analysis.
    
    Extends the base EnemyAI with intelligent behavioral patterns specific
    to different Egyptian enemy archetypes.
    """
    
    def __init__(self, enemy_id: str, personality: EnemyPersonality, 
                 difficulty: AIDifficultyLevel = AIDifficultyLevel.NORMAL, **kwargs):
        super().__init__(enemy_id=enemy_id, difficulty=difficulty, **kwargs)
        
        self.personality = personality
        self.player_analyzer = PlayerAnalyzer()
        
        # Personality-specific parameters
        self.personality_traits = self._configure_personality_traits()
        
        # Advanced decision making
        self.card_preferences: Dict[str, float] = {}
        self.situational_modifiers: Dict[str, float] = {}
        self.counter_strategies: Dict[str, List[str]] = {}
        
        self._initialize_personality_specific_behavior()
        
        logging.info(f"Enhanced AI created for {enemy_id} with personality {personality.value}")
    
    def _configure_personality_traits(self) -> Dict[str, float]:
        """Configure AI traits based on personality."""
        base_traits = {
            'aggression': self.aggression_level,
            'patience': self.patience_level,
            'risk_tolerance': self.risk_tolerance,
            'adaptability': 0.5,
            'prediction_accuracy': 0.5,
            'tactical_thinking': 0.5
        }
        
        # Personality-specific trait modifications
        if self.personality == EnemyPersonality.MUMMY_WARRIOR:
            base_traits.update({
                'aggression': 0.8,
                'patience': 0.2,
                'risk_tolerance': 0.7,
                'adaptability': 0.3,
                'tactical_thinking': 0.4
            })
        
        elif self.personality == EnemyPersonality.ANUBIS_SENTINEL:
            base_traits.update({
                'aggression': 0.3,
                'patience': 0.8,
                'risk_tolerance': 0.3,
                'adaptability': 0.6,
                'tactical_thinking': 0.7
            })
        
        elif self.personality == EnemyPersonality.RA_PRIEST:
            base_traits.update({
                'aggression': 0.4,
                'patience': 0.7,
                'risk_tolerance': 0.5,
                'adaptability': 0.8,
                'tactical_thinking': 0.8
            })
        
        elif self.personality == EnemyPersonality.SCARAB_GUARDIAN:
            base_traits.update({
                'aggression': 0.7,
                'patience': 0.3,
                'risk_tolerance': 0.6,
                'adaptability': 0.7,
                'tactical_thinking': 0.5
            })
        
        elif self.personality == EnemyPersonality.STRATEGIC_PHARAOH:
            base_traits.update({
                'aggression': 0.5,
                'patience': 0.6,
                'risk_tolerance': 0.4,
                'adaptability': 0.9,
                'tactical_thinking': 0.9
            })
        
        elif self.personality == EnemyPersonality.CHAOTIC_DJINN:
            base_traits.update({
                'aggression': 0.6,
                'patience': 0.2,
                'risk_tolerance': 0.8,
                'adaptability': 0.4,
                'tactical_thinking': 0.3
            })
        
        return base_traits
    
    def _initialize_personality_specific_behavior(self) -> None:
        """Initialize behavior patterns specific to personality."""
        
        if self.personality == EnemyPersonality.MUMMY_WARRIOR:
            # Prefers direct damage and physical attacks
            self.card_preferences = {
                'damage': 0.8,
                'buff_self': 0.6,
                'defensive': 0.2
            }
            
            self.counter_strategies = {
                'high_defense_player': ['buff_damage', 'multi_attack'],
                'low_health_player': ['aggressive_finish'],
                'magic_heavy_player': ['physical_resistance']
            }
        
        elif self.personality == EnemyPersonality.ANUBIS_SENTINEL:
            # Focuses on defense and counter-attacks
            self.card_preferences = {
                'block': 0.8,
                'counter_attack': 0.7,
                'debuff_player': 0.6,
                'damage': 0.4
            }
            
            self.counter_strategies = {
                'aggressive_player': ['defensive_stance', 'counter_attack'],
                'burst_damage_player': ['preemptive_block'],
                'low_patience_player': ['defensive_stall']
            }
        
        elif self.personality == EnemyPersonality.RA_PRIEST:
            # Magic, healing, and strategic play
            self.card_preferences = {
                'heal': 0.8,
                'magic_damage': 0.7,
                'buff_self': 0.6,
                'debuff_player': 0.7
            }
            
            self.counter_strategies = {
                'physical_heavy_player': ['magic_shield', 'debuff'],
                'low_health_enemy': ['prioritize_healing'],
                'fast_player': ['slow_debuffs']
            }
        
        elif self.personality == EnemyPersonality.SCARAB_GUARDIAN:
            # Speed, poison, and hit-and-run tactics
            self.card_preferences = {
                'poison': 0.8,
                'quick_attack': 0.7,
                'evasion': 0.6,
                'multi_hit': 0.5
            }
            
            self.counter_strategies = {
                'tank_player': ['poison_stack', 'evasion'],
                'healing_player': ['burst_poison'],
                'slow_player': ['speed_advantage']
            }
    
    def observe_player_action(self, action_type: ActionType, card_name: Optional[str] = None,
                            card_type: Optional[str] = None, sand_cost: int = 0,
                            player_health: int = 100) -> None:
        """Observe player action and update analysis."""
        self.player_analyzer.observe_player_action(
            action_type, card_name, card_type, sand_cost, player_health
        )
        
        # Update threat assessment based on new information
        self.threat_assessment.update_player_state(
            self.hourglass.current_sand if self.hourglass else 0,
            action_type
        )
    
    def _make_decision(self) -> None:
        """Enhanced decision making with personality and player analysis."""
        if not self.hourglass or not self.combat_engine:
            return
        
        # Get player threat and behavior analysis
        player_threat = self.player_analyzer.get_player_threat_assessment()
        player_predictions = self.player_analyzer.predict_player_next_move()
        
        # Get valid actions
        valid_actions = self.combat_engine.get_valid_actions(self.enemy_id)
        if not valid_actions:
            return
        
        # Enhanced action evaluation with personality influence
        evaluations = []
        combat_status = self.combat_engine.get_combat_status()
        
        for action_type in valid_actions:
            action_costs = self.combat_engine.get_action_costs(self.enemy_id)
            sand_cost = action_costs.get(action_type, 0)
            
            # Get base evaluation
            evaluation = self.action_evaluator.evaluate_action(
                action_type, sand_cost, self.hourglass.current_sand, combat_status
            )
            
            # Apply personality-based modifications
            evaluation = self._apply_personality_modifiers(evaluation, player_threat, player_predictions)
            
            evaluations.append(evaluation)
        
        # Select best action with personality influence
        best_action = self._select_action_with_personality(evaluations, player_predictions)
        
        if best_action and self._should_execute_action(best_action):
            self._queue_action(best_action)
            self.decision_history.append(best_action)
            if len(self.decision_history) > 50:
                self.decision_history.pop(0)
    
    def _apply_personality_modifiers(self, evaluation, player_threat: float, 
                                   player_predictions: Dict[str, float]) -> 'ActionEvaluation':
        """Apply personality-specific modifiers to action evaluation."""
        
        # Base personality trait influence
        traits = self.personality_traits
        
        # Modify based on personality type
        if self.personality == EnemyPersonality.MUMMY_WARRIOR:
            # Mummy Warriors get bonus for aggressive actions when player threat is low
            if evaluation.action_type == ActionType.PLAY_CARD and player_threat < 0.5:
                evaluation.expected_value *= 1.3
                evaluation.urgency *= 1.2
        
        elif self.personality == EnemyPersonality.ANUBIS_SENTINEL:
            # Anubis Sentinels get bonus for defensive actions when player threat is high
            if player_threat > 0.6:
                evaluation.sand_efficiency *= 1.2
                evaluation.threat_reduction *= 1.4
        
        elif self.personality == EnemyPersonality.RA_PRIEST:
            # Ra Priests adapt based on player behavior
            if 'attack' in player_predictions and player_predictions['attack'] > 0.6:
                # Player likely to attack, prepare defenses
                evaluation.threat_reduction *= 1.3
        
        elif self.personality == EnemyPersonality.SCARAB_GUARDIAN:
            # Scarab Guardians prefer quick, efficient actions
            evaluation.sand_efficiency *= 1.2
            if evaluation.urgency > 0.7:
                evaluation.expected_value *= 1.1
        
        # Apply general trait modifiers
        evaluation.expected_value *= (1.0 + traits['tactical_thinking'] * 0.2)
        evaluation.confidence *= (1.0 + traits['prediction_accuracy'] * 0.1)
        
        return evaluation
    
    def _select_action_with_personality(self, evaluations, player_predictions) -> Optional['ActionEvaluation']:
        """Select action with personality-influenced decision making."""
        if not evaluations:
            return None
        
        # Sort by total score
        evaluations.sort(key=lambda e: e.get_total_score(), reverse=True)
        
        # Apply personality-specific selection logic
        if self.personality == EnemyPersonality.CHAOTIC_DJINN:
            # Chaotic Djinn sometimes picks random actions
            if random.random() < 0.3:
                return random.choice(evaluations[:min(3, len(evaluations))])
        
        elif self.personality == EnemyPersonality.STRATEGIC_PHARAOH:
            # Strategic Pharaoh considers multiple factors
            # Weight actions based on player predictions
            for evaluation in evaluations:
                if evaluation.action_type == ActionType.ABILITY:
                    # Boost ability use if player is predictable
                    predictability = max(player_predictions.values())
                    if predictability > 0.7:
                        evaluation.expected_value *= 1.2
        
        # Add personality-based randomness
        randomness_factor = {
            EnemyPersonality.MUMMY_WARRIOR: 0.2,
            EnemyPersonality.ANUBIS_SENTINEL: 0.1,
            EnemyPersonality.RA_PRIEST: 0.15,
            EnemyPersonality.SCARAB_GUARDIAN: 0.25,
            EnemyPersonality.STRATEGIC_PHARAOH: 0.05,
            EnemyPersonality.CHAOTIC_DJINN: 0.4
        }
        
        rand_factor = randomness_factor.get(self.personality, 0.15)
        if random.random() < rand_factor and len(evaluations) > 1:
            # Sometimes pick suboptimal action
            return random.choice(evaluations[:min(3, len(evaluations))])
        
        return evaluations[0]
    
    def get_ai_status(self) -> Dict[str, Any]:
        """Get comprehensive AI status including personality info."""
        base_status = super().get_ai_status()
        
        base_status.update({
            'personality': self.personality.value,
            'personality_traits': self.personality_traits,
            'player_analysis': {
                'threat_level': self.player_analyzer.get_player_threat_assessment(),
                'predicted_moves': self.player_analyzer.predict_player_next_move(),
                'behavior_pattern': {
                    'preferred_card_type': self.player_analyzer.behavior_pattern.get_preferred_card_type(),
                    'is_aggressive': self.player_analyzer.behavior_pattern.is_player_aggressive(),
                    'is_conservative': self.player_analyzer.behavior_pattern.is_player_conservative(),
                    'avg_sand_spending': self.player_analyzer.behavior_pattern.get_average_sand_spending()
                }
            }
        })
        
        return base_status


class EnemyAIManager:
    """
    Enhanced AI Manager for coordinating multiple intelligent enemy AIs.
    
    Manages different personality types and provides unified interface
    for advanced AI behaviors.
    """
    
    def __init__(self):
        self.ais: Dict[str, EnhancedEnemyAI] = {}
        self.global_difficulty = AIDifficultyLevel.NORMAL
        self.personality_distribution: Dict[EnemyPersonality, int] = defaultdict(int)
    
    def create_enemy_ai(self, enemy_id: str, enemy_type: str, hourglass: HourGlass,
                       combat_engine, difficulty: Optional[AIDifficultyLevel] = None) -> EnhancedEnemyAI:
        """Create an enhanced AI with appropriate personality for enemy type."""
        
        # Map enemy types to personalities
        personality_mapping = {
            'mummified_priest': EnemyPersonality.RA_PRIEST,
            'tomb_sentinel': EnemyPersonality.ANUBIS_SENTINEL,
            'pharaoh_lich': EnemyPersonality.STRATEGIC_PHARAOH,
            'scarab_swarm': EnemyPersonality.SCARAB_GUARDIAN,
            'chaos_djinn': EnemyPersonality.CHAOTIC_DJINN,
            'sand_wraith': EnemyPersonality.MUMMY_WARRIOR,
            'serpent_of_apophis': EnemyPersonality.STRATEGIC_PHARAOH,
            'anubite_guard': EnemyPersonality.ANUBIS_SENTINEL,
            'sphinx_guardian': EnemyPersonality.STRATEGIC_PHARAOH
        }
        
        # Default personality based on enemy type or fallback
        personality = personality_mapping.get(enemy_type, EnemyPersonality.MUMMY_WARRIOR)
        
        ai_difficulty = difficulty or self.global_difficulty
        
        ai = EnhancedEnemyAI(
            enemy_id=enemy_id,
            personality=personality,
            difficulty=ai_difficulty
        )
        
        ai.set_hourglass(hourglass)
        ai.set_combat_engine(combat_engine)
        
        self.ais[enemy_id] = ai
        self.personality_distribution[personality] += 1
        
        logging.info(f"Created enhanced AI for {enemy_id} ({enemy_type}) with personality {personality.value}")
        
        return ai
    
    def observe_player_action(self, action_type: ActionType, card_name: Optional[str] = None,
                            card_type: Optional[str] = None, sand_cost: int = 0,
                            player_health: int = 100) -> None:
        """Broadcast player action observation to all AIs."""
        for ai in self.ais.values():
            ai.observe_player_action(action_type, card_name, card_type, sand_cost, player_health)
    
    def update_all(self, player_sand: int, player_recent_action: Optional[ActionType] = None) -> None:
        """Update all enhanced AIs."""
        for ai in self.ais.values():
            ai.update(player_sand, player_recent_action)
    
    def get_ai(self, enemy_id: str) -> Optional[EnhancedEnemyAI]:
        """Get specific enhanced enemy AI."""
        return self.ais.get(enemy_id)
    
    def remove_ai(self, enemy_id: str) -> None:
        """Remove AI and update personality distribution."""
        if enemy_id in self.ais:
            ai = self.ais[enemy_id]
            self.personality_distribution[ai.personality] -= 1
            del self.ais[enemy_id]
            logging.info(f"Removed enhanced AI for {enemy_id}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'total_ais': len(self.ais),
            'personality_distribution': dict(self.personality_distribution),
            'global_difficulty': self.global_difficulty.value,
            'individual_ai_status': {
                enemy_id: ai.get_ai_status() 
                for enemy_id, ai in self.ais.items()
            }
        }


# Global enhanced AI manager
enhanced_ai_manager = EnemyAIManager()