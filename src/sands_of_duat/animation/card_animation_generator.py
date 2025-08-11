"""
Card Animation Generator - Game Integration Layer
High-level interface for generating animations for Egyptian cards in the game.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum, auto

from .animation_pipeline import animation_pipeline, CardAnimationSpec, BatchGenerationRequest
from ..core.asset_loader import get_asset_loader
from ..core.constants import Colors

class AnimationPriority(Enum):
    """Animation generation priority levels."""
    LOW = 1      # Background generation
    NORMAL = 2   # Standard priority
    HIGH = 3     # User requested
    URGENT = 4   # Needed immediately

@dataclass 
class GameCardSpec:
    """Game-specific card specification for animation."""
    card_id: str
    name: str
    card_type: str
    rarity: str
    god: str
    description: str
    power: int = 0
    health: int = 0
    cost: int = 0

class CardAnimationGenerator:
    """
    Game-integrated card animation generator.
    Provides high-level interface for generating Egyptian card animations.
    """
    
    def __init__(self):
        """Initialize card animation generator."""
        self.logger = logging.getLogger("card_animation_generator")
        self.asset_loader = get_asset_loader()
        
        # Generation state
        self.is_initialized = False
        self.generation_active = False
        self.pending_cards = []
        self.completed_cards = {}
        
        # Callbacks
        self.progress_callbacks = []
        self.completion_callbacks = []
        
        # Egyptian card database for animation
        self.egyptian_cards = self._load_egyptian_card_database()
        
        self.logger.info("Card Animation Generator initialized")
    
    async def initialize(self) -> bool:
        """Initialize the animation generator."""
        try:
            success = await animation_pipeline.initialize()
            if success:
                self.is_initialized = True
                self.logger.info("Card Animation Generator ready")
                return True
            else:
                self.logger.error("Failed to initialize Card Animation Generator")
                return False
                
        except Exception as e:
            self.logger.error(f"Card Animation Generator initialization error: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown animation generator."""
        await animation_pipeline.shutdown()
        self.is_initialized = False
        self.logger.info("Card Animation Generator shut down")
    
    def _load_egyptian_card_database(self) -> Dict[str, GameCardSpec]:
        """Load Egyptian card specifications for animation generation."""
        return {
            # RA - Sun God Cards
            "ra_solar_deity": GameCardSpec(
                card_id="ra_01", name="Ra, Solar Deity", card_type="creature", 
                rarity="legendary", god="ra", power=12, health=12, cost=8,
                description="Supreme sun god with radiant solar disk crown, divine falcon head, golden solar barque"
            ),
            "solar_scarab": GameCardSpec(
                card_id="ra_02", name="Solar Scarab", card_type="creature",
                rarity="common", god="ra", power=2, health=1, cost=1,
                description="Golden scarab beetle glowing with solar energy, pushing sun disk across sky"
            ),
            "solar_flare": GameCardSpec(
                card_id="ra_03", name="Solar Flare", card_type="spell",
                rarity="rare", god="ra", cost=3,
                description="Devastating solar energy beam erupting from Ra's solar disk"
            ),
            
            # ANUBIS - Death God Cards  
            "anubis_judge": GameCardSpec(
                card_id="anubis_01", name="Anubis, Judge of the Dead", card_type="creature",
                rarity="legendary", god="anubis", power=8, health=10, cost=7,
                description="Jackal-headed god of mummification, holding scales of justice, purple underworld energy"
            ),
            "mummy_guardian": GameCardSpec(
                card_id="anubis_02", name="Mummy Guardian", card_type="creature",
                rarity="epic", god="anubis", power=6, health=8, cost=5,
                description="Ancient mummified warrior wrapped in mystical bandages, glowing purple eyes"
            ),
            "death_ritual": GameCardSpec(
                card_id="anubis_03", name="Death Ritual", card_type="spell",
                rarity="rare", god="anubis", cost=4,
                description="Dark mummification magic swirling with purple underworld energy"
            ),
            
            # ISIS - Magic Goddess Cards
            "isis_mother_goddess": GameCardSpec(
                card_id="isis_01", name="Isis, Mother Goddess", card_type="creature",
                rarity="legendary", god="isis", power=6, health=12, cost=6,
                description="Divine mother with outstretched wings, healing blue aura, ankh symbol glowing"
            ),
            "healing_light": GameCardSpec(
                card_id="isis_02", name="Healing Light", card_type="spell",
                rarity="common", god="isis", cost=2,
                description="Gentle blue healing energy radiating from Isis's outstretched hands"
            ),
            "protective_ward": GameCardSpec(
                card_id="isis_03", name="Protective Ward", card_type="spell", 
                rarity="rare", god="isis", cost=3,
                description="Magical protective barrier shimmering with maternal divine energy"
            ),
            
            # SET - Chaos God Cards
            "set_chaos_lord": GameCardSpec(
                card_id="set_01", name="Set, Lord of Chaos", card_type="creature",
                rarity="legendary", god="set", power=10, health=8, cost=7,
                description="Chaos deity with storm clouds, red lightning, desert winds swirling around"
            ),
            "chaos_storm": GameCardSpec(
                card_id="set_02", name="Chaos Storm", card_type="spell",
                rarity="epic", god="set", cost=5,
                description="Devastating storm of chaos energy with crimson lightning bolts"
            ),
            "desert_winds": GameCardSpec(
                card_id="set_03", name="Desert Winds", card_type="spell",
                rarity="common", god="set", cost=2,
                description="Swirling sand tornado carrying chaotic energy across battlefield"
            ),
            
            # THOTH - Wisdom God Cards
            "thoth_wisdom_keeper": GameCardSpec(
                card_id="thoth_01", name="Thoth, Keeper of Wisdom", card_type="creature",
                rarity="legendary", god="thoth", power=4, health=8, cost=5,
                description="Ibis-headed god with writing reed, floating papyrus scrolls, glowing hieroglyphs"
            ),
            "ancient_knowledge": GameCardSpec(
                card_id="thoth_02", name="Ancient Knowledge", card_type="spell",
                rarity="rare", god="thoth", cost=3,
                description="Floating hieroglyphic symbols revealing ancient wisdom and power"
            ),
            
            # HORUS - Sky God Cards
            "horus_sky_lord": GameCardSpec(
                card_id="horus_01", name="Horus, Lord of the Sky", card_type="creature",
                rarity="legendary", god="horus", power=8, health=6, cost=6,
                description="Falcon-headed god with royal regalia, eye of horus glowing, sky blue radiance"
            ),
            "falcon_strike": GameCardSpec(
                card_id="horus_02", name="Falcon Strike", card_type="spell",
                rarity="common", god="horus", cost=2,
                description="Divine falcon diving with sky blue energy trailing behind"
            ),
            
            # ARTIFACTS
            "ankh_of_eternity": GameCardSpec(
                card_id="artifact_01", name="Ankh of Eternity", card_type="artifact",
                rarity="legendary", god="isis", cost=4,
                description="Golden ankh symbol pulsing with eternal life energy, blue healing aura"
            ),
            "scarab_amulet": GameCardSpec(
                card_id="artifact_02", name="Scarab Amulet", card_type="artifact",
                rarity="epic", god="ra", cost=3,
                description="Golden scarab beetle amulet with solar energy gems, protective glow"
            ),
            "canopic_jar": GameCardSpec(
                card_id="artifact_03", name="Canopic Jar", card_type="artifact",
                rarity="rare", god="anubis", cost=2,
                description="Mystical canopic jar containing preserved organs, purple underworld energy"
            )
        }
    
    async def generate_card_animation(self, card_id: str, priority: AnimationPriority = AnimationPriority.NORMAL) -> Optional[str]:
        """Generate animation for a specific card."""
        if not self.is_initialized:
            self.logger.error("Animation generator not initialized")
            return None
        
        card_spec = self.egyptian_cards.get(card_id)
        if not card_spec:
            self.logger.error(f"Card specification not found: {card_id}")
            return None
        
        self.logger.info(f"Generating animation for card: {card_spec.name}")
        
        # Convert to animation spec
        anim_spec = CardAnimationSpec(
            card_name=card_spec.name,
            card_type=card_spec.card_type,
            rarity=card_spec.rarity,
            god_association=card_spec.god,
            base_description=card_spec.description,
            priority=priority.value
        )
        
        try:
            # Generate single card animation
            animation_path = await animation_pipeline.generate_single_card_animation(anim_spec)
            
            if animation_path:
                self.completed_cards[card_id] = animation_path
                self.logger.info(f"Animation completed for {card_spec.name}: {animation_path}")
                
                # Execute completion callbacks
                for callback in self.completion_callbacks:
                    try:
                        callback(card_id, animation_path)
                    except Exception as e:
                        self.logger.error(f"Completion callback error: {e}")
                
                return animation_path
            else:
                self.logger.error(f"Animation generation failed for {card_spec.name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Animation generation error for {card_id}: {e}")
            return None
    
    async def generate_god_collection(self, god: str, priority: AnimationPriority = AnimationPriority.NORMAL) -> Dict[str, str]:
        """Generate animations for all cards associated with a specific god."""
        if not self.is_initialized:
            self.logger.error("Animation generator not initialized")
            return {}
        
        # Find all cards for this god
        god_cards = [
            card for card in self.egyptian_cards.values() 
            if card.god.lower() == god.lower()
        ]
        
        if not god_cards:
            self.logger.error(f"No cards found for god: {god}")
            return {}
        
        self.logger.info(f"Generating {len(god_cards)} animations for {god}")
        
        # Create batch request
        animation_specs = []
        for card in god_cards:
            spec = CardAnimationSpec(
                card_name=card.name,
                card_type=card.card_type,
                rarity=card.rarity,
                god_association=card.god,
                base_description=card.description,
                priority=priority.value
            )
            animation_specs.append(spec)
        
        batch_request = BatchGenerationRequest(
            batch_name=f"{god}_collection",
            cards=animation_specs,
            concurrent_limit=2,
            callback=self._batch_completion_callback
        )
        
        try:
            # Generate batch
            completed_animations = await animation_pipeline.generate_batch_animations(batch_request)
            
            # Update completed cards tracking
            for card in god_cards:
                if card.name in completed_animations:
                    self.completed_cards[card.card_id] = completed_animations[card.name]
            
            self.logger.info(f"God collection generation completed for {god}: {len(completed_animations)} animations")
            return completed_animations
            
        except Exception as e:
            self.logger.error(f"God collection generation error for {god}: {e}")
            return {}
    
    async def generate_all_cards(self, priority: AnimationPriority = AnimationPriority.LOW) -> Dict[str, str]:
        """Generate animations for all cards in the database."""
        if not self.is_initialized:
            self.logger.error("Animation generator not initialized") 
            return {}
        
        self.logger.info(f"Generating animations for all {len(self.egyptian_cards)} cards")
        self.generation_active = True
        
        try:
            # Create batch for all cards
            animation_specs = []
            for card in self.egyptian_cards.values():
                spec = CardAnimationSpec(
                    card_name=card.name,
                    card_type=card.card_type,
                    rarity=card.rarity,
                    god_association=card.god,
                    base_description=card.description,
                    priority=priority.value
                )
                animation_specs.append(spec)
            
            batch_request = BatchGenerationRequest(
                batch_name="complete_collection",
                cards=animation_specs,
                concurrent_limit=2,
                callback=self._batch_completion_callback
            )
            
            # Generate all animations
            completed_animations = await animation_pipeline.generate_batch_animations(batch_request)
            
            # Update tracking
            for card_id, card in self.egyptian_cards.items():
                if card.name in completed_animations:
                    self.completed_cards[card_id] = completed_animations[card.name]
            
            self.generation_active = False
            self.logger.info(f"Complete collection generation finished: {len(completed_animations)} animations")
            
            return completed_animations
            
        except Exception as e:
            self.logger.error(f"Complete collection generation error: {e}")
            self.generation_active = False
            return {}
    
    def _batch_completion_callback(self, completed: Dict[str, str], failed: List[str]):
        """Handle batch generation completion."""
        self.logger.info(f"Batch completed: {len(completed)} success, {len(failed)} failed")
        
        if failed:
            self.logger.warning(f"Failed animations: {', '.join(failed)}")
        
        # Execute progress callbacks
        for callback in self.progress_callbacks:
            try:
                callback(len(completed), len(failed))
            except Exception as e:
                self.logger.error(f"Progress callback error: {e}")
    
    def get_card_list(self) -> List[Dict[str, Any]]:
        """Get list of all available cards for animation."""
        return [
            {
                "card_id": card_id,
                "name": card.name,
                "type": card.card_type,
                "rarity": card.rarity,
                "god": card.god,
                "description": card.description,
                "has_animation": card_id in self.completed_cards
            }
            for card_id, card in self.egyptian_cards.items()
        ]
    
    def get_generation_status(self) -> Dict[str, Any]:
        """Get current generation status."""
        pipeline_status = animation_pipeline.get_pipeline_status()
        
        total_cards = len(self.egyptian_cards)
        completed_cards = len(self.completed_cards)
        completion_percentage = (completed_cards / total_cards) * 100 if total_cards > 0 else 0
        
        return {
            "total_cards": total_cards,
            "completed_cards": completed_cards,
            "completion_percentage": completion_percentage,
            "generation_active": self.generation_active,
            "pipeline_status": pipeline_status
        }
    
    def add_progress_callback(self, callback: Callable[[int, int], None]):
        """Add progress callback (completed_count, failed_count)."""
        self.progress_callbacks.append(callback)
    
    def add_completion_callback(self, callback: Callable[[str, str], None]):
        """Add completion callback (card_id, animation_path).""" 
        self.completion_callbacks.append(callback)
    
    def get_completed_animations(self) -> Dict[str, str]:
        """Get all completed animations."""
        return self.completed_cards.copy()
    
    def has_animation(self, card_id: str) -> bool:
        """Check if card has generated animation."""
        return card_id in self.completed_cards
    
    def get_animation_path(self, card_id: str) -> Optional[str]:
        """Get animation file path for card."""
        return self.completed_cards.get(card_id)

# Global card animation generator instance
card_animation_generator = CardAnimationGenerator()