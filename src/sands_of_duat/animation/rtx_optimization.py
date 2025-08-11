"""
RTX 5070 Optimization Module - GPU Performance Tuning
Optimizes ComfyUI and AnimateDiff generation for RTX 5070 hardware.
"""

import psutil
import GPUtil
import logging
import asyncio
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class GPUMetrics:
    """GPU performance metrics."""
    name: str
    memory_total: int
    memory_used: int
    memory_free: int
    utilization: float
    temperature: int
    power_draw: int

@dataclass  
class OptimizationProfile:
    """RTX optimization profile."""
    profile_name: str
    batch_size: int
    resolution_limits: Dict[str, tuple]
    concurrent_requests: int
    memory_management: Dict[str, Any]
    vram_threshold: float
    performance_mode: str

class RTXOptimizer:
    """
    RTX 5070 optimization manager for ComfyUI AnimateDiff generation.
    Provides hardware-specific tuning for optimal animation generation.
    """
    
    def __init__(self):
        """Initialize RTX optimizer."""
        self.logger = logging.getLogger("rtx_optimizer")
        
        # Hardware detection
        self.gpu_info: Optional[GPUMetrics] = None
        self.is_rtx_5070 = False
        self.optimization_active = False
        
        # Optimization profiles
        self.profiles = self._load_optimization_profiles()
        self.active_profile: Optional[OptimizationProfile] = None
        
        # Performance monitoring
        self.performance_history = []
        self.memory_warnings = []
        
        # Auto-optimization settings
        self.auto_optimize = True
        self.dynamic_batching = True
        self.memory_cleanup_threshold = 0.85  # 85% VRAM usage
        
        self.logger.info("RTX Optimizer initialized")
    
    def initialize(self) -> bool:
        """Initialize RTX optimizer with hardware detection."""
        try:
            self.gpu_info = self._detect_gpu()
            
            if self.gpu_info:
                self.logger.info(f"GPU detected: {self.gpu_info.name}")
                self.logger.info(f"VRAM: {self.gpu_info.memory_total}MB")
                
                # Check for RTX 5070
                if "rtx 5070" in self.gpu_info.name.lower():
                    self.is_rtx_5070 = True
                    self.active_profile = self.profiles["rtx_5070_optimal"]
                    self.logger.info("RTX 5070 detected - loading optimal profile")
                else:
                    # Use general profile for other GPUs
                    self.active_profile = self.profiles["general_gpu"]
                    self.logger.info("Using general GPU optimization profile")
                
                self.optimization_active = True
                return True
            else:
                self.logger.warning("No compatible GPU detected")
                return False
                
        except Exception as e:
            self.logger.error(f"RTX optimization initialization failed: {e}")
            return False
    
    def _detect_gpu(self) -> Optional[GPUMetrics]:
        """Detect GPU hardware and capabilities."""
        try:
            gpus = GPUtil.getGPUs()
            
            if gpus:
                gpu = gpus[0]  # Use first GPU
                return GPUMetrics(
                    name=gpu.name,
                    memory_total=int(gpu.memoryTotal),
                    memory_used=int(gpu.memoryUsed),
                    memory_free=int(gpu.memoryFree),
                    utilization=gpu.load * 100,
                    temperature=int(gpu.temperature),
                    power_draw=0  # Not available in GPUtil
                )
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"GPU detection failed: {e}")
            return None
    
    def _load_optimization_profiles(self) -> Dict[str, OptimizationProfile]:
        """Load RTX optimization profiles."""
        return {
            "rtx_5070_optimal": OptimizationProfile(
                profile_name="RTX 5070 Optimal",
                batch_size=2,
                resolution_limits={
                    "common": (512, 768),
                    "rare": (640, 896), 
                    "epic": (768, 1024),
                    "legendary": (768, 1024)  # Max for stable generation
                },
                concurrent_requests=2,
                memory_management={
                    "enable_attention_slicing": True,
                    "enable_xformers": True,
                    "enable_cpu_offload": False,  # RTX 5070 has enough VRAM
                    "enable_model_cpu_offload": False,
                    "enable_sequential_cpu_offload": False
                },
                vram_threshold=0.8,  # 80% VRAM threshold
                performance_mode="balanced"
            ),
            "rtx_5070_performance": OptimizationProfile(
                profile_name="RTX 5070 Performance", 
                batch_size=1,  # Single batch for max quality
                resolution_limits={
                    "common": (640, 896),
                    "rare": (768, 1024),
                    "epic": (896, 1152),
                    "legendary": (1024, 1344)  # Ultra-high quality
                },
                concurrent_requests=1,
                memory_management={
                    "enable_attention_slicing": False,
                    "enable_xformers": True,
                    "enable_cpu_offload": False,
                    "enable_model_cpu_offload": False,
                    "enable_sequential_cpu_offload": False
                },
                vram_threshold=0.9,  # Allow higher VRAM usage
                performance_mode="performance"
            ),
            "rtx_5070_memory_efficient": OptimizationProfile(
                profile_name="RTX 5070 Memory Efficient",
                batch_size=1,
                resolution_limits={
                    "common": (512, 768),
                    "rare": (512, 768),
                    "epic": (640, 896),
                    "legendary": (640, 896)
                },
                concurrent_requests=3,  # More concurrent, lower resolution
                memory_management={
                    "enable_attention_slicing": True,
                    "enable_xformers": True,
                    "enable_cpu_offload": True,
                    "enable_model_cpu_offload": True,
                    "enable_sequential_cpu_offload": False
                },
                vram_threshold=0.7,
                performance_mode="memory_efficient"
            ),
            "general_gpu": OptimizationProfile(
                profile_name="General GPU",
                batch_size=1,
                resolution_limits={
                    "common": (512, 768),
                    "rare": (512, 768),
                    "epic": (640, 896), 
                    "legendary": (768, 1024)
                },
                concurrent_requests=1,
                memory_management={
                    "enable_attention_slicing": True,
                    "enable_xformers": True,
                    "enable_cpu_offload": True,
                    "enable_model_cpu_offload": True,
                    "enable_sequential_cpu_offload": True
                },
                vram_threshold=0.7,
                performance_mode="conservative"
            )
        }
    
    def get_optimal_settings(self, rarity: str, card_type: str) -> Dict[str, Any]:
        """Get optimal generation settings for card specifications."""
        if not self.active_profile:
            return self._get_fallback_settings()
        
        # Get resolution from profile
        width, height = self.active_profile.resolution_limits.get(
            rarity.lower(), self.active_profile.resolution_limits["common"]
        )
        
        # Adjust settings based on card type
        if card_type.lower() == "spell":
            # Spells benefit from higher motion strength
            motion_strength = 1.3
            frames = 20 if rarity.lower() == "legendary" else 16
        elif card_type.lower() == "artifact":
            # Artifacts need subtle motion
            motion_strength = 0.8
            frames = 16
        else:
            # Creatures - standard settings
            motion_strength = 1.0
            frames = 24 if rarity.lower() == "legendary" else 16
        
        return {
            "width": width,
            "height": height,
            "frames": frames,
            "batch_size": self.active_profile.batch_size,
            "motion_strength": motion_strength,
            "concurrent_requests": self.active_profile.concurrent_requests,
            "memory_management": self.active_profile.memory_management
        }
    
    def _get_fallback_settings(self) -> Dict[str, Any]:
        """Get fallback settings when no profile is active."""
        return {
            "width": 512,
            "height": 768,
            "frames": 16,
            "batch_size": 1,
            "motion_strength": 1.0,
            "concurrent_requests": 1,
            "memory_management": {
                "enable_attention_slicing": True,
                "enable_xformers": False,
                "enable_cpu_offload": True,
                "enable_model_cpu_offload": True,
                "enable_sequential_cpu_offload": True
            }
        }
    
    async def monitor_performance(self) -> GPUMetrics:
        """Monitor current GPU performance."""
        if not self.optimization_active:
            return None
        
        try:
            current_metrics = self._detect_gpu()
            
            if current_metrics:
                # Check for memory warnings
                memory_usage_percent = (current_metrics.memory_used / current_metrics.memory_total)
                
                if memory_usage_percent > self.memory_cleanup_threshold:
                    self.memory_warnings.append({
                        "timestamp": asyncio.get_event_loop().time(),
                        "memory_usage": memory_usage_percent,
                        "message": f"High VRAM usage: {memory_usage_percent:.1%}"
                    })
                    
                    if self.auto_optimize:
                        await self._trigger_memory_cleanup()
                
                # Store performance history
                self.performance_history.append({
                    "timestamp": asyncio.get_event_loop().time(),
                    "metrics": current_metrics
                })
                
                # Keep only last 100 entries
                if len(self.performance_history) > 100:
                    self.performance_history.pop(0)
                
                return current_metrics
            
        except Exception as e:
            self.logger.error(f"Performance monitoring error: {e}")
        
        return None
    
    async def _trigger_memory_cleanup(self):
        """Trigger GPU memory cleanup."""
        self.logger.warning("Triggering GPU memory cleanup due to high usage")
        
        # In a real implementation, this would:
        # 1. Clear unused model weights
        # 2. Flush CUDA cache
        # 3. Reduce concurrent requests temporarily
        # 4. Switch to memory-efficient profile if available
        
        if self.is_rtx_5070 and self.active_profile.profile_name != "RTX 5070 Memory Efficient":
            self.logger.info("Switching to memory-efficient profile")
            self.active_profile = self.profiles["rtx_5070_memory_efficient"]
    
    def switch_profile(self, profile_name: str) -> bool:
        """Switch to a different optimization profile."""
        if profile_name in self.profiles:
            self.active_profile = self.profiles[profile_name]
            self.logger.info(f"Switched to optimization profile: {profile_name}")
            return True
        else:
            self.logger.error(f"Unknown optimization profile: {profile_name}")
            return False
    
    def get_profile_recommendations(self) -> List[str]:
        """Get profile recommendations based on current hardware."""
        if self.is_rtx_5070:
            return [
                "rtx_5070_optimal",      # Balanced performance
                "rtx_5070_performance",  # Maximum quality
                "rtx_5070_memory_efficient"  # Maximum throughput
            ]
        else:
            return ["general_gpu"]
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization status."""
        status = {
            "optimization_active": self.optimization_active,
            "gpu_detected": self.gpu_info is not None,
            "is_rtx_5070": self.is_rtx_5070,
            "active_profile": self.active_profile.profile_name if self.active_profile else None,
            "auto_optimize": self.auto_optimize,
            "memory_warnings": len(self.memory_warnings)
        }
        
        if self.gpu_info:
            status["gpu_info"] = {
                "name": self.gpu_info.name,
                "memory_total": self.gpu_info.memory_total,
                "memory_used": self.gpu_info.memory_used,
                "memory_usage_percent": (self.gpu_info.memory_used / self.gpu_info.memory_total) * 100,
                "utilization": self.gpu_info.utilization,
                "temperature": self.gpu_info.temperature
            }
        
        return status
    
    def export_performance_report(self, output_path: str):
        """Export performance monitoring report."""
        report = {
            "optimization_status": self.get_optimization_status(),
            "active_profile": self.active_profile.__dict__ if self.active_profile else None,
            "performance_history": self.performance_history[-20:],  # Last 20 entries
            "memory_warnings": self.memory_warnings,
            "recommendations": self.get_profile_recommendations()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Performance report exported: {output_path}")
    
    def enable_auto_optimization(self, enabled: bool = True):
        """Enable or disable automatic optimization."""
        self.auto_optimize = enabled
        self.logger.info(f"Auto-optimization {'enabled' if enabled else 'disabled'}")
    
    def clear_performance_history(self):
        """Clear performance monitoring history."""
        self.performance_history.clear()
        self.memory_warnings.clear()
        self.logger.info("Performance history cleared")

# Global RTX optimizer instance  
rtx_optimizer = RTXOptimizer()