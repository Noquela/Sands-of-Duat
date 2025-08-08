#!/usr/bin/env python3
"""
BA-KA SOUL SYSTEM
=================

Authentic Egyptian soul mechanics based on ancient beliefs about the human soul.
Implements Ba (personality/soul) and Ka (life force/double) interactions in combat.

Key Egyptian Soul Components:
- Ba: The personality soul, bird-like, travels between worlds
- Ka: The life force double, needs offerings, stays near body  
- Akh: The glorified spirit (Ba + Ka united in afterlife)
- Ren: The true name (power component)
- Sheut: The shadow (hidden power)
"""

import logging
import random
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class SoulState(Enum):
    """States of the Egyptian soul components."""
    UNIFIED = "unified"           # Ba and Ka together (living state)
    BA_SEPARATED = "ba_separated" # Ba has left the body
    KA_MANIFESTED = "ka_manifested" # Ka appears as double
    SOUL_SPLIT = "soul_split"     # Both Ba and Ka active separately
    AKH_FORMED = "akh_formed"     # Glorified spirit achieved
    SOUL_LOST = "soul_lost"       # Soul components scattered
    DEVOURER_THREAT = "devourer_threat" # Ammit threatens consumption

class BaAbility(Enum):
    """Abilities of the Ba (personality soul)."""
    ASTRAL_TRAVEL = ("astral_travel", "Travel between physical and spiritual realms")
    IDENTITY_PRESERVATION = ("identity_preservation", "Maintain personality after death")
    MEMORY_ACCESS = ("memory_access", "Access memories from past lives") 
    SPIRITUAL_SIGHT = ("spiritual_sight", "See hidden spiritual entities")
    PERSONALITY_PROJECTION = ("personality_projection", "Project personality onto others")
    ANCESTRAL_COMMUNICATION = ("ancestral_communication", "Communicate with the dead")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

class KaAbility(Enum):
    """Abilities of the Ka (life force double)."""
    LIFE_FORCE_MANIPULATION = ("life_force_manipulation", "Control vital energy")
    PHYSICAL_DOUBLING = ("physical_doubling", "Create physical double")
    SUSTENANCE_ABSORPTION = ("sustenance_absorption", "Gain power from offerings")
    VITALITY_TRANSFER = ("vitality_transfer", "Transfer life force between entities")
    ANCESTRAL_STRENGTH = ("ancestral_strength", "Draw power from lineage")
    PROTECTIVE_MANIFESTATION = ("protective_manifestation", "Manifest as guardian")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

@dataclass
class BaComponent:
    """The Ba - personality soul that can travel between worlds."""
    strength: float = 1.0          # Ba spiritual strength
    mobility: float = 1.0          # Ability to travel between realms
    identity_coherence: float = 1.0 # How well personality is preserved
    active_abilities: List[BaAbility] = field(default_factory=list)
    astral_position: Tuple[float, float] = (0.0, 0.0)  # Position in astral realm
    memory_fragments: List[str] = field(default_factory=list)
    separation_time: int = 0       # How long Ba has been separated
    
    def separate_from_body(self) -> bool:
        """Ba separates from physical form to travel."""
        if self.strength > 0.3:  # Need minimum strength to separate
            self.separation_time = 0
            return True
        return False
    
    def travel_to_realm(self, realm: str) -> bool:
        """Ba travels to different spiritual realm."""
        travel_cost = 0.1 * self.mobility
        if self.strength > travel_cost:
            self.strength -= travel_cost
            return True
        return False
    
    def preserve_memories(self, experience: str):
        """Ba preserves important memories."""
        if len(self.memory_fragments) < 10:  # Limited memory storage
            self.memory_fragments.append(experience)
    
    def get_astral_power(self) -> float:
        """Calculate Ba's power in astral combat."""
        return self.strength * self.mobility * self.identity_coherence

@dataclass  
class KaComponent:
    """The Ka - life force double that needs sustenance."""
    vital_force: float = 1.0       # Raw life energy
    manifestation_strength: float = 1.0  # Ability to appear physically
    sustenance_level: float = 1.0  # Nourishment from offerings
    active_abilities: List[KaAbility] = field(default_factory=list)
    offering_history: List[str] = field(default_factory=list)
    manifestation_time: int = 0    # How long Ka has been manifested
    ancestral_connections: int = 0  # Strength of lineage connections
    
    def manifest_physically(self) -> bool:
        """Ka manifests as visible double."""
        manifestation_cost = 0.2
        if self.vital_force > manifestation_cost and self.sustenance_level > 0.5:
            self.vital_force -= manifestation_cost
            self.manifestation_time = 0
            return True
        return False
    
    def receive_offering(self, offering_type: str, power: float):
        """Ka receives sustenance from offerings."""
        self.sustenance_level = min(2.0, self.sustenance_level + power * 0.5)
        self.offering_history.append(f"{offering_type}:{power}")
        
        # Strengthen manifestation based on offering quality
        if power > 0.8:  # High quality offering
            self.manifestation_strength += 0.1
    
    def transfer_life_force(self, target, amount: float) -> bool:
        """Transfer vital force to another entity."""
        if self.vital_force > amount:
            self.vital_force -= amount
            return True
        return False
    
    def get_life_force_power(self) -> float:
        """Calculate Ka's life force power."""
        return self.vital_force * self.manifestation_strength * self.sustenance_level

@dataclass
class BaKaState:
    """Complete Ba-Ka soul state for an entity."""
    ba: BaComponent = field(default_factory=BaComponent)
    ka: KaComponent = field(default_factory=KaComponent) 
    soul_state: SoulState = SoulState.UNIFIED
    akh_progress: float = 0.0      # Progress toward Akh formation (0-1)
    divine_judgment_score: float = 0.0  # Ma'at judgment result
    name_power: float = 1.0        # Ren (true name) power
    shadow_strength: float = 1.0   # Sheut (shadow) power
    soul_coherence: float = 1.0    # Overall soul integrity
    
    def __post_init__(self):
        # Initialize with basic abilities based on soul strength
        if self.ba.strength > 0.7:
            self.ba.active_abilities.append(BaAbility.SPIRITUAL_SIGHT)
        if self.ka.vital_force > 0.7:
            self.ka.active_abilities.append(KaAbility.LIFE_FORCE_MANIPULATION)

class BaKaManager:
    """
    Manager for Ba-Ka soul mechanics in combat.
    
    Handles authentic Egyptian soul interactions including:
    - Ba separation and astral travel
    - Ka manifestation and sustenance
    - Akh formation (unified glorified spirit)
    - Soul-based combat abilities
    - Afterlife judgment effects
    """
    
    def __init__(self):
        self.entity_souls: Dict[str, BaKaState] = {}
        self.astral_realm_entities: List[str] = []  # Entities with Ba in astral realm
        self.manifested_kas: List[str] = []        # Entities with manifested Ka
        self.akh_candidates: List[str] = []        # Entities progressing toward Akh
        self.soul_interactions: List[Dict[str, Any]] = []  # Record of soul interactions
        
    def initialize_soul(self, entity_id: str, base_power: float = 1.0) -> BaKaState:
        """Initialize Ba-Ka state for an entity."""
        soul_state = BaKaState()
        
        # Randomize initial soul component strengths
        soul_state.ba.strength = base_power * random.uniform(0.8, 1.2)
        soul_state.ba.mobility = base_power * random.uniform(0.7, 1.3)
        soul_state.ba.identity_coherence = base_power * random.uniform(0.9, 1.1)
        
        soul_state.ka.vital_force = base_power * random.uniform(0.8, 1.2)
        soul_state.ka.manifestation_strength = base_power * random.uniform(0.7, 1.3)
        soul_state.ka.sustenance_level = random.uniform(0.5, 1.0)
        
        self.entity_souls[entity_id] = soul_state
        logger.info(f"Initialized soul for {entity_id}: Ba {soul_state.ba.strength:.2f}, Ka {soul_state.ka.vital_force:.2f}")
        
        return soul_state
    
    def separate_ba(self, entity_id: str) -> bool:
        """Attempt Ba separation for astral combat."""
        if entity_id not in self.entity_souls:
            return False
            
        soul_state = self.entity_souls[entity_id]
        
        if soul_state.soul_state != SoulState.UNIFIED:
            return False  # Already separated
            
        if soul_state.ba.separate_from_body():
            if soul_state.soul_state == SoulState.KA_MANIFESTED:
                soul_state.soul_state = SoulState.SOUL_SPLIT
            else:
                soul_state.soul_state = SoulState.BA_SEPARATED
                
            self.astral_realm_entities.append(entity_id)
            
            # Ba separation provides spiritual powers but physical vulnerability
            soul_state.soul_coherence -= 0.2  # Temporary vulnerability
            
            self.soul_interactions.append({
                "type": "ba_separation",
                "entity_id": entity_id,
                "success": True,
                "astral_power": soul_state.ba.get_astral_power()
            })
            
            logger.info(f"{entity_id}'s Ba separates - gains astral power {soul_state.ba.get_astral_power():.2f}")
            return True
        
        return False
    
    def manifest_ka(self, entity_id: str) -> bool:
        """Manifest Ka as physical double."""
        if entity_id not in self.entity_souls:
            return False
            
        soul_state = self.entity_souls[entity_id]
        
        if soul_state.ka.manifest_physically():
            if soul_state.soul_state == SoulState.BA_SEPARATED:
                soul_state.soul_state = SoulState.SOUL_SPLIT
            else:
                soul_state.soul_state = SoulState.KA_MANIFESTED
                
            self.manifested_kas.append(entity_id)
            
            # Ka manifestation provides physical power and protection
            ka_power = soul_state.ka.get_life_force_power()
            
            self.soul_interactions.append({
                "type": "ka_manifestation", 
                "entity_id": entity_id,
                "success": True,
                "life_force_power": ka_power
            })
            
            logger.info(f"{entity_id}'s Ka manifests - gains life force power {ka_power:.2f}")
            return True
        
        return False
    
    def offer_sustenance(self, entity_id: str, offering_type: str, power: float):
        """Provide sustenance offering to strengthen Ka."""
        if entity_id not in self.entity_souls:
            return
            
        soul_state = self.entity_souls[entity_id]
        soul_state.ka.receive_offering(offering_type, power)
        
        # Strong offerings can trigger special abilities
        if power > 1.0:
            if KaAbility.ANCESTRAL_STRENGTH not in soul_state.ka.active_abilities:
                soul_state.ka.active_abilities.append(KaAbility.ANCESTRAL_STRENGTH)
                logger.info(f"{entity_id} gains Ancestral Strength from powerful offering")
        
        logger.info(f"{entity_id} receives {offering_type} offering (power {power:.2f})")
    
    def attempt_akh_formation(self, entity_id: str) -> bool:
        """Attempt to form Akh (glorified spirit) by uniting Ba and Ka."""
        if entity_id not in self.entity_souls:
            return False
            
        soul_state = self.entity_souls[entity_id]
        
        # Require both Ba and Ka to be active and strong
        if (soul_state.soul_state == SoulState.SOUL_SPLIT and 
            soul_state.ba.strength > 0.8 and 
            soul_state.ka.vital_force > 0.8 and
            soul_state.divine_judgment_score > 0):  # Must pass divine judgment
            
            # Calculate Akh formation chance
            ba_power = soul_state.ba.get_astral_power()
            ka_power = soul_state.ka.get_life_force_power()
            judgment_bonus = soul_state.divine_judgment_score * 0.2
            
            akh_chance = min(0.9, (ba_power + ka_power + judgment_bonus) * 0.3)
            
            if random.random() < akh_chance:
                soul_state.soul_state = SoulState.AKH_FORMED
                soul_state.akh_progress = 1.0
                
                # Akh grants tremendous power
                soul_state.soul_coherence = 2.0  # Transcendent state
                
                # Remove from separate lists
                if entity_id in self.astral_realm_entities:
                    self.astral_realm_entities.remove(entity_id)
                if entity_id in self.manifested_kas:
                    self.manifested_kas.remove(entity_id)
                    
                self.akh_candidates.append(entity_id)
                
                self.soul_interactions.append({
                    "type": "akh_formation",
                    "entity_id": entity_id,
                    "success": True,
                    "total_power": ba_power + ka_power
                })
                
                logger.info(f"{entity_id} achieves Akh formation - becomes glorified spirit!")
                return True
        
        return False
    
    def reunite_soul(self, entity_id: str) -> bool:
        """Reunite separated Ba and Ka components."""
        if entity_id not in self.entity_souls:
            return False
            
        soul_state = self.entity_souls[entity_id]
        
        if soul_state.soul_state in [SoulState.BA_SEPARATED, SoulState.KA_MANIFESTED, SoulState.SOUL_SPLIT]:
            # Gradual reunification process
            reunification_power = (soul_state.ba.strength + soul_state.ka.vital_force) / 2
            
            if reunification_power > 0.5:
                soul_state.soul_state = SoulState.UNIFIED
                soul_state.soul_coherence = min(1.5, soul_state.soul_coherence + 0.3)
                
                # Remove from active lists
                if entity_id in self.astral_realm_entities:
                    self.astral_realm_entities.remove(entity_id)
                if entity_id in self.manifested_kas:
                    self.manifested_kas.remove(entity_id)
                
                # Ba gains strength from journey, Ka gains from sustenance
                soul_state.ba.strength = min(1.5, soul_state.ba.strength + 0.1)
                soul_state.ka.vital_force = min(1.5, soul_state.ka.vital_force + 0.1)
                
                logger.info(f"{entity_id}'s soul reunites - stronger from the journey")
                return True
        
        return False
    
    def process_soul_combat(self, attacker_id: str, defender_id: str, attack_type: str) -> Dict[str, Any]:
        """Process soul-based combat between entities."""
        if attacker_id not in self.entity_souls or defender_id not in self.entity_souls:
            return {"success": False, "message": "Soul states not found"}
        
        attacker_soul = self.entity_souls[attacker_id]
        defender_soul = self.entity_souls[defender_id]
        
        results = {
            "success": True,
            "attack_type": attack_type,
            "damage_dealt": 0,
            "special_effects": []
        }
        
        if attack_type == "astral_strike":
            # Ba vs Ba combat in astral realm
            if attacker_soul.soul_state in [SoulState.BA_SEPARATED, SoulState.SOUL_SPLIT]:
                attacker_power = attacker_soul.ba.get_astral_power()
                defender_resistance = defender_soul.ba.strength if defender_soul.soul_state != SoulState.UNIFIED else defender_soul.ba.strength * 0.5
                
                damage = max(0, attacker_power - defender_resistance) * 2  # Astral damage multiplier
                results["damage_dealt"] = damage
                
                # Astral damage affects Ba strength
                defender_soul.ba.strength = max(0.1, defender_soul.ba.strength - damage * 0.1)
                
                if damage > 1.0:
                    results["special_effects"].append("Astral shock - personality fragments scattered")
                    
        elif attack_type == "life_drain":
            # Ka vs Ka life force combat
            if attacker_soul.soul_state in [SoulState.KA_MANIFESTED, SoulState.SOUL_SPLIT]:
                attacker_power = attacker_soul.ka.get_life_force_power()
                
                # Attempt to drain life force
                drain_amount = attacker_power * 0.3
                if defender_soul.ka.transfer_life_force(attacker_soul.ka, drain_amount):
                    attacker_soul.ka.vital_force += drain_amount * 0.8  # Some loss in transfer
                    results["damage_dealt"] = drain_amount * 10  # Convert to combat damage
                    results["special_effects"].append("Life force drained")
                    
        elif attack_type == "soul_sunder":
            # Attempt to separate opponent's Ba and Ka forcefully
            if (attacker_soul.soul_state == SoulState.AKH_FORMED and 
                defender_soul.soul_state == SoulState.UNIFIED):
                
                sunder_power = attacker_soul.ba.get_astral_power() + attacker_soul.ka.get_life_force_power()
                defense_power = defender_soul.soul_coherence
                
                if sunder_power > defense_power * 1.5:
                    # Force soul separation
                    if random.random() < 0.6:  # 60% chance
                        self.separate_ba(defender_id)
                        results["special_effects"].append("Soul forcefully sundered!")
                        results["damage_dealt"] = sunder_power
                        
        elif attack_type == "name_binding":
            # Attack using true name power (Ren)
            name_power = attacker_soul.name_power
            if name_power > defender_soul.name_power:
                binding_strength = (name_power - defender_soul.name_power) * 5
                results["damage_dealt"] = binding_strength
                results["special_effects"].append("Bound by true name magic")
                
                # Reduce defender's name power
                defender_soul.name_power = max(0.1, defender_soul.name_power - 0.2)
        
        # Record interaction
        self.soul_interactions.append({
            "type": f"soul_combat_{attack_type}",
            "attacker": attacker_id,
            "defender": defender_id,
            "results": results
        })
        
        return results
    
    def process_divine_judgment(self, entity_id: str, actions: List[Tuple[str, float]]) -> float:
        """Process divine judgment of an entity's actions for Ma'at balance."""
        if entity_id not in self.entity_souls:
            return 0.0
            
        soul_state = self.entity_souls[entity_id]
        
        # Calculate moral balance based on actions
        total_balance = 0.0
        for action_type, moral_weight in actions:
            total_balance += moral_weight
            
        # Modify based on soul state
        if soul_state.soul_state == SoulState.AKH_FORMED:
            total_balance *= 1.3  # Akh spirits judged more favorably
        elif soul_state.soul_state == SoulState.SOUL_LOST:
            total_balance *= 0.5  # Damaged souls judged more harshly
            
        soul_state.divine_judgment_score = total_balance
        
        # Extreme negative judgment threatens with Ammit (the Devourer)
        if total_balance < -5.0:
            soul_state.soul_state = SoulState.DEVOURER_THREAT
            logger.warning(f"{entity_id} faces the threat of Ammit the Devourer!")
            
        return total_balance
    
    def handle_soul_death(self, entity_id: str) -> Dict[str, Any]:
        """Handle what happens to the soul when the entity dies."""
        if entity_id not in self.entity_souls:
            return {"success": False}
            
        soul_state = self.entity_souls[entity_id]
        death_results = {
            "soul_preserved": False,
            "afterlife_destination": "lost_in_darkness",
            "resurrection_possible": False,
            "special_effects": []
        }
        
        if soul_state.soul_state == SoulState.AKH_FORMED:
            # Akh spirits have achieved immortality
            death_results["soul_preserved"] = True
            death_results["afterlife_destination"] = "field_of_reeds"
            death_results["resurrection_possible"] = True
            death_results["special_effects"].append("Akh spirit transcends death")
            
        elif soul_state.soul_state == SoulState.DEVOURER_THREAT:
            # Threatened by Ammit - soul may be devoured
            if random.random() < 0.7:  # 70% chance of being devoured
                soul_state.soul_state = SoulState.SOUL_LOST
                death_results["afterlife_destination"] = "devoured_by_ammit"
                death_results["special_effects"].append("Soul devoured by Ammit - true death")
            else:
                death_results["afterlife_destination"] = "reprieve_granted"
                death_results["special_effects"].append("Divine reprieve granted")
                
        elif soul_state.divine_judgment_score > 0:
            # Positive judgment - enters underworld safely
            death_results["soul_preserved"] = True
            death_results["afterlife_destination"] = "underworld_safe_passage"
            if soul_state.ba.strength > 0.7 and soul_state.ka.vital_force > 0.7:
                death_results["resurrection_possible"] = True
                
        else:
            # Neutral or slightly negative - wandering spirit
            death_results["afterlife_destination"] = "wandering_spirit"
            if soul_state.ba.strength > 0.5:
                death_results["soul_preserved"] = True
                
        logger.info(f"{entity_id}'s soul faces death: {death_results['afterlife_destination']}")
        return death_results
    
    def get_soul_power_modifiers(self, entity_id: str) -> Dict[str, float]:
        """Get combat modifiers based on current soul state."""
        if entity_id not in self.entity_souls:
            return {}
            
        soul_state = self.entity_souls[entity_id]
        modifiers = {}
        
        # Base soul coherence affects all actions
        modifiers["soul_coherence"] = soul_state.soul_coherence
        
        if soul_state.soul_state == SoulState.BA_SEPARATED:
            modifiers["spiritual_power"] = soul_state.ba.get_astral_power()
            modifiers["physical_vulnerability"] = 0.7  # More vulnerable physically
            modifiers["astral_sight"] = 1.5  # Can see spiritual entities
            
        elif soul_state.soul_state == SoulState.KA_MANIFESTED:
            modifiers["life_force_power"] = soul_state.ka.get_life_force_power()
            modifiers["physical_strength"] = 1.4  # Ka doubles physical power
            modifiers["sustenance_need"] = 0.8    # Needs more offerings
            
        elif soul_state.soul_state == SoulState.SOUL_SPLIT:
            modifiers["dual_existence"] = 2.0     # Can act in both realms
            modifiers["power_drain"] = 0.9        # Maintaining both is taxing
            modifiers["versatility"] = 1.6        # More action options
            
        elif soul_state.soul_state == SoulState.AKH_FORMED:
            modifiers["transcendent_power"] = 2.5  # Tremendous power
            modifiers["divine_connection"] = 2.0   # Direct divine link
            modifiers["immortal_essence"] = 1.8    # Resistance to permanent death
            
        elif soul_state.soul_state == SoulState.SOUL_LOST:
            modifiers["power_fragmentation"] = 0.3  # Severely weakened
            modifiers["identity_loss"] = 0.5        # Personality fragmenting
            
        # Add ability-based modifiers
        for ability in soul_state.ba.active_abilities:
            if ability == BaAbility.ASTRAL_TRAVEL:
                modifiers["mobility"] = 1.3
            elif ability == BaAbility.SPIRITUAL_SIGHT:
                modifiers["detection"] = 1.4
                
        for ability in soul_state.ka.active_abilities:
            if ability == KaAbility.LIFE_FORCE_MANIPULATION:
                modifiers["healing_power"] = 1.5
            elif ability == KaAbility.ANCESTRAL_STRENGTH:
                modifiers["legacy_power"] = 1.3
                
        return modifiers
    
    def get_soul_status_description(self, entity_id: str) -> str:
        """Get detailed description of entity's soul state."""
        if entity_id not in self.entity_souls:
            return "Soul state unknown"
            
        soul_state = self.entity_souls[entity_id]
        
        descriptions = {
            SoulState.UNIFIED: "Soul is unified - Ba and Ka in harmony",
            SoulState.BA_SEPARATED: "Ba travels in the astral realm while Ka remains with body",
            SoulState.KA_MANIFESTED: "Ka appears as a life force double",
            SoulState.SOUL_SPLIT: "Both Ba and Ka are active - dual existence",
            SoulState.AKH_FORMED: "Akh achieved - glorified immortal spirit",
            SoulState.SOUL_LOST: "Soul fragments scattered - identity fragmenting",
            SoulState.DEVOURER_THREAT: "Ammit the Devourer threatens to consume the soul"
        }
        
        base_desc = descriptions.get(soul_state.soul_state, "Unknown soul state")
        
        # Add additional details
        details = []
        if soul_state.ba.strength > 1.2:
            details.append("strong Ba")
        elif soul_state.ba.strength < 0.5:
            details.append("weakened Ba")
            
        if soul_state.ka.vital_force > 1.2:
            details.append("powerful Ka")
        elif soul_state.ka.vital_force < 0.5:
            details.append("depleted Ka")
            
        if soul_state.akh_progress > 0.7:
            details.append("approaching Akh")
            
        if soul_state.divine_judgment_score > 2:
            details.append("judged righteous")
        elif soul_state.divine_judgment_score < -2:
            details.append("judged wicked")
            
        if details:
            base_desc += f" ({', '.join(details)})"
            
        return base_desc