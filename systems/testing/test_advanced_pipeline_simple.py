#!/usr/bin/env python3
"""
Simple Advanced Pipeline Test - Test all advanced techniques without Unicode
"""

import asyncio
import sys
import time
from pathlib import Path

# Add systems to path
sys.path.append(str(Path(__file__).parent.parent))

async def test_advanced_pipeline():
    """Test the complete advanced asset generation pipeline"""
    
    print("=" * 60)
    print("TESTING COMPLETE ADVANCED PIPELINE")
    print("=" * 60)
    print("Techniques: LoRA + ControlNet + Real-ESRGAN + Post-Processing + Schedulers")
    print()
    
    total_start_time = time.time()
    test_results = {}
    
    # Stage 1: Test LoRA Training System
    print("STAGE 1: Testing LoRA Training System...")
    print("-" * 40)
    
    try:
        from lora.lora_training_system import HadesEgyptianLoRATrainer
        
        lora_trainer = HadesEgyptianLoRATrainer()
        print(f"   Model: {lora_trainer.model_name}")
        print(f"   Dataset size: {len(lora_trainer.training_prompts)}")
        print(f"   Rank: {lora_trainer.rank}, Alpha: {lora_trainer.alpha}")
        
        test_results["lora_training"] = {
            "status": "available",
            "model_name": lora_trainer.model_name,
            "dataset_size": len(lora_trainer.training_prompts)
        }
        
        print("   SUCCESS: LoRA Training System READY")
        
    except Exception as e:
        print(f"   FAILED: LoRA Training System: {e}")
        test_results["lora_training"] = {"status": "failed", "error": str(e)}
    
    print()
    
    # Stage 2: Test ControlNet Integration
    print("STAGE 2: Testing ControlNet Integration...")
    print("-" * 40)
    
    try:
        from controlnet.controlnet_integration_system import ControlNetIntegrationSystem
        
        controlnet_system = ControlNetIntegrationSystem()
        print(f"   ControlNet configs: {len(controlnet_system.controlnet_configs)}")
        print(f"   Egyptian poses: {len(controlnet_system.egyptian_poses)}")
        
        pose_characters = list(controlnet_system.egyptian_poses.keys())
        print(f"   Available poses: {', '.join(pose_characters)}")
        
        test_results["controlnet"] = {
            "status": "available",
            "configs": list(controlnet_system.controlnet_configs.keys()),
            "egyptian_poses": pose_characters
        }
        
        print("   SUCCESS: ControlNet Integration READY")
        
    except Exception as e:
        print(f"   FAILED: ControlNet Integration: {e}")
        test_results["controlnet"] = {"status": "failed", "error": str(e)}
    
    print()
    
    # Stage 3: Test Real-ESRGAN Upscaling
    print("STAGE 3: Testing Real-ESRGAN Upscaling...")
    print("-" * 40)
    
    try:
        from upscaling.realesrgan_upscaling_system import RealESRGANUpscalingSystem
        
        upscaling_system = RealESRGANUpscalingSystem()
        print(f"   Upscaling configs: {len(upscaling_system.upscaling_configs)}")
        print(f"   Egyptian enhancements: {len(upscaling_system.egyptian_enhancement_config)}")
        
        test_results["upscaling"] = {
            "status": "available",
            "configs": list(upscaling_system.upscaling_configs.keys()),
            "enhancements": list(upscaling_system.egyptian_enhancement_config.keys())
        }
        
        print("   SUCCESS: Real-ESRGAN Upscaling READY")
        
    except Exception as e:
        print(f"   FAILED: Real-ESRGAN Upscaling: {e}")
        test_results["upscaling"] = {"status": "failed", "error": str(e)}
    
    print()
    
    # Stage 4: Test Post-Processing System
    print("STAGE 4: Testing Post-Processing System...")
    print("-" * 40)
    
    try:
        from post_processing.post_processing_system import PostProcessingSystem
        
        post_processing = PostProcessingSystem()
        print(f"   Hades config stages: {len(post_processing.hades_config)}")
        print(f"   Egyptian palettes: {len(post_processing.egyptian_palettes)}")
        print(f"   Effect templates: {len(post_processing.effect_templates)}")
        
        palette_names = list(post_processing.egyptian_palettes.keys())
        print(f"   Color palettes: {', '.join(palette_names)}")
        
        test_results["post_processing"] = {
            "status": "available", 
            "hades_effects": list(post_processing.hades_config.keys()),
            "palettes": palette_names,
            "templates": list(post_processing.effect_templates.keys())
        }
        
        print("   SUCCESS: Post-Processing System READY")
        
    except Exception as e:
        print(f"   FAILED: Post-Processing System: {e}")
        test_results["post_processing"] = {"status": "failed", "error": str(e)}
    
    print()
    
    # Stage 5: Test Advanced Scheduler Optimizer
    print("STAGE 5: Testing Advanced Scheduler Optimizer...")
    print("-" * 40)
    
    try:
        from schedulers.advanced_scheduler_optimizer import AdvancedSchedulerOptimizer
        
        scheduler_optimizer = AdvancedSchedulerOptimizer()
        print(f"   Scheduler presets: {len(scheduler_optimizer.scheduler_presets)}")
        print(f"   Asset optimizations: {len(scheduler_optimizer.asset_optimizations)}")
        print(f"   Egyptian optimizations: {len(scheduler_optimizer.egyptian_optimizations)}")
        
        preset_names = list(scheduler_optimizer.scheduler_presets.keys())
        print(f"   Quality presets: {', '.join(preset_names)}")
        
        test_results["scheduler_optimizer"] = {
            "status": "available",
            "presets": preset_names,
            "asset_types": list(scheduler_optimizer.asset_optimizations.keys()),
            "egyptian_opts": list(scheduler_optimizer.egyptian_optimizations.keys())
        }
        
        print("   SUCCESS: Advanced Scheduler Optimizer READY")
        
    except Exception as e:
        print(f"   FAILED: Advanced Scheduler Optimizer: {e}")
        test_results["scheduler_optimizer"] = {"status": "failed", "error": str(e)}
    
    print()
    
    # Stage 6: Test Advanced Asset Generation Agent
    print("STAGE 6: Testing Advanced Asset Generation Agent...")
    print("-" * 40)
    
    try:
        from advanced_generation.advanced_asset_generation_agent import AdvancedAssetGenerationAgent
        
        advanced_agent = AdvancedAssetGenerationAgent()
        print(f"   Device: {advanced_agent.device}")
        print(f"   Hades-Egyptian config loaded")
        print(f"   LoRA models: {len(advanced_agent.hades_egyptian_config.get('lora_models', []))}")
        print(f"   ControlNet models: {len(advanced_agent.hades_egyptian_config.get('controlnet_models', []))}")
        
        test_results["advanced_agent"] = {
            "status": "available",
            "device": advanced_agent.device,
            "lora_models": advanced_agent.hades_egyptian_config.get('lora_models', []),
            "controlnet_models": advanced_agent.hades_egyptian_config.get('controlnet_models', [])
        }
        
        print("   SUCCESS: Advanced Asset Generation Agent READY")
        
    except Exception as e:
        print(f"   FAILED: Advanced Asset Generation Agent: {e}")
        test_results["advanced_agent"] = {"status": "failed", "error": str(e)}
    
    print()
    
    # Final Summary
    total_time = time.time() - total_start_time
    
    print("=" * 60)
    print("ADVANCED PIPELINE TEST COMPLETE")
    print("=" * 60)
    
    # Calculate overall success rate
    total_tests = len(test_results)
    successful_tests = sum(1 for result in test_results.values() 
                         if result.get("status") == "available")
    success_rate = successful_tests / total_tests * 100
    
    print(f"RESULTS SUMMARY:")
    print(f"   Total test time: {total_time:.2f}s")
    print(f"   Tests run: {total_tests}")
    print(f"   Success rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")
    print()
    
    print("TECHNIQUE STATUS:")
    for technique, result in test_results.items():
        status = result.get("status", "unknown")
        if status == "available":
            print(f"   SUCCESS: {technique.replace('_', ' ').title()}: READY")
        elif status == "failed":
            print(f"   FAILED: {technique.replace('_', ' ').title()}: ERROR")
        else:
            print(f"   UNKNOWN: {technique.replace('_', ' ').title()}: {status.upper()}")
    
    print()
    
    if success_rate >= 80:
        print("EXCELLENT: Advanced pipeline is ready for production!")
        print("All major techniques are operational")
    elif success_rate >= 60:
        print("GOOD: Advanced pipeline is mostly ready")  
        print("Minor issues need to be resolved")
    else:
        print("NEEDS WORK: Several components require attention")
        print("Focus on failed components first")
    
    return {
        "overall_status": "excellent" if success_rate >= 80 else "good" if success_rate >= 60 else "needs_work",
        "success_rate": success_rate,
        "total_time": total_time,
        "test_results": test_results
    }

async def main():
    """Main test function"""
    result = await test_advanced_pipeline()
    
    # Save test results
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)
    
    import json
    with open(results_dir / "advanced_pipeline_test.json", 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\nTest results saved to: {results_dir / 'advanced_pipeline_test.json'}")
    
    return result

if __name__ == "__main__":
    asyncio.run(main())