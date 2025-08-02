"""
Cross-Reference Validator

Validates relationships and dependencies between different content types
to ensure consistency and prevent broken references in the game.

Features:
- Card-to-effect validation
- Deck-to-card validation  
- Event-to-card/enemy validation
- Enemy ability validation
- Keyword consistency checking
- Performance optimized for large content libraries
"""

import logging
from typing import Dict, Set, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

from .schemas import (
    Card, Enemy, Event, Deck, Effect, Ability, 
    EffectType, KeywordType, HourOfNight
)
from .validator import ValidationError, ValidationReport


@dataclass
class CrossReferenceDatabase:
    """Database of all content references for validation."""
    # Content ID sets
    card_ids: Set[str] = field(default_factory=set)
    enemy_ids: Set[str] = field(default_factory=set)
    event_ids: Set[str] = field(default_factory=set)
    deck_ids: Set[str] = field(default_factory=set)
    
    # Content objects by ID
    cards: Dict[str, Card] = field(default_factory=dict)
    enemies: Dict[str, Enemy] = field(default_factory=dict)
    events: Dict[str, Event] = field(default_factory=dict)
    decks: Dict[str, Deck] = field(default_factory=dict)
    
    # Reference mappings
    card_keywords: Dict[str, Set[KeywordType]] = field(default_factory=dict)
    card_effects: Dict[str, List[EffectType]] = field(default_factory=dict)
    enemy_abilities: Dict[str, List[str]] = field(default_factory=dict)
    deck_cards: Dict[str, List[str]] = field(default_factory=dict)
    
    # Reverse lookups
    cards_by_keyword: Dict[KeywordType, Set[str]] = field(default_factory=lambda: defaultdict(set))
    cards_by_effect: Dict[EffectType, Set[str]] = field(default_factory=lambda: defaultdict(set))
    events_by_hour: Dict[HourOfNight, Set[str]] = field(default_factory=lambda: defaultdict(set))
    enemies_by_hour: Dict[HourOfNight, Set[str]] = field(default_factory=lambda: defaultdict(set))
    
    def add_card(self, card: Card) -> None:
        """Add a card to the database."""
        self.card_ids.add(card.id)
        self.cards[card.id] = card
        self.card_keywords[card.id] = set(card.keywords)
        self.card_effects[card.id] = [effect.effect_type for effect in card.effects]
        
        # Update reverse lookups
        for keyword in card.keywords:
            self.cards_by_keyword[keyword].add(card.id)
        for effect in card.effects:
            self.cards_by_effect[effect.effect_type].add(card.id)
    
    def add_enemy(self, enemy: Enemy) -> None:
        """Add an enemy to the database."""
        self.enemy_ids.add(enemy.id)
        self.enemies[enemy.id] = enemy
        self.enemy_abilities[enemy.id] = [ability.name for ability in enemy.abilities]
        
        # Update reverse lookups
        if enemy.hour_of_night:
            self.enemies_by_hour[enemy.hour_of_night].add(enemy.id)
    
    def add_event(self, event: Event) -> None:
        """Add an event to the database."""
        self.event_ids.add(event.id)
        self.events[event.id] = event
        
        # Update reverse lookups
        if event.hour_of_night:
            self.events_by_hour[event.hour_of_night].add(event.id)
    
    def add_deck(self, deck: Deck) -> None:
        """Add a deck to the database."""
        self.deck_ids.add(deck.id)
        self.decks[deck.id] = deck
        self.deck_cards[deck.id] = deck.cards.copy()


class CrossReferenceValidator:
    """
    Validates cross-references between different content types.
    
    Ensures that all references between cards, enemies, events, and decks
    are valid and that the content forms a consistent game world.
    """
    
    def __init__(self, enable_performance_tracking: bool = False):
        self.logger = logging.getLogger(__name__)
        self.enable_performance_tracking = enable_performance_tracking
        self.database = CrossReferenceDatabase()
        
        # Known valid pools for card discovery/gain effects
        self.valid_card_pools = {
            "divine_cards", "knowledge_cards", "spirit_cards", "forbidden_knowledge",
            "memory_cards", "decay_cards", "truth_cards", "isis_magic", "guide_cards",
            "combat_techniques", "any"
        }
        
        # Known valid blessing/curse types
        self.valid_blessing_types = {
            "safe_passage", "divine_favor", "protection", "soul_peace", "purification",
            "wisdom", "freedom", "order", "divine_protection", "tactical_insight",
            "death_mastery", "divine_judgment", "pure_heart", "perfect_soul", 
            "acceptance", "truth", "purity", "maternal_protection", "transcendence",
            "divine_ascension", "enlightenment", "eternal_life"
        }
        
        self.valid_curse_types = {
            "mirage_sickness", "forbidden_knowledge", "decay_touch"
        }
        
        # Known valid debuff/buff types
        self.valid_buff_types = {
            "strength", "dexterity", "regeneration", "intangible", "thorns"
        }
        
        self.valid_debuff_types = {
            "poison", "weak", "vulnerable", "curse"
        }
    
    def populate_database(self, cards: Dict[str, Any], enemies: Dict[str, Any], 
                         events: Dict[str, Any], decks: Dict[str, Any]) -> None:
        """Populate the reference database with all content."""
        self.database = CrossReferenceDatabase()  # Reset
        
        # Add cards
        for card_id, card_data in cards.items():
            try:
                card = Card(**card_data)
                self.database.add_card(card)
            except Exception as e:
                self.logger.warning(f"Failed to parse card {card_id}: {e}")
        
        # Add enemies
        for enemy_id, enemy_data in enemies.items():
            try:
                enemy = Enemy(**enemy_data)
                self.database.add_enemy(enemy)
            except Exception as e:
                self.logger.warning(f"Failed to parse enemy {enemy_id}: {e}")
        
        # Add events
        for event_id, event_data in events.items():
            try:
                event = Event(**event_data)
                self.database.add_event(event)
            except Exception as e:
                self.logger.warning(f"Failed to parse event {event_id}: {e}")
        
        # Add decks
        for deck_id, deck_data in decks.items():
            try:
                deck = Deck(**deck_data)
                self.database.add_deck(deck)
            except Exception as e:
                self.logger.warning(f"Failed to parse deck {deck_id}: {e}")
    
    def validate_all_cross_references(self) -> ValidationReport:
        """Validate all cross-references in the database."""
        report = ValidationReport()
        
        # Validate deck card references
        deck_errors = self._validate_deck_references()
        report.cross_reference_issues.extend(deck_errors)
        
        # Validate event card/enemy references
        event_errors = self._validate_event_references()
        report.cross_reference_issues.extend(event_errors)
        
        # Validate effect metadata references
        effect_errors = self._validate_effect_references()
        report.cross_reference_issues.extend(effect_errors)
        
        # Validate keyword consistency
        keyword_errors = self._validate_keyword_consistency()
        report.cross_reference_issues.extend(keyword_errors)
        
        # Validate hour of night distribution
        hour_errors = self._validate_hour_distribution()
        report.cross_reference_issues.extend(hour_errors)
        
        # Validate balance and progression
        balance_errors = self._validate_balance_progression()
        report.cross_reference_issues.extend(balance_errors)
        
        return report
    
    def _validate_deck_references(self) -> List[ValidationError]:
        """Validate that all deck card references are valid."""
        errors = []
        
        for deck_id, deck in self.database.decks.items():
            for card_id in deck.cards:
                if card_id not in self.database.card_ids:
                    errors.append(ValidationError(
                        error_type="invalid_card_reference",
                        message=f"Deck '{deck_id}' references non-existent card '{card_id}'",
                        item_id=deck_id
                    ))
            
            # Validate deck composition balance
            card_costs = []
            for card_id in deck.cards:
                if card_id in self.database.cards:
                    card_costs.append(self.database.cards[card_id].sand_cost)
            
            if card_costs:
                avg_cost = sum(card_costs) / len(card_costs)
                if avg_cost > 3.5:
                    errors.append(ValidationError(
                        error_type="deck_balance_warning",
                        message=f"Deck '{deck_id}' has high average sand cost ({avg_cost:.1f}) - may be difficult to play",
                        item_id=deck_id,
                        severity="warning"
                    ))
                elif avg_cost < 1.5:
                    errors.append(ValidationError(
                        error_type="deck_balance_warning",
                        message=f"Deck '{deck_id}' has low average sand cost ({avg_cost:.1f}) - may lack powerful options",
                        item_id=deck_id,
                        severity="warning"
                    ))
        
        return errors
    
    def _validate_event_references(self) -> List[ValidationError]:
        """Validate event references to cards, enemies, and other content."""
        errors = []
        
        for event_id, event in self.database.events.items():
            for option in event.options:
                for effect in option.effects:
                    # Check card references in effects
                    if hasattr(effect, 'metadata') and effect.metadata:
                        card_id = effect.metadata.get('card_id')
                        if card_id and card_id not in self.database.card_ids:
                            errors.append(ValidationError(
                                error_type="invalid_card_reference",
                                message=f"Event '{event_id}' references non-existent card '{card_id}'",
                                item_id=event_id
                            ))
                        
                        # Check enemy references
                        enemy_id = effect.metadata.get('enemy_id')
                        if enemy_id and enemy_id not in self.database.enemy_ids:
                            errors.append(ValidationError(
                                error_type="invalid_enemy_reference",
                                message=f"Event '{event_id}' references non-existent enemy '{enemy_id}'",
                                item_id=event_id
                            ))
                        
                        # Check card pool references
                        pool = effect.metadata.get('pool')
                        if pool and pool not in self.valid_card_pools:
                            errors.append(ValidationError(
                                error_type="invalid_pool_reference",
                                message=f"Event '{event_id}' references unknown card pool '{pool}'",
                                item_id=event_id,
                                severity="warning"
                            ))
                
                # Check requirements
                if option.requirements:
                    for req in option.requirements:
                        req_type = req.get('type')
                        if req_type == 'card_in_deck':
                            card_id = req.get('card_id')
                            if card_id and card_id not in self.database.card_ids:
                                errors.append(ValidationError(
                                    error_type="invalid_card_reference",
                                    message=f"Event '{event_id}' requirement references non-existent card '{card_id}'",
                                    item_id=event_id
                                ))
                        elif req_type == 'card_with_keyword':
                            keyword = req.get('keyword')
                            if keyword and keyword not in [k.value for k in KeywordType]:
                                errors.append(ValidationError(
                                    error_type="invalid_keyword_reference",
                                    message=f"Event '{event_id}' requirement references unknown keyword '{keyword}'",
                                    item_id=event_id
                                ))
        
        return errors
    
    def _validate_effect_references(self) -> List[ValidationError]:
        """Validate effect metadata references."""
        errors = []
        
        # Check all card effects
        for card_id, card in self.database.cards.items():
            for effect in card.effects:
                errors.extend(self._validate_single_effect(effect, card_id, "card"))
        
        # Check all enemy ability effects
        for enemy_id, enemy in self.database.enemies.items():
            for ability in enemy.abilities:
                for effect in ability.effects:
                    errors.extend(self._validate_single_effect(effect, enemy_id, "enemy"))
        
        return errors
    
    def _validate_single_effect(self, effect: Effect, item_id: str, item_type: str) -> List[ValidationError]:
        """Validate a single effect's metadata references."""
        errors = []
        
        if not effect.metadata:
            return errors
        
        # Validate blessing types
        if effect.effect_type in [EffectType.BLESSING] and 'blessing_type' in effect.metadata:
            blessing_type = effect.metadata['blessing_type']
            if blessing_type not in self.valid_blessing_types:
                errors.append(ValidationError(
                    error_type="invalid_blessing_type",
                    message=f"{item_type.title()} '{item_id}' uses unknown blessing type '{blessing_type}'",
                    item_id=item_id,
                    severity="warning"
                ))
        
        # Validate curse types
        if effect.effect_type in [EffectType.CURSE] and 'curse_type' in effect.metadata:
            curse_type = effect.metadata['curse_type']
            if curse_type not in self.valid_curse_types:
                errors.append(ValidationError(
                    error_type="invalid_curse_type",
                    message=f"{item_type.title()} '{item_id}' uses unknown curse type '{curse_type}'",
                    item_id=item_id,
                    severity="warning"
                ))
        
        # Validate buff types
        if effect.effect_type in [EffectType.BUFF] and 'buff_type' in effect.metadata:
            buff_type = effect.metadata['buff_type']
            if buff_type not in self.valid_buff_types:
                errors.append(ValidationError(
                    error_type="invalid_buff_type",
                    message=f"{item_type.title()} '{item_id}' uses unknown buff type '{buff_type}'",
                    item_id=item_id,
                    severity="warning"
                ))
        
        # Validate debuff types
        if effect.effect_type in [EffectType.DEBUFF] and 'debuff_type' in effect.metadata:
            debuff_type = effect.metadata['debuff_type']
            if debuff_type not in self.valid_debuff_types:
                errors.append(ValidationError(
                    error_type="invalid_debuff_type",
                    message=f"{item_type.title()} '{item_id}' uses unknown debuff type '{debuff_type}'",
                    item_id=item_id,
                    severity="warning"
                ))
        
        return errors
    
    def _validate_keyword_consistency(self) -> List[ValidationError]:
        """Validate keyword usage consistency across content."""
        errors = []
        
        # Check for Egyptian mythology theme consistency
        egyptian_gods = {KeywordType.ANUBIS, KeywordType.THOTH, KeywordType.ISIS, 
                        KeywordType.OSIRIS, KeywordType.HORUS, KeywordType.SET,
                        KeywordType.BASTET, KeywordType.SEKHMET}
        
        for card_id, keywords in self.database.card_keywords.items():
            god_keywords = keywords.intersection(egyptian_gods)
            if len(god_keywords) > 1:
                errors.append(ValidationError(
                    error_type="keyword_consistency_warning",
                    message=f"Card '{card_id}' has multiple god keywords: {[k.value for k in god_keywords]}",
                    item_id=card_id,
                    severity="warning"
                ))
        
        # Check for conflicting mechanical keywords
        conflicting_pairs = [
            (KeywordType.EXHAUST, KeywordType.RETAIN),
            (KeywordType.ETHEREAL, KeywordType.INNATE)
        ]
        
        for card_id, keywords in self.database.card_keywords.items():
            for keyword1, keyword2 in conflicting_pairs:
                if keyword1 in keywords and keyword2 in keywords:
                    errors.append(ValidationError(
                        error_type="conflicting_keywords",
                        message=f"Card '{card_id}' has conflicting keywords: {keyword1.value} and {keyword2.value}",
                        item_id=card_id
                    ))
        
        return errors
    
    def _validate_hour_distribution(self) -> List[ValidationError]:
        """Validate distribution of content across the 12 hours of night."""
        errors = []
        
        # Check that each hour has content
        all_hours = set(HourOfNight)
        hours_with_events = set(self.database.events_by_hour.keys())
        hours_with_enemies = set(self.database.enemies_by_hour.keys())
        
        hours_without_events = all_hours - hours_with_events
        hours_without_enemies = all_hours - hours_with_enemies
        
        if hours_without_events:
            errors.append(ValidationError(
                error_type="missing_hour_content",
                message=f"Hours without events: {[h.value for h in hours_without_events]}",
                severity="warning"
            ))
        
        if hours_without_enemies:
            errors.append(ValidationError(
                error_type="missing_hour_content",
                message=f"Hours without enemies: {[h.value for h in hours_without_enemies]}",
                severity="warning"
            ))
        
        # Check for hour progression balance
        for hour in HourOfNight:
            enemy_count = len(self.database.enemies_by_hour.get(hour, set()))
            event_count = len(self.database.events_by_hour.get(hour, set()))
            
            if enemy_count == 0 and event_count == 0:
                errors.append(ValidationError(
                    error_type="empty_hour",
                    message=f"Hour '{hour.value}' has no content (enemies or events)",
                    severity="warning"
                ))
        
        return errors
    
    def _validate_balance_progression(self) -> List[ValidationError]:
        """Validate game balance and progression curves."""
        errors = []
        
        # Analyze sand cost distribution
        sand_costs = [card.sand_cost for card in self.database.cards.values()]
        if sand_costs:
            cost_distribution = {i: sand_costs.count(i) for i in range(7)}
            
            # Check for gaps in sand cost curve
            for cost in range(7):
                if cost_distribution[cost] == 0:
                    errors.append(ValidationError(
                        error_type="sand_cost_gap",
                        message=f"No cards with sand cost {cost} - may create gaps in gameplay progression",
                        severity="warning"
                    ))
        
        # Analyze enemy health/sand ratios by hour
        hour_order = list(HourOfNight)
        prev_avg_difficulty = 0
        
        for i, hour in enumerate(hour_order):
            enemies_in_hour = [
                self.database.enemies[enemy_id] 
                for enemy_id in self.database.enemies_by_hour.get(hour, set())
            ]
            
            if enemies_in_hour:
                avg_health = sum(e.max_health for e in enemies_in_hour) / len(enemies_in_hour)
                avg_sand = sum(e.max_sand for e in enemies_in_hour) / len(enemies_in_hour)
                difficulty_rating = avg_health + (avg_sand * 10)  # Simple difficulty metric
                
                # Check for progression consistency
                if i > 0 and difficulty_rating < prev_avg_difficulty * 0.8:
                    errors.append(ValidationError(
                        error_type="difficulty_regression",
                        message=f"Hour '{hour.value}' enemies may be easier than previous hour - difficulty regression",
                        severity="warning"
                    ))
                
                prev_avg_difficulty = difficulty_rating
        
        return errors
    
    def get_reference_statistics(self) -> Dict[str, Any]:
        """Get statistics about content references and relationships."""
        stats = {
            'total_cards': len(self.database.card_ids),
            'total_enemies': len(self.database.enemy_ids),
            'total_events': len(self.database.event_ids),
            'total_decks': len(self.database.deck_ids),
            'cards_by_cost': {},
            'enemies_by_hour': {},
            'events_by_hour': {},
            'keyword_usage': {},
            'effect_usage': {}
        }
        
        # Cards by sand cost
        for card in self.database.cards.values():
            cost = card.sand_cost
            stats['cards_by_cost'][cost] = stats['cards_by_cost'].get(cost, 0) + 1
        
        # Content by hour
        for hour in HourOfNight:
            stats['enemies_by_hour'][hour.value] = len(self.database.enemies_by_hour.get(hour, set()))
            stats['events_by_hour'][hour.value] = len(self.database.events_by_hour.get(hour, set()))
        
        # Keyword usage
        for keyword in KeywordType:
            stats['keyword_usage'][keyword.value] = len(self.database.cards_by_keyword.get(keyword, set()))
        
        # Effect usage
        for effect_type in EffectType:
            stats['effect_usage'][effect_type.value] = len(self.database.cards_by_effect.get(effect_type, set()))
        
        return stats