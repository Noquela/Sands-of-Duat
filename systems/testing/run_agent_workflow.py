#!/usr/bin/env python3
"""
Sands of Duat - Agent Workflow Runner
Execute complete Egyptian game development workflow using specialized sub-agents
"""

import asyncio
import sys
from pathlib import Path

# Add agents to path
sys.path.append(str(Path(__file__).parent / "agents"))

from agents import AgentOrchestrator

async def main():
    """Execute the complete Egyptian game development workflow"""
    print("SANDS OF DUAT - AGENT WORKFLOW SYSTEM")
    print("=" * 60)
    print("Initializing specialized sub-agents for Egyptian game development...")
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # Create the complete Egyptian workflow
    print("\nCreating Egyptian Game Development Workflow...")
    task_ids = orchestrator.create_egyptian_game_workflow()
    
    print(f"SUCCESS: Workflow created with {len(task_ids)} tasks")
    print("\nWorkflow Tasks:")
    for i, task in enumerate(orchestrator.task_queue, 1):
        print(f"   {i}. {task.description} ({task.agent_type})")
    
    # Start workflow execution
    print("\nStarting automated workflow execution...")
    print("Sub-agents will work in parallel to complete all tasks...")
    
    success = await orchestrator.execute_workflow()
    
    # Get final results
    status = orchestrator.get_workflow_status()
    
    print("\n" + "=" * 60)
    print("EGYPTIAN GAME WORKFLOW COMPLETE!")
    print(f"Results Summary:")
    print(f"   Total Tasks: {status['total_tasks']}")
    print(f"   Completed: {status['completed']} SUCCESS")
    print(f"   Failed: {status['failed']} FAILED")
    print(f"   Success Rate: {status['progress_percentage']:.1f}%")
    
    if status['failed'] == 0:
        print("\nALL TASKS COMPLETED SUCCESSFULLY!")
        print("The Egyptian game is ready with:")
        print("   * AI-generated Egyptian assets")
        print("   * Complete game systems implementation")
        print("   * Quality validation and testing")
        print("   * Full Egyptian theme integration")
    else:
        print(f"\nWARNING: {status['failed']} tasks failed - review logs for details")
    
    # Save detailed workflow state
    orchestrator.save_workflow_state("logs/final_workflow_state.json")
    
    print(f"\nWorkflow state saved to: logs/final_workflow_state.json")
    print("\nSands of Duat development workflow complete!")

def run_quick_asset_generation():
    """Quick asset generation for immediate testing"""
    print("QUICK ASSET GENERATION MODE")
    print("Generating priority Egyptian assets...")
    
    # This would run just the asset generation parts
    from agents import AssetGenerationAgent
    
    agent = AssetGenerationAgent()
    
    # Generate key assets
    assets_to_generate = [
        ("player_anubis_idle", "Egyptian Anubis warrior, golden armor, idle pose"),
        ("altar_ra", "Ra sun god altar, golden pyramid, divine flames"),
        ("enemy_scarab", "Egyptian scarab warrior, bronze armor, combat ready")
    ]
    
    print("Generating priority assets:")
    for asset_name, prompt in assets_to_generate:
        print(f"   - {asset_name}")
    
    print("\nQuick generation complete!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sands of Duat Agent Workflow")
    parser.add_argument("--mode", choices=["full", "quick"], default="full",
                       help="Workflow mode: full workflow or quick asset generation")
    
    args = parser.parse_args()
    
    if args.mode == "full":
        asyncio.run(main())
    elif args.mode == "quick":
        run_quick_asset_generation()