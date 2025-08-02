#!/usr/bin/env python3
"""
Agent Orchestrator - Central coordination for Sands of Duat development workflow
Manages specialized sub-agents for automated game development
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"

@dataclass
class Task:
    """Task definition for agent workflow"""
    task_id: str
    agent_type: str
    task_type: str
    description: str
    priority: int = 5
    dependencies: List[str] = None
    parameters: Dict[str, Any] = None
    status: AgentStatus = AgentStatus.IDLE
    result: Any = None
    error: str = ""
    created_at: float = 0.0
    started_at: float = 0.0
    completed_at: float = 0.0

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.parameters is None:
            self.parameters = {}
        if self.created_at == 0.0:
            self.created_at = time.time()

class AgentOrchestrator:
    """Central orchestrator for managing specialized sub-agents"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.running = False
        
        # Initialize specialized agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialized sub-agents"""
        from .asset_generation_agent import AssetGenerationAgent
        from .game_development_agent import GameDevelopmentAgent
        from .quality_control_agent import QualityControlAgent
        
        self.agents = {
            "asset_generator": AssetGenerationAgent(),
            "game_developer": GameDevelopmentAgent(), 
            "quality_controller": QualityControlAgent()
        }
        
        print("🤖 Agent Orchestrator initialized with specialized sub-agents:")
        for agent_name, agent in self.agents.items():
            print(f"   - {agent_name}: {agent.__class__.__name__}")
    
    def add_task(self, task: Task) -> str:
        """Add task to the workflow queue"""
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: (-t.priority, t.created_at))
        print(f"📋 Task added: {task.task_id} ({task.agent_type})")
        return task.task_id
    
    def create_egyptian_game_workflow(self) -> List[str]:
        """Create complete workflow for Egyptian game development"""
        workflow_tasks = [
            Task(
                task_id="asset_gen_player",
                agent_type="asset_generator",
                task_type="generate_sprite_sheet",
                description="Generate Anubis player sprite sheets",
                priority=10,
                parameters={
                    "sprite_type": "player",
                    "character": "anubis_warrior",
                    "animations": ["idle", "walk", "attack", "dash"],
                    "size": (1024, 256),
                    "frames": 4
                }
            ),
            Task(
                task_id="asset_gen_enemies",
                agent_type="asset_generator", 
                task_type="generate_sprite_sheet",
                description="Generate Egyptian enemy sprites",
                priority=9,
                parameters={
                    "sprite_type": "enemy",
                    "enemies": ["scarab_warrior", "mummy_guard", "anubis_sentinel"],
                    "animations": ["idle", "walk", "attack"],
                    "size": (768, 192),
                    "frames": 4
                }
            ),
            Task(
                task_id="asset_gen_altars",
                agent_type="asset_generator",
                task_type="generate_environment",
                description="Generate Egyptian god altars",
                priority=8,
                dependencies=["asset_gen_player"],
                parameters={
                    "environment_type": "altars",
                    "gods": ["Ra", "Thoth", "Isis", "Ptah"],
                    "size": (384, 384),
                    "style": "divine_shrine"
                }
            ),
            Task(
                task_id="game_dev_artifacts",
                agent_type="game_developer",
                task_type="implement_system",
                description="Implement Egyptian artifact system",
                priority=7,
                dependencies=["asset_gen_altars"],
                parameters={
                    "system_type": "artifact_system",
                    "gods": ["Ra", "Thoth", "Isis", "Ptah"],
                    "artifacts_per_god": 3,
                    "stat_effects": ["damage", "speed", "health", "crit_chance"]
                }
            ),
            Task(
                task_id="game_dev_combat",
                agent_type="game_developer",
                task_type="implement_system", 
                description="Implement Egyptian combat system",
                priority=6,
                dependencies=["asset_gen_enemies", "game_dev_artifacts"],
                parameters={
                    "system_type": "combat_system",
                    "combat_style": "hades_inspired",
                    "enemy_types": ["scarab", "mummy", "sentinel"],
                    "attack_patterns": ["melee", "ranged", "special"]
                }
            ),
            Task(
                task_id="quality_test_assets",
                agent_type="quality_controller",
                task_type="validate_assets",
                description="Quality control for all generated assets",
                priority=5,
                dependencies=["asset_gen_player", "asset_gen_enemies", "asset_gen_altars"],
                parameters={
                    "validation_criteria": ["quality", "consistency", "egyptian_theme", "game_ready"]
                }
            ),
            Task(
                task_id="quality_test_gameplay",
                agent_type="quality_controller",
                task_type="test_gameplay",
                description="Test complete Egyptian gameplay workflow", 
                priority=4,
                dependencies=["game_dev_combat", "quality_test_assets"],
                parameters={
                    "test_scenarios": ["hub_exploration", "altar_interaction", "combat_flow", "artifact_progression"]
                }
            )
        ]
        
        # Add all tasks to queue
        task_ids = []
        for task in workflow_tasks:
            task_ids.append(self.add_task(task))
        
        print(f"🏺 Egyptian Game Workflow created with {len(workflow_tasks)} tasks")
        return task_ids
    
    async def execute_workflow(self) -> bool:
        """Execute the complete workflow with all sub-agents"""
        print("🚀 Starting Egyptian Game Development Workflow...")
        self.running = True
        
        while self.running and (self.task_queue or self._has_active_tasks()):
            # Find ready tasks (dependencies completed)
            ready_tasks = self._get_ready_tasks()
            
            if ready_tasks:
                # Execute ready tasks in parallel
                await self._execute_parallel_tasks(ready_tasks)
            else:
                # Wait for running tasks to complete
                await asyncio.sleep(1)
            
            # Check if workflow is complete
            if not self.task_queue and not self._has_active_tasks():
                print("✅ Workflow completed successfully!")
                break
        
        return True
    
    def _get_ready_tasks(self) -> List[Task]:
        """Get tasks that are ready to execute (dependencies met)"""
        ready_tasks = []
        
        for task in self.task_queue:
            if task.status == AgentStatus.IDLE:
                # Check if all dependencies are completed
                deps_completed = all(
                    self._is_task_completed(dep_id) 
                    for dep_id in task.dependencies
                )
                
                if deps_completed:
                    ready_tasks.append(task)
        
        return ready_tasks
    
    def _is_task_completed(self, task_id: str) -> bool:
        """Check if a task is completed"""
        for task in self.completed_tasks:
            if task.task_id == task_id and task.status == AgentStatus.COMPLETED:
                return True
        return False
    
    def _has_active_tasks(self) -> bool:
        """Check if any tasks are currently being worked on"""
        return any(
            task.status == AgentStatus.WORKING 
            for task in self.task_queue
        )
    
    async def _execute_parallel_tasks(self, tasks: List[Task]) -> None:
        """Execute multiple tasks in parallel"""
        if not tasks:
            return
        
        print(f"⚡ Executing {len(tasks)} parallel tasks...")
        
        # Create coroutines for each task
        coroutines = []
        for task in tasks:
            if task.agent_type in self.agents:
                coroutine = self._execute_task(task)
                coroutines.append(coroutine)
        
        # Execute tasks in parallel
        if coroutines:
            await asyncio.gather(*coroutines, return_exceptions=True)
    
    async def _execute_task(self, task: Task) -> bool:
        """Execute a single task using the appropriate agent"""
        try:
            task.status = AgentStatus.WORKING
            task.started_at = time.time()
            
            print(f"🔄 Starting task: {task.task_id} ({task.description})")
            
            # Get the appropriate agent
            agent = self.agents.get(task.agent_type)
            if not agent:
                raise ValueError(f"Unknown agent type: {task.agent_type}")
            
            # Execute task based on type
            if task.task_type == "generate_sprite_sheet":
                result = await agent.generate_sprite_sheet(**task.parameters)
            elif task.task_type == "generate_environment":
                result = await agent.generate_environment(**task.parameters)
            elif task.task_type == "implement_system":
                result = await agent.implement_system(**task.parameters)
            elif task.task_type == "validate_assets":
                result = await agent.validate_assets(**task.parameters)
            elif task.task_type == "test_gameplay":
                result = await agent.test_gameplay(**task.parameters)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            # Mark task as completed
            task.status = AgentStatus.COMPLETED
            task.result = result
            task.completed_at = time.time()
            
            # Move to completed tasks
            self.task_queue.remove(task)
            self.completed_tasks.append(task)
            
            duration = task.completed_at - task.started_at
            print(f"✅ Completed: {task.task_id} (took {duration:.2f}s)")
            
            return True
            
        except Exception as e:
            task.status = AgentStatus.FAILED
            task.error = str(e)
            print(f"❌ Failed: {task.task_id} - {str(e)}")
            return False
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current status of the workflow"""
        total_tasks = len(self.task_queue) + len(self.completed_tasks)
        completed_count = len([t for t in self.completed_tasks if t.status == AgentStatus.COMPLETED])
        failed_count = len([t for t in self.completed_tasks if t.status == AgentStatus.FAILED])
        working_count = len([t for t in self.task_queue if t.status == AgentStatus.WORKING])
        
        return {
            "total_tasks": total_tasks,
            "completed": completed_count,
            "failed": failed_count,
            "working": working_count,
            "pending": len(self.task_queue) - working_count,
            "progress_percentage": (completed_count / total_tasks * 100) if total_tasks > 0 else 0
        }
    
    def save_workflow_state(self, filepath: str) -> None:
        """Save current workflow state to file"""
        state = {
            "task_queue": [self._task_to_dict(t) for t in self.task_queue],
            "completed_tasks": [self._task_to_dict(t) for t in self.completed_tasks],
            "timestamp": time.time()
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"💾 Workflow state saved to: {filepath}")
    
    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert task to dictionary for serialization"""
        return {
            "task_id": task.task_id,
            "agent_type": task.agent_type,
            "task_type": task.task_type,
            "description": task.description,
            "priority": task.priority,
            "dependencies": task.dependencies,
            "parameters": task.parameters,
            "status": task.status.value,
            "result": str(task.result) if task.result else None,
            "error": task.error,
            "created_at": task.created_at,
            "started_at": task.started_at,
            "completed_at": task.completed_at
        }

async def main():
    """Example usage of the Agent Orchestrator"""
    orchestrator = AgentOrchestrator()
    
    # Create Egyptian game development workflow
    task_ids = orchestrator.create_egyptian_game_workflow()
    
    # Execute the workflow
    success = await orchestrator.execute_workflow()
    
    # Get final status
    status = orchestrator.get_workflow_status()
    print(f"\n🏺 EGYPTIAN GAME WORKFLOW COMPLETE!")
    print(f"   Total tasks: {status['total_tasks']}")
    print(f"   Completed: {status['completed']}")
    print(f"   Failed: {status['failed']}")
    print(f"   Success rate: {status['progress_percentage']:.1f}%")
    
    # Save workflow state
    orchestrator.save_workflow_state("logs/workflow_state.json")

if __name__ == "__main__":
    asyncio.run(main())