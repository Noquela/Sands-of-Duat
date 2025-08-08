#!/usr/bin/env python3
"""
HOUR-GLASS INITIATIVE SYSTEM
============================

Egyptian time-based initiative system where actions flow like sand through
an hourglass. Based on authentic Egyptian concepts of time and cosmic order.
"""

import math
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class TimePhase(Enum):
    """Egyptian time phases based on solar cycle."""
    DAWN = "dawn"           # Khepri - Morning transformation
    MIDDAY = "midday"       # Ra - Peak power
    DUSK = "dusk"          # Atum - Evening completion
    MIDNIGHT = "midnight"   # Underworld journey

@dataclass
class SandFlow:
    """Represents the flow of time sand in the hourglass."""
    current_position: float = 0.0  # -1.0 (top) to 1.0 (bottom)
    flow_rate: float = 0.1         # Sand flow speed per turn
    divine_modifiers: Dict[str, float] = field(default_factory=dict)
    cosmic_disruptions: List[Tuple[str, float, int]] = field(default_factory=list)  # name, modifier, duration

class HourGlassInitiative:
    """
    Egyptian Hour-Glass Initiative System
    
    Time flows like sand through an hourglass. Position determines action order:
    - Top of glass (-1.0): Swift actions, light magic
    - Middle (0.0): Balanced actions, most spells  
    - Bottom (+1.0): Heavy actions, powerful magic, resurrection
    
    Based on Egyptian beliefs about time, ma'at (balance), and cosmic order.
    """
    
    def __init__(self):
        self.sand_flow = SandFlow()
        self.entity_positions: Dict[str, float] = {}  # entity_id -> position
        self.action_weights: Dict[str, float] = {
            'swift_strike': -0.8,      # Light, quick attacks
            'blessing': -0.6,          # Divine blessings flow upward
            'normal_attack': -0.2,     # Standard combat actions
            'spell_cast': 0.0,         # Balanced magical actions
            'divine_intervention': 0.3, # Heavy divine magic
            'resurrection': 0.8,       # Powerful underworld magic
            'cosmic_judgment': 1.0     # Ultimate divine actions
        }
        self.time_phase = TimePhase.DAWN
        self.turn_counter = 0
        
    def calculate_initiative_order(self, entities: Dict[str, Any]) -> List[str]:
        """
        Calculate turn order based on hourglass position and action weights.
        
        Returns entity IDs in order of action (fastest to slowest).
        """
        entity_initiative = []
        
        for entity_id, entity in entities.items():
            if not entity.is_alive:
                continue
                
            # Base position in hourglass
            base_position = self.entity_positions.get(entity_id, 0.0)
            
            # Apply divine modifiers
            divine_modifier = self._get_divine_modifier(entity)
            
            # Apply time phase effects
            phase_modifier = self._get_time_phase_modifier(entity)
            
            # Calculate final initiative position
            final_position = base_position + divine_modifier + phase_modifier
            final_position = max(-1.0, min(1.0, final_position))  # Clamp to hourglass bounds
            
            entity_initiative.append((entity_id, final_position))
            
        # Sort by position (lowest/top first = fastest)
        entity_initiative.sort(key=lambda x: x[1])
        
        logger.info(f"Initiative order calculated for {self.time_phase.value}:")
        for entity_id, position in entity_initiative:
            logger.info(f"  {entity_id}: {position:.2f}")
            
        return [entity_id for entity_id, _ in entity_initiative]
    
    def apply_action_weight(self, entity_id: str, action_type: str) -> float:
        """Apply action weight to entity's hourglass position."""
        if entity_id not in self.entity_positions:
            self.entity_positions[entity_id] = 0.0
            
        action_weight = self.action_weights.get(action_type, 0.0)
        
        # Heavy actions sink in the hourglass
        self.entity_positions[entity_id] += action_weight * 0.3
        
        # Clamp to hourglass bounds
        self.entity_positions[entity_id] = max(-1.0, min(1.0, self.entity_positions[entity_id]))
        
        return self.entity_positions[entity_id]
    
    def advance_time(self) -> TimePhase:
        """Advance the cosmic time and sand flow."""
        self.turn_counter += 1
        
        # Sand flows down through hourglass
        self.sand_flow.current_position += self.sand_flow.flow_rate
        
        # Apply cosmic disruptions
        self._process_cosmic_disruptions()
        
        # Determine time phase (4 turns per phase)
        phase_index = (self.turn_counter // 4) % 4
        old_phase = self.time_phase
        self.time_phase = list(TimePhase)[phase_index]
        
        if self.time_phase != old_phase:
            logger.info(f"Time phase changed: {old_phase.value} → {self.time_phase.value}")
            self._apply_phase_transition_effects()
        
        # Reset hourglass when it reaches bottom (represents cosmic cycle)
        if self.sand_flow.current_position >= 1.0:
            self._reset_hourglass()
            
        return self.time_phase
    
    def add_divine_intervention(self, god_name: str, modifier: float, duration: int):
        """Add divine intervention affecting time flow."""
        self.sand_flow.divine_modifiers[god_name] = modifier
        self.sand_flow.cosmic_disruptions.append((god_name, modifier, duration))
        
        logger.info(f"Divine intervention: {god_name} affects time flow by {modifier} for {duration} turns")
    
    def _get_divine_modifier(self, entity) -> float:
        """Calculate divine favor modifier for initiative."""
        if hasattr(entity, 'card') and hasattr(entity.card, 'stats'):
            divine_favor = getattr(entity.card.stats, 'divine_favor', 0)
            
            # Divine favor affects position in hourglass
            # Positive favor = lighter (move up), negative = heavier (sink down)
            return -divine_favor * 0.05  # Convert to position modifier
            
        return 0.0
    
    def _get_time_phase_modifier(self, entity) -> float:
        """Calculate time phase modifier based on entity's nature."""
        phase_modifiers = {
            TimePhase.DAWN: {
                'light': -0.2,      # Light entities faster at dawn
                'divine': -0.1,     # Divine entities empowered
                'undead': 0.1,      # Undead sluggish in light
                'darkness': 0.2     # Dark entities slower
            },
            TimePhase.MIDDAY: {
                'solar': -0.3,      # Solar entities peak power
                'ra': -0.4,         # Ra's domain
                'light': -0.1,      # Light still favored
                'darkness': 0.3     # Darkness weakened
            },
            TimePhase.DUSK: {
                'balance': -0.1,    # Balanced time
                'transition': -0.2, # Transition magic stronger
                'maat': -0.1        # Ma'at's influence
            },
            TimePhase.MIDNIGHT: {
                'undead': -0.2,     # Undead empowered
                'darkness': -0.3,   # Dark magic stronger
                'underworld': -0.4, # Underworld entities peak
                'light': 0.2,       # Light magic weakened
                'divine': 0.1       # Most gods rest
            }
        }
        
        if not hasattr(entity, 'card'):
            return 0.0
            
        total_modifier = 0.0
        entity_tags = getattr(entity.card, 'tags', [])
        
        for tag in entity_tags:
            if tag in phase_modifiers[self.time_phase]:
                total_modifier += phase_modifiers[self.time_phase][tag]
                
        return total_modifier
    
    def _process_cosmic_disruptions(self):
        """Process ongoing cosmic disruptions affecting time."""
        remaining_disruptions = []
        
        for name, modifier, duration in self.sand_flow.cosmic_disruptions:
            if duration > 1:
                remaining_disruptions.append((name, modifier, duration - 1))
            else:
                # Remove expired divine intervention
                if name in self.sand_flow.divine_modifiers:
                    del self.sand_flow.divine_modifiers[name]
                    logger.info(f"Divine intervention by {name} has ended")
                    
        self.sand_flow.cosmic_disruptions = remaining_disruptions
    
    def _apply_phase_transition_effects(self):
        """Apply effects when time phase changes."""
        effects = {
            TimePhase.DAWN: "New beginnings empower light magic",
            TimePhase.MIDDAY: "Ra's presence strengthens solar magic", 
            TimePhase.DUSK: "Balance of ma'at affects all entities",
            TimePhase.MIDNIGHT: "Underworld forces gain strength"
        }
        
        logger.info(f"Phase transition effect: {effects[self.time_phase]}")
        
        # Apply universal effects based on phase
        if self.time_phase == TimePhase.DAWN:
            # Reset negative modifiers (new day, fresh start)
            for entity_id in self.entity_positions:
                if self.entity_positions[entity_id] > 0.5:
                    self.entity_positions[entity_id] *= 0.7  # Reduce heavy penalties
                    
        elif self.time_phase == TimePhase.MIDNIGHT:
            # Underworld magic disrupts normal order
            self.sand_flow.flow_rate += 0.05  # Time flows faster
    
    def _reset_hourglass(self):
        """Reset the hourglass when sand reaches bottom (cosmic cycle complete)."""
        logger.info("Cosmic cycle complete - resetting hourglass")
        
        self.sand_flow.current_position = -1.0  # Return to top
        self.sand_flow.flow_rate = 0.1  # Reset flow rate
        
        # Entities settle to new positions based on their nature
        for entity_id in self.entity_positions:
            # Gradually move toward neutral position
            current_pos = self.entity_positions[entity_id]
            self.entity_positions[entity_id] = current_pos * 0.5
    
    def get_time_description(self) -> str:
        """Get descriptive text for current time state."""
        position_desc = ""
        if self.sand_flow.current_position < -0.5:
            position_desc = "The sands gather at the top of time's hourglass"
        elif self.sand_flow.current_position < 0.0:
            position_desc = "Time flows steadily through the upper chamber"  
        elif self.sand_flow.current_position < 0.5:
            position_desc = "Sands cascade through the narrow center"
        else:
            position_desc = "The lower chamber fills with the weight of time"
            
        phase_desc = {
            TimePhase.DAWN: "Khepri pushes the sun across the horizon",
            TimePhase.MIDDAY: "Ra stands triumphant in his solar barque", 
            TimePhase.DUSK: "Atum completes the day's journey",
            TimePhase.MIDNIGHT: "The sun travels through the underworld"
        }
        
        return f"{position_desc}. {phase_desc[self.time_phase]}."
    
    def get_initiative_preview(self, entities: Dict[str, Any], action_type: str) -> List[Tuple[str, float]]:
        """Preview initiative order if specific action is taken."""
        preview_positions = {}
        action_weight = self.action_weights.get(action_type, 0.0)
        
        for entity_id, entity in entities.items():
            if not entity.is_alive:
                continue
                
            base_position = self.entity_positions.get(entity_id, 0.0)
            
            # Simulate action weight application
            preview_position = base_position + (action_weight * 0.3)
            preview_position = max(-1.0, min(1.0, preview_position))
            
            # Apply other modifiers
            divine_modifier = self._get_divine_modifier(entity)
            phase_modifier = self._get_time_phase_modifier(entity)
            final_position = preview_position + divine_modifier + phase_modifier
            final_position = max(-1.0, min(1.0, final_position))
            
            preview_positions[entity_id] = final_position
        
        # Sort by position
        sorted_positions = sorted(preview_positions.items(), key=lambda x: x[1])
        return sorted_positions