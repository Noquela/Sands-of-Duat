"""
Advanced Systems Package - Professional Egyptian asset generation systems
Organized into specialized modules for maintainability and scalability
"""

# Import main system classes for easy access
from .advanced_generation.advanced_asset_generation_agent import AdvancedAssetGenerationAgent
from .core_agents.agent_orchestrator import AgentOrchestrator
from .core_agents.asset_generation_agent import AssetGenerationAgent
from .lora.lora_training_system import HadesEgyptianLoRATrainer
from .controlnet.controlnet_integration_system import ControlNetIntegrationSystem
from .upscaling.realesrgan_upscaling_system import RealESRGANUpscalingSystem
from .post_processing.post_processing_system import PostProcessingSystem
from .schedulers.advanced_scheduler_optimizer import AdvancedSchedulerOptimizer

__all__ = [
    "AdvancedAssetGenerationAgent",
    "AgentOrchestrator", 
    "AssetGenerationAgent",
    "HadesEgyptianLoRATrainer",
    "ControlNetIntegrationSystem",
    "RealESRGANUpscalingSystem",
    "PostProcessingSystem",
    "AdvancedSchedulerOptimizer"
]

__version__ = "1.0.0"
__author__ = "Sands of Duat Development Team"
__description__ = "Advanced Egyptian asset generation systems with Hades-quality techniques"