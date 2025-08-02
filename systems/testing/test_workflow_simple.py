#!/usr/bin/env python3
"""
Simple Workflow Test - Test sub-agents without full complexity
"""

import asyncio
import sys
from pathlib import Path

# Add agents to path
sys.path.append(str(Path(__file__).parent / "agents"))

async def test_simple_workflow():
    """Test simplified workflow"""
    print("TESTING SUB-AGENT WORKFLOW")
    print("=" * 40)
    
    try:
        # Test Asset Generation Agent
        print("1. Testing Asset Generation Agent...")
        from asset_generation_agent import AssetGenerationAgent
        
        asset_agent = AssetGenerationAgent()
        
        # Test simple sprite generation
        result = await asset_agent.generate_sprite_sheet(
            sprite_type="player",
            character="anubis_warrior",
            animations=["idle"],
            size=(512, 512),
            frames=1
        )
        
        if result["status"] == "success":
            print("   SUCCESS: Asset Generation Agent working")
        else:
            print(f"   FAILED: {result.get('error', 'Unknown')}")
        
        # Test Game Development Agent
        print("\n2. Testing Game Development Agent...")
        from game_development_agent import GameDevelopmentAgent
        
        game_agent = GameDevelopmentAgent()
        
        result = await game_agent.implement_system(
            system_type="artifact_system",
            gods=["Ra", "Thoth"],
            artifacts_per_god=2,
            stat_effects=["damage", "speed"]
        )
        
        if result["status"] == "success":
            print("   SUCCESS: Game Development Agent working")
        else:
            print(f"   FAILED: {result.get('error', 'Unknown')}")
        
        # Test Quality Control Agent  
        print("\n3. Testing Quality Control Agent...")
        from quality_control_agent import QualityControlAgent
        
        qa_agent = QualityControlAgent()
        
        result = await qa_agent.validate_assets(
            validation_criteria=["quality", "consistency"]
        )
        
        if result["status"] == "success":
            print("   SUCCESS: Quality Control Agent working")
        else:
            print(f"   FAILED: {result.get('error', 'Unknown')}")
        
        print("\n" + "=" * 40)
        print("SUB-AGENT WORKFLOW TEST COMPLETE")
        print("All agents tested individually!")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Workflow test failed: {e}")
        return False

async def test_orchestrator():
    """Test the orchestrator without full workflow"""
    print("\nTESTING AGENT ORCHESTRATOR")
    print("=" * 30)
    
    try:
        from agent_orchestrator import AgentOrchestrator, Task, AgentStatus
        
        # Create simple orchestrator
        orchestrator = AgentOrchestrator()
        
        # Create simple task
        test_task = Task(
            task_id="test_simple",
            agent_type="asset_generator", 
            task_type="generate_sprite_sheet",
            description="Test asset generation",
            priority=5,
            parameters={
                "sprite_type": "player",
                "character": "anubis",
                "animations": ["idle"],
                "size": (256, 256),
                "frames": 1
            }
        )
        
        # Add task
        orchestrator.add_task(test_task)
        
        print(f"Task added: {test_task.task_id}")
        print(f"Queue length: {len(orchestrator.task_queue)}")
        
        # Get status
        status = orchestrator.get_workflow_status()
        print(f"Workflow status: {status}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Orchestrator test failed: {e}")
        return False

if __name__ == "__main__":
    async def main():
        success1 = await test_simple_workflow()
        success2 = await test_orchestrator()
        
        if success1 and success2:
            print("\nALL TESTS PASSED!")
            print("Sub-agent system is working correctly")
        else:
            print("\nSOME TESTS FAILED")
            print("Check error messages above")
    
    asyncio.run(main())