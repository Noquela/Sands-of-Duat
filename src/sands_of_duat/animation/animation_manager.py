"""
Animation Manager - Unified AI Animation Generation
Handles both local AI generation and ComfyUI integration for Egyptian card animations.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable
from enum import Enum

# Import local AI generator
try:
    from .local_ai_generator import LocalAIGenerator
    LOCAL_AI_AVAILABLE = True
except ImportError:
    LOCAL_AI_AVAILABLE = False
    LocalAIGenerator = None

# Import ComfyUI integration
try:
    from .comfyui_integration import ComfyUIManager
    COMFYUI_AVAILABLE = True
except ImportError:
    COMFYUI_AVAILABLE = False
    ComfyUIManager = None

class GenerationMode(Enum):
    """Animation generation modes."""
    LOCAL_AI = "local_ai"       # Use local Stable Diffusion + AnimateDiff
    COMFYUI = "comfyui"         # Use ComfyUI server
    PLACEHOLDER = "placeholder"  # Use placeholder animations

class AnimationManager:
    """Unified manager for all animation generation methods."""
    
    def __init__(self):
        self.logger = logging.getLogger("animation_manager")
        self.mode = GenerationMode.PLACEHOLDER
        
        # Initialize generators
        self.local_ai_generator = None
        self.comfyui_manager = None
        
        # Output directories
        self.ai_output_dir = Path("assets/animations/ai_generated")
        self.placeholder_output_dir = Path("assets/animations/generated")
        
        self.ai_output_dir.mkdir(parents=True, exist_ok=True)
        self.placeholder_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine best available mode
        self._detect_best_mode()
        
    def _detect_best_mode(self):
        """Detect the best available generation mode."""
        if LOCAL_AI_AVAILABLE:
            self.mode = GenerationMode.LOCAL_AI
            self.logger.info("🤖 Local AI generation available")
        elif COMFYUI_AVAILABLE:
            self.mode = GenerationMode.COMFYUI
            self.logger.info("🖥️ ComfyUI generation available")
        else:
            self.mode = GenerationMode.PLACEHOLDER
            self.logger.info("📎 Using placeholder animations")
    
    async def initialize(self) -> bool:
        """Initialize the animation generation system."""
        self.logger.info(f"Initializing animation manager in {self.mode.value} mode")
        
        if self.mode == GenerationMode.LOCAL_AI and LOCAL_AI_AVAILABLE:
            self.local_ai_generator = LocalAIGenerator()
            success = await self.local_ai_generator.initialize()
            if success:
                self.logger.info("✅ Local AI generator initialized")
                return True
            else:
                self.logger.warning("❌ Local AI initialization failed, falling back to placeholder")
                self.mode = GenerationMode.PLACEHOLDER
                
        elif self.mode == GenerationMode.COMFYUI and COMFYUI_AVAILABLE:
            self.comfyui_manager = ComfyUIManager()
            success = await self.comfyui_manager.initialize()
            if success:
                self.logger.info("✅ ComfyUI manager initialized")
                return True
            else:
                self.logger.warning("❌ ComfyUI initialization failed, falling back to placeholder")
                self.mode = GenerationMode.PLACEHOLDER
        
        # Placeholder mode always "succeeds"
        self.logger.info("📎 Using placeholder animation mode")
        return True
    
    async def generate_card_animation(self, card_name: str, force_regenerate: bool = False) -> Optional[str]:
        """Generate animation for a specific card."""
        output_path = None
        
        if self.mode == GenerationMode.LOCAL_AI and self.local_ai_generator:
            output_path = self.ai_output_dir / f"{card_name}_animated.gif"
            
            # Check if already exists
            if output_path.exists() and not force_regenerate:
                self.logger.info(f"Using existing animation: {card_name}")
                return str(output_path)
            
            self.logger.info(f"🎨 Generating AI animation for {card_name}")
            success = await self.local_ai_generator.generate_animated_card(card_name, str(output_path))
            
            if success:
                self.logger.info(f"✅ Generated: {card_name}")
                return str(output_path)
            else:
                self.logger.error(f"❌ Failed to generate: {card_name}")
                
        elif self.mode == GenerationMode.COMFYUI and self.comfyui_manager:
            # TODO: Implement ComfyUI generation
            self.logger.info(f"ComfyUI generation not yet implemented for {card_name}")
            
        # Fallback to placeholder
        placeholder_path = self.placeholder_output_dir / f"{card_name}.gif"
        if placeholder_path.exists():
            self.logger.info(f"📎 Using placeholder animation: {card_name}")
            return str(placeholder_path)
        
        return None
    
    async def generate_all_cards(self, card_names: Optional[List[str]] = None) -> Dict[str, Optional[str]]:
        """Generate animations for all cards or specified list."""
        if not await self.initialize():
            self.logger.error("Failed to initialize animation manager")
            return {}
        
        # Default card names if none provided
        if card_names is None:
            card_names = [
                "ra_solar_deity",
                "anubis_judge_of_the_dead", 
                "isis_mother_goddess",
                "set_chaos_lord",
                "thoth_wisdom_keeper",
                "horus_sky_god"
            ]
        
        results = {}
        
        if self.mode == GenerationMode.LOCAL_AI and self.local_ai_generator:
            self.logger.info(f"🎨 Generating {len(card_names)} AI animations...")
            
            # Generate all animations
            ai_results = await self.local_ai_generator.generate_all_cards(animated=True)
            
            for card_name in card_names:
                if card_name in ai_results and ai_results[card_name]:
                    output_path = self.ai_output_dir / f"{card_name}_animated.gif"
                    results[card_name] = str(output_path)
                else:
                    results[card_name] = None
                    
        else:
            # Generate individual cards for other modes
            for card_name in card_names:
                result = await self.generate_card_animation(card_name)
                results[card_name] = result
        
        successful = sum(1 for r in results.values() if r is not None)
        self.logger.info(f"Generation complete: {successful}/{len(card_names)} animations ready")
        
        return results
    
    def get_card_animation_path(self, card_name: str) -> Optional[str]:
        """Get the path to a card's animation if it exists."""
        # Check AI generated first
        ai_path = self.ai_output_dir / f"{card_name}_animated.gif"
        if ai_path.exists():
            return str(ai_path)
        
        # Check placeholder
        placeholder_path = self.placeholder_output_dir / f"{card_name}.gif"
        if placeholder_path.exists():
            return str(placeholder_path)
        
        return None
    
    def list_available_animations(self) -> Dict[str, str]:
        """List all available card animations."""
        animations = {}
        
        # Check AI generated animations
        if self.ai_output_dir.exists():
            for gif_file in self.ai_output_dir.glob("*_animated.gif"):
                card_name = gif_file.stem.replace("_animated", "")
                animations[card_name] = str(gif_file)
        
        # Check placeholder animations  
        if self.placeholder_output_dir.exists():
            for gif_file in self.placeholder_output_dir.glob("*.gif"):
                card_name = gif_file.stem
                if card_name not in animations:  # Don't overwrite AI animations
                    animations[card_name] = str(gif_file)
        
        return animations
    
    def get_generation_status(self) -> Dict[str, any]:
        """Get status information about the animation system."""
        return {
            "mode": self.mode.value,
            "local_ai_available": LOCAL_AI_AVAILABLE,
            "comfyui_available": COMFYUI_AVAILABLE,
            "available_animations": len(self.list_available_animations()),
            "ai_output_dir": str(self.ai_output_dir),
            "placeholder_output_dir": str(self.placeholder_output_dir)
        }
    
    def cleanup(self):
        """Cleanup resources."""
        if self.local_ai_generator:
            self.local_ai_generator.cleanup_models()
        
        self.logger.info("Animation manager cleaned up")

# Global animation manager instance
animation_manager = AnimationManager()