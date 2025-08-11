"""
Animation Pipeline - Orchestrates Card Animation Generation
High-level pipeline for managing Egyptian card animation generation workflow.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum, auto
import json
from datetime import datetime

from .comfyui_integration import comfyui_manager, AnimationRequest, RequestStatus

class PipelineStatus(Enum):
    """Pipeline execution status."""
    IDLE = auto()
    PREPARING = auto()
    GENERATING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class CardAnimationSpec:
    """Specification for card animation generation."""
    card_name: str
    card_type: str      # "creature", "spell", "artifact"
    rarity: str         # "common", "rare", "epic", "legendary" 
    god_association: str # "ra", "anubis", "isis", "set"
    base_description: str
    animation_style: str = "mystical"
    priority: int = 2   # 1=low, 2=normal, 3=high, 4=urgent

@dataclass
class BatchGenerationRequest:
    """Request for batch animation generation."""
    batch_name: str
    cards: List[CardAnimationSpec]
    output_directory: str = "assets/animations/generated"
    concurrent_limit: int = 2
    callback: Optional[Callable] = None

class AnimationPipeline:
    """
    High-level animation generation pipeline for Egyptian cards.
    Orchestrates ComfyUI integration with game-specific requirements.
    """
    
    def __init__(self):
        """Initialize animation pipeline."""
        self.logger = logging.getLogger("animation_pipeline")
        self.status = PipelineStatus.IDLE
        
        # Pipeline state
        self.current_batch: Optional[BatchGenerationRequest] = None
        self.active_requests: Dict[str, AnimationRequest] = {}
        self.completed_animations: Dict[str, str] = {}  # card_name -> file_path
        self.failed_animations: List[str] = []
        
        # Egyptian theming templates
        self.god_associations = {
            "ra": {
                "colors": ["golden", "solar", "radiant"],
                "elements": ["sun disk", "solar rays", "golden scarabs", "solar barque"],
                "atmosphere": "divine solar radiance, golden light beams"
            },
            "anubis": {
                "colors": ["obsidian black", "royal gold", "deep purple"],
                "elements": ["jackal head", "scales of justice", "mummification wraps", "canopic jars"],
                "atmosphere": "mystical underworld energy, purple shadows"
            },
            "isis": {
                "colors": ["deep blue", "silver", "star white"],
                "elements": ["wings spread", "ankh symbol", "healing light", "protective aura"],
                "atmosphere": "maternal divine energy, healing blue light"
            },
            "set": {
                "colors": ["crimson red", "storm gray", "desert orange"],
                "elements": ["storm clouds", "lightning", "chaos energy", "desert winds"],
                "atmosphere": "chaotic storm energy, red lightning"
            },
            "thoth": {
                "colors": ["wisdom blue", "silver", "scroll white"],
                "elements": ["ibis head", "writing reed", "papyrus scrolls", "hieroglyphs"],
                "atmosphere": "intellectual divine light, floating knowledge"
            },
            "horus": {
                "colors": ["sky blue", "royal gold", "falcon brown"],
                "elements": ["falcon wings", "eye of horus", "sky realm", "royal regalia"],
                "atmosphere": "royal divine presence, sky blue radiance"
            }
        }
        
        self.logger.info("Animation Pipeline initialized")
    
    async def initialize(self) -> bool:
        """Initialize pipeline with ComfyUI connection."""
        try:
            success = await comfyui_manager.initialize()
            if success:
                self.logger.info("Animation Pipeline connected to ComfyUI")
                return True
            else:
                self.logger.error("Failed to connect Animation Pipeline to ComfyUI")
                return False
                
        except Exception as e:
            self.logger.error(f"Animation Pipeline initialization failed: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown pipeline."""
        await comfyui_manager.shutdown()
        self.logger.info("Animation Pipeline shut down")
    
    async def generate_single_card_animation(self, spec: CardAnimationSpec) -> Optional[str]:
        """Generate animation for a single card."""
        self.logger.info(f"Generating animation for: {spec.card_name}")
        
        try:
            # Build animation request
            request = self._build_animation_request(spec)
            
            # Queue for generation
            request_id = await comfyui_manager.queue_animation_request(request)
            
            if not request_id:
                self.logger.error(f"Failed to queue animation for {spec.card_name}")
                return None
            
            # Wait for completion
            return await self._wait_for_single_completion(request_id, spec.card_name)
            
        except Exception as e:
            self.logger.error(f"Single card animation generation failed: {e}")
            return None
    
    async def generate_batch_animations(self, batch_request: BatchGenerationRequest) -> Dict[str, str]:
        """Generate animations for a batch of cards."""
        self.status = PipelineStatus.PREPARING
        self.current_batch = batch_request
        
        self.logger.info(f"Starting batch generation: {batch_request.batch_name} ({len(batch_request.cards)} cards)")
        
        try:
            # Prepare all requests
            animation_requests = []
            for spec in batch_request.cards:
                request = self._build_animation_request(spec)
                animation_requests.append((spec, request))
            
            self.status = PipelineStatus.GENERATING
            
            # Submit requests with concurrency limit
            semaphore = asyncio.Semaphore(batch_request.concurrent_limit)
            tasks = []
            
            for spec, request in animation_requests:
                task = asyncio.create_task(
                    self._generate_with_semaphore(semaphore, spec, request)
                )
                tasks.append(task)
            
            # Wait for all to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            completed_animations = {}
            for i, result in enumerate(results):
                spec = batch_request.cards[i]
                if isinstance(result, str) and result:
                    completed_animations[spec.card_name] = result
                    self.completed_animations[spec.card_name] = result
                else:
                    self.failed_animations.append(spec.card_name)
            
            self.status = PipelineStatus.COMPLETED if completed_animations else PipelineStatus.FAILED
            
            # Execute callback
            if batch_request.callback:
                batch_request.callback(completed_animations, self.failed_animations)
            
            self.logger.info(f"Batch generation completed: {len(completed_animations)} success, {len(self.failed_animations)} failed")
            
            return completed_animations
            
        except Exception as e:
            self.logger.error(f"Batch generation failed: {e}")
            self.status = PipelineStatus.FAILED
            return {}
    
    async def _generate_with_semaphore(self, semaphore: asyncio.Semaphore, 
                                     spec: CardAnimationSpec, request: AnimationRequest) -> Optional[str]:
        """Generate animation with concurrency control."""
        async with semaphore:
            request_id = await comfyui_manager.queue_animation_request(request)
            if request_id:
                return await self._wait_for_single_completion(request_id, spec.card_name)
            return None
    
    def _build_animation_request(self, spec: CardAnimationSpec) -> AnimationRequest:
        """Build ComfyUI animation request from card specification."""
        # Get god theming
        god_theme = self.god_associations.get(spec.god_association.lower(), self.god_associations["ra"])
        
        # Build enhanced prompt
        style_prompt = self._build_enhanced_prompt(spec, god_theme)
        
        # Set optimal parameters based on rarity
        width, height = self._get_optimal_dimensions(spec.rarity)
        frames = self._get_optimal_frames(spec.rarity)
        motion_strength = self._get_motion_strength(spec.card_type, spec.rarity)
        
        return AnimationRequest(
            card_name=spec.card_name,
            card_type=spec.card_type,
            rarity=spec.rarity,
            god_association=spec.god_association,
            style_prompt=style_prompt,
            negative_prompt=self._build_negative_prompt(),
            width=width,
            height=height,
            frames=frames,
            fps=8,
            motion_strength=motion_strength,
            priority=spec.priority
        )
    
    def _build_enhanced_prompt(self, spec: CardAnimationSpec, god_theme: Dict) -> str:
        """Build enhanced prompt with Egyptian theming."""
        base_elements = [
            f"ancient egyptian {spec.card_type}",
            spec.base_description,
            f"associated with {spec.god_association}",
            god_theme["atmosphere"]
        ]
        
        # Add rarity-based enhancements
        if spec.rarity.lower() == "legendary":
            base_elements.extend([
                "divine cosmic energy",
                "celestial radiance", 
                "godlike presence",
                "sacred geometry patterns"
            ])
        elif spec.rarity.lower() == "epic":
            base_elements.extend([
                "powerful magical aura",
                "intense mystical energy",
                "glowing hieroglyphic symbols"
            ])
        else:
            base_elements.extend([
                "mystical energy",
                "ancient magic",
                "desert atmosphere"
            ])
        
        # Add god-specific elements
        base_elements.extend(god_theme["elements"][:2])  # First 2 elements
        
        # Add visual quality terms
        quality_terms = [
            "masterpiece",
            "best quality", 
            "highly detailed",
            "cinematic lighting",
            "egyptian art style",
            "golden ratio composition",
            "mystical atmosphere"
        ]
        
        return ", ".join(base_elements + quality_terms)
    
    def _build_negative_prompt(self) -> str:
        """Build comprehensive negative prompt."""
        return ", ".join([
            "blurry", "low quality", "distorted", "bad anatomy",
            "deformed", "ugly", "bad proportions", "extra limbs",
            "watermark", "signature", "text", "modern objects",
            "contemporary clothing", "cars", "phones", "computers"
        ])
    
    def _get_optimal_dimensions(self, rarity: str) -> tuple:
        """Get optimal dimensions based on rarity."""
        if rarity.lower() == "legendary":
            return (768, 1024)  # Higher resolution for legendary
        elif rarity.lower() == "epic":
            return (640, 896)
        else:
            return (512, 768)   # Standard resolution
    
    def _get_optimal_frames(self, rarity: str) -> int:
        """Get optimal frame count based on rarity."""
        if rarity.lower() == "legendary":
            return 32  # Longer animation for legendary
        elif rarity.lower() == "epic":
            return 24
        else:
            return 16  # Standard length
    
    def _get_motion_strength(self, card_type: str, rarity: str) -> float:
        """Get optimal motion strength based on card type and rarity."""
        base_strength = {
            "creature": 1.0,
            "spell": 1.3,    # More dynamic motion for spells
            "artifact": 0.8   # Subtle motion for artifacts
        }.get(card_type.lower(), 1.0)
        
        # Adjust for rarity
        if rarity.lower() == "legendary":
            base_strength *= 1.2
        elif rarity.lower() == "epic":
            base_strength *= 1.1
            
        return min(base_strength, 2.0)  # Cap at 2.0
    
    async def _wait_for_single_completion(self, request_id: str, card_name: str) -> Optional[str]:
        """Wait for single animation completion."""
        max_wait = 300  # 5 minutes
        wait_time = 0
        
        while wait_time < max_wait:
            status = comfyui_manager.get_request_status(request_id)
            
            if status == RequestStatus.COMPLETED:
                if request_id in comfyui_manager.completed_requests:
                    result = comfyui_manager.completed_requests[request_id]
                    animation_path = result.get("animation_path")
                    if animation_path:
                        self.logger.info(f"Animation completed for {card_name}: {animation_path}")
                        return animation_path
                    
            elif status == RequestStatus.FAILED:
                self.logger.error(f"Animation failed for {card_name}")
                return None
                
            await asyncio.sleep(5)
            wait_time += 5
        
        self.logger.error(f"Animation timeout for {card_name}")
        return None
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        queue_info = comfyui_manager.get_queue_info()
        
        return {
            "pipeline_status": self.status.name,
            "current_batch": self.current_batch.batch_name if self.current_batch else None,
            "completed_animations": len(self.completed_animations),
            "failed_animations": len(self.failed_animations),
            "comfyui_queue": queue_info
        }
    
    def save_batch_report(self, output_path: str):
        """Save batch generation report."""
        report = {
            "batch_name": self.current_batch.batch_name if self.current_batch else "Unknown",
            "timestamp": datetime.now().isoformat(),
            "status": self.status.name,
            "completed_animations": self.completed_animations,
            "failed_animations": self.failed_animations,
            "pipeline_status": self.get_pipeline_status()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Batch report saved: {output_path}")

# Global animation pipeline instance
animation_pipeline = AnimationPipeline()