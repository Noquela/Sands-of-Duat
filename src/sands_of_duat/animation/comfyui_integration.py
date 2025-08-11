"""
ComfyUI Integration Manager - Professional Animation Generation Pipeline
Handles communication with ComfyUI for Egyptian card animation generation.
"""

import asyncio
import aiohttp
import json
import os
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
from datetime import datetime

@dataclass
class AnimationRequest:
    """Request structure for animation generation."""
    card_name: str
    card_type: str  # "creature", "spell", "artifact"
    rarity: str     # "common", "rare", "epic", "legendary"
    god_association: str  # "ra", "anubis", "isis", "set", etc.
    style_prompt: str
    negative_prompt: str = ""
    width: int = 512
    height: int = 768
    frames: int = 16
    fps: int = 8
    motion_strength: float = 1.0
    seed: int = -1
    batch_id: str = ""
    priority: int = 1  # 1=low, 2=normal, 3=high, 4=urgent
    callback: Optional[Callable] = None

class RequestStatus(Enum):
    """Animation request status."""
    QUEUED = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

class ComfyUIManager:
    """
    Professional ComfyUI integration for automated Egyptian card animation generation.
    Handles queue management, RTX 5070 optimization, and batch processing.
    """
    
    def __init__(self, comfyui_url: str = "http://127.0.0.1:8188"):
        """Initialize ComfyUI manager."""
        self.comfyui_url = comfyui_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger("comfyui_manager")
        
        # Request management
        self.request_queue: List[AnimationRequest] = []
        self.active_requests: Dict[str, AnimationRequest] = {}
        self.completed_requests: Dict[str, Dict] = {}
        
        # Status tracking
        self.is_connected = False
        self.is_processing = False
        self.server_info = {}
        
        # Configuration
        self.max_concurrent_requests = 2  # RTX 5070 optimal
        self.request_timeout = 300  # 5 minutes
        self.retry_attempts = 3
        
        # Egyptian card animation templates
        self.animation_templates = self._load_animation_templates()
        
        self.logger.info("ComfyUI Manager initialized for Egyptian card generation")
    
    async def initialize(self) -> bool:
        """Initialize connection to ComfyUI."""
        try:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.request_timeout)
            )
            
            # Test connection
            async with self.session.get(f"{self.comfyui_url}/system_stats") as response:
                if response.status == 200:
                    self.server_info = await response.json()
                    self.is_connected = True
                    self.logger.info(f"Connected to ComfyUI at {self.comfyui_url}")
                    return True
                    
        except Exception as e:
            self.logger.error(f"Failed to connect to ComfyUI: {e}")
            self.is_connected = False
            
        return False
    
    async def shutdown(self):
        """Clean shutdown of ComfyUI manager."""
        if self.session:
            await self.session.close()
        self.is_connected = False
        self.logger.info("ComfyUI Manager shut down")
    
    def _load_animation_templates(self) -> Dict[str, Dict]:
        """Load Egyptian card animation templates."""
        return {
            "creature_basic": {
                "workflow": "egyptian_creature_animate.json",
                "base_prompt": "ancient egyptian {god} creature, mystical aura, golden light, desert sands, hieroglyphic symbols floating, magical energy swirling",
                "motion_modules": ["gentle_sway", "particle_float", "aura_pulse"],
                "duration": 2.0
            },
            "creature_legendary": {
                "workflow": "egyptian_legendary_animate.json", 
                "base_prompt": "divine ancient egyptian {god} deity, radiant golden aura, cosmic energy, sacred geometry, hieroglyphs glowing, celestial particles",
                "motion_modules": ["divine_presence", "energy_emanation", "cosmic_swirl"],
                "duration": 3.0
            },
            "spell_effect": {
                "workflow": "egyptian_spell_animate.json",
                "base_prompt": "ancient egyptian magic spell, mystical energy waves, golden hieroglyphic runes, magical circles, sand tornado, divine power",
                "motion_modules": ["energy_waves", "rune_rotation", "sand_swirl"],
                "duration": 1.5
            },
            "artifact_power": {
                "workflow": "egyptian_artifact_animate.json",
                "base_prompt": "ancient egyptian artifact, golden scarab, mystical gems glowing, divine energy radiating, sand particles swirling around",
                "motion_modules": ["gem_pulse", "energy_radiate", "particle_orbit"],
                "duration": 2.5
            }
        }
    
    async def queue_animation_request(self, request: AnimationRequest) -> str:
        """Queue an animation generation request."""
        if not self.is_connected:
            self.logger.error("ComfyUI not connected - cannot queue request")
            return ""
        
        # Generate unique request ID
        request_id = f"anim_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.request_queue)}"
        request.batch_id = request_id
        
        # Enhance prompt with Egyptian theming
        enhanced_request = self._enhance_request_with_templates(request)
        
        # Add to queue with priority sorting
        self.request_queue.append(enhanced_request)
        self.request_queue.sort(key=lambda x: x.priority, reverse=True)
        
        self.logger.info(f"Queued animation request: {request_id} ({request.card_name})")
        
        # Start processing if not already running
        if not self.is_processing:
            asyncio.create_task(self._process_queue())
            
        return request_id
    
    def _enhance_request_with_templates(self, request: AnimationRequest) -> AnimationRequest:
        """Enhance request with Egyptian animation templates."""
        # Determine template based on card type and rarity
        if request.rarity.lower() == "legendary" and request.card_type == "creature":
            template_key = "creature_legendary"
        elif request.card_type == "creature":
            template_key = "creature_basic"
        elif request.card_type == "spell":
            template_key = "spell_effect"
        else:
            template_key = "artifact_power"
        
        template = self.animation_templates.get(template_key, self.animation_templates["creature_basic"])
        
        # Enhance prompt with template
        enhanced_prompt = template["base_prompt"].format(god=request.god_association.lower())
        request.style_prompt = f"{enhanced_prompt}, {request.style_prompt}"
        
        # Set optimal parameters for RTX 5070
        request.frames = 16 if request.rarity.lower() != "legendary" else 24
        request.fps = 8
        
        return request
    
    async def _process_queue(self):
        """Process animation generation queue."""
        self.is_processing = True
        
        while self.request_queue and len(self.active_requests) < self.max_concurrent_requests:
            request = self.request_queue.pop(0)
            
            # Start processing request
            task = asyncio.create_task(self._process_single_request(request))
            self.active_requests[request.batch_id] = request
            
        # Check if we're done processing
        if not self.request_queue and not self.active_requests:
            self.is_processing = False
            self.logger.info("Animation queue processing complete")
    
    async def _process_single_request(self, request: AnimationRequest):
        """Process a single animation request."""
        try:
            self.logger.info(f"Processing animation: {request.batch_id} ({request.card_name})")
            
            # Build ComfyUI workflow
            workflow = self._build_animatediff_workflow(request)
            
            # Submit to ComfyUI
            result = await self._submit_workflow(workflow)
            
            if result and "images" in result:
                # Save generated animation
                animation_path = await self._save_animation(request, result["images"])
                
                # Mark as completed
                self.completed_requests[request.batch_id] = {
                    "status": RequestStatus.COMPLETED,
                    "animation_path": animation_path,
                    "metadata": {
                        "card_name": request.card_name,
                        "frames": request.frames,
                        "duration": request.frames / request.fps,
                        "generated_at": datetime.now().isoformat()
                    }
                }
                
                # Execute callback if provided
                if request.callback:
                    request.callback(request.batch_id, animation_path)
                
                self.logger.info(f"Animation completed: {request.batch_id}")
                
            else:
                raise Exception("Failed to generate animation")
                
        except Exception as e:
            self.logger.error(f"Animation generation failed for {request.batch_id}: {e}")
            self.completed_requests[request.batch_id] = {
                "status": RequestStatus.FAILED,
                "error": str(e)
            }
        finally:
            # Remove from active requests
            self.active_requests.pop(request.batch_id, None)
            
            # Continue processing queue
            if self.request_queue:
                asyncio.create_task(self._process_queue())
    
    def _build_animatediff_workflow(self, request: AnimationRequest) -> Dict[str, Any]:
        """Build ComfyUI AnimateDiff workflow for Egyptian card animation."""
        workflow = {
            "1": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "revAnimated_v122.safetensors"  # Good for fantasy/mystical content
                }
            },
            "2": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": request.style_prompt,
                    "clip": ["1", 1]
                }
            },
            "3": {
                "class_type": "CLIPTextEncode", 
                "inputs": {
                    "text": f"{request.negative_prompt}, blurry, low quality, distorted, bad anatomy, watermark",
                    "clip": ["1", 1]
                }
            },
            "4": {
                "class_type": "AnimateDiffLoader",
                "inputs": {
                    "model_name": "mm_sd_v15_v2.ckpt",  # AnimateDiff motion module
                    "beta_schedule": "sqrt_linear"
                }
            },
            "5": {
                "class_type": "AnimateDiffSampler",
                "inputs": {
                    "model": ["1", 0],
                    "motion_module": ["4", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "seed": request.seed if request.seed > 0 else -1,
                    "steps": 20,
                    "cfg": 8.0,
                    "sampler_name": "euler_ancestral",
                    "scheduler": "normal",
                    "width": request.width,
                    "height": request.height,
                    "length": request.frames,
                    "motion_scale": request.motion_strength
                }
            },
            "6": {
                "class_type": "VHS_VideoCombine",
                "inputs": {
                    "images": ["5", 0],
                    "frame_rate": request.fps,
                    "loop_count": 0,
                    "filename_prefix": f"egyptian_card_{request.card_name}",
                    "format": "image/gif",
                    "pingpong": False,
                    "save_output": True
                }
            }
        }
        
        return workflow
    
    async def _submit_workflow(self, workflow: Dict[str, Any]) -> Optional[Dict]:
        """Submit workflow to ComfyUI and wait for completion."""
        try:
            # Submit workflow
            async with self.session.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow}
            ) as response:
                if response.status != 200:
                    return None
                    
                result = await response.json()
                prompt_id = result.get("prompt_id")
                
                if not prompt_id:
                    return None
            
            # Poll for completion
            return await self._wait_for_completion(prompt_id)
            
        except Exception as e:
            self.logger.error(f"Failed to submit workflow: {e}")
            return None
    
    async def _wait_for_completion(self, prompt_id: str) -> Optional[Dict]:
        """Wait for workflow completion and retrieve results."""
        max_attempts = 60  # 5 minute timeout
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Check queue status
                async with self.session.get(f"{self.comfyui_url}/queue") as response:
                    if response.status == 200:
                        queue_data = await response.json()
                        
                        # Check if prompt is still in queue
                        running = queue_data.get("queue_running", [])
                        pending = queue_data.get("queue_pending", [])
                        
                        prompt_in_queue = any(
                            item[1] == prompt_id for item in running + pending
                        )
                        
                        if not prompt_in_queue:
                            # Prompt completed, get results
                            return await self._get_results(prompt_id)
                
                await asyncio.sleep(5)  # Wait 5 seconds
                attempt += 1
                
            except Exception as e:
                self.logger.error(f"Error waiting for completion: {e}")
                await asyncio.sleep(5)
                attempt += 1
        
        self.logger.error(f"Timeout waiting for prompt {prompt_id}")
        return None
    
    async def _get_results(self, prompt_id: str) -> Optional[Dict]:
        """Retrieve generation results."""
        try:
            async with self.session.get(f"{self.comfyui_url}/history/{prompt_id}") as response:
                if response.status == 200:
                    history = await response.json()
                    
                    if prompt_id in history:
                        outputs = history[prompt_id].get("outputs", {})
                        return outputs
                        
        except Exception as e:
            self.logger.error(f"Failed to get results for {prompt_id}: {e}")
            
        return None
    
    async def _save_animation(self, request: AnimationRequest, images: List[Dict]) -> str:
        """Save generated animation to disk."""
        output_dir = Path("assets/animations/generated")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{request.card_name.lower().replace(' ', '_')}_anim.gif"
        output_path = output_dir / filename
        
        # For now, save the first image/animation from results
        # In a full implementation, this would handle the actual GIF data
        if images:
            image_data = images[0]
            
            # Save animation file
            with open(output_path, "wb") as f:
                if "gifs" in image_data:
                    # Save GIF data
                    gif_data = base64.b64decode(image_data["gifs"][0]["image"])
                    f.write(gif_data)
                
        self.logger.info(f"Animation saved: {output_path}")
        return str(output_path)
    
    def get_request_status(self, request_id: str) -> Optional[RequestStatus]:
        """Get status of an animation request."""
        if request_id in self.active_requests:
            return RequestStatus.PROCESSING
        elif request_id in self.completed_requests:
            status_data = self.completed_requests[request_id]
            return status_data.get("status", RequestStatus.FAILED)
        elif any(req.batch_id == request_id for req in self.request_queue):
            return RequestStatus.QUEUED
        else:
            return None
    
    def get_queue_info(self) -> Dict[str, Any]:
        """Get current queue information."""
        return {
            "queued": len(self.request_queue),
            "processing": len(self.active_requests),
            "completed": len(self.completed_requests),
            "is_connected": self.is_connected,
            "is_processing": self.is_processing
        }

# Global ComfyUI manager instance
comfyui_manager = ComfyUIManager()