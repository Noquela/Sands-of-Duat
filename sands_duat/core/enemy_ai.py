"""
Enemy AI System with Strategic Sand Management

Implements intelligent enemy behavior that strategically manages
sand resources, timing actions optimally, and adapting to player
strategies in the Hour-Glass Initiative system.

Key Features:
- Strategic sand resource management
- Action timing optimization
- Adaptive behavior based on player patterns
- Multiple AI difficulty levels
- Sand-efficient action selection

Classes:
- SandStrategy: Different sand management strategies
- EnemyAI: Main AI decision-making system
- ActionEvaluator: Evaluates action effectiveness
- ThreatAssessment: Analyzes combat threats
"""

import logging
import random
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Callable
from pydantic import BaseModel, Field
from dataclasses import dataclass
from collections import defaultdict, deque

from .combat_enhanced import EnhancedCombatAction, ActionType, ActionPriority, EnhancedCombatEngine
from .hourglass import HourGlass
from .sand_visuals import sand_visualizer


class SandStrategy(Enum):
    """Different sand management strategies for enemies."""
    AGGRESSIVE = "aggressive"      # Spend sand quickly for immediate pressure
    CONSERVATIVE = "conservative"  # Save sand for powerful moves
    ADAPTIVE = "adaptive"         # Adjust based on player behavior
    OPPORTUNISTIC = "opportunistic"  # Wait for optimal moments
    BALANCED = "balanced"         # Mix of all strategies


class AIThreatLevel(Enum):
    """Threat assessment levels."""
    MINIMAL = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    CRITICAL = 5


class AIDifficultyLevel(Enum):
    """AI difficulty levels."""
    EASY = "easy"
    NORMAL = "normal"  
    HARD = "hard"
    EXPERT = "expert"
    MASTER = "master"


@dataclass
class ActionEvaluation:
    """Evaluation of a potential action."""
    action_type: ActionType
    expected_value: float  # Higher is better
    sand_efficiency: float  # Value per sand spent
    threat_reduction: float  # How much this reduces player threat
    opportunity_cost: float  # What we give up by taking this action
    urgency: float  # How time-sensitive this action is
    confidence: float  # AI confidence in this evaluation (0-1)
    
    def get_total_score(self) -> float:
        """Calculate total action score."""
        return (self.expected_value * 0.3 + 
                self.sand_efficiency * 0.2 +
                self.threat_reduction * 0.2 +
                (1.0 - self.opportunity_cost) * 0.15 +
                self.urgency * 0.15) * self.confidence


class ThreatAssessment(BaseModel):
    """Assesses threats and opportunities in combat."""
    
    enemy_id: str
    player_threat_level: AIThreatLevel = AIThreatLevel.MODERATE
    player_sand_pattern: List[int] = Field(default_factory=list)  # Recent sand levels
    player_action_history: List[ActionType] = Field(default_factory=list)
    time_pressure: float = Field(default=0.5, ge=0.0, le=1.0)  # How much time pressure we're under
    
    def update_player_state(self, player_sand: int, recent_action: Optional[ActionType] = None) -> None:
        """Update assessment based on player state."""
        # Track sand patterns
        self.player_sand_pattern.append(player_sand)
        if len(self.player_sand_pattern) > 20:  # Keep last 20 observations
            self.player_sand_pattern.pop(0)
        
        # Track action history
        if recent_action:
            self.player_action_history.append(recent_action)
            if len(self.player_action_history) > 10:  # Keep last 10 actions
                self.player_action_history.pop(0)
        
        # Update threat level based on player sand
        self._assess_threat_level()
    
    def _assess_threat_level(self) -> None:
        """Assess current threat level from player."""
        if not self.player_sand_pattern:
            return
        
        current_sand = self.player_sand_pattern[-1]
        avg_sand = sum(self.player_sand_pattern) / len(self.player_sand_pattern)
        
        # High sand = high threat potential
        if current_sand >= 5:
            self.player_threat_level = AIThreatLevel.HIGH
        elif current_sand >= 3 and avg_sand >= 3:
            self.player_threat_level = AIThreatLevel.MODERATE
        elif current_sand <= 1:
            self.player_threat_level = AIThreatLevel.LOW
        else:
            self.player_threat_level = AIThreatLevel.MODERATE
    
    def predict_player_next_action(self) -> Dict[ActionType, float]:
        """Predict probability of player's next action."""
        if not self.player_action_history:
            # Default predictions
            return {
                ActionType.PLAY_CARD: 0.6,
                ActionType.ABILITY: 0.2,
                ActionType.END_TURN: 0.15,
                ActionType.FLEE: 0.05
            }
        
        # Analyze recent patterns
        action_counts = defaultdict(int)
        for action in self.player_action_history[-5:]:  # Last 5 actions
            action_counts[action] += 1
        
        total = sum(action_counts.values())
        if total == 0:
            total = 1
        
        # Convert to probabilities with some base probability
        predictions = {}
        for action_type in ActionType:
            count = action_counts.get(action_type, 0)
            base_prob = 0.1  # Minimum probability
            pattern_prob = count / total * 0.8  # 80% weight to patterns
            predictions[action_type] = base_prob + pattern_prob
        
        # Normalize
        total_prob = sum(predictions.values())
        for action_type in predictions:
            predictions[action_type] /= total_prob
        
        return predictions
    
    def get_recommended_strategy(self) -> SandStrategy:
        """Get recommended strategy based on current assessment."""
        if self.player_threat_level == AIThreatLevel.CRITICAL:
            return SandStrategy.AGGRESSIVE
        elif self.player_threat_level == AIThreatLevel.HIGH:
            return SandStrategy.OPPORTUNISTIC
        elif self.player_threat_level == AIThreatLevel.LOW:
            return SandStrategy.CONSERVATIVE
        else:
            return SandStrategy.BALANCED


class ActionEvaluator(BaseModel):
    """Evaluates the effectiveness of potential actions."""
    
    enemy_id: str
    difficulty: AIDifficultyLevel = AIDifficultyLevel.NORMAL
    threat_assessment: ThreatAssessment
    
    def evaluate_action(self, action_type: ActionType, sand_cost: int, 
                       current_sand: int, combat_state: Dict[str, Any]) -> ActionEvaluation:
        """Evaluate a potential action."""
        
        # Base evaluation
        evaluation = ActionEvaluation(
            action_type=action_type,
            expected_value=self._calculate_expected_value(action_type, combat_state),
            sand_efficiency=self._calculate_sand_efficiency(action_type, sand_cost),
            threat_reduction=self._calculate_threat_reduction(action_type),
            opportunity_cost=self._calculate_opportunity_cost(action_type, sand_cost, current_sand),
            urgency=self._calculate_urgency(action_type),
            confidence=self._get_confidence_level()
        )
        
        return evaluation
    
    def _calculate_expected_value(self, action_type: ActionType, combat_state: Dict[str, Any]) -> float:
        """Calculate expected value of an action."""
        base_values = {
            ActionType.PLAY_CARD: 0.7,
            ActionType.ABILITY: 0.8,
            ActionType.END_TURN: 0.1,
            ActionType.FLEE: 0.0
        }
        
        value = base_values.get(action_type, 0.5)
        
        # Adjust based on combat state
        if action_type == ActionType.PLAY_CARD:
            # Cards are more valuable when we need to apply pressure
            if self.threat_assessment.player_threat_level == AIThreatLevel.HIGH:
                value += 0.2
        elif action_type == ActionType.ABILITY:
            # Abilities are more valuable in critical situations
            if self.threat_assessment.player_threat_level >= AIThreatLevel.HIGH:
                value += 0.3
        
        return min(1.0, value)
    
    def _calculate_sand_efficiency(self, action_type: ActionType, sand_cost: int) -> float:
        """Calculate sand efficiency (value per sand)."""
        if sand_cost == 0:
            return 1.0  # Free actions are always efficient
        
        base_efficiency = {
            ActionType.PLAY_CARD: 0.7,  # Good efficiency
            ActionType.ABILITY: 0.6,    # Slightly less efficient but powerful
            ActionType.END_TURN: 1.0,   # Free
            ActionType.FLEE: 1.0        # Free
        }
        
        efficiency = base_efficiency.get(action_type, 0.5)
        return efficiency / max(1, sand_cost)
    
    def _calculate_threat_reduction(self, action_type: ActionType) -> float:
        """Calculate how much this action reduces player threat."""
        threat_reduction = {
            ActionType.PLAY_CARD: 0.6,
            ActionType.ABILITY: 0.8,
            ActionType.END_TURN: 0.0,
            ActionType.FLEE: 0.0
        }
        
        base_reduction = threat_reduction.get(action_type, 0.0)
        
        # Scale by current threat level
        threat_multiplier = self.threat_assessment.player_threat_level.value / 5.0
        return base_reduction * threat_multiplier
    
    def _calculate_opportunity_cost(self, action_type: ActionType, sand_cost: int, current_sand: int) -> float:
        """Calculate opportunity cost of spending sand now."""
        if sand_cost == 0:
            return 0.0
        
        # Higher cost when we're low on sand
        sand_ratio = sand_cost / max(1, current_sand)
        base_cost = sand_ratio * 0.5
        
        # Adjust based on strategy
        if self.threat_assessment.get_recommended_strategy() == SandStrategy.CONSERVATIVE:
            base_cost += 0.2  # Higher opportunity cost for conservative strategy
        elif self.threat_assessment.get_recommended_strategy() == SandStrategy.AGGRESSIVE:
            base_cost -= 0.1  # Lower opportunity cost for aggressive strategy
        
        return min(1.0, base_cost)
    
    def _calculate_urgency(self, action_type: ActionType) -> float:
        """Calculate urgency of action."""
        base_urgency = {
            ActionType.PLAY_CARD: 0.5,
            ActionType.ABILITY: 0.7,
            ActionType.END_TURN: 0.1,
            ActionType.FLEE: 1.0  # Fleeing is always urgent when considered
        }
        
        urgency = base_urgency.get(action_type, 0.5)
        
        # Increase urgency with threat level
        if self.threat_assessment.player_threat_level >= AIThreatLevel.HIGH:
            urgency += 0.3
        
        return min(1.0, urgency)
    
    def _get_confidence_level(self) -> float:
        """Get AI confidence level based on difficulty."""
        confidence_by_difficulty = {
            AIDifficultyLevel.EASY: 0.6,
            AIDifficultyLevel.NORMAL: 0.7,
            AIDifficultyLevel.HARD: 0.8,
            AIDifficultyLevel.EXPERT: 0.9,
            AIDifficultyLevel.MASTER: 0.95
        }
        
        base_confidence = confidence_by_difficulty.get(self.difficulty, 0.7)
        
        # Add some randomness
        randomness = random.uniform(-0.1, 0.1)
        return max(0.1, min(1.0, base_confidence + randomness))


class EnemyAI(BaseModel):
    """
    Main enemy AI system with strategic sand management.
    
    Manages decision-making, action timing, and strategic adaptation
    for enemies in the Hour-Glass Initiative combat system.
    """
    
    enemy_id: str
    difficulty: AIDifficultyLevel = AIDifficultyLevel.NORMAL
    strategy: SandStrategy = SandStrategy.BALANCED
    hourglass: Optional[HourGlass] = Field(default=None, exclude=True)
    combat_engine: Optional[EnhancedCombatEngine] = Field(default=None, exclude=True)
    
    # AI state
    threat_assessment: ThreatAssessment = Field(default=None)
    action_evaluator: ActionEvaluator = Field(default=None)
    decision_history: List[ActionEvaluation] = Field(default_factory=list)
    last_decision_time: float = Field(default=0.0)
    
    # Strategy parameters
    aggression_level: float = Field(default=0.5, ge=0.0, le=1.0)
    patience_level: float = Field(default=0.5, ge=0.0, le=1.0)
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Performance tracking
    actions_taken: int = Field(default=0)
    sand_spent: int = Field(default=0)
    decisions_per_second: float = Field(default=0.0)
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.threat_assessment:
            self.threat_assessment = ThreatAssessment(enemy_id=self.enemy_id)
        if not self.action_evaluator:
            self.action_evaluator = ActionEvaluator(
                enemy_id=self.enemy_id,
                difficulty=self.difficulty,
                threat_assessment=self.threat_assessment
            )
        self._configure_for_difficulty()
    
    def _configure_for_difficulty(self) -> None:
        """Configure AI parameters based on difficulty level."""
        if self.difficulty == AIDifficultyLevel.EASY:
            self.aggression_level = 0.3
            self.patience_level = 0.7
            self.risk_tolerance = 0.3
        elif self.difficulty == AIDifficultyLevel.NORMAL:
            self.aggression_level = 0.5
            self.patience_level = 0.5
            self.risk_tolerance = 0.5
        elif self.difficulty == AIDifficultyLevel.HARD:
            self.aggression_level = 0.7
            self.patience_level = 0.4
            self.risk_tolerance = 0.7
        elif self.difficulty == AIDifficultyLevel.EXPERT:
            self.aggression_level = 0.8
            self.patience_level = 0.3
            self.risk_tolerance = 0.8
        else:  # MASTER
            self.aggression_level = 0.9
            self.patience_level = 0.2
            self.risk_tolerance = 0.9
    
    def set_hourglass(self, hourglass: HourGlass) -> None:
        """Set the hourglass this AI manages."""
        self.hourglass = hourglass
    
    def set_combat_engine(self, engine: EnhancedCombatEngine) -> None:
        """Set the combat engine for action queuing."""
        self.combat_engine = engine
    
    def update(self, player_sand: int, player_recent_action: Optional[ActionType] = None) -> None:
        """Update AI state and make decisions."""
        if not self.hourglass or not self.combat_engine:
            return
        
        # Update threat assessment
        self.threat_assessment.update_player_state(player_sand, player_recent_action)
        
        # Adapt strategy if needed
        self._adapt_strategy()
        
        # Make decision if it's time
        current_time = time.time()
        decision_interval = self._get_decision_interval()
        
        if current_time - self.last_decision_time >= decision_interval:
            self._make_decision()
            self.last_decision_time = current_time
    
    def _adapt_strategy(self) -> None:
        """Adapt strategy based on current situation."""
        if self.strategy == SandStrategy.ADAPTIVE:
            recommended = self.threat_assessment.get_recommended_strategy()
            if recommended != SandStrategy.ADAPTIVE:
                self.strategy = recommended
                logging.debug(f"AI {self.enemy_id} adapted strategy to {recommended.value}")
    
    def _get_decision_interval(self) -> float:
        """Get how often AI should make decisions."""
        base_interval = {
            AIDifficultyLevel.EASY: 2.0,
            AIDifficultyLevel.NORMAL: 1.5,
            AIDifficultyLevel.HARD: 1.0,
            AIDifficultyLevel.EXPERT: 0.8,
            AIDifficultyLevel.MASTER: 0.5
        }
        
        interval = base_interval.get(self.difficulty, 1.0)
        
        # Adjust based on urgency
        if self.threat_assessment.player_threat_level >= AIThreatLevel.HIGH:
            interval *= 0.7  # React faster to high threats
        
        return interval
    
    def _make_decision(self) -> None:
        """Make an AI decision and potentially queue an action."""
        if not self.hourglass or not self.combat_engine:
            return
        
        # Get valid actions
        valid_actions = self.combat_engine.get_valid_actions(self.enemy_id)
        if not valid_actions:
            return
        
        # Evaluate all possible actions
        evaluations = []
        combat_status = self.combat_engine.get_combat_status()
        
        for action_type in valid_actions:
            action_costs = self.combat_engine.get_action_costs(self.enemy_id)
            sand_cost = action_costs.get(action_type, 0)
            
            evaluation = self.action_evaluator.evaluate_action(
                action_type, sand_cost, self.hourglass.current_sand, combat_status
            )
            evaluations.append(evaluation)
        
        # Select best action based on strategy
        best_action = self._select_action(evaluations)
        
        if best_action and self._should_execute_action(best_action):
            self._queue_action(best_action)
            self.decision_history.append(best_action)
            if len(self.decision_history) > 50:  # Keep last 50 decisions
                self.decision_history.pop(0)
    
    def _select_action(self, evaluations: List[ActionEvaluation]) -> Optional[ActionEvaluation]:
        """Select the best action based on current strategy."""
        if not evaluations:
            return None
        
        # Sort by total score
        evaluations.sort(key=lambda e: e.get_total_score(), reverse=True)
        
        # Strategy-based selection
        if self.strategy == SandStrategy.AGGRESSIVE:
            # Prefer high-cost, high-impact actions
            evaluations.sort(key=lambda e: e.urgency * e.expected_value, reverse=True)
        elif self.strategy == SandStrategy.CONSERVATIVE:
            # Prefer sand-efficient actions
            evaluations.sort(key=lambda e: e.sand_efficiency, reverse=True)
        elif self.strategy == SandStrategy.OPPORTUNISTIC:
            # Wait for optimal moments
            best = evaluations[0]
            if best.get_total_score() < 0.7:  # Arbitrary threshold
                return None  # Wait for better opportunity
        
        # Add some randomness based on difficulty
        randomness_factor = {
            AIDifficultyLevel.EASY: 0.3,
            AIDifficultyLevel.NORMAL: 0.2,
            AIDifficultyLevel.HARD: 0.1,
            AIDifficultyLevel.EXPERT: 0.05,
            AIDifficultyLevel.MASTER: 0.02
        }
        
        rand_factor = randomness_factor.get(self.difficulty, 0.1)
        if random.random() < rand_factor and len(evaluations) > 1:
            # Sometimes pick suboptimal action
            return random.choice(evaluations[:3])  # Top 3 actions
        
        return evaluations[0]
    
    def _should_execute_action(self, evaluation: ActionEvaluation) -> bool:
        """Decide whether to execute the selected action."""
        # Always execute if it's high urgency
        if evaluation.urgency >= 0.8:
            return True
        
        # Check patience level
        if evaluation.get_total_score() < self.patience_level:
            return False  # Wait for better opportunity
        
        # Consider sand conservation
        if evaluation.action_type in [ActionType.PLAY_CARD, ActionType.ABILITY]:
            if self.hourglass.current_sand <= 2 and self.strategy == SandStrategy.CONSERVATIVE:
                return False  # Save sand
        
        return True
    
    def _queue_action(self, evaluation: ActionEvaluation) -> None:
        """Queue the selected action."""
        action_costs = self.combat_engine.get_action_costs(self.enemy_id)
        sand_cost = action_costs.get(evaluation.action_type, 0)
        
        # Create enhanced action
        action = EnhancedCombatAction(
            action_type=evaluation.action_type,
            actor_id=self.enemy_id,
            sand_cost=sand_cost,
            priority=self._get_action_priority(evaluation),
            animation_duration=self._get_animation_duration(evaluation.action_type)
        )
        
        # Queue the action
        success = self.combat_engine.queue_action(action)
        
        if success:
            self.actions_taken += 1
            self.sand_spent += sand_cost
            logging.debug(f"AI {self.enemy_id} queued {evaluation.action_type.value} (cost: {sand_cost})")
        else:
            logging.warning(f"AI {self.enemy_id} failed to queue {evaluation.action_type.value}")
    
    def _get_action_priority(self, evaluation: ActionEvaluation) -> int:
        """Get priority for the action."""
        base_priority = ActionPriority.STANDARD.value
        
        # Adjust based on urgency
        if evaluation.urgency >= 0.8:
            base_priority = ActionPriority.REACTION.value
        elif evaluation.urgency <= 0.3:
            base_priority = ActionPriority.PASSIVE.value
        
        # Add randomness
        return base_priority + random.randint(-5, 5)
    
    def _get_animation_duration(self, action_type: ActionType) -> float:
        """Get expected animation duration for action."""
        durations = {
            ActionType.PLAY_CARD: 0.8,
            ActionType.ABILITY: 1.2,
            ActionType.END_TURN: 0.2,
            ActionType.FLEE: 0.5
        }
        
        base_duration = durations.get(action_type, 0.5)
        
        # Add slight randomness
        return base_duration + random.uniform(-0.1, 0.1)
    
    def get_ai_status(self) -> Dict[str, Any]:
        """Get comprehensive AI status for debugging."""
        return {
            'enemy_id': self.enemy_id,
            'difficulty': self.difficulty.value,
            'strategy': self.strategy.value,
            'aggression_level': self.aggression_level,
            'patience_level': self.patience_level,
            'risk_tolerance': self.risk_tolerance,
            'threat_assessment': {
                'player_threat_level': self.threat_assessment.player_threat_level.value,
                'recommended_strategy': self.threat_assessment.get_recommended_strategy().value
            },
            'performance': {
                'actions_taken': self.actions_taken,
                'sand_spent': self.sand_spent,
                'decisions_per_second': self.decisions_per_second
            },
            'recent_decisions': [
                {
                    'action_type': eval.action_type.value,
                    'total_score': eval.get_total_score(),
                    'confidence': eval.confidence
                }
                for eval in self.decision_history[-5:]  # Last 5 decisions
            ]
        }
    
    def force_action(self, action_type: ActionType) -> bool:
        """Force AI to attempt a specific action (for testing/debugging)."""
        if not self.combat_engine:
            return False
        
        action_costs = self.combat_engine.get_action_costs(self.enemy_id)
        sand_cost = action_costs.get(action_type, 0)
        
        if not self.hourglass.can_afford(sand_cost):
            return False
        
        action = EnhancedCombatAction(
            action_type=action_type,
            actor_id=self.enemy_id,
            sand_cost=sand_cost,
            priority=ActionPriority.INTERRUPT.value
        )
        
        return self.combat_engine.queue_action(action)


class EnemyAIManager:
    """
    Manages multiple enemy AIs in combat.
    
    Coordinates AI decision-making and provides unified
    interface for AI management.
    """
    
    def __init__(self):
        self.ais: Dict[str, EnemyAI] = {}
        self.global_difficulty = AIDifficultyLevel.NORMAL
    
    def register_enemy_ai(self, enemy_id: str, hourglass: HourGlass, 
                         combat_engine: EnhancedCombatEngine,
                         difficulty: Optional[AIDifficultyLevel] = None) -> EnemyAI:
        """Register a new enemy AI."""
        ai_difficulty = difficulty or self.global_difficulty
        
        ai = EnemyAI(
            enemy_id=enemy_id,
            difficulty=ai_difficulty
        )
        ai.set_hourglass(hourglass)
        ai.set_combat_engine(combat_engine)
        
        self.ais[enemy_id] = ai
        logging.info(f"Registered enemy AI for {enemy_id} with difficulty {ai_difficulty.value}")
        
        return ai
    
    def unregister_enemy_ai(self, enemy_id: str) -> None:
        """Remove enemy AI."""
        if enemy_id in self.ais:
            del self.ais[enemy_id]
            logging.info(f"Unregistered enemy AI for {enemy_id}")
    
    def update_all(self, player_sand: int, player_recent_action: Optional[ActionType] = None) -> None:
        """Update all enemy AIs."""
        for ai in self.ais.values():
            ai.update(player_sand, player_recent_action)
    
    def set_global_difficulty(self, difficulty: AIDifficultyLevel) -> None:
        """Set difficulty for all AIs."""
        self.global_difficulty = difficulty
        for ai in self.ais.values():
            ai.difficulty = difficulty
            ai._configure_for_difficulty()
    
    def get_ai(self, enemy_id: str) -> Optional[EnemyAI]:
        """Get specific enemy AI."""
        return self.ais.get(enemy_id)
    
    def get_all_ai_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all AIs."""
        return {
            enemy_id: ai.get_ai_status()
            for enemy_id, ai in self.ais.items()
        }


# Global enemy AI manager
enemy_ai_manager = EnemyAIManager()