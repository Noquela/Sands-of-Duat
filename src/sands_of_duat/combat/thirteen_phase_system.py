#!/usr/bin/env python3
"""
13-PHASE COMBAT SYSTEM
======================

Egyptian underworld journey combat system based on the 12-hour night journey
of Ra through the Duat (underworld), plus a preparation phase.

Each phase represents a crucial stage in the cosmic battle between order and chaos.
"""

import logging
import random
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class CombatPhase(Enum):
    """13 phases of Egyptian underworld combat."""
    # Phase 0: Preparation
    DAWN_PREPARATION = ("dawn_preparation", "Prepare for the journey into darkness", 0)
    
    # Phases 1-12: The 12 Hours of Night Journey
    DIVINE_INVOCATION = ("divine_invocation", "Call upon the gods for protection", 1)
    BA_SEPARATION = ("ba_separation", "Soul prepares to leave the body", 2) 
    TARGETING = ("targeting", "Choose your path through the underworld", 3)
    COMBAT_ACTION = ("combat_action", "Battle the forces of chaos", 4)
    DAMAGE_RESOLUTION = ("damage_resolution", "Wounds of battle manifest", 5)
    DIVINE_JUDGMENT = ("divine_judgment", "Ma'at weighs hearts against truth", 6)
    SPELL_WEAVING = ("spell_weaving", "Heka magic flows through combat", 7)
    STATUS_EFFECTS = ("status_effects", "Curses and blessings take hold", 8)
    UNDERWORLD_PASSAGE = ("underworld_passage", "Journey deeper into the Duat", 9)
    KA_MANIFESTATION = ("ka_manifestation", "Life force reveals its power", 10)
    AFTERLIFE_TRANSITION = ("afterlife_transition", "Death and rebirth unfold", 11)
    COSMIC_BALANCE = ("cosmic_balance", "Ma'at restores universal order", 12)
    DUSK_CLEANUP = ("dusk_cleanup", "Return to the world of the living", 13)
    
    def __init__(self, key: str, description: str, hour: int):
        self.key = key
        self.description = description
        self.hour = hour  # Underworld hour (0-13)

@dataclass
class PhaseContext:
    """Context for a combat phase execution."""
    phase: CombatPhase
    turn_number: int
    active_entities: List[str]
    phase_modifiers: Dict[str, float] = field(default_factory=dict)
    underworld_effects: List[str] = field(default_factory=list)
    divine_interventions: List[str] = field(default_factory=list)
    cosmic_balance: float = 0.0  # Ma'at balance for this phase

@dataclass
class UnderWorldLocation:
    """A location in the Egyptian underworld."""
    name: str
    hour: int
    description: str
    special_rules: List[str] = field(default_factory=list)
    environmental_effects: Dict[str, float] = field(default_factory=dict)
    guardian_entities: List[str] = field(default_factory=list)
    passage_requirements: List[str] = field(default_factory=list)

class ThirteenPhaseManager:
    """
    Manages the 13-phase Egyptian combat system.
    
    Each combat follows Ra's journey through the underworld:
    - Preparation phase sets the stage
    - 12 underworld hours represent core combat mechanics
    - Each phase has unique rules and Egyptian mythological significance
    """
    
    def __init__(self):
        self.current_phase = CombatPhase.DAWN_PREPARATION
        self.phase_history: List[CombatPhase] = []
        self.phase_handlers: Dict[CombatPhase, Callable] = {}
        self.underworld_locations = self._initialize_underworld()
        self.cosmic_cycle_count = 0
        self.phase_context = None
        
        # Register phase handlers
        self._register_phase_handlers()
    
    def _initialize_underworld(self) -> Dict[int, UnderWorldLocation]:
        """Initialize the 12 underworld locations based on Egyptian mythology."""
        locations = {
            0: UnderWorldLocation(
                "Hall of Preparation", 0,
                "The threshold between life and death",
                ["setup_phase", "divine_protection"],
                {"preparation_bonus": 1.2},
                [],
                []
            ),
            1: UnderWorldLocation(
                "First Hour - Entrance Gate", 1,
                "Descent into the underworld begins",
                ["divine_invocation", "protection_spells"],
                {"magic_amplification": 1.1},
                ["Guardian of the Gate"],
                ["divine_blessing"]
            ),
            2: UnderWorldLocation(
                "Second Hour - Ba Separation", 2, 
                "Souls begin to separate from bodies",
                ["ba_ka_mechanics", "soul_vulnerability"],
                {"soul_magic_power": 1.3, "physical_resilience": 0.8},
                [],
                []
            ),
            3: UnderWorldLocation(
                "Third Hour - Waters of Nun", 3,
                "Primordial waters where paths diverge", 
                ["targeting_complexity", "choice_consequences"],
                {"flow_disruption": 0.9, "targeting_precision": 1.2},
                ["Serpents of Nun"],
                []
            ),
            4: UnderWorldLocation(
                "Fourth Hour - Combat Trials", 4,
                "The great battle against Apophis begins",
                ["combat_intensity", "chaos_attacks"],
                {"damage_amplification": 1.4, "chaos_resistance": 0.7},
                ["Apophis Spawn", "Chaos Warriors"],
                ["combat_prowess"]
            ),
            5: UnderWorldLocation(
                "Fifth Hour - Wounds and Healing", 5,
                "Consequences of battle manifest",
                ["damage_resolution", "healing_magic"],
                {"healing_power": 1.5, "damage_persistence": 1.2},
                ["Healers of Thoth"],
                []
            ),
            6: UnderWorldLocation(
                "Sixth Hour - Hall of Ma'at", 6,
                "Hearts are weighed against the feather",
                ["divine_judgment", "moral_consequences"],
                {"judgment_accuracy": 2.0, "divine_favor": 1.3},
                ["Ma'at", "42 Assessor Gods"],
                ["pure_heart", "righteous_actions"]
            ),
            7: UnderWorldLocation(
                "Seventh Hour - Heka's Domain", 7,
                "Raw magic flows through the underworld",
                ["spell_weaving", "magical_mastery"],
                {"spell_power": 1.6, "mana_efficiency": 1.3},
                ["Heka Guardians"],
                ["magical_knowledge"]
            ),
            8: UnderWorldLocation(
                "Eighth Hour - Curse Chamber", 8,
                "Curses and blessings reach full power",
                ["status_effects", "temporal_magic"],
                {"curse_potency": 1.5, "blessing_duration": 1.4},
                ["Curse Weavers"],
                []
            ),
            9: UnderWorldLocation(
                "Ninth Hour - Deep Passage", 9,
                "Journey into the heart of darkness",
                ["underworld_navigation", "environmental_hazards"],
                {"movement_difficulty": 1.3, "hidden_passages": 1.2},
                ["Underworld Guides"],
                ["navigation_skill"]
            ),
            10: UnderWorldLocation(
                "Tenth Hour - Ka Manifestation", 10,
                "Life force reveals its true nature",
                ["ka_powers", "life_force_mastery"],
                {"ka_amplification": 1.7, "life_force_flow": 1.4},
                [],
                ["strong_ka"]
            ),
            11: UnderWorldLocation(
                "Eleventh Hour - Death's Threshold", 11,
                "The boundary between death and rebirth",
                ["death_mechanics", "resurrection_magic"],
                {"death_resistance": 0.6, "resurrection_power": 2.0},
                ["Death Guardians", "Osiris Aspects"],
                ["death_acceptance"]
            ),
            12: UnderWorldLocation(
                "Twelfth Hour - Cosmic Balance", 12,
                "Universal order is restored or shattered",
                ["cosmic_effects", "balance_restoration"],
                {"cosmic_power": 2.0, "balance_sensitivity": 1.8},
                ["Cosmic Guardians"],
                ["cosmic_understanding"]
            ),
            13: UnderWorldLocation(
                "Dawn Return", 13,
                "Return to the world of the living",
                ["cleanup_phase", "cycle_completion"],
                {"renewal_power": 1.5},
                [],
                []
            )
        }
        return locations
    
    def _register_phase_handlers(self):
        """Register handlers for each combat phase."""
        self.phase_handlers = {
            CombatPhase.DAWN_PREPARATION: self._handle_dawn_preparation,
            CombatPhase.DIVINE_INVOCATION: self._handle_divine_invocation,
            CombatPhase.BA_SEPARATION: self._handle_ba_separation,
            CombatPhase.TARGETING: self._handle_targeting,
            CombatPhase.COMBAT_ACTION: self._handle_combat_action,
            CombatPhase.DAMAGE_RESOLUTION: self._handle_damage_resolution,
            CombatPhase.DIVINE_JUDGMENT: self._handle_divine_judgment,
            CombatPhase.SPELL_WEAVING: self._handle_spell_weaving,
            CombatPhase.STATUS_EFFECTS: self._handle_status_effects,
            CombatPhase.UNDERWORLD_PASSAGE: self._handle_underworld_passage,
            CombatPhase.KA_MANIFESTATION: self._handle_ka_manifestation,
            CombatPhase.AFTERLIFE_TRANSITION: self._handle_afterlife_transition,
            CombatPhase.COSMIC_BALANCE: self._handle_cosmic_balance,
            CombatPhase.DUSK_CLEANUP: self._handle_dusk_cleanup
        }
    
    def execute_phase(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the current combat phase."""
        # Create phase context
        self.phase_context = PhaseContext(
            phase=self.current_phase,
            turn_number=combat_state.get('turn_number', 0),
            active_entities=[eid for eid, entity in entities.items() if entity.is_alive]
        )
        
        # Get underworld location effects
        location = self.underworld_locations[self.current_phase.hour]
        self.phase_context.phase_modifiers.update(location.environmental_effects)
        
        logger.info(f"Executing Phase {self.current_phase.hour}: {self.current_phase.description}")
        logger.info(f"Location: {location.name} - {location.description}")
        
        # Execute phase-specific logic
        if self.current_phase in self.phase_handlers:
            phase_results = self.phase_handlers[self.current_phase](entities, combat_state)
        else:
            phase_results = self._handle_default_phase(entities, combat_state)
        
        # Record phase in history
        self.phase_history.append(self.current_phase)
        
        return phase_results
    
    def advance_phase(self) -> CombatPhase:
        """Advance to the next combat phase."""
        phases = list(CombatPhase)
        current_index = phases.index(self.current_phase)
        
        if current_index < len(phases) - 1:
            self.current_phase = phases[current_index + 1]
        else:
            # Complete cosmic cycle, return to beginning
            self.current_phase = CombatPhase.DAWN_PREPARATION
            self.cosmic_cycle_count += 1
            logger.info(f"Cosmic cycle {self.cosmic_cycle_count} complete - returning to preparation")
        
        logger.info(f"Phase advanced to: {self.current_phase.description}")
        return self.current_phase
    
    # Phase Handler Methods
    def _handle_dawn_preparation(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 0: Prepare for underworld journey."""
        results = {"phase": "dawn_preparation", "effects": []}
        
        # Grant preparation bonuses
        for entity_id, entity in entities.items():
            if entity.is_alive:
                # Divine protection preparation
                if hasattr(entity, 'divine_protection') and entity.divine_protection:
                    entity.preparation_bonus = 1.2
                    results["effects"].append(f"{entity_id} receives divine protection")
                
                # Set initial Ba-Ka state
                if hasattr(entity, 'ba_ka_state'):
                    entity.ba_ka_state.prepare_for_underworld()
                    results["effects"].append(f"{entity_id}'s soul prepares for the journey")
        
        return results
    
    def _handle_divine_invocation(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 1: Call upon gods for protection and power."""
        results = {"phase": "divine_invocation", "effects": []}
        
        for entity_id, entity in entities.items():
            if entity.is_alive and hasattr(entity, 'card'):
                # Check for divine allegiance
                if hasattr(entity.card, 'divine_allegiance'):
                    god = entity.card.divine_allegiance
                    # Apply god-specific bonuses
                    if god == "Ra":
                        entity.temp_modifiers["light_power"] = 1.3
                        results["effects"].append(f"{entity_id} calls upon Ra - light magic empowered")
                    elif god == "Anubis": 
                        entity.temp_modifiers["death_resistance"] = 1.4
                        results["effects"].append(f"{entity_id} calls upon Anubis - death magic enhanced")
                    elif god == "Isis":
                        entity.temp_modifiers["healing_power"] = 1.5
                        results["effects"].append(f"{entity_id} calls upon Isis - healing magic strengthened")
                    elif god == "Thoth":
                        entity.temp_modifiers["spell_power"] = 1.3
                        results["effects"].append(f"{entity_id} calls upon Thoth - all spells enhanced")
        
        return results
    
    def _handle_ba_separation(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Soul separation mechanics."""
        results = {"phase": "ba_separation", "effects": []}
        
        for entity_id, entity in entities.items():
            if entity.is_alive and hasattr(entity, 'ba_ka_state'):
                # Attempt Ba separation
                separation_chance = 0.3  # Base 30% chance
                
                # Modify based on spiritual power
                if hasattr(entity.card, 'stats') and hasattr(entity.card.stats, 'divine_favor'):
                    separation_chance += entity.card.stats.divine_favor * 0.02
                
                if random.random() < separation_chance:
                    entity.ba_ka_state.separate_ba()
                    entity.temp_modifiers["soul_vulnerability"] = 1.5  # More vulnerable
                    entity.temp_modifiers["spiritual_power"] = 2.0    # But more powerful
                    results["effects"].append(f"{entity_id}'s Ba separates - vulnerable but empowered")
                else:
                    results["effects"].append(f"{entity_id}'s soul remains unified")
        
        return results
    
    def _handle_targeting(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Enhanced targeting in the waters of Nun."""
        results = {"phase": "targeting", "effects": []}
        
        # Apply targeting modifiers from underworld location
        targeting_precision = self.phase_context.phase_modifiers.get("targeting_precision", 1.0)
        
        if targeting_precision > 1.0:
            results["effects"].append("The waters of Nun enhance targeting precision")
        
        # Store targeting bonuses for use in combat action phase
        combat_state["targeting_precision"] = targeting_precision
        
        return results
    
    def _handle_combat_action(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 4: Main combat against chaos forces."""
        results = {"phase": "combat_action", "effects": []}
        
        # Apply combat intensity from Apophis battle
        damage_amp = self.phase_context.phase_modifiers.get("damage_amplification", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive:
                # Chaos resistance check
                chaos_resistance = entity.temp_modifiers.get("chaos_resistance", 1.0)
                final_damage_mod = damage_amp / chaos_resistance
                
                entity.temp_modifiers["combat_damage_multiplier"] = final_damage_mod
                
                if final_damage_mod > 1.2:
                    results["effects"].append(f"{entity_id} faces intensified chaos forces")
                elif final_damage_mod < 0.9:
                    results["effects"].append(f"{entity_id} resists the chaos effectively")
        
        return results
    
    def _handle_damage_resolution(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 5: Wounds manifest and healing occurs."""
        results = {"phase": "damage_resolution", "effects": []}
        
        healing_power = self.phase_context.phase_modifiers.get("healing_power", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive:
                # Apply any healing effects with modifier
                if hasattr(entity, 'pending_healing') and entity.pending_healing > 0:
                    actual_healing = int(entity.pending_healing * healing_power)
                    entity.current_health = min(entity.max_health, entity.current_health + actual_healing)
                    entity.pending_healing = 0
                    results["effects"].append(f"{entity_id} heals for {actual_healing} (Thoth's blessing)")
                
                # Apply damage persistence
                damage_persistence = self.phase_context.phase_modifiers.get("damage_persistence", 1.0)
                if damage_persistence > 1.0 and hasattr(entity, 'damage_over_time'):
                    entity.damage_over_time = int(entity.damage_over_time * damage_persistence)
        
        return results
    
    def _handle_divine_judgment(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 6: Ma'at weighs hearts and judges actions."""
        results = {"phase": "divine_judgment", "effects": []}
        
        judgment_accuracy = self.phase_context.phase_modifiers.get("judgment_accuracy", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive and hasattr(entity, 'moral_actions'):
                # Calculate moral balance
                good_actions = sum(1 for action in entity.moral_actions if action > 0)
                evil_actions = sum(1 for action in entity.moral_actions if action < 0)
                
                moral_balance = (good_actions - evil_actions) * judgment_accuracy
                
                if moral_balance > 2:
                    # Righteous judgment - divine blessing
                    entity.temp_modifiers["divine_blessing"] = 1.3
                    results["effects"].append(f"{entity_id} judged righteous - receives Ma'at's blessing")
                    self.phase_context.cosmic_balance += 1
                elif moral_balance < -2:
                    # Wicked judgment - divine curse
                    entity.temp_modifiers["divine_curse"] = 0.7
                    results["effects"].append(f"{entity_id} judged wicked - suffers Ma'at's curse")
                    self.phase_context.cosmic_balance -= 1
                else:
                    results["effects"].append(f"{entity_id} judged as balanced")
        
        return results
    
    def _handle_spell_weaving(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 7: Heka magic flows through combat."""
        results = {"phase": "spell_weaving", "effects": []}
        
        spell_power = self.phase_context.phase_modifiers.get("spell_power", 1.0)
        mana_efficiency = self.phase_context.phase_modifiers.get("mana_efficiency", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive:
                # Apply Heka's magic enhancement
                entity.temp_modifiers["spell_power"] = entity.temp_modifiers.get("spell_power", 1.0) * spell_power
                entity.temp_modifiers["mana_efficiency"] = mana_efficiency
                
                if spell_power > 1.3:
                    results["effects"].append(f"{entity_id} channels Heka's raw magical power")
        
        return results
    
    def _handle_status_effects(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 8: Curses and blessings reach peak power."""
        results = {"phase": "status_effects", "effects": []}
        
        curse_potency = self.phase_context.phase_modifiers.get("curse_potency", 1.0)
        blessing_duration = self.phase_context.phase_modifiers.get("blessing_duration", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive and hasattr(entity, 'status_effects'):
                for effect_name, effect_data in entity.status_effects.items():
                    if 'curse' in effect_name.lower():
                        # Amplify curse effects
                        effect_data['potency'] *= curse_potency
                        if curse_potency > 1.3:
                            results["effects"].append(f"{entity_id}'s {effect_name} intensifies")
                    elif 'blessing' in effect_name.lower() or 'buff' in effect_name.lower():
                        # Extend blessing duration
                        effect_data['duration'] = int(effect_data['duration'] * blessing_duration)
                        if blessing_duration > 1.3:
                            results["effects"].append(f"{entity_id}'s {effect_name} duration extended")
        
        return results
    
    def _handle_underworld_passage(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 9: Navigate deeper into the underworld."""
        results = {"phase": "underworld_passage", "effects": []}
        
        # Environmental navigation challenges
        movement_difficulty = self.phase_context.phase_modifiers.get("movement_difficulty", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive:
                # Navigation skill check
                navigation_skill = getattr(entity, 'navigation_skill', 0.5)
                
                if navigation_skill * random.random() > movement_difficulty * 0.7:
                    # Successful navigation
                    entity.temp_modifiers["underworld_mastery"] = 1.2
                    results["effects"].append(f"{entity_id} navigates the underworld successfully")
                else:
                    # Lost in the darkness
                    entity.temp_modifiers["lost_penalty"] = 0.8
                    results["effects"].append(f"{entity_id} becomes lost in the underworld")
        
        return results
    
    def _handle_ka_manifestation(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 10: Life force reveals its power."""
        results = {"phase": "ka_manifestation", "effects": []}
        
        ka_amplification = self.phase_context.phase_modifiers.get("ka_amplification", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive and hasattr(entity, 'ba_ka_state'):
                # Manifest Ka power
                entity.ba_ka_state.manifest_ka()
                
                # Apply Ka amplification
                ka_power = entity.ba_ka_state.get_ka_power() * ka_amplification
                entity.temp_modifiers["life_force_power"] = ka_power
                
                results["effects"].append(f"{entity_id}'s Ka manifests with power {ka_power:.2f}")
        
        return results
    
    def _handle_afterlife_transition(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 11: Handle death and resurrection."""
        results = {"phase": "afterlife_transition", "effects": []}
        
        resurrection_power = self.phase_context.phase_modifiers.get("resurrection_power", 1.0)
        death_resistance = self.phase_context.phase_modifiers.get("death_resistance", 1.0)
        
        for entity_id, entity in entities.items():
            if not entity.is_alive:
                # Check for resurrection
                if hasattr(entity.card, 'keywords') and any('resurrection' in str(kw) for kw in entity.card.keywords):
                    resurrection_chance = 0.3 * resurrection_power
                    
                    if random.random() < resurrection_chance:
                        entity.is_alive = True
                        entity.current_health = max(1, int(entity.max_health * 0.3))
                        results["effects"].append(f"{entity_id} resurrects by divine intervention")
                        
            elif entity.current_health <= 0:
                # Apply death resistance
                if random.random() < (0.2 * death_resistance):
                    entity.current_health = 1
                    results["effects"].append(f"{entity_id} resists death at the threshold")
        
        return results
    
    def _handle_cosmic_balance(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 12: Restore universal balance."""
        results = {"phase": "cosmic_balance", "effects": []}
        
        total_balance = self.phase_context.cosmic_balance
        cosmic_power = self.phase_context.phase_modifiers.get("cosmic_power", 1.0)
        
        if abs(total_balance) > 3:
            # Significant cosmic imbalance - universal effects
            if total_balance > 0:
                # Order dominant - bless the righteous
                for entity_id, entity in entities.items():
                    if entity.is_alive and hasattr(entity, 'moral_actions'):
                        good_actions = sum(1 for action in entity.moral_actions if action > 0)
                        if good_actions > 0:
                            entity.temp_modifiers["cosmic_order_blessing"] = 1.0 + (cosmic_power * 0.2)
                            results["effects"].append(f"{entity_id} blessed by cosmic order")
            else:
                # Chaos dominant - chaotic effects on all
                for entity_id, entity in entities.items():
                    if entity.is_alive:
                        chaos_effect = random.choice(["confusion", "weakness", "madness"])
                        entity.temp_modifiers[f"chaos_{chaos_effect}"] = 0.8
                        results["effects"].append(f"{entity_id} affected by cosmic chaos: {chaos_effect}")
        
        return results
    
    def _handle_dusk_cleanup(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 13: Return to the world of the living."""
        results = {"phase": "dusk_cleanup", "effects": []}
        
        renewal_power = self.phase_context.phase_modifiers.get("renewal_power", 1.0)
        
        for entity_id, entity in entities.items():
            if entity.is_alive:
                # Clear temporary underworld modifiers
                underworld_modifiers = [key for key in entity.temp_modifiers.keys() 
                                      if any(word in key.lower() for word in 
                                           ['underworld', 'chaos', 'curse', 'lost'])]
                
                for modifier in underworld_modifiers:
                    del entity.temp_modifiers[modifier]
                
                # Apply renewal effects
                if hasattr(entity, 'ba_ka_state'):
                    entity.ba_ka_state.reunite_soul()
                
                # Partial healing from surviving the underworld
                renewal_healing = int(entity.max_health * 0.1 * renewal_power)
                entity.current_health = min(entity.max_health, entity.current_health + renewal_healing)
                
                results["effects"].append(f"{entity_id} emerges renewed from the underworld")
        
        return results
    
    def _handle_default_phase(self, entities: Dict[str, Any], combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Default phase handler."""
        return {"phase": self.current_phase.key, "effects": ["Phase executed with default behavior"]}
    
    def get_phase_description(self) -> str:
        """Get detailed description of current phase."""
        location = self.underworld_locations[self.current_phase.hour]
        
        description = f"**{self.current_phase.description}**\n"
        description += f"*Hour {self.current_phase.hour} of the Underworld Journey*\n\n"
        description += f"**Location:** {location.name}\n"
        description += f"{location.description}\n\n"
        
        if location.special_rules:
            description += f"**Special Rules:** {', '.join(location.special_rules)}\n"
        
        if location.environmental_effects:
            description += f"**Environmental Effects:**\n"
            for effect, value in location.environmental_effects.items():
                description += f"  • {effect}: {value:.1f}x\n"
        
        if location.guardian_entities:
            description += f"**Guardians Present:** {', '.join(location.guardian_entities)}\n"
        
        return description
    
    def is_combat_complete(self) -> bool:
        """Check if the full underworld journey is complete."""
        return (self.current_phase == CombatPhase.DUSK_CLEANUP and 
                len(self.phase_history) >= 13)
    
    def get_journey_progress(self) -> Dict[str, Any]:
        """Get progress through the underworld journey."""
        total_phases = 14  # 0-13
        completed_phases = len([p for p in self.phase_history if p != self.current_phase])
        
        return {
            "current_phase": self.current_phase.key,
            "current_hour": self.current_phase.hour,
            "completed_phases": completed_phases,
            "total_phases": total_phases,
            "progress_percentage": (completed_phases / total_phases) * 100,
            "cosmic_cycles": self.cosmic_cycle_count,
            "phase_history": [p.key for p in self.phase_history]
        }