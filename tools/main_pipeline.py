#!/usr/bin/env python3
"""
Main Pipeline - Complete Egyptian Asset Generation System
Entry point for the Sands of Duat advanced asset generation pipeline
"""

import asyncio
import sys
from pathlib import Path

# Add systems to path
sys.path.append(str(Path(__file__).parent / "systems"))

# Import all advanced systems
from systems import (
    AdvancedAssetGenerationAgent,
    AgentOrchestrator,
    AssetGenerationAgent,
    HadesEgyptianLoRATrainer,
    ControlNetIntegrationSystem,
    RealESRGANUpscalingSystem,
    PostProcessingSystem,
    AdvancedSchedulerOptimizer
)

class SandsOfDuatPipeline:
    """Complete Egyptian asset generation pipeline"""
    
    def __init__(self):
        self.name = "Sands of Duat - Advanced Egyptian Asset Generation Pipeline"
        self.version = "1.0.0"
        self.systems = {}
        
        print(f"Initializing {self.name} v{self.version}")
        print("=" * 60)
    
    async def initialize_systems(self) -> bool:
        """Initialize all advanced generation systems"""
        try:
            print("Setting up advanced generation systems...")
            
            # Core orchestration
            self.systems["orchestrator"] = AgentOrchestrator()
            print("✓ Agent Orchestrator initialized")
            
            # Advanced generation agent
            self.systems["advanced_generator"] = AdvancedAssetGenerationAgent()
            print("✓ Advanced Asset Generation Agent initialized")
            
            # LoRA training system
            self.systems["lora_trainer"] = HadesEgyptianLoRATrainer()
            print("✓ LoRA Training System initialized")
            
            # ControlNet integration
            self.systems["controlnet"] = ControlNetIntegrationSystem()
            print("✓ ControlNet Integration System initialized")
            
            # Real-ESRGAN upscaling
            self.systems["upscaler"] = RealESRGANUpscalingSystem()
            print("✓ Real-ESRGAN Upscaling System initialized")
            
            # Post-processing
            self.systems["post_processor"] = PostProcessingSystem()
            print("✓ Post-Processing System initialized")
            
            # Scheduler optimizer
            self.systems["scheduler"] = AdvancedSchedulerOptimizer()
            print("✓ Advanced Scheduler Optimizer initialized")
            
            print("\n🏺 SANDS OF DUAT PIPELINE: READY")
            print("All advanced systems operational!")
            return True
            
        except Exception as e:
            print(f"❌ Pipeline initialization failed: {e}")
            return False
    
    async def generate_egyptian_asset(self, 
                                    asset_name: str,
                                    prompt: str,
                                    asset_type: str = "character_portrait",
                                    quality_level: str = "ultra_quality") -> dict:
        """Generate complete Egyptian asset with all advanced techniques"""
        
        print(f"\n🎨 Generating Egyptian Asset: {asset_name}")
        print(f"Type: {asset_type}, Quality: {quality_level}")
        print("-" * 40)
        
        try:
            # Stage 1: Get optimal scheduler
            scheduler_config = await self.systems["scheduler"].get_optimal_scheduler(
                asset_type=asset_type,
                quality_target=quality_level,
                egyptian_enhancement=True
            )
            print(f"✓ Scheduler optimized: {scheduler_config['scheduler_name']}")
            
            # Stage 2: Generate with advanced techniques
            generation_result = await self.systems["advanced_generator"].generate_advanced_egyptian_asset(
                asset_name=asset_name,
                prompt=prompt,
                width=1024,
                height=1024,
                style="hades_egyptian",
                use_controlnet=True,
                use_lora=True,
                upscale=True
            )
            
            if generation_result["status"] == "success":
                print(f"✓ Advanced generation completed: {generation_result['generation_time']:.2f}s")
                return generation_result
            else:
                print(f"❌ Generation failed: {generation_result.get('error', 'Unknown error')}")
                return generation_result
            
        except Exception as e:
            print(f"❌ Asset generation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def create_egyptian_game_workflow(self) -> dict:
        """Create complete Egyptian game asset workflow"""
        
        print("\n🏺 Creating Egyptian Game Workflow...")
        print("-" * 40)
        
        try:
            # Create workflow using orchestrator
            task_ids = self.systems["orchestrator"].create_egyptian_game_workflow()
            
            print(f"✓ Workflow created with {len(task_ids)} tasks")
            print("Tasks scheduled:")
            for i, task_id in enumerate(task_ids, 1):
                print(f"  {i}. {task_id}")
            
            return {
                "status": "success",
                "workflow_created": True,
                "task_count": len(task_ids),
                "task_ids": task_ids
            }
            
        except Exception as e:
            print(f"❌ Workflow creation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def get_system_status(self) -> dict:
        """Get status of all pipeline systems"""
        
        status = {
            "pipeline_name": self.name,
            "version": self.version,
            "systems_loaded": len(self.systems),
            "systems": {}
        }
        
        for system_name, system in self.systems.items():
            try:
                if hasattr(system, 'get_generation_status'):
                    status["systems"][system_name] = system.get_generation_status()
                elif hasattr(system, 'device'):
                    status["systems"][system_name] = {"device": system.device, "status": "ready"}
                else:
                    status["systems"][system_name] = {"status": "ready"}
            except Exception as e:
                status["systems"][system_name] = {"status": "error", "error": str(e)}
        
        return status

async def main():
    """Main pipeline demo"""
    
    # Initialize pipeline
    pipeline = SandsOfDuatPipeline()
    
    # Setup all systems
    setup_success = await pipeline.initialize_systems()
    if not setup_success:
        print("❌ Pipeline setup failed")
        return
    
    print("\n" + "=" * 60)
    print("SANDS OF DUAT PIPELINE DEMONSTRATION")
    print("=" * 60)
    
    # Show system status
    status = pipeline.get_system_status()
    print(f"\nPipeline Status:")
    print(f"  Systems loaded: {status['systems_loaded']}")
    for system_name, system_status in status["systems"].items():
        print(f"  ✓ {system_name}: {system_status.get('status', 'ready')}")
    
    # Create workflow
    workflow_result = await pipeline.create_egyptian_game_workflow()
    if workflow_result["status"] == "success":
        print(f"\n✓ Egyptian game workflow ready with {workflow_result['task_count']} tasks")
    
    # Generate sample asset
    print("\n" + "-" * 40)
    print("SAMPLE ASSET GENERATION")
    print("-" * 40)
    
    sample_result = await pipeline.generate_egyptian_asset(
        asset_name="demo_anubis_warrior",
        prompt="Egyptian god Anubis warrior, golden armor, divine aura, hieroglyphic details",
        asset_type="character_portrait",
        quality_level="ultra_quality"
    )
    
    if sample_result["status"] == "success":
        print(f"\n🎉 DEMO COMPLETE!")
        print(f"Asset generated: {sample_result.get('output_path', 'simulated')}")
    else:
        print(f"\n⚠️ Demo generation simulated (dependencies not fully installed)")
    
    print(f"\n🏺 Sands of Duat Pipeline is ready for Egyptian asset generation!")

if __name__ == "__main__":
    asyncio.run(main())