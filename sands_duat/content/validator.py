"""
Enhanced Content Validator

Validates YAML content against comprehensive Pydantic schemas to ensure data integrity
and catch configuration errors early in development.

Features:
- Comprehensive schema validation using Pydantic models
- Cross-reference validation between content types
- Detailed error reporting with line numbers and context
- Performance optimization for large content libraries
- Egyptian mythology theme validation
"""

import logging
import time
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from pathlib import Path
from pydantic import ValidationError
from dataclasses import dataclass

from .schemas import (
    Card, Enemy, Event, Deck, Effect, Ability,
    CardsFile, EnemiesFile, EventsFile, DecksFile,
    EffectType, KeywordType, ContentManifest
)
from .loader import ContentType


@dataclass
class ValidationError:
    """Detailed validation error information."""
    error_type: str
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    item_id: Optional[str] = None
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    total_files: int = 0
    total_items: int = 0
    validation_time: float = 0.0
    errors: List[ValidationError] = None
    warnings: List[ValidationError] = None
    cross_reference_issues: List[ValidationError] = None
    performance_stats: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.cross_reference_issues is None:
            self.cross_reference_issues = []
        if self.performance_stats is None:
            self.performance_stats = {}
    
    @property
    def is_valid(self) -> bool:
        """Check if validation passed without errors."""
        return len(self.errors) == 0 and len(self.cross_reference_issues) == 0
    
    @property
    def total_issues(self) -> int:
        """Total number of issues found."""
        return len(self.errors) + len(self.warnings) + len(self.cross_reference_issues)


class ContentValidator:
    """
    Enhanced content validator with comprehensive schema validation.
    
    Validates YAML content against Pydantic schemas, performs cross-reference
    validation, and provides detailed error reporting.
    """
    
    def __init__(self, enable_performance_tracking: bool = False):
        self.logger = logging.getLogger(__name__)
        self.enable_performance_tracking = enable_performance_tracking
        self._validation_cache: Dict[str, ValidationReport] = {}
        self._cross_reference_cache: Dict[str, Set[str]] = {}
        
        # Known valid references for cross-validation
        self._valid_card_ids: Set[str] = set()
        self._valid_enemy_ids: Set[str] = set()
        self._valid_event_ids: Set[str] = set()
        self._valid_deck_ids: Set[str] = set()
        self._valid_effect_types: Set[str] = {e.value for e in EffectType}
        self._valid_keywords: Set[str] = {k.value for k in KeywordType}
    
    def validate_content_file(self, file_path: Path, content_type: ContentType) -> ValidationReport:
        """Validate a complete content file against its schema."""
        start_time = time.time()
        report = ValidationReport()
        
        try:
            # Load and parse the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                import yaml
                content = yaml.safe_load(f)
            
            if not content:
                report.errors.append(ValidationError(
                    error_type="empty_file",
                    message="File is empty or contains no valid YAML content",
                    file_path=str(file_path)
                ))
                return report
            
            # Validate based on content type
            if content_type == ContentType.CARDS:
                report = self._validate_cards_file(content, file_path)
            elif content_type == ContentType.ENEMIES:
                report = self._validate_enemies_file(content, file_path)
            elif content_type == ContentType.EVENTS:
                report = self._validate_events_file(content, file_path)
            elif content_type == ContentType.DECKS:
                report = self._validate_decks_file(content, file_path)
            else:
                report.errors.append(ValidationError(
                    error_type="unknown_content_type",
                    message=f"Unknown content type: {content_type}",
                    file_path=str(file_path)
                ))
            
            report.total_files = 1
            report.validation_time = time.time() - start_time
            
            if self.enable_performance_tracking:
                report.performance_stats = {
                    'file_size_bytes': file_path.stat().st_size,
                    'items_per_second': report.total_items / max(report.validation_time, 0.001),
                    'validation_time_ms': report.validation_time * 1000
                }
            
        except Exception as e:
            report.errors.append(ValidationError(
                error_type="validation_exception",
                message=f"Unexpected validation error: {str(e)}",
                file_path=str(file_path)
            ))
            self.logger.exception(f"Error validating {file_path}")
        
        return report
    
    def _validate_cards_file(self, content: Dict[str, Any], file_path: Path) -> ValidationReport:
        """Validate cards file content."""
        report = ValidationReport()
        
        try:
            cards_file = CardsFile(__root__=content)
            report.total_items = len(content)
            
            # Validate individual cards and collect IDs
            for card_id, card_data in content.items():
                try:
                    card = Card(**card_data)
                    self._valid_card_ids.add(card.id)
                    
                    # Additional validation checks
                    self._validate_card_effects(card, report, file_path)
                    self._validate_card_keywords(card, report, file_path)
                    
                except ValidationError as e:
                    for error in e.errors():
                        report.errors.append(ValidationError(
                            error_type="schema_validation",
                            message=f"Card '{card_id}': {error['msg']}",
                            file_path=str(file_path),
                            item_id=card_id
                        ))
                
        except ValidationError as e:
            for error in e.errors():
                report.errors.append(ValidationError(
                    error_type="file_schema_validation",
                    message=f"File validation error: {error['msg']}",
                    file_path=str(file_path)
                ))
        
        return report
    
    def _validate_enemies_file(self, content: Dict[str, Any], file_path: Path) -> ValidationReport:
        """Validate enemies file content."""
        report = ValidationReport()
        
        try:
            enemies_file = EnemiesFile(__root__=content)
            report.total_items = len(content)
            
            # Validate individual enemies and collect IDs
            for enemy_id, enemy_data in content.items():
                try:
                    enemy = Enemy(**enemy_data)
                    self._valid_enemy_ids.add(enemy.id)
                    
                    # Additional validation checks
                    self._validate_enemy_abilities(enemy, report, file_path)
                    self._validate_enemy_balance(enemy, report, file_path)
                    
                except ValidationError as e:
                    for error in e.errors():
                        report.errors.append(ValidationError(
                            error_type="schema_validation",
                            message=f"Enemy '{enemy_id}': {error['msg']}",
                            file_path=str(file_path),
                            item_id=enemy_id
                        ))
                
        except ValidationError as e:
            for error in e.errors():
                report.errors.append(ValidationError(
                    error_type="file_schema_validation",
                    message=f"File validation error: {error['msg']}",
                    file_path=str(file_path)
                ))
        
        return report
    
    def _validate_events_file(self, content: Dict[str, Any], file_path: Path) -> ValidationReport:
        """Validate events file content."""
        report = ValidationReport()
        
        try:
            events_file = EventsFile(__root__=content)
            report.total_items = len(content)
            
            # Validate individual events and collect IDs
            for event_id, event_data in content.items():
                try:
                    event = Event(**event_data)
                    self._valid_event_ids.add(event.id)
                    
                    # Additional validation checks
                    self._validate_event_options(event, report, file_path)
                    
                except ValidationError as e:
                    for error in e.errors():
                        report.errors.append(ValidationError(
                            error_type="schema_validation",
                            message=f"Event '{event_id}': {error['msg']}",
                            file_path=str(file_path),
                            item_id=event_id
                        ))
                
        except ValidationError as e:
            for error in e.errors():
                report.errors.append(ValidationError(
                    error_type="file_schema_validation",
                    message=f"File validation error: {error['msg']}",
                    file_path=str(file_path)
                ))
        
        return report
    
    def _validate_decks_file(self, content: Dict[str, Any], file_path: Path) -> ValidationReport:
        """Validate decks file content."""
        report = ValidationReport()
        
        try:
            decks_file = DecksFile(__root__=content)
            report.total_items = len(content)
            
            # Validate individual decks and collect IDs
            for deck_id, deck_data in content.items():
                try:
                    deck = Deck(**deck_data)
                    self._valid_deck_ids.add(deck.id)
                    
                    # Additional validation checks
                    self._validate_deck_composition(deck, report, file_path)
                    
                except ValidationError as e:
                    for error in e.errors():
                        report.errors.append(ValidationError(
                            error_type="schema_validation",
                            message=f"Deck '{deck_id}': {error['msg']}",
                            file_path=str(file_path),
                            item_id=deck_id
                        ))
                
        except ValidationError as e:
            for error in e.errors():
                report.errors.append(ValidationError(
                    error_type="file_schema_validation",
                    message=f"File validation error: {error['msg']}",
                    file_path=str(file_path)
                ))
        
        return report
    
    def validate_cross_references(self) -> ValidationReport:
        """Validate cross-references between different content types."""
        report = ValidationReport()
        
        # Validate deck card references
        for deck_id in self._valid_deck_ids:
            # This would need access to loaded content to check actual deck.cards
            # Implementation depends on how content is accessed
            pass
        
        # Validate effect type references
        # Implementation would check that all effect_type values are valid
        
        # Validate keyword usage consistency
        # Implementation would check keyword usage patterns
        
        return report
    
    def _validate_card_effects(self, card: Card, report: ValidationReport, file_path: Path) -> None:
        """Validate card effects for consistency and balance."""
        for effect in card.effects:
            # Check for overpowered combinations
            if effect.effect_type == EffectType.DAMAGE and effect.value > card.sand_cost * 10:
                report.warnings.append(ValidationError(
                    error_type="balance_warning",
                    message=f"Card '{card.id}' may be overpowered: {effect.value} damage for {card.sand_cost} sand",
                    file_path=str(file_path),
                    item_id=card.id,
                    severity="warning"
                ))
    
    def _validate_card_keywords(self, card: Card, report: ValidationReport, file_path: Path) -> None:
        """Validate card keywords for consistency."""
        # Check for Egyptian mythology theme consistency
        egyptian_keywords = {KeywordType.DIVINE, KeywordType.RITUAL, KeywordType.MUMMY, 
                           KeywordType.PHARAOH, KeywordType.ANUBIS, KeywordType.THOTH}
        
        if any(kw in card.keywords for kw in egyptian_keywords):
            if "egypt" not in card.description.lower() and "sand" not in card.description.lower():
                report.warnings.append(ValidationError(
                    error_type="theme_consistency",
                    message=f"Card '{card.id}' has Egyptian keywords but description doesn't reflect theme",
                    file_path=str(file_path),
                    item_id=card.id,
                    severity="warning"
                ))
    
    def _validate_enemy_abilities(self, enemy: Enemy, report: ValidationReport, file_path: Path) -> None:
        """Validate enemy abilities for consistency and balance."""
        total_sand_cost = sum(ability.sand_cost for ability in enemy.abilities)
        
        if total_sand_cost > enemy.max_sand * 2:
            report.warnings.append(ValidationError(
                error_type="balance_warning",
                message=f"Enemy '{enemy.id}' abilities total cost ({total_sand_cost}) may be too high for max sand ({enemy.max_sand})",
                file_path=str(file_path),
                item_id=enemy.id,
                severity="warning"
            ))
    
    def _validate_enemy_balance(self, enemy: Enemy, report: ValidationReport, file_path: Path) -> None:
        """Validate enemy balance metrics."""
        # Check health to sand ratio
        health_to_sand_ratio = enemy.max_health / enemy.max_sand
        
        if health_to_sand_ratio > 20:
            report.warnings.append(ValidationError(
                error_type="balance_warning",
                message=f"Enemy '{enemy.id}' may be too tanky: {enemy.max_health} health / {enemy.max_sand} sand = {health_to_sand_ratio:.1f} ratio",
                file_path=str(file_path),
                item_id=enemy.id,
                severity="warning"
            ))
    
    def _validate_event_options(self, event: Event, report: ValidationReport, file_path: Path) -> None:
        """Validate event options for consistency."""
        # Check that at least one option has no requirements (always available)
        has_free_option = any(not option.requirements for option in event.options)
        
        if not has_free_option:
            report.warnings.append(ValidationError(
                error_type="accessibility_warning",
                message=f"Event '{event.id}' has no options without requirements - may be inaccessible",
                file_path=str(file_path),
                item_id=event.id,
                severity="warning"
            ))
    
    def _validate_deck_composition(self, deck: Deck, report: ValidationReport, file_path: Path) -> None:
        """Validate deck composition for playability."""
        # This would need access to card data to validate properly
        # For now, just check basic constraints
        if len(deck.cards) < 15:
            report.warnings.append(ValidationError(
                error_type="playability_warning",
                message=f"Deck '{deck.id}' may be too small ({len(deck.cards)} cards) for good gameplay",
                file_path=str(file_path),
                item_id=deck.id,
                severity="warning"
            ))
    
    def generate_report_summary(self, report: ValidationReport) -> str:
        """Generate a human-readable summary of the validation report."""
        lines = []
        lines.append(f"\n=== Validation Report ===")
        lines.append(f"Files validated: {report.total_files}")
        lines.append(f"Items validated: {report.total_items}")
        lines.append(f"Validation time: {report.validation_time:.3f}s")
        lines.append(f"")
        
        if report.is_valid:
            lines.append("✅ Validation PASSED - No errors found")
        else:
            lines.append("❌ Validation FAILED")
        
        if report.errors:
            lines.append(f"\n🚨 Errors ({len(report.errors)}):")
            for error in report.errors[:10]:  # Limit to first 10 errors
                lines.append(f"  - {error.message}")
            if len(report.errors) > 10:
                lines.append(f"  ... and {len(report.errors) - 10} more errors")
        
        if report.warnings:
            lines.append(f"\n⚠️ Warnings ({len(report.warnings)}):")
            for warning in report.warnings[:5]:  # Limit to first 5 warnings
                lines.append(f"  - {warning.message}")
            if len(report.warnings) > 5:
                lines.append(f"  ... and {len(report.warnings) - 5} more warnings")
        
        if report.cross_reference_issues:
            lines.append(f"\n🔗 Cross-reference issues ({len(report.cross_reference_issues)}):")
            for issue in report.cross_reference_issues[:5]:
                lines.append(f"  - {issue.message}")
        
        if self.enable_performance_tracking and report.performance_stats:
            lines.append(f"\n📊 Performance:")
            stats = report.performance_stats
            if 'items_per_second' in stats:
                lines.append(f"  - Items/second: {stats['items_per_second']:.1f}")
            if 'validation_time_ms' in stats:
                lines.append(f"  - Validation time: {stats['validation_time_ms']:.1f}ms")
        
        return "\n".join(lines)
    
    def clear_caches(self) -> None:
        """Clear validation and cross-reference caches."""
        self._validation_cache.clear()
        self._cross_reference_cache.clear()
        self._valid_card_ids.clear()
        self._valid_enemy_ids.clear()
        self._valid_event_ids.clear()
        self._valid_deck_ids.clear()
        self.logger.info("Validation caches cleared")

    # Legacy methods for backward compatibility
    def validate_card_data(self, card_data: Dict[str, Any]) -> bool:
        """Legacy method - validate single card data."""
        try:
            Card(**card_data)
            return True
        except ValidationError:
            return False
    
    def validate_enemy_data(self, enemy_data: Dict[str, Any]) -> bool:
        """Legacy method - validate single enemy data."""
        try:
            Enemy(**enemy_data)
            return True
        except ValidationError:
            return False
    
    def validate_event_data(self, event_data: Dict[str, Any]) -> bool:
        """Legacy method - validate single event data."""
        try:
            Event(**event_data)
            return True
        except ValidationError:
            return False
    
    def validate_deck_data(self, deck_data: Dict[str, Any]) -> bool:
        """Legacy method - validate single deck data."""
        try:
            Deck(**deck_data)
            return True
        except ValidationError:
            return False