#!/usr/bin/env python3
"""
UNDERWORLD PASSAGE SYSTEM
=========================

Egyptian underworld navigation system based on the 12-hour journey of Ra
through the Duat. Each hour represents a different challenge and location
in the Egyptian afterlife with authentic mythological elements.
"""

import logging
import random
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class UnderworldHour(Enum):
    """The 12 hours of the underworld journey."""
    FIRST_HOUR = ("first_hour", "Entry to the West", "The descent begins")
    SECOND_HOUR = ("second_hour", "Waters of Nun", "Primordial waters of creation")
    THIRD_HOUR = ("third_hour", "City of Rostau", "Sokar's hidden domain")
    FOURTH_HOUR = ("fourth_hour", "Path of Awakening", "Call to the sleeping gods")
    FIFTH_HOUR = ("fifth_hour", "Sokar's Cavern", "The most dangerous passage")
    SIXTH_HOUR = ("sixth_hour", "Khepri's Boat", "Transformation begins")
    SEVENTH_HOUR = ("seventh_hour", "Isis and Nephthys", "Divine protection")
    EIGHTH_HOUR = ("eighth_hour", "Fiery Domain", "Trial by fire")
    NINTH_HOUR = ("ninth_hour", "Blessed Dead", "Meeting the righteous")
    TENTH_HOUR = ("tenth_hour", "Drowning Enemies", "Defeating chaos")
    ELEVENTH_HOUR = ("eleventh_hour", "Preparing Dawn", "Gathering divine power")
    TWELFTH_HOUR = ("twelfth_hour", "Rebirth Portal", "Return to life")
    
    def __init__(self, key: str, display_name: str, description: str):
        self.key = key
        self.display_name = display_name
        self.description = description

class PassageChallenge(Enum):
    """Types of challenges in the underworld."""
    NAVIGATION = ("navigation", "Find the correct path through darkness")
    GUARDIAN_BATTLE = ("guardian_battle", "Defeat the hour's guardian")
    RIDDLE_SOLVING = ("riddle_solving", "Answer the sphinx's riddle")
    MORAL_TEST = ("moral_test", "Prove your worthiness through action")
    DIVINE_TRIAL = ("divine_trial", "Face judgment from a god")
    CHAOS_RESISTANCE = ("chaos_resistance", "Resist corrupting influences")
    SOUL_BINDING = ("soul_binding", "Maintain Ba-Ka connection")
    FEAR_OVERCOMING = ("fear_overcoming", "Conquer deepest fears")
    MEMORY_TRIAL = ("memory_trial", "Recall important truths")
    TRANSFORMATION = ("transformation", "Undergo spiritual change")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

@dataclass
class UnderworldLocation:
    """A specific location in the underworld."""
    hour: UnderworldHour
    name: str
    description: str
    challenges: List[PassageChallenge] = field(default_factory=list)
    guardian_names: List[str] = field(default_factory=list)
    environmental_effects: Dict[str, float] = field(default_factory=dict)
    required_knowledge: List[str] = field(default_factory=list)
    divine_presences: List[str] = field(default_factory=list)
    mythological_significance: str = ""
    passage_requirements: List[str] = field(default_factory=list)
    
    def get_difficulty_rating(self) -> float:
        """Calculate difficulty rating for this location."""
        base_difficulty = len(self.challenges) * 0.2
        guardian_difficulty = len(self.guardian_names) * 0.3
        knowledge_difficulty = len(self.required_knowledge) * 0.1
        return min(1.0, base_difficulty + guardian_difficulty + knowledge_difficulty)

@dataclass
class PassageAttempt:
    """An attempt to pass through an underworld location."""
    entity_id: str
    location: UnderworldLocation
    start_time: datetime = field(default_factory=datetime.now)
    challenges_faced: List[PassageChallenge] = field(default_factory=list)
    challenge_results: Dict[str, bool] = field(default_factory=dict)
    divine_interventions: List[str] = field(default_factory=list)
    final_result: Optional[str] = None
    experience_gained: Dict[str, float] = field(default_factory=dict)

@dataclass
class UnderworldJourney:
    """Complete journey through the underworld."""
    journey_id: str
    entity_id: str
    start_hour: UnderworldHour = UnderworldHour.FIRST_HOUR
    current_hour: UnderworldHour = UnderworldHour.FIRST_HOUR
    completed_hours: List[UnderworldHour] = field(default_factory=list)
    passage_attempts: List[PassageAttempt] = field(default_factory=list)
    total_time: float = 0.0  # Time spent in underworld
    divine_protectors: List[str] = field(default_factory=list)
    accumulated_power: Dict[str, float] = field(default_factory=dict)
    transformation_level: float = 0.0  # How much the soul has transformed

class UnderworldPassageSystem:
    """
    System for navigating the Egyptian underworld.
    
    Based on authentic Egyptian texts like the Amduat (Book of What is in the Underworld)
    and other funerary literature describing Ra's nightly journey.
    """
    
    def __init__(self):
        self.locations = self._initialize_underworld_locations()
        self.active_journeys: Dict[str, UnderworldJourney] = {}
        self.completed_journeys: List[UnderworldJourney] = []
        self.divine_guides = {
            "Ra": {"guidance_power": 0.8, "protection": 0.9, "transformation": 0.7},
            "Anubis": {"guidance_power": 0.9, "protection": 0.7, "transformation": 0.8},
            "Isis": {"guidance_power": 0.7, "protection": 0.9, "transformation": 0.9},
            "Thoth": {"guidance_power": 1.0, "protection": 0.6, "transformation": 0.8},
            "Osiris": {"guidance_power": 0.6, "protection": 0.8, "transformation": 1.0}
        }
        
    def _initialize_underworld_locations(self) -> Dict[UnderworldHour, UnderworldLocation]:
        """Initialize all 12 underworld locations with authentic details."""
        
        locations = {}
        
        # First Hour - Entry to the West
        locations[UnderworldHour.FIRST_HOUR] = UnderworldLocation(
            hour=UnderworldHour.FIRST_HOUR,
            name="Western Horizon Gate",
            description="The great gate where day dies and night begins. Massive stone pylons guard the entrance to the underworld.",
            challenges=[PassageChallenge.GUARDIAN_BATTLE, PassageChallenge.SOUL_BINDING],
            guardian_names=["Sia (Divine Perception)", "Hu (Divine Utterance)"],
            environmental_effects={"light_reduction": 0.3, "spiritual_pressure": 1.2},
            required_knowledge=["true_name", "proper_spells"],
            divine_presences=["Atum"],
            mythological_significance="The daily death of Ra begins his underworld journey",
            passage_requirements=["divine_protection", "proper_offerings"]
        )
        
        # Second Hour - Waters of Nun
        locations[UnderworldHour.SECOND_HOUR] = UnderworldLocation(
            hour=UnderworldHour.SECOND_HOUR,
            name="Primordial Waters",
            description="The chaotic waters that existed before creation. Here Ra's boat navigates the primordial floods.",
            challenges=[PassageChallenge.NAVIGATION, PassageChallenge.CHAOS_RESISTANCE],
            guardian_names=["Water Serpents", "Chaos Spawn"],
            environmental_effects={"chaos_influence": 1.5, "navigation_difficulty": 1.3},
            required_knowledge=["water_spells", "navigation_wisdom"],
            divine_presences=["Nun"],
            mythological_significance="Return to the primordial state before creation",
            passage_requirements=["chaos_resistance", "divine_boat"]
        )
        
        # Third Hour - City of Rostau
        locations[UnderworldHour.THIRD_HOUR] = UnderworldLocation(
            hour=UnderworldHour.THIRD_HOUR,
            name="Sokar's Hidden City",
            description="The mysterious cavern city of Sokar, god of the necropolis. Hidden passages wind through darkness.",
            challenges=[PassageChallenge.RIDDLE_SOLVING, PassageChallenge.FEAR_OVERCOMING],
            guardian_names=["Sokar", "Mummy Guardians", "Sphinx of Rostau"],
            environmental_effects={"fear_amplification": 1.6, "riddle_complexity": 1.4},
            required_knowledge=["riddle_answers", "burial_customs"],
            divine_presences=["Sokar"],
            mythological_significance="The most hidden and dangerous part of the underworld",
            passage_requirements=["courage", "wisdom", "proper_passwords"]
        )
        
        # Fourth Hour - Path of Awakening
        locations[UnderworldHour.FOURTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.FOURTH_HOUR,
            name="Valley of the Awakeners",
            description="Here the gods sleep until Ra's light awakens them. Calls echo through the valley.",
            challenges=[PassageChallenge.DIVINE_TRIAL, PassageChallenge.MEMORY_TRIAL],
            guardian_names=["Sleeping Gods", "Voice of Ra"],
            environmental_effects={"divine_awakening": 1.3, "memory_clarity": 1.2},
            required_knowledge=["divine_names", "awakening_formulas"],
            divine_presences=["Various Sleeping Gods"],
            mythological_significance="The awakening of divine powers for the journey ahead",
            passage_requirements=["divine_knowledge", "respectful_approach"]
        )
        
        # Fifth Hour - Sokar's Cavern (Most Dangerous)
        locations[UnderworldHour.FIFTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.FIFTH_HOUR,
            name="Cavern of Death",
            description="The deepest, most dangerous cavern where even Ra's light struggles to penetrate. Death itself dwells here.",
            challenges=[PassageChallenge.GUARDIAN_BATTLE, PassageChallenge.FEAR_OVERCOMING, 
                       PassageChallenge.SOUL_BINDING, PassageChallenge.TRANSFORMATION],
            guardian_names=["Sokar in his shrine", "Death Demons", "Apep's Children"],
            environmental_effects={"death_power": 2.0, "fear_maximum": 1.8, "transformation_pressure": 1.5},
            required_knowledge=["death_spells", "transformation_ritual", "sokar_prayers"],
            divine_presences=["Sokar", "Death Aspects"],
            mythological_significance="The place where even gods face their mortality",
            passage_requirements=["maximum_protection", "divine_intervention", "soul_strength"]
        )
        
        # Sixth Hour - Khepri's Boat
        locations[UnderworldHour.SIXTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.SIXTH_HOUR,
            name="Transformation Chamber",
            description="Where Ra begins his transformation from aged Atum to young Khepri. Scarab beetles guide the change.",
            challenges=[PassageChallenge.TRANSFORMATION, PassageChallenge.DIVINE_TRIAL],
            guardian_names=["Khepri", "Sacred Scarabs"],
            environmental_effects={"transformation_energy": 1.7, "renewal_power": 1.4},
            required_knowledge=["transformation_spells", "scarab_symbolism"],
            divine_presences=["Khepri", "Atum"],
            mythological_significance="The beginning of rebirth and renewal",
            passage_requirements=["readiness_for_change", "divine_blessing"]
        )
        
        # Seventh Hour - Isis and Nephthys
        locations[UnderworldHour.SEVENTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.SEVENTH_HOUR,
            name="Sanctuary of the Sister Goddesses",
            description="Isis and Nephthys provide divine protection and healing magic. A place of respite and restoration.",
            challenges=[PassageChallenge.MORAL_TEST, PassageChallenge.DIVINE_TRIAL],
            guardian_names=["Isis", "Nephthys"],
            environmental_effects={"healing_amplification": 1.6, "divine_protection": 1.5, "moral_clarity": 1.3},
            required_knowledge=["goddess_honors", "moral_principles"],
            divine_presences=["Isis", "Nephthys"],
            mythological_significance="Divine feminine protection and restoration",
            passage_requirements=["pure_intent", "respect_for_goddesses"]
        )
        
        # Eighth Hour - Fiery Domain
        locations[UnderworldHour.EIGHTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.EIGHTH_HOUR,
            name="Lake of Fire",
            description="A realm of purifying flames that burn away impurities. Only the worthy can pass through unharmed.",
            challenges=[PassageChallenge.CHAOS_RESISTANCE, PassageChallenge.MORAL_TEST],
            guardian_names=["Fire Demons", "Purifying Flames"],
            environmental_effects={"fire_damage": 1.5, "purification_power": 1.6, "moral_testing": 1.4},
            required_knowledge=["fire_protection", "purification_rites"],
            divine_presences=["Sekhmet"],
            mythological_significance="Purification through divine fire",
            passage_requirements=["moral_purity", "fire_protection"]
        )
        
        # Ninth Hour - Blessed Dead
        locations[UnderworldHour.NINTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.NINTH_HOUR,
            name="Fields of the Blessed",
            description="Where the righteous dead dwell in peace. They offer guidance and blessing to worthy travelers.",
            challenges=[PassageChallenge.MORAL_TEST, PassageChallenge.MEMORY_TRIAL],
            guardian_names=["Blessed Ancestors", "Righteous Spirits"],
            environmental_effects={"blessing_power": 1.5, "wisdom_enhancement": 1.3, "peace_influence": 1.4},
            required_knowledge=["ancestor_veneration", "righteous_living"],
            divine_presences=["Blessed Dead"],
            mythological_significance="Communion with the righteous departed",
            passage_requirements=["moral_standing", "ancestor_respect"]
        )
        
        # Tenth Hour - Drowning Enemies
        locations[UnderworldHour.TENTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.TENTH_HOUR,
            name="Waters of Defeat",
            description="Where the enemies of Ra are drowned and defeated. The forces of chaos meet their end.",
            challenges=[PassageChallenge.GUARDIAN_BATTLE, PassageChallenge.CHAOS_RESISTANCE],
            guardian_names=["Executioner Gods", "Drowning Waters"],
            environmental_effects={"chaos_defeat": 1.6, "battle_intensity": 1.4, "justice_power": 1.3},
            required_knowledge=["battle_spells", "justice_principles"],
            divine_presences=["Ra's Executioners"],
            mythological_significance="The defeat of chaos and evil",
            passage_requirements=["alignment_with_order", "battle_readiness"]
        )
        
        # Eleventh Hour - Preparing Dawn
        locations[UnderworldHour.ELEVENTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.ELEVENTH_HOUR,
            name="Dawn Preparation Chamber",
            description="Ra gathers his strength for rebirth as the new sun. Divine power accumulates for the final transformation.",
            challenges=[PassageChallenge.TRANSFORMATION, PassageChallenge.DIVINE_TRIAL],
            guardian_names=["Dawn Guardians", "Ra's Aspects"],
            environmental_effects={"power_accumulation": 1.7, "dawn_energy": 1.5, "transformation_readiness": 1.4},
            required_knowledge=["dawn_rituals", "solar_magic"],
            divine_presences=["Ra", "Khepri"],
            mythological_significance="Preparation for rebirth and renewal",
            passage_requirements=["spiritual_readiness", "accumulated_power"]
        )
        
        # Twelfth Hour - Rebirth Portal
        locations[UnderworldHour.TWELFTH_HOUR] = UnderworldLocation(
            hour=UnderworldHour.TWELFTH_HOUR,
            name="Gate of Dawn",
            description="The portal of rebirth where Ra emerges as the new sun. The moment of triumph and renewal.",
            challenges=[PassageChallenge.TRANSFORMATION, PassageChallenge.DIVINE_TRIAL],
            guardian_names=["Khepri", "Dawn Serpent", "Gate Guardians"],
            environmental_effects={"rebirth_energy": 2.0, "triumph_power": 1.6, "dawn_glory": 1.5},
            required_knowledge=["rebirth_formulas", "dawn_songs"],
            divine_presences=["Khepri", "Ra Reborn"],
            mythological_significance="The successful completion of death and rebirth",
            passage_requirements=["full_transformation", "divine_approval"]
        )
        
        return locations
    
    def start_underworld_journey(self, entity_id: str, divine_protector: str = "Anubis") -> UnderworldJourney:
        """Begin a journey through the underworld."""
        journey_id = f"journey_{entity_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        journey = UnderworldJourney(
            journey_id=journey_id,
            entity_id=entity_id,
            divine_protectors=[divine_protector]
        )
        
        self.active_journeys[entity_id] = journey
        
        logger.info(f"{entity_id} begins underworld journey with {divine_protector} as guide")
        return journey
    
    def attempt_passage(self, entity_id: str, special_knowledge: List[str] = None, 
                       divine_interventions: List[str] = None) -> PassageAttempt:
        """Attempt to pass through the current underworld location."""
        if entity_id not in self.active_journeys:
            raise ValueError(f"No active journey for {entity_id}")
        
        journey = self.active_journeys[entity_id]
        current_location = self.locations[journey.current_hour]
        
        # Create passage attempt
        attempt = PassageAttempt(
            entity_id=entity_id,
            location=current_location,
            divine_interventions=divine_interventions or []
        )
        
        # Calculate base success chance
        base_success = 0.3  # Base 30% chance
        
        # Apply divine protector bonuses
        for protector in journey.divine_protectors:
            if protector in self.divine_guides:
                guide_stats = self.divine_guides[protector]
                base_success += guide_stats["guidance_power"] * 0.2
        
        # Apply knowledge bonuses
        knowledge_bonus = 0.0
        if special_knowledge:
            for knowledge in special_knowledge:
                if knowledge in current_location.required_knowledge:
                    knowledge_bonus += 0.15  # 15% per relevant knowledge
        
        # Apply divine intervention bonuses
        intervention_bonus = 0.0
        if divine_interventions:
            for intervention in divine_interventions:
                intervention_bonus += 0.1  # 10% per intervention
        
        # Calculate challenge-specific success
        challenge_successes = []
        for challenge in current_location.challenges:
            challenge_success = self._attempt_challenge(
                challenge, base_success + knowledge_bonus + intervention_bonus, 
                journey, special_knowledge
            )
            attempt.challenge_results[challenge.key] = challenge_success
            challenge_successes.append(challenge_success)
            attempt.challenges_faced.append(challenge)
        
        # Overall passage success (need to pass most challenges)
        success_rate = sum(challenge_successes) / len(challenge_successes) if challenge_successes else 0
        passage_success = success_rate >= 0.6  # Need 60% success rate
        
        # Apply environmental effects and calculate experience
        self._apply_environmental_effects(attempt, journey, passage_success)
        
        # Determine final result
        if passage_success:
            attempt.final_result = "success"
            self._advance_journey_hour(journey)
            logger.info(f"{entity_id} successfully passes {current_location.name}")
        else:
            attempt.final_result = "failure"
            self._handle_passage_failure(journey, attempt)
            logger.info(f"{entity_id} fails to pass {current_location.name}")
        
        journey.passage_attempts.append(attempt)
        return attempt
    
    def _attempt_challenge(self, challenge: PassageChallenge, base_chance: float, 
                          journey: UnderworldJourney, special_knowledge: List[str] = None) -> bool:
        """Attempt a specific challenge."""
        challenge_modifiers = {
            PassageChallenge.NAVIGATION: 0.1,
            PassageChallenge.GUARDIAN_BATTLE: -0.1,  # Harder
            PassageChallenge.RIDDLE_SOLVING: 0.05,
            PassageChallenge.MORAL_TEST: 0.15,  # Easier for good entities
            PassageChallenge.DIVINE_TRIAL: 0.0,
            PassageChallenge.CHAOS_RESISTANCE: -0.05,
            PassageChallenge.SOUL_BINDING: 0.1,
            PassageChallenge.FEAR_OVERCOMING: -0.05,
            PassageChallenge.MEMORY_TRIAL: 0.08,
            PassageChallenge.TRANSFORMATION: -0.1  # Hardest
        }
        
        modified_chance = base_chance + challenge_modifiers.get(challenge, 0.0)
        
        # Apply journey-specific modifiers
        if challenge == PassageChallenge.TRANSFORMATION:
            modified_chance += journey.transformation_level * 0.1
        
        # Knowledge can help with specific challenges
        if special_knowledge:
            knowledge_help = {
                PassageChallenge.RIDDLE_SOLVING: ["riddle_answers", "wisdom"],
                PassageChallenge.DIVINE_TRIAL: ["divine_names", "proper_prayers"],
                PassageChallenge.NAVIGATION: ["underworld_maps", "navigation_wisdom"],
                PassageChallenge.MORAL_TEST: ["moral_principles", "righteous_living"]
            }
            
            if challenge in knowledge_help:
                for knowledge in special_knowledge:
                    if knowledge in knowledge_help[challenge]:
                        modified_chance += 0.1
        
        # Cap at 95% max chance
        final_chance = min(0.95, modified_chance)
        success = random.random() < final_chance
        
        logger.info(f"Challenge {challenge.key}: {final_chance:.2f} chance -> {'SUCCESS' if success else 'FAILURE'}")
        return success
    
    def _apply_environmental_effects(self, attempt: PassageAttempt, journey: UnderworldJourney, success: bool):
        """Apply environmental effects and calculate experience gained."""
        location = attempt.location
        
        # Base experience from facing challenges
        base_exp = len(attempt.challenges_faced) * 0.1
        
        # Bonus for success
        if success:
            base_exp *= 1.5
        
        # Apply environmental modifiers to experience
        for effect, multiplier in location.environmental_effects.items():
            if "power" in effect or "energy" in effect:
                base_exp *= (1.0 + (multiplier - 1.0) * 0.1)
        
        # Distribute experience among different aspects
        attempt.experience_gained = {
            "underworld_knowledge": base_exp * 0.3,
            "divine_connection": base_exp * 0.2,
            "transformation_progress": base_exp * 0.3,
            "courage": base_exp * 0.2
        }
        
        # Update journey stats
        journey.transformation_level += attempt.experience_gained["transformation_progress"]
        journey.total_time += random.uniform(0.5, 1.5)  # Each hour takes time
        
        # Accumulate power from successful passages
        if success:
            for power_type, amount in attempt.experience_gained.items():
                journey.accumulated_power[power_type] = journey.accumulated_power.get(power_type, 0) + amount
    
    def _advance_journey_hour(self, journey: UnderworldJourney):
        """Advance the journey to the next hour."""
        journey.completed_hours.append(journey.current_hour)
        
        # Get next hour
        hours = list(UnderworldHour)
        current_index = hours.index(journey.current_hour)
        
        if current_index < len(hours) - 1:
            journey.current_hour = hours[current_index + 1]
        else:
            # Journey complete!
            self._complete_journey(journey)
    
    def _handle_passage_failure(self, journey: UnderworldJourney, attempt: PassageAttempt):
        """Handle what happens when passage fails."""
        # Failure consequences based on location
        location = attempt.location
        
        if location.hour == UnderworldHour.FIFTH_HOUR:  # Most dangerous hour
            # Risk of being lost or destroyed
            if random.random() < 0.3:  # 30% chance of severe consequences
                logger.warning(f"{journey.entity_id} faces severe consequences in Sokar's Cavern")
                journey.transformation_level -= 0.5  # Lose progress
        
        # Generally, failure means delay and potential harm
        journey.total_time += random.uniform(1.0, 3.0)  # Additional time penalty
        
        # Can attempt again with accumulated experience
        # (in a real game, this might cost resources or have other penalties)
    
    def _complete_journey(self, journey: UnderworldJourney):
        """Complete the underworld journey."""
        journey.current_hour = None  # Journey finished
        
        # Calculate final transformation and rewards
        total_exp = sum(journey.accumulated_power.values())
        
        # Determine journey outcome
        if total_exp > 8.0:
            outcome = "triumphant_rebirth"
        elif total_exp > 5.0:
            outcome = "successful_passage"
        elif total_exp > 2.0:
            outcome = "difficult_survival"
        else:
            outcome = "barely_escaped"
        
        logger.info(f"{journey.entity_id} completes underworld journey: {outcome}")
        logger.info(f"Total transformation: {journey.transformation_level:.2f}")
        logger.info(f"Journey time: {journey.total_time:.1f} hours")
        
        # Move to completed journeys
        self.completed_journeys.append(journey)
        if journey.entity_id in self.active_journeys:
            del self.active_journeys[journey.entity_id]
        
        return outcome
    
    def get_journey_status(self, entity_id: str) -> Dict[str, Any]:
        """Get status of an entity's underworld journey."""
        if entity_id in self.active_journeys:
            journey = self.active_journeys[entity_id]
            current_location = self.locations[journey.current_hour]
            
            return {
                "status": "active",
                "current_hour": journey.current_hour.name,
                "current_location": current_location.name,
                "hours_completed": len(journey.completed_hours),
                "total_hours": 12,
                "progress": len(journey.completed_hours) / 12,
                "transformation_level": journey.transformation_level,
                "divine_protectors": journey.divine_protectors,
                "time_spent": journey.total_time,
                "next_challenges": [c.description for c in current_location.challenges]
            }
        
        # Check completed journeys
        for journey in self.completed_journeys:
            if journey.entity_id == entity_id:
                return {
                    "status": "completed",
                    "transformation_achieved": journey.transformation_level,
                    "total_time": journey.total_time,
                    "accumulated_power": journey.accumulated_power
                }
        
        return {"status": "no_journey"}
    
    def get_location_details(self, hour: UnderworldHour) -> Dict[str, Any]:
        """Get detailed information about an underworld location."""
        location = self.locations[hour]
        
        return {
            "name": location.name,
            "description": location.description,
            "challenges": [{"type": c.key, "description": c.description} for c in location.challenges],
            "guardians": location.guardian_names,
            "difficulty": location.get_difficulty_rating(),
            "required_knowledge": location.required_knowledge,
            "divine_presences": location.divine_presences,
            "environmental_effects": location.environmental_effects,
            "mythological_significance": location.mythological_significance,
            "passage_requirements": location.passage_requirements
        }
    
    def request_divine_intervention(self, entity_id: str, god_name: str, intervention_type: str) -> bool:
        """Request divine intervention during underworld passage."""
        if entity_id not in self.active_journeys:
            return False
        
        journey = self.active_journeys[entity_id]
        
        # Check if god is available for intervention
        if god_name not in self.divine_guides:
            return False
        
        # Different types of intervention
        intervention_success = False
        if intervention_type == "guidance":
            # Improve navigation and knowledge
            intervention_success = random.random() < 0.7
        elif intervention_type == "protection":
            # Provide defense against guardians
            intervention_success = random.random() < 0.6
        elif intervention_type == "transformation":
            # Aid in spiritual transformation
            intervention_success = random.random() < 0.5
        
        if intervention_success:
            if god_name not in journey.divine_protectors:
                journey.divine_protectors.append(god_name)
            logger.info(f"{god_name} provides {intervention_type} to {entity_id}")
        
        return intervention_success
    
    def get_available_knowledge(self) -> List[Dict[str, str]]:
        """Get list of all knowledge that can help in underworld passage."""
        all_knowledge = set()
        for location in self.locations.values():
            all_knowledge.update(location.required_knowledge)
        
        return [{"key": knowledge, "description": f"Knowledge of {knowledge.replace('_', ' ')}"} 
                for knowledge in sorted(all_knowledge)]