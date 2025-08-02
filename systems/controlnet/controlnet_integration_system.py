#!/usr/bin/env python3
"""
ControlNet Integration System - Advanced pose and depth control for Hades-Egyptian assets
Implements specialized ControlNet models for precise character and environment generation
"""

import torch
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image
import asyncio
import time

class ControlNetIntegrationSystem:
    """Advanced ControlNet integration for Hades-Egyptian asset generation"""
    
    def __init__(self, device="cuda"):
        self.device = device
        self.controlnet_models = {}
        self.preprocessors = {}
        self.pose_detection_models = {}
        
        # ControlNet configurations for different asset types
        self.controlnet_configs = {
            "character_pose": {
                "model": "diffusers/controlnet-openpose-sdxl-1.0",
                "strength": 0.8,
                "guidance_scale": 7.5,
                "description": "Human pose control for character generation"
            },
            "depth_control": {
                "model": "diffusers/controlnet-depth-sdxl-1.0", 
                "strength": 0.7,
                "guidance_scale": 8.0,
                "description": "Depth map control for 3D understanding"
            },
            "lineart_control": {
                "model": "diffusers/controlnet-canny-sdxl-1.0",
                "strength": 0.6,
                "guidance_scale": 7.0,
                "description": "Edge and line art control"
            },
            "egyptian_pose": {
                "model": "custom/egyptian-pose-controlnet",
                "strength": 0.9,
                "guidance_scale": 8.5,
                "description": "Egyptian mythology specific poses"
            }
        }
        
        # Egyptian character pose templates
        self.egyptian_poses = {
            "anubis_guardian": {
                "pose_type": "standing_guard",
                "key_points": {
                    "head": "jackal_head_profile",
                    "arms": "ceremonial_cross_chest",
                    "stance": "wide_authoritative",
                    "weapon": "staff_vertical"
                },
                "template_path": "assets/pose_templates/anubis_guardian.json"
            },
            "ra_divine": {
                "pose_type": "divine_blessing",
                "key_points": {
                    "head": "solar_crown_front",
                    "arms": "raised_blessing",
                    "stance": "centered_divine",
                    "aura": "solar_energy"
                },
                "template_path": "assets/pose_templates/ra_divine.json"
            },
            "thoth_wisdom": {
                "pose_type": "scribe_scholarly",
                "key_points": {
                    "head": "ibis_contemplative",
                    "arms": "scroll_reading",
                    "stance": "seated_scholar",
                    "tools": "writing_implement"
                },
                "template_path": "assets/pose_templates/thoth_wisdom.json"
            },
            "isis_magic": {
                "pose_type": "magical_casting",
                "key_points": {
                    "head": "crowned_graceful",
                    "arms": "spell_casting",
                    "stance": "flowing_magical",
                    "symbols": "ankh_magic"
                },
                "template_path": "assets/pose_templates/isis_magic.json"
            }
        }
        
        print("ControlNet Integration System initialized")
        print("   Egyptian pose templates loaded")
        print("   Advanced control configurations ready")
    
    async def setup_controlnet_models(self) -> bool:
        """Setup all ControlNet models and preprocessors"""
        try:
            print("Setting up ControlNet models...")
            
            # Install dependencies
            await self._install_controlnet_dependencies()
            
            # Load ControlNet models
            await self._load_controlnet_models()
            
            # Setup preprocessors
            await self._setup_preprocessors()
            
            # Create Egyptian pose templates
            await self._create_egyptian_pose_templates()
            
            print("ControlNet models setup complete!")
            return True
            
        except Exception as e:
            print(f"ControlNet setup failed: {e}")
            return False
    
    async def _install_controlnet_dependencies(self):
        """Install ControlNet and related dependencies"""
        import subprocess
        
        dependencies = [
            "diffusers[controlnet]",
            "controlnet-aux",
            "opencv-python",
            "mediapipe",
            "transformers",
            "accelerate"
        ]
        
        print("Installing ControlNet dependencies...")
        for dep in dependencies:
            try:
                subprocess.run([
                    "pip", "install", dep, "--quiet"
                ], check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to install {dep}, continuing...")
    
    async def _load_controlnet_models(self):
        """Load ControlNet models for different control types"""
        try:
            from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
            from diffusers import AutoencoderKL
            
            print("Loading ControlNet models...")
            
            # Load fixed VAE
            vae = AutoencoderKL.from_pretrained(
                "madebyollin/sdxl-vae-fp16-fix",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            # Load pose ControlNet
            pose_controlnet = ControlNetModel.from_pretrained(
                "thibaud/controlnet-openpose-sdxl-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None
            )
            
            # Load depth ControlNet
            depth_controlnet = ControlNetModel.from_pretrained(
                "diffusers/controlnet-depth-sdxl-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None
            )
            
            # Create ControlNet pipelines
            pose_pipeline = StableDiffusionXLControlNetPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                controlnet=pose_controlnet,
                vae=vae,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True
            ).to(self.device)
            
            depth_pipeline = StableDiffusionXLControlNetPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                controlnet=depth_controlnet,
                vae=vae,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True
            ).to(self.device)
            
            # Enable optimizations
            if self.device == "cuda":
                pose_pipeline.enable_attention_slicing()
                depth_pipeline.enable_attention_slicing()
                pose_pipeline.enable_model_cpu_offload()
                depth_pipeline.enable_model_cpu_offload()
            
            self.controlnet_models = {
                "pose": {
                    "model": pose_controlnet,
                    "pipeline": pose_pipeline
                },
                "depth": {
                    "model": depth_controlnet,
                    "pipeline": depth_pipeline
                }
            }
            
            print("ControlNet models loaded successfully")
            
        except Exception as e:
            print(f"Failed to load ControlNet models: {e}")
            raise
    
    async def _setup_preprocessors(self):
        """Setup image preprocessors for ControlNet"""
        try:
            from controlnet_aux import (
                OpenposeDetector,
                MidasDetector,
                CannyDetector,
                LineartDetector
            )
            
            print("Setting up ControlNet preprocessors...")
            
            # OpenPose for human pose detection
            openpose = OpenposeDetector.from_pretrained("lllyasviel/Annotators")
            
            # Midas for depth estimation
            midas = MidasDetector.from_pretrained("lllyasviel/Annotators")
            
            # Canny for edge detection
            canny = CannyDetector()
            
            # Lineart for clean line art
            lineart = LineartDetector.from_pretrained("lllyasviel/Annotators")
            
            self.preprocessors = {
                "openpose": openpose,
                "midas": midas,
                "canny": canny,
                "lineart": lineart
            }
            
            print("Preprocessors setup complete")
            
        except Exception as e:
            print(f"Failed to setup preprocessors: {e}")
            # Continue without preprocessors for fallback
    
    async def _create_egyptian_pose_templates(self):
        """Create Egyptian mythology specific pose templates"""
        templates_dir = Path("assets/pose_templates")
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        for character, pose_data in self.egyptian_poses.items():
            template_path = Path(pose_data["template_path"])
            
            # Create pose template with Egyptian characteristics
            pose_template = {
                "character": character,
                "pose_type": pose_data["pose_type"],
                "keypoints": self._generate_egyptian_keypoints(pose_data),
                "style_modifiers": self._get_egyptian_style_modifiers(character),
                "anatomical_adjustments": self._get_egyptian_anatomy_adjustments(character)
            }
            
            # Save template
            import json
            with open(template_path, 'w') as f:
                json.dump(pose_template, f, indent=2)
        
        print("Egyptian pose templates created")
    
    def _generate_egyptian_keypoints(self, pose_data: Dict) -> Dict:
        """Generate keypoints for Egyptian character poses"""
        keypoints = pose_data["key_points"]
        
        # Map to OpenPose format with Egyptian characteristics
        egyptian_keypoints = {
            "nose": [0.5, 0.15],  # Head position
            "neck": [0.5, 0.25],
            "right_shoulder": [0.4, 0.3],
            "left_shoulder": [0.6, 0.3],
            "right_elbow": [0.3, 0.45],
            "left_elbow": [0.7, 0.45],
            "right_wrist": [0.25, 0.6],
            "left_wrist": [0.75, 0.6],
            "right_hip": [0.45, 0.65],
            "left_hip": [0.55, 0.65],
            "right_knee": [0.45, 0.8],
            "left_knee": [0.55, 0.8],
            "right_ankle": [0.45, 0.95],
            "left_ankle": [0.55, 0.95]
        }
        
        # Adjust based on Egyptian pose characteristics
        if "ceremonial_cross_chest" in keypoints.get("arms", ""):
            egyptian_keypoints["right_wrist"] = [0.55, 0.5]  # Crossed arms
            egyptian_keypoints["left_wrist"] = [0.45, 0.5]
        
        if "wide_authoritative" in keypoints.get("stance", ""):
            egyptian_keypoints["right_ankle"] = [0.35, 0.95]  # Wider stance
            egyptian_keypoints["left_ankle"] = [0.65, 0.95]
        
        return egyptian_keypoints
    
    def _get_egyptian_style_modifiers(self, character: str) -> List[str]:
        """Get style modifiers for Egyptian characters"""
        base_modifiers = [
            "ancient Egyptian art style",
            "hieroglyphic details",
            "golden accents",
            "divine aura"
        ]
        
        character_specific = {
            "anubis_guardian": ["jackal head", "ceremonial armor", "protective stance"],
            "ra_divine": ["solar disk crown", "divine radiance", "solar energy"],
            "thoth_wisdom": ["ibis head", "scribe tools", "wisdom aura"],
            "isis_magic": ["royal crown", "magical symbols", "flowing robes"]
        }
        
        return base_modifiers + character_specific.get(character, [])
    
    def _get_egyptian_anatomy_adjustments(self, character: str) -> Dict:
        """Get anatomical adjustments for Egyptian gods"""
        adjustments = {
            "anubis_guardian": {
                "head": "jackal_proportions",
                "ears": "pointed_upright",
                "snout": "elongated_canine"
            },
            "ra_divine": {
                "head": "human_divine",
                "crown": "solar_disk",
                "aura": "solar_energy"
            },
            "thoth_wisdom": {
                "head": "ibis_proportions",
                "beak": "curved_ibis",
                "neck": "elongated_elegant"
            },
            "isis_magic": {
                "head": "human_divine",
                "crown": "royal_elegant",
                "posture": "graceful_magical"
            }
        }
        
        return adjustments.get(character, {})
    
    async def generate_pose_controlled_asset(self, 
                                           character: str,
                                           pose_type: str,
                                           prompt: str,
                                           width: int = 1024,
                                           height: int = 1024,
                                           control_strength: float = 0.8) -> Dict[str, Any]:
        """Generate asset with precise pose control"""
        
        print(f"Generating pose-controlled {character} asset...")
        start_time = time.time()
        
        try:
            # Load Egyptian pose template
            pose_template = await self._load_egyptian_pose_template(character, pose_type)
            
            # Generate pose control image
            pose_image = await self._create_pose_control_image(pose_template, width, height)
            
            # Enhanced prompt with Egyptian characteristics
            enhanced_prompt = await self._enhance_prompt_for_egyptian_pose(
                prompt, character, pose_template
            )
            
            # Generate with pose control
            result_image = await self._generate_with_pose_control(
                enhanced_prompt, pose_image, control_strength, width, height
            )
            
            # Save with metadata
            output_path = await self._save_pose_controlled_asset(
                result_image, character, pose_type, enhanced_prompt
            )
            
            generation_time = time.time() - start_time
            
            return {
                "status": "success",
                "character": character,
                "pose_type": pose_type,
                "output_path": str(output_path),
                "generation_time": generation_time,
                "control_strength": control_strength,
                "enhanced_prompt": enhanced_prompt
            }
            
        except Exception as e:
            print(f"Pose control generation failed: {e}")
            return {
                "status": "failed",
                "character": character,
                "pose_type": pose_type,
                "error": str(e)
            }
    
    async def _load_egyptian_pose_template(self, character: str, pose_type: str) -> Dict:
        """Load Egyptian character pose template"""
        try:
            if character in self.egyptian_poses:
                template_path = Path(self.egyptian_poses[character]["template_path"])
                
                if template_path.exists():
                    import json
                    with open(template_path, 'r') as f:
                        return json.load(f)
            
            # Fallback to default pose
            return self._create_default_egyptian_pose(character)
            
        except Exception as e:
            print(f"Failed to load pose template: {e}")
            return self._create_default_egyptian_pose(character)
    
    def _create_default_egyptian_pose(self, character: str) -> Dict:
        """Create default Egyptian pose for character"""
        return {
            "character": character,
            "pose_type": "standing_divine",
            "keypoints": self._generate_egyptian_keypoints({
                "key_points": {"stance": "wide_authoritative", "arms": "ceremonial"}
            }),
            "style_modifiers": self._get_egyptian_style_modifiers(character)
        }
    
    async def _create_pose_control_image(self, pose_template: Dict, 
                                       width: int, height: int) -> Image.Image:
        """Create pose control image from template"""
        
        # Create blank canvas
        pose_canvas = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw keypoints and skeleton
        keypoints = pose_template["keypoints"]
        
        # Convert normalized coordinates to pixel coordinates
        pixel_keypoints = {}
        for joint, (x, y) in keypoints.items():
            pixel_x = int(x * width)
            pixel_y = int(y * height)
            pixel_keypoints[joint] = (pixel_x, pixel_y)
            
            # Draw keypoint
            cv2.circle(pose_canvas, (pixel_x, pixel_y), 8, (255, 255, 255), -1)
        
        # Draw skeleton connections
        skeleton_connections = [
            ("neck", "nose"),
            ("neck", "right_shoulder"),
            ("neck", "left_shoulder"),
            ("right_shoulder", "right_elbow"),
            ("right_elbow", "right_wrist"),
            ("left_shoulder", "left_elbow"),
            ("left_elbow", "left_wrist"),
            ("neck", "right_hip"),
            ("neck", "left_hip"),
            ("right_hip", "right_knee"),
            ("right_knee", "right_ankle"),
            ("left_hip", "left_knee"),
            ("left_knee", "left_ankle")
        ]
        
        for joint1, joint2 in skeleton_connections:
            if joint1 in pixel_keypoints and joint2 in pixel_keypoints:
                pt1 = pixel_keypoints[joint1]
                pt2 = pixel_keypoints[joint2]
                cv2.line(pose_canvas, pt1, pt2, (255, 255, 255), 3)
        
        return Image.fromarray(pose_canvas)
    
    async def _enhance_prompt_for_egyptian_pose(self, base_prompt: str, 
                                              character: str, 
                                              pose_template: Dict) -> str:
        """Enhance prompt with Egyptian pose characteristics"""
        
        style_modifiers = pose_template.get("style_modifiers", [])
        
        # Build enhanced prompt
        enhanced = f"masterpiece, best quality, {base_prompt}"
        enhanced += f", {', '.join(style_modifiers[:4])}"  # Limit for token count
        enhanced += ", cel-shaded art style, Hades game style, outlined illustration"
        enhanced += ", dramatic lighting, divine aura, ancient Egyptian mythology"
        
        return enhanced
    
    async def _generate_with_pose_control(self, prompt: str, pose_image: Image.Image,
                                        control_strength: float, width: int, height: int) -> Image.Image:
        """Generate image with pose control"""
        
        if "pose" not in self.controlnet_models:
            raise ValueError("Pose ControlNet model not available")
        
        pipeline = self.controlnet_models["pose"]["pipeline"]
        
        # Generate with pose control
        generator = torch.Generator(device=self.device).manual_seed(42)
        
        with torch.autocast(self.device):
            result = pipeline(
                prompt=prompt,
                image=pose_image,
                negative_prompt="blurry, low quality, deformed, bad anatomy, realistic photo",
                width=width,
                height=height,
                num_inference_steps=50,
                guidance_scale=7.5,
                controlnet_conditioning_scale=control_strength,
                generator=generator
            )
        
        return result.images[0]
    
    async def _save_pose_controlled_asset(self, image: Image.Image, character: str,
                                        pose_type: str, prompt: str) -> Path:
        """Save pose controlled asset with metadata"""
        
        output_dir = Path("assets/generated/pose_controlled")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        asset_name = f"{character}_{pose_type}_pose_controlled"
        output_path = output_dir / f"{asset_name}.png"
        
        # Save image
        image.save(output_path, optimize=True)
        
        # Save metadata
        metadata = {
            "character": character,
            "pose_type": pose_type,
            "prompt": prompt,
            "generation_time": time.time(),
            "control_type": "pose",
            "technique": "ControlNet OpenPose"
        }
        
        metadata_path = output_dir / f"{asset_name}_metadata.json"
        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    async def generate_depth_controlled_environment(self, environment_type: str,
                                                  depth_reference: Optional[Image.Image] = None,
                                                  prompt: str = "",
                                                  width: int = 1024,
                                                  height: int = 1024) -> Dict[str, Any]:
        """Generate environment with depth control"""
        
        print(f"Generating depth-controlled {environment_type} environment...")
        
        try:
            # Create or use depth reference
            if depth_reference is None:
                depth_image = await self._create_egyptian_environment_depth_map(
                    environment_type, width, height
                )
            else:
                depth_image = depth_reference
            
            # Enhanced environment prompt
            enhanced_prompt = await self._enhance_environment_prompt(
                prompt, environment_type
            )
            
            # Generate with depth control
            result_image = await self._generate_with_depth_control(
                enhanced_prompt, depth_image, width, height
            )
            
            # Save environment asset
            output_path = await self._save_environment_asset(
                result_image, environment_type, enhanced_prompt
            )
            
            return {
                "status": "success",
                "environment_type": environment_type,
                "output_path": str(output_path),
                "enhanced_prompt": enhanced_prompt
            }
            
        except Exception as e:
            print(f"Depth control generation failed: {e}")
            return {
                "status": "failed",
                "environment_type": environment_type,
                "error": str(e)
            }
    
    async def _create_egyptian_environment_depth_map(self, environment_type: str,
                                                   width: int, height: int) -> Image.Image:
        """Create depth map for Egyptian environments"""
        
        # Create depth canvas
        depth_canvas = np.zeros((height, width), dtype=np.uint8)
        
        if environment_type == "temple_interior":
            # Temple with pillars and depth layers
            # Background wall (darkest)
            depth_canvas[:, :] = 50
            
            # Middle pillars
            pillar_width = width // 8
            for i in range(3):
                x_start = (i + 1) * width // 4 - pillar_width // 2
                x_end = x_start + pillar_width
                depth_canvas[:, x_start:x_end] = 150
            
            # Foreground floor (brightest)
            floor_start = int(height * 0.7)
            depth_canvas[floor_start:, :] = 255
            
        elif environment_type == "pyramid_chamber":
            # Pyramid interior with central focus
            center_x, center_y = width // 2, height // 2
            
            # Create radial depth
            y, x = np.ogrid[:height, :width]
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            max_distance = np.sqrt(center_x**2 + center_y**2)
            depth_canvas = (255 * (1 - distance / max_distance)).astype(np.uint8)
            
        else:
            # Default temple layout
            depth_canvas[:, :] = 128  # Mid-depth base
        
        # Apply Gaussian blur for smooth transitions
        depth_canvas = cv2.GaussianBlur(depth_canvas, (21, 21), 0)
        
        # Convert to RGB
        depth_rgb = cv2.cvtColor(depth_canvas, cv2.COLOR_GRAY2RGB)
        
        return Image.fromarray(depth_rgb)
    
    async def _enhance_environment_prompt(self, base_prompt: str, 
                                        environment_type: str) -> str:
        """Enhance prompt for Egyptian environments"""
        
        environment_specific = {
            "temple_interior": "ancient Egyptian temple interior, massive stone pillars, hieroglyphic carvings, golden torches, sacred atmosphere",
            "pyramid_chamber": "Egyptian pyramid burial chamber, golden sarcophagus, treasure piles, mysterious lighting, ancient secrets",
            "altar_room": "Egyptian god altar chamber, divine shrine, sacred flames, golden decorations, mystical energy"
        }
        
        specific_prompt = environment_specific.get(environment_type, 
            "ancient Egyptian architecture")
        
        enhanced = f"masterpiece, best quality, {base_prompt}, {specific_prompt}"
        enhanced += ", Hades game environment style, cel-shaded art"
        enhanced += ", dramatic lighting, depth of field, architectural details"
        
        return enhanced
    
    async def _generate_with_depth_control(self, prompt: str, depth_image: Image.Image,
                                         width: int, height: int) -> Image.Image:
        """Generate image with depth control"""
        
        if "depth" not in self.controlnet_models:
            raise ValueError("Depth ControlNet model not available")
        
        pipeline = self.controlnet_models["depth"]["pipeline"]
        
        generator = torch.Generator(device=self.device).manual_seed(42)
        
        with torch.autocast(self.device):
            result = pipeline(
                prompt=prompt,
                image=depth_image,
                negative_prompt="blurry, low quality, flat, no depth, realistic photo",
                width=width,
                height=height,
                num_inference_steps=50,
                guidance_scale=8.0,
                controlnet_conditioning_scale=0.7,
                generator=generator
            )
        
        return result.images[0]
    
    async def _save_environment_asset(self, image: Image.Image, environment_type: str,
                                    prompt: str) -> Path:
        """Save environment asset with metadata"""
        
        output_dir = Path("assets/generated/depth_controlled")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        asset_name = f"environment_{environment_type}_depth_controlled"
        output_path = output_dir / f"{asset_name}.png"
        
        # Save image
        image.save(output_path, optimize=True)
        
        # Save metadata
        metadata = {
            "environment_type": environment_type,
            "prompt": prompt,
            "generation_time": time.time(),
            "control_type": "depth",
            "technique": "ControlNet Depth"
        }
        
        metadata_path = output_dir / f"{asset_name}_metadata.json"
        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path

# Test function
async def test_controlnet_integration():
    """Test ControlNet integration system"""
    print("Testing ControlNet Integration System...")
    
    system = ControlNetIntegrationSystem()
    
    # Setup models
    setup_success = await system.setup_controlnet_models()
    if not setup_success:
        print("ControlNet setup failed")
        return
    
    # Test pose control
    pose_result = await system.generate_pose_controlled_asset(
        character="anubis_guardian",
        pose_type="standing_guard",
        prompt="Egyptian god Anubis guardian, golden armor, divine authority",
        width=512,
        height=512
    )
    
    print(f"Pose control result: {pose_result}")
    
    # Test depth control
    depth_result = await system.generate_depth_controlled_environment(
        environment_type="temple_interior",
        prompt="Ancient Egyptian temple, mysterious atmosphere",
        width=512,
        height=512
    )
    
    print(f"Depth control result: {depth_result}")

if __name__ == "__main__":
    asyncio.run(test_controlnet_integration())