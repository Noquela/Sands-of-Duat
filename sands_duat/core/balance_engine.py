"""
Balance Engine for Sands of Duat

Advanced card balancing system that ensures strategic depth and fair play
while maintaining the Egyptian underworld theme.

Features:
- Dynamic power level calculation
- Sand cost efficiency analysis  
- Synergy evaluation and balancing
- Real-time balance adjustments
- Meta-game progression tracking
"""

import logging
import statistics
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from .cards import Card, CardEffect, EffectType, CardType, CardRarity
from .hourglass import HourGlass


class BalanceMetric(Enum):
    """Metrics used for card balance evaluation."""
    DAMAGE_PER_SAND = "damage_per_sand"
    HEAL_PER_SAND = "heal_per_sand"
    CARD_ADVANTAGE = "card_advantage"
    TEMPO_VALUE = "tempo_value"
    SYNERGY_POTENTIAL = "synergy_potential"
    FLEXIBILITY = "flexibility"


@dataclass
class CardAnalysis:
    """Analysis results for a single card."""
    card_id: str
    power_level: float
    efficiency_rating: float
    balance_score: float
    recommendations: List[str]
    synergy_ratings: Dict[str, float]
    meta_position: str  # "underpowered", "balanced", "overpowered"


class BalanceEngine:
    """
    Advanced balance engine for strategic card evaluation.
    
    Analyzes cards across multiple dimensions to ensure
    balanced gameplay and meaningful strategic choices.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Balance constants - refined through playtesting
        self.DAMAGE_PER_SAND_BASELINE = 5.0  # Expected damage per sand
        self.HEAL_PER_SAND_BASELINE = 4.0    # Expected healing per sand
        self.CARD_DRAW_VALUE = 3.0           # Sand value of drawing 1 card
        self.STATUS_EFFECT_VALUES = {
            "vulnerable": 2.0,  # Value per stack
            "weak": 1.5,
            "strength": 2.5,
            "dexterity": 2.0,
            "block": 1.0,      # Per point of block
        }
        
        # Rarity power scaling
        self.RARITY_POWER_MULTIPLIERS = {
            CardRarity.COMMON: 1.0,
            CardRarity.UNCOMMON: 1.2,
            CardRarity.RARE: 1.4,
            CardRarity.EPIC: 1.7,
            CardRarity.LEGENDARY: 2.0
        }
        
        self.logger.info("Balance Engine initialized")
    
    def analyze_card(self, card: Card) -> CardAnalysis:
        """
        Perform comprehensive balance analysis on a card.
        
        Args:
            card: Card to analyze
            
        Returns:
            Detailed analysis with balance recommendations
        """
        power_level = self.calculate_power_level(card)
        efficiency_rating = self.calculate_efficiency(card)
        synergy_ratings = self.evaluate_synergies(card)
        balance_score = self.calculate_balance_score(card, power_level, efficiency_rating)
        
        recommendations = self.generate_recommendations(card, power_level, efficiency_rating)
        meta_position = self.determine_meta_position(balance_score)
        
        analysis = CardAnalysis(
            card_id=card.id,
            power_level=power_level,
            efficiency_rating=efficiency_rating,
            balance_score=balance_score,
            recommendations=recommendations,
            synergy_ratings=synergy_ratings,
            meta_position=meta_position
        )
        
        self.logger.debug(f"Analyzed {card.name}: {meta_position} (score: {balance_score:.2f})")
        return analysis
    
    def calculate_power_level(self, card: Card) -> float:
        """
        Calculate the raw power level of a card.
        
        Considers all effects and their values relative to sand cost.
        """
        total_value = 0.0
        
        for effect in card.effects:
            effect_value = self.evaluate_effect_value(effect)
            
            # Apply resonance bonuses
            if effect.resonance_bonus:
                for sand_amount, bonus in effect.resonance_bonus.items():
                    effect_value += bonus * 0.3  # Average 30% of bonus value
            
            # Apply momentum scaling
            if effect.momentum_scaling:
                effect_value *= 1.2  # 20% bonus for momentum synergy
            
            total_value += effect_value
        
        # Apply rarity multiplier
        rarity_multiplier = self.RARITY_POWER_MULTIPLIERS.get(card.rarity, 1.0)
        total_value *= rarity_multiplier
        
        # Apply keyword bonuses
        keyword_bonus = self.calculate_keyword_value(card)
        total_value += keyword_bonus
        
        # Adjust for special mechanics
        if card.mummified:
            total_value *= 1.4  # Mummified cards are more powerful
        
        if card.exhaust:
            total_value *= 1.6  # One-time use cards should be stronger
        
        if card.ethereal:
            total_value *= 0.8  # Temporary cards are weaker
        
        return total_value
    
    def evaluate_effect_value(self, effect: CardEffect) -> float:
        """Evaluate the sand value of a single card effect."""
        if effect.effect_type == EffectType.DAMAGE:
            return effect.value / self.DAMAGE_PER_SAND_BASELINE
        
        elif effect.effect_type == EffectType.HEAL:
            return effect.value / self.HEAL_PER_SAND_BASELINE
        
        elif effect.effect_type == EffectType.BLOCK:
            return effect.value * self.STATUS_EFFECT_VALUES["block"]
        
        elif effect.effect_type == EffectType.DRAW_CARDS:
            return effect.value * self.CARD_DRAW_VALUE
        
        elif effect.effect_type == EffectType.GAIN_SAND:
            return effect.value * 1.5  # Sand is valuable
        
        elif effect.effect_type in [EffectType.APPLY_VULNERABLE, EffectType.APPLY_WEAK]:
            status_name = effect.effect_type.value.replace("apply_", "")
            base_value = self.STATUS_EFFECT_VALUES.get(status_name, 1.0)
            duration = effect.metadata.get("duration", 1)
            return effect.value * base_value * min(duration, 3) * 0.5  # Diminishing returns
        
        elif effect.effect_type in [EffectType.APPLY_STRENGTH, EffectType.APPLY_DEXTERITY]:
            status_name = effect.effect_type.value.replace("apply_", "")
            base_value = self.STATUS_EFFECT_VALUES.get(status_name, 1.0)
            duration = effect.metadata.get("duration", 1)
            return effect.value * base_value * min(duration, 5) * 0.3
        
        elif effect.effect_type == EffectType.MAX_HEALTH_INCREASE:
            return effect.value * 0.8  # Permanent health is valuable
        
        elif effect.effect_type == EffectType.PERMANENT_SAND_INCREASE:
            return effect.value * 5.0  # Very valuable long-term
        
        # New mechanics
        elif effect.effect_type == EffectType.MUMMIFY:
            return 3.0  # Fixed value for mummification
        
        elif effect.effect_type == EffectType.DIVINE_JUDGMENT:
            return 2.5  # Moderate value for judgment effects
        
        elif effect.effect_type == EffectType.SOUL_FRAGMENT:
            return effect.value * 1.5  # Flexible resource
        
        else:
            return 1.0  # Default value for unknown effects
    
    def calculate_keyword_value(self, card: Card) -> float:
        """Calculate the additional value provided by card keywords."""
        keyword_values = {
            "instant": 2.0,     # Can interrupt, very valuable
            "retain": 1.5,      # Flexibility bonus
            "divine": 0.5,      # Synergy potential
            "pharaoh": 0.8,     # Strong synergy potential
            "ritual": 1.0,      # Chain potential
            "cantrip": 1.0,     # Replaces itself
        }
        
        total_value = 0.0
        for keyword in card.keywords:
            total_value += keyword_values.get(keyword.lower(), 0.0)
        
        return total_value
    
    def calculate_efficiency(self, card: Card) -> float:
        """
        Calculate sand cost efficiency of a card.
        
        Higher efficiency means better value per sand spent.
        """
        if card.sand_cost == 0:
            # 0-cost cards are evaluated differently
            power_level = self.calculate_power_level(card)
            return min(power_level * 2, 10.0)  # Cap to prevent infinite efficiency
        
        power_level = self.calculate_power_level(card)
        return power_level / card.sand_cost
    
    def evaluate_synergies(self, card: Card) -> Dict[str, float]:
        """
        Evaluate potential synergies with other cards/mechanics.
        
        Returns ratings for different synergy categories.
        """
        synergies = {
            "divine_pantheon": 0.0,
            "ritual_chains": 0.0,
            "mummification": 0.0,
            "temporal_momentum": 0.0,
            "sand_resonance": 0.0,
            "soul_fragment": 0.0
        }
        
        # Divine pantheon synergies
        divine_keywords = {"ra", "thoth", "anubis", "isis", "horus", "bastet", "sekhmet", "osiris"}
        if any(keyword in card.keywords for keyword in divine_keywords):
            synergies["divine_pantheon"] = 3.0
        
        # Ritual chain potential
        if "ritual" in card.keywords or any(effect.effect_type == EffectType.BLESSING for effect in card.effects):
            synergies["ritual_chains"] = 2.5
        
        # Mummification synergies
        if card.mummified or "mummy" in card.keywords:
            synergies["mummification"] = 2.0
        
        # Temporal momentum potential
        if any(effect.momentum_scaling for effect in card.effects):
            synergies["temporal_momentum"] = 2.8
        
        # Sand resonance potential
        if any(effect.resonance_bonus for effect in card.effects):
            synergies["sand_resonance"] = 2.2
        
        # Soul fragment mechanics
        if card.soul_fragments > 0 or any(effect.effect_type == EffectType.SOUL_FRAGMENT for effect in card.effects):
            synergies["soul_fragment"] = 1.8
        
        return synergies
    
    def calculate_balance_score(self, card: Card, power_level: float, efficiency: float) -> float:
        """
        Calculate overall balance score for a card.
        
        Score of 1.0 = perfectly balanced
        Score > 1.0 = overpowered
        Score < 1.0 = underpowered
        """
        expected_power = card.sand_cost * 1.0  # Baseline expectation
        if card.sand_cost == 0:
            expected_power = 0.8  # 0-cost cards should be slightly weaker
        
        # Adjust expectations based on rarity
        rarity_multiplier = self.RARITY_POWER_MULTIPLIERS.get(card.rarity, 1.0)
        expected_power *= rarity_multiplier
        
        # Calculate deviation from expected power
        power_ratio = power_level / expected_power if expected_power > 0 else 1.0
        
        # Efficiency weighting (prefer efficient cards but not too efficient)
        ideal_efficiency = 1.2  # Slightly above baseline is good
        efficiency_ratio = min(efficiency / ideal_efficiency, 2.0)  # Cap excessive efficiency
        
        # Combine metrics
        balance_score = (power_ratio * 0.7) + (efficiency_ratio * 0.3)
        
        return balance_score
    
    def generate_recommendations(self, card: Card, power_level: float, efficiency: float) -> List[str]:
        """Generate specific balance recommendations for a card."""
        recommendations = []
        
        balance_score = self.calculate_balance_score(card, power_level, efficiency)
        
        if balance_score > 1.3:
            recommendations.append("Card is overpowered - consider reducing effect values or increasing sand cost")
            
            if efficiency > 2.0:
                recommendations.append("Efficiency too high - increase sand cost by 1")
            
            # Specific effect recommendations
            for effect in card.effects:
                if effect.effect_type == EffectType.DAMAGE and effect.value > card.sand_cost * 6:
                    recommendations.append(f"Damage too high - reduce from {effect.value} to {card.sand_cost * 5}")
        
        elif balance_score < 0.7:
            recommendations.append("Card is underpowered - consider increasing effect values or adding synergy")
            
            if efficiency < 0.8:
                recommendations.append("Efficiency too low - reduce sand cost by 1 or increase effect values")
            
            # Enhancement suggestions
            if not any(effect.resonance_bonus for effect in card.effects):
                recommendations.append("Add sand resonance bonus to increase strategic depth")
        
        else:
            recommendations.append("Card balance is good - no major changes needed")
        
        # Synergy recommendations
        synergy_count = sum(1 for rating in self.evaluate_synergies(card).values() if rating > 2.0)
        if synergy_count == 0:
            recommendations.append("Consider adding keyword synergies to increase strategic potential")
        
        return recommendations
    
    def determine_meta_position(self, balance_score: float) -> str:
        """Determine a card's position in the meta-game."""
        if balance_score >= 1.3:
            return "overpowered"
        elif balance_score >= 0.8:
            return "balanced"
        else:
            return "underpowered"
    
    def analyze_card_set(self, cards: List[Card]) -> Dict[str, Any]:
        """
        Analyze an entire set of cards for balance.
        
        Args:
            cards: List of cards to analyze
            
        Returns:
            Comprehensive set analysis with recommendations
        """
        analyses = [self.analyze_card(card) for card in cards]
        
        # Calculate set-wide statistics
        balance_scores = [analysis.balance_score for analysis in analyses]
        power_levels = [analysis.power_level for analysis in analyses]
        
        set_analysis = {
            "total_cards": len(cards),
            "average_balance_score": statistics.mean(balance_scores),
            "balance_score_std": statistics.stdev(balance_scores) if len(balance_scores) > 1 else 0,
            "overpowered_count": len([a for a in analyses if a.meta_position == "overpowered"]),
            "underpowered_count": len([a for a in analyses if a.meta_position == "underpowered"]),
            "balanced_count": len([a for a in analyses if a.meta_position == "balanced"]),
            "card_analyses": analyses,
            "recommendations": self.generate_set_recommendations(analyses)
        }
        
        self.logger.info(f"Analyzed {len(cards)} cards: {set_analysis['balanced_count']} balanced, "
                        f"{set_analysis['overpowered_count']} overpowered, {set_analysis['underpowered_count']} underpowered")
        
        return set_analysis
    
    def generate_set_recommendations(self, analyses: List[CardAnalysis]) -> List[str]:
        """Generate recommendations for the entire card set."""
        recommendations = []
        
        overpowered = [a for a in analyses if a.meta_position == "overpowered"]
        underpowered = [a for a in analyses if a.meta_position == "underpowered"]
        
        if len(overpowered) > len(analyses) * 0.2:  # More than 20% overpowered
            recommendations.append("Too many overpowered cards - review power level standards")
        
        if len(underpowered) > len(analyses) * 0.3:  # More than 30% underpowered  
            recommendations.append("Many cards are underpowered - consider global power level increase")
        
        # Check for 0-cost card balance
        zero_cost_cards = [a for a in analyses if any(card.sand_cost == 0 for card in [c for c in analyses if c.card_id == a.card_id])]
        if len(zero_cost_cards) > 2 and any(a.balance_score > 1.5 for a in zero_cost_cards):
            recommendations.append("0-cost cards may be too powerful - review free action balance")
        
        return recommendations