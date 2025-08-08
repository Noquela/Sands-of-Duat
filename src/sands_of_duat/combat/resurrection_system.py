#!/usr/bin/env python3
"""
RESURRECTION SYSTEM
===================

Egyptian resurrection mechanics based on authentic afterlife beliefs.
Implements various forms of returning from death according to Egyptian
mythology, including mummification, Ba-Ka reunification, and divine intervention.
"""

import logging
import random
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ResurrectionType(Enum):
    """Different types of resurrection in Egyptian beliefs."""
    MUMMIFICATION_PRESERVATION = ("mummification", "Physical preservation allowing Ba to return")
    BA_KA_REUNIFICATION = ("ba_ka_reunion", "Soul components reuniting to restore life")
    DIVINE_INTERVENTION = ("divine_intervention", "Direct intervention by gods")
    OSIRIAN_REBIRTH = ("osirian_rebirth", "Death and rebirth like Osiris")
    PHARAOH_APOTHEOSIS = ("pharaoh_apotheosis", "Royal transformation to divine state")
    FIELD_OF_REEDS_RETURN = ("field_return", "Return from the blessed afterlife")
    ANCESTOR_CALLING = ("ancestor_calling", "Called back by living descendants")
    MAGICAL_RESTORATION = ("magical_restoration", "Restored through powerful magic")
    JUDGMENT_REVERSAL = ("judgment_reversal", "Divine judgment overturned")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

class PreservationState(Enum):
    """State of physical preservation."""
    FRESH_CORPSE = ("fresh", "Recently deceased, optimal for resurrection")
    MUMMIFIED_PERFECT = ("perfect_mummy", "Perfectly preserved through mummification")
    MUMMIFIED_GOOD = ("good_mummy", "Well preserved with minor damage")
    MUMMIFIED_DAMAGED = ("damaged_mummy", "Preservation compromised but viable")
    DECAYED = ("decayed", "Physical form significantly deteriorated")
    DESTROYED = ("destroyed", "Physical form completely destroyed")
    SPIRITUAL_ONLY = ("spiritual", "Only spiritual essence remains")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

class AfterlifeDestination(Enum):
    """Where the soul resides in death."""
    FIELD_OF_REEDS = ("field_of_reeds", "Paradise of the blessed")
    OSIRIS_REALM = ("osiris_realm", "Domain of Osiris in the underworld")
    WANDERING_SPIRIT = ("wandering", "Lost between worlds")
    DUAT_PASSAGE = ("duat_passage", "Still journeying through the underworld")
    ANCESTOR_REALM = ("ancestor_realm", "With family ancestors")
    DIVINE_SERVICE = ("divine_service", "Serving the gods")
    TRAPPED_TOMB = ("trapped_tomb", "Bound to burial place")
    DEVOURED = ("devoured", "Consumed by Ammit - true death")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

@dataclass
class DeathRecord:
    """Record of an entity's death and afterlife status."""
    entity_id: str
    death_time: datetime
    cause_of_death: str
    preservation_state: PreservationState = PreservationState.FRESH_CORPSE
    afterlife_destination: AfterlifeDestination = AfterlifeDestination.WANDERING_SPIRIT
    ba_location: str = "with_body"  # Where the Ba currently is
    ka_status: str = "weakening"    # Status of the Ka
    divine_judgment_score: float = 0.0
    resurrection_attempts: List[Dict[str, Any]] = field(default_factory=list)
    time_since_death: float = 0.0  # In hours
    mummification_quality: float = 0.0  # 0-1 scale
    tomb_protections: List[str] = field(default_factory=list)
    funeral_rites_performed: List[str] = field(default_factory=list)
    divine_favors: Dict[str, float] = field(default_factory=dict)
    family_connections: List[str] = field(default_factory=list)  # Living relatives
    
    def get_resurrection_difficulty(self) -> float:
        """Calculate base difficulty for resurrection."""
        base_difficulty = 0.5
        
        # Time since death increases difficulty
        time_factor = min(2.0, self.time_since_death / 72.0)  # 72 hours = 3 days
        base_difficulty += time_factor * 0.3
        
        # Preservation state affects difficulty
        preservation_modifiers = {
            PreservationState.FRESH_CORPSE: -0.2,
            PreservationState.MUMMIFIED_PERFECT: -0.3,
            PreservationState.MUMMIFIED_GOOD: -0.1,
            PreservationState.MUMMIFIED_DAMAGED: 0.1,
            PreservationState.DECAYED: 0.4,
            PreservationState.DESTROYED: 0.8,
            PreservationState.SPIRITUAL_ONLY: 0.6
        }
        
        base_difficulty += preservation_modifiers.get(self.preservation_state, 0.0)
        
        # Divine judgment affects resurrection
        if self.divine_judgment_score < -5:
            base_difficulty += 0.5  # Wicked souls harder to resurrect
        elif self.divine_judgment_score > 5:
            base_difficulty -= 0.3  # Righteous souls easier to resurrect
        
        return max(0.1, min(1.0, base_difficulty))

@dataclass
class ResurrectionAttempt:
    """A specific attempt to resurrect an entity."""
    attempt_id: str
    entity_id: str
    resurrector_id: Optional[str]  # Who is attempting the resurrection
    resurrection_type: ResurrectionType
    start_time: datetime = field(default_factory=datetime.now)
    required_components: List[str] = field(default_factory=list)
    available_components: List[str] = field(default_factory=list)
    divine_interventions: List[str] = field(default_factory=list)
    ritual_power: float = 0.0
    success_chance: float = 0.0
    result: Optional[str] = None
    complications: List[str] = field(default_factory=list)

class EgyptianResurrectionSystem:
    """
    Egyptian resurrection system implementing authentic afterlife mechanics.
    
    Based on Egyptian beliefs about death, preservation, soul components,
    divine intervention, and the various ways the dead can return to life.
    """
    
    def __init__(self):
        self.death_records: Dict[str, DeathRecord] = {}
        self.active_resurrections: Dict[str, ResurrectionAttempt] = {}
        self.resurrection_history: List[ResurrectionAttempt] = []
        
        # Resurrection requirements by type
        self.resurrection_requirements = {
            ResurrectionType.MUMMIFICATION_PRESERVATION: {
                "required_components": ["preserved_body", "opening_mouth_ritual", "proper_burial"],
                "divine_approval": ["Anubis"],
                "minimum_preservation": PreservationState.MUMMIFIED_DAMAGED,
                "base_success": 0.6
            },
            ResurrectionType.BA_KA_REUNIFICATION: {
                "required_components": ["soul_calling_ritual", "ba_guidance", "ka_offerings"],
                "divine_approval": ["Isis", "Anubis"],
                "minimum_preservation": PreservationState.DECAYED,
                "base_success": 0.4
            },
            ResurrectionType.DIVINE_INTERVENTION: {
                "required_components": ["divine_favor", "proper_prayers", "significant_offering"],
                "divine_approval": ["Ra", "Osiris", "Isis"],
                "minimum_preservation": PreservationState.SPIRITUAL_ONLY,
                "base_success": 0.3
            },
            ResurrectionType.OSIRIAN_REBIRTH: {
                "required_components": ["death_acceptance", "righteous_life", "divine_judgment"],
                "divine_approval": ["Osiris", "Isis"],
                "minimum_preservation": PreservationState.DESTROYED,
                "base_success": 0.2
            },
            ResurrectionType.PHARAOH_APOTHEOSIS: {
                "required_components": ["royal_burial", "pyramid_power", "divine_bloodline"],
                "divine_approval": ["Ra", "Horus"],
                "minimum_preservation": PreservationState.MUMMIFIED_GOOD,
                "base_success": 0.7
            },
            ResurrectionType.FIELD_OF_REEDS_RETURN: {
                "required_components": ["blessed_status", "divine_permission", "worthy_cause"],
                "divine_approval": ["Osiris", "Ra"],
                "minimum_preservation": PreservationState.SPIRITUAL_ONLY,
                "base_success": 0.5
            },
            ResurrectionType.ANCESTOR_CALLING: {
                "required_components": ["family_ritual", "ancestor_offerings", "blood_connection"],
                "divine_approval": [],
                "minimum_preservation": PreservationState.DECAYED,
                "base_success": 0.3
            },
            ResurrectionType.MAGICAL_RESTORATION: {
                "required_components": ["powerful_magic", "ritual_components", "magical_knowledge"],
                "divine_approval": ["Thoth", "Isis"],
                "minimum_preservation": PreservationState.MUMMIFIED_DAMAGED,
                "base_success": 0.4
            },
            ResurrectionType.JUDGMENT_REVERSAL: {
                "required_components": ["moral_redemption", "divine_mercy", "intercession"],
                "divine_approval": ["Ma'at", "Osiris"],
                "minimum_preservation": PreservationState.SPIRITUAL_ONLY,
                "base_success": 0.1
            }
        }
        
        # Gods and their resurrection specialties
        self.divine_resurrection_powers = {
            "Osiris": {
                "specialty": "underworld_ruler",
                "power_bonus": 0.3,
                "preferred_types": [ResurrectionType.OSIRIAN_REBIRTH, ResurrectionType.DIVINE_INTERVENTION]
            },
            "Isis": {
                "specialty": "magical_healing",
                "power_bonus": 0.4,
                "preferred_types": [ResurrectionType.MAGICAL_RESTORATION, ResurrectionType.BA_KA_REUNIFICATION]
            },
            "Anubis": {
                "specialty": "mummification_expert", 
                "power_bonus": 0.5,
                "preferred_types": [ResurrectionType.MUMMIFICATION_PRESERVATION]
            },
            "Ra": {
                "specialty": "solar_renewal",
                "power_bonus": 0.3,
                "preferred_types": [ResurrectionType.DIVINE_INTERVENTION, ResurrectionType.PHARAOH_APOTHEOSIS]
            },
            "Thoth": {
                "specialty": "magical_knowledge",
                "power_bonus": 0.2,
                "preferred_types": [ResurrectionType.MAGICAL_RESTORATION, ResurrectionType.JUDGMENT_REVERSAL]
            },
            "Horus": {
                "specialty": "royal_power",
                "power_bonus": 0.3,
                "preferred_types": [ResurrectionType.PHARAOH_APOTHEOSIS]
            }
        }
    
    def record_death(self, entity_id: str, cause_of_death: str, 
                     divine_judgment_score: float = 0.0) -> DeathRecord:
        """Record an entity's death and initialize afterlife status."""
        death_record = DeathRecord(
            entity_id=entity_id,
            death_time=datetime.now(),
            cause_of_death=cause_of_death,
            divine_judgment_score=divine_judgment_score
        )
        
        # Determine initial afterlife destination based on judgment
        if divine_judgment_score > 8:
            death_record.afterlife_destination = AfterlifeDestination.FIELD_OF_REEDS
        elif divine_judgment_score > 0:
            death_record.afterlife_destination = AfterlifeDestination.OSIRIS_REALM
        elif divine_judgment_score > -5:
            death_record.afterlife_destination = AfterlifeDestination.DUAT_PASSAGE
        elif divine_judgment_score > -10:
            death_record.afterlife_destination = AfterlifeDestination.WANDERING_SPIRIT
        else:
            death_record.afterlife_destination = AfterlifeDestination.DEVOURED
        
        self.death_records[entity_id] = death_record
        
        logger.info(f"{entity_id} died from {cause_of_death}, afterlife: {death_record.afterlife_destination.description}")
        return death_record
    
    def perform_mummification(self, entity_id: str, embalmers_skill: float = 0.5, 
                             resources_quality: float = 0.5) -> float:
        """Perform mummification on a deceased entity."""
        if entity_id not in self.death_records:
            return 0.0
        
        death_record = self.death_records[entity_id]
        
        # Time window for effective mummification (first 24 hours best)
        time_since_death = (datetime.now() - death_record.death_time).total_seconds() / 3600
        time_penalty = min(0.5, time_since_death / 24.0)  # Max 50% penalty after 24 hours
        
        # Calculate mummification quality
        base_quality = (embalmers_skill + resources_quality) / 2
        final_quality = max(0.0, base_quality - time_penalty)
        
        # Update preservation state based on quality
        if final_quality >= 0.9:
            death_record.preservation_state = PreservationState.MUMMIFIED_PERFECT
        elif final_quality >= 0.7:
            death_record.preservation_state = PreservationState.MUMMIFIED_GOOD
        elif final_quality >= 0.4:
            death_record.preservation_state = PreservationState.MUMMIFIED_DAMAGED
        else:
            death_record.preservation_state = PreservationState.DECAYED
        
        death_record.mummification_quality = final_quality
        death_record.funeral_rites_performed.append("mummification")
        
        logger.info(f"Mummification of {entity_id} completed: quality {final_quality:.2f}")
        return final_quality
    
    def perform_funeral_rites(self, entity_id: str, rites: List[str], 
                             ritual_power: float = 0.5) -> Dict[str, Any]:
        """Perform funeral rites that affect resurrection chances."""
        if entity_id not in self.death_records:
            return {"success": False, "message": "Entity not found"}
        
        death_record = self.death_records[entity_id]
        
        # Available funeral rites and their effects
        rite_effects = {
            "opening_of_the_mouth": {"ba_guidance": 0.3, "ka_strengthening": 0.2},
            "canopic_jar_ritual": {"preservation_bonus": 0.2, "organ_protection": 0.3},
            "book_of_the_dead": {"underworld_guidance": 0.4, "divine_protection": 0.2},
            "proper_burial": {"tomb_power": 0.3, "ancestor_connection": 0.2},
            "daily_offerings": {"ka_sustenance": 0.4, "ongoing_power": 0.1},
            "protective_amulets": {"spiritual_protection": 0.3, "curse_resistance": 0.2},
            "family_mourning": {"emotional_connection": 0.2, "calling_power": 0.3}
        }
        
        results = {"rites_performed": [], "total_benefit": 0.0, "effects": {}}
        
        for rite in rites:
            if rite in rite_effects:
                death_record.funeral_rites_performed.append(rite)
                
                # Apply rite effects modified by ritual power
                for effect, base_value in rite_effects[rite].items():
                    benefit = base_value * ritual_power
                    results["effects"][effect] = results["effects"].get(effect, 0) + benefit
                    results["total_benefit"] += benefit
                
                results["rites_performed"].append(rite)
                logger.info(f"Performed {rite} for {entity_id}")
        
        return results
    
    def attempt_resurrection(self, entity_id: str, resurrection_type: ResurrectionType,
                            resurrector_id: Optional[str] = None, 
                            available_components: List[str] = None,
                            divine_interventions: List[str] = None) -> ResurrectionAttempt:
        """Attempt to resurrect an entity using specified method."""
        if entity_id not in self.death_records:
            raise ValueError(f"No death record for {entity_id}")
        
        death_record = self.death_records[entity_id]
        
        # Create resurrection attempt
        attempt = ResurrectionAttempt(
            attempt_id=f"resurrection_{entity_id}_{len(death_record.resurrection_attempts)}",
            entity_id=entity_id,
            resurrector_id=resurrector_id,
            resurrection_type=resurrection_type,
            available_components=available_components or [],
            divine_interventions=divine_interventions or []
        )
        
        # Get requirements for this resurrection type
        requirements = self.resurrection_requirements[resurrection_type]
        attempt.required_components = requirements["required_components"].copy()
        
        # Check if preservation state is sufficient
        min_preservation = requirements["minimum_preservation"]
        if self._is_preservation_insufficient(death_record.preservation_state, min_preservation):
            attempt.result = "insufficient_preservation"
            attempt.complications.append(f"Requires at least {min_preservation.description}")
            death_record.resurrection_attempts.append(attempt.__dict__)
            return attempt
        
        # Calculate success chance
        base_success = requirements["base_success"]
        
        # Modify based on death record factors
        difficulty_modifier = death_record.get_resurrection_difficulty()
        success_chance = base_success * (1.0 - difficulty_modifier)
        
        # Component availability bonus
        available_required = sum(1 for comp in attempt.required_components 
                               if comp in attempt.available_components)
        component_bonus = (available_required / len(attempt.required_components)) * 0.3
        success_chance += component_bonus
        
        # Divine intervention bonuses
        divine_bonus = 0.0
        for intervention in attempt.divine_interventions:
            if intervention in self.divine_resurrection_powers:
                god_power = self.divine_resurrection_powers[intervention]
                if resurrection_type in god_power["preferred_types"]:
                    divine_bonus += god_power["power_bonus"]
                else:
                    divine_bonus += god_power["power_bonus"] * 0.5  # Half bonus for non-specialty
        
        success_chance += divine_bonus
        
        # Afterlife destination affects resurrection
        destination_modifiers = {
            AfterlifeDestination.FIELD_OF_REEDS: 0.2,   # Blessed can return easier
            AfterlifeDestination.OSIRIS_REALM: 0.1,    # Under divine protection
            AfterlifeDestination.WANDERING_SPIRIT: 0.0, # Neutral
            AfterlifeDestination.DUAT_PASSAGE: -0.1,   # Still journeying
            AfterlifeDestination.ANCESTOR_REALM: 0.05,  # Some connection
            AfterlifeDestination.DIVINE_SERVICE: -0.2,  # Serving gods, reluctant to leave
            AfterlifeDestination.TRAPPED_TOMB: -0.3,    # Bound by curse or obligation
            AfterlifeDestination.DEVOURED: -1.0        # True death, nearly impossible
        }
        
        success_chance += destination_modifiers.get(death_record.afterlife_destination, 0.0)
        
        # Cap success chance
        attempt.success_chance = max(0.01, min(0.95, success_chance))
        
        # Attempt the resurrection
        success = random.random() < attempt.success_chance
        
        if success:
            attempt.result = "success"
            self._complete_successful_resurrection(entity_id, attempt)
        else:
            attempt.result = "failure"
            self._handle_resurrection_failure(entity_id, attempt)
        
        # Record the attempt
        death_record.resurrection_attempts.append(attempt.__dict__)
        self.resurrection_history.append(attempt)
        
        logger.info(f"Resurrection attempt for {entity_id}: {attempt.result} (chance: {attempt.success_chance:.2f})")
        
        return attempt
    
    def _is_preservation_insufficient(self, current: PreservationState, required: PreservationState) -> bool:
        """Check if preservation state is insufficient for resurrection type."""
        preservation_order = [
            PreservationState.MUMMIFIED_PERFECT,
            PreservationState.MUMMIFIED_GOOD, 
            PreservationState.FRESH_CORPSE,
            PreservationState.MUMMIFIED_DAMAGED,
            PreservationState.DECAYED,
            PreservationState.SPIRITUAL_ONLY,
            PreservationState.DESTROYED
        ]
        
        try:
            current_index = preservation_order.index(current)
            required_index = preservation_order.index(required)
            return current_index > required_index
        except ValueError:
            return True  # If not found, assume insufficient
    
    def _complete_successful_resurrection(self, entity_id: str, attempt: ResurrectionAttempt):
        """Complete a successful resurrection."""
        death_record = self.death_records[entity_id]
        
        # Determine resurrection outcome based on type and circumstances
        resurrection_effects = {
            "restored_to_life": True,
            "health_percentage": 1.0,  # Full health by default
            "permanent_changes": [],
            "gained_abilities": [],
            "lost_abilities": [],
            "divine_blessings": [],
            "transformation_level": 0.0
        }
        
        # Type-specific effects
        if attempt.resurrection_type == ResurrectionType.MUMMIFICATION_PRESERVATION:
            # Traditional Egyptian resurrection - near full restoration
            resurrection_effects["health_percentage"] = 0.9
            resurrection_effects["gained_abilities"].append("undead_resistance")
            resurrection_effects["permanent_changes"].append("preserved_appearance")
            
        elif attempt.resurrection_type == ResurrectionType.BA_KA_REUNIFICATION:
            # Soul-based resurrection - spiritual enhancement
            resurrection_effects["health_percentage"] = 0.8
            resurrection_effects["gained_abilities"].extend(["soul_sight", "spiritual_communication"])
            resurrection_effects["transformation_level"] = 0.3
            
        elif attempt.resurrection_type == ResurrectionType.DIVINE_INTERVENTION:
            # Divine miracle - powerful but may have conditions
            resurrection_effects["health_percentage"] = 1.0
            resurrection_effects["divine_blessings"].append(f"blessed_by_{random.choice(attempt.divine_interventions)}")
            resurrection_effects["gained_abilities"].append("divine_favor")
            
        elif attempt.resurrection_type == ResurrectionType.OSIRIAN_REBIRTH:
            # Death and rebirth transformation - major changes
            resurrection_effects["health_percentage"] = 1.0
            resurrection_effects["transformation_level"] = 0.8
            resurrection_effects["gained_abilities"].extend(["death_immunity", "underworld_access"])
            resurrection_effects["permanent_changes"].append("osirian_transformation")
            
        elif attempt.resurrection_type == ResurrectionType.PHARAOH_APOTHEOSIS:
            # Royal divine transformation - become god-like
            resurrection_effects["health_percentage"] = 1.2  # More than full health
            resurrection_effects["transformation_level"] = 1.0
            resurrection_effects["gained_abilities"].extend(["divine_authority", "royal_power", "immortal_essence"])
            resurrection_effects["permanent_changes"].append("divine_apotheosis")
        
        # Apply quality modifiers based on mummification and rites
        if death_record.mummification_quality > 0:
            resurrection_effects["health_percentage"] *= (0.8 + death_record.mummification_quality * 0.2)
        
        if len(death_record.funeral_rites_performed) > 3:
            resurrection_effects["gained_abilities"].append("ritual_empowerment")
        
        # Remove from death records (they're alive now)
        logger.info(f"Successfully resurrected {entity_id} via {attempt.resurrection_type.key}")
        logger.info(f"Resurrection effects: {resurrection_effects}")
        
        # In a real game, this would restore the entity to active gameplay
        return resurrection_effects
    
    def _handle_resurrection_failure(self, entity_id: str, attempt: ResurrectionAttempt):
        """Handle what happens when resurrection fails."""
        death_record = self.death_records[entity_id]
        
        # Failure consequences
        consequences = []
        
        # Determine failure type
        if attempt.success_chance < 0.1:
            failure_type = "hopeless"
            consequences.extend([
                "Soul retreats deeper into afterlife",
                "Resistance to future attempts increases"
            ])
            # Make future attempts harder
            death_record.divine_judgment_score -= 1.0
            
        elif attempt.success_chance < 0.3:
            failure_type = "dangerous"
            consequences.extend([
                "Spiritual energy partially expended",
                "Soul trauma from failed return"
            ])
            
        else:
            failure_type = "near_miss" 
            consequences.extend([
                "Soul briefly stirred but could not return",
                "Preparation for future attempt improved"
            ])
            # Slight bonus to next attempt
            death_record.divine_judgment_score += 0.5
        
        # Random additional consequences
        if random.random() < 0.3:  # 30% chance
            additional_consequences = [
                "Disturbed other spirits in the process",
                "Attracted underworld guardians' attention",
                "Created spiritual disturbance in area",
                "Expended rare ritual components",
                "Drew divine displeasure from gods"
            ]
            consequences.append(random.choice(additional_consequences))
        
        attempt.complications.extend(consequences)
        
        logger.warning(f"Resurrection of {entity_id} failed ({failure_type}): {', '.join(consequences)}")
    
    def update_death_records(self, time_passed_hours: float):
        """Update death records based on passing time."""
        for entity_id, record in self.death_records.items():
            record.time_since_death += time_passed_hours
            
            # Natural decay affects preservation
            if record.preservation_state == PreservationState.FRESH_CORPSE and record.time_since_death > 72:
                record.preservation_state = PreservationState.DECAYED
                logger.info(f"{entity_id} body has decayed due to time passage")
            
            # Ka weakens over time without offerings
            if "daily_offerings" not in record.funeral_rites_performed:
                if record.time_since_death > 168:  # 1 week
                    record.ka_status = "severely_weakened"
                elif record.time_since_death > 48:  # 2 days
                    record.ka_status = "weakening"
    
    def get_resurrection_options(self, entity_id: str) -> List[Dict[str, Any]]:
        """Get available resurrection options for an entity."""
        if entity_id not in self.death_records:
            return []
        
        death_record = self.death_records[entity_id]
        options = []
        
        for res_type, requirements in self.resurrection_requirements.items():
            # Check if preservation is sufficient
            if self._is_preservation_insufficient(death_record.preservation_state, 
                                                requirements["minimum_preservation"]):
                continue
            
            # Check if afterlife destination allows resurrection
            if (death_record.afterlife_destination == AfterlifeDestination.DEVOURED and 
                res_type != ResurrectionType.JUDGMENT_REVERSAL):
                continue
            
            # Calculate estimated success chance
            base_success = requirements["base_success"]
            difficulty_mod = death_record.get_resurrection_difficulty()
            estimated_chance = base_success * (1.0 - difficulty_mod)
            
            option = {
                "type": res_type.key,
                "description": res_type.description,
                "required_components": requirements["required_components"],
                "divine_approval_needed": requirements["divine_approval"],
                "estimated_success_chance": max(0.01, min(0.95, estimated_chance)),
                "difficulty": "easy" if estimated_chance > 0.7 else "medium" if estimated_chance > 0.4 else "hard",
                "time_sensitive": death_record.time_since_death < 24  # First day is easier
            }
            
            options.append(option)
        
        return sorted(options, key=lambda x: x["estimated_success_chance"], reverse=True)
    
    def get_entity_death_status(self, entity_id: str) -> Dict[str, Any]:
        """Get comprehensive death and afterlife status for an entity."""
        if entity_id not in self.death_records:
            return {"status": "alive", "message": "Entity is not deceased"}
        
        record = self.death_records[entity_id]
        
        return {
            "status": "deceased",
            "time_since_death": record.time_since_death,
            "cause_of_death": record.cause_of_death,
            "preservation_state": {
                "current": record.preservation_state.key,
                "description": record.preservation_state.description,
                "mummification_quality": record.mummification_quality
            },
            "afterlife_location": {
                "destination": record.afterlife_destination.key,
                "description": record.afterlife_destination.description
            },
            "soul_status": {
                "ba_location": record.ba_location,
                "ka_status": record.ka_status
            },
            "divine_standing": record.divine_judgment_score,
            "funeral_preparations": {
                "rites_performed": record.funeral_rites_performed,
                "tomb_protections": record.tomb_protections,
                "family_connections": record.family_connections
            },
            "resurrection_history": {
                "attempts_made": len(record.resurrection_attempts),
                "last_attempt": record.resurrection_attempts[-1] if record.resurrection_attempts else None
            },
            "resurrection_difficulty": record.get_resurrection_difficulty()
        }
    
    def can_communicate_with_dead(self, entity_id: str, communication_type: str) -> bool:
        """Check if communication with a deceased entity is possible."""
        if entity_id not in self.death_records:
            return False
        
        record = self.death_records[entity_id]
        
        # Communication possibilities based on afterlife status
        communication_possibilities = {
            AfterlifeDestination.WANDERING_SPIRIT: ["seance", "medium", "dream"],
            AfterlifeDestination.TRAPPED_TOMB: ["tomb_visitation", "offering_ritual"],
            AfterlifeDestination.ANCESTOR_REALM: ["family_ritual", "ancestral_calling"],
            AfterlifeDestination.DUAT_PASSAGE: ["underworld_journey"],
            AfterlifeDestination.OSIRIS_REALM: ["divine_intervention"],
            AfterlifeDestination.FIELD_OF_REEDS: ["blessed_communication"],
            AfterlifeDestination.DIVINE_SERVICE: [],  # Too busy serving gods
            AfterlifeDestination.DEVOURED: []  # True death, no communication
        }
        
        possible_types = communication_possibilities.get(record.afterlife_destination, [])
        return communication_type in possible_types