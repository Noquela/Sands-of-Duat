"""
Multi-Agent Development System para Sands of Duat
Usando Qwen-2.5-Coder 14B-Instruct via Ollama

Sistema de agentes especializados:
- UI Agent: Interface e UX
- Code Agent: Implementação e lógica
- QA Agent: Qualidade e testes
"""

import os
import sys
import time
import json
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime

# Adicionar o path do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from crewai import Agent, Task, Crew, Process
    from crewai.llm import LLM
    import torch
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Install with: pip install crewai torch")
    sys.exit(1)


class AgentManager:
    """Gerenciador dos agentes CrewAI para desenvolvimento do jogo."""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "deepseek-coder:6.7b-instruct"  # Using available model
        self.llm = None
        self.agents = {}
        self.crew = None
        
        # Configurações de VRAM
        self.max_vram_gb = 11.5
        self.context_limit = 4096
        
        self._init_llm()
        self._create_agents()
    
    def _init_llm(self):
        """Inicializa a conexão com Ollama."""
        print("Iniciando conexão com Qwen-2.5-Coder...")
        
        # Verificar se Ollama está rodando
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if self.model_name not in result.stdout:
                print(f"Modelo {self.model_name} não encontrado. Baixando...")
                subprocess.run(['ollama', 'pull', self.model_name], check=True)
        except subprocess.CalledProcessError:
            print("Ollama não está rodando. Execute: ollama serve")
            sys.exit(1)
        
        # Configurar LLM
        self.llm = LLM(
            model=f"ollama/{self.model_name}",
            base_url=self.base_url,
            temperature=0.4
        )
        
        print("Qwen-2.5-Coder conectado!")
    
    def _create_agents(self):
        """Cria os agentes especializados."""
        
        # UI/UX Agent - Especialista em interface e experiência do usuário
        self.agents['ui'] = Agent(
            role='UI/UX Specialist',
            goal='Design and implement intuitive, responsive user interfaces for the Hour-Glass Initiative card game',
            backstory="""You are a senior UI/UX developer specializing in game interfaces. 
            You understand the unique challenges of real-time card games and the Hour-Glass Initiative system.
            Your expertise includes pygame UI components, responsive layouts, visual feedback systems, and accessibility.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
        
        # Code Agent - Especialista em implementação e arquitetura
        self.agents['code'] = Agent(
            role='Senior Game Developer',
            goal='Implement robust, performant game systems and mechanics for the Hour-Glass Initiative system',
            backstory="""You are a senior game developer with expertise in Python, pygame, and real-time systems.
            You specialize in the Hour-Glass Initiative mechanics, action queues, timing systems, and combat mechanics.
            You write clean, documented code with proper error handling and performance optimization.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
        
        # QA Agent - Especialista em qualidade e testes
        self.agents['qa'] = Agent(
            role='QA Engineer & Game Tester',
            goal='Ensure code quality, performance, and gameplay balance for the Hour-Glass Initiative system',
            backstory="""You are a QA engineer specializing in game testing and code quality.
            You understand the Hour-Glass Initiative mechanics and can identify bugs, performance issues, and balance problems.
            You write comprehensive tests and provide detailed feedback on gameplay feel and technical implementation.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
        
        print("Agentes criados: UI, Code, QA")
    
    def check_vram_usage(self) -> float:
        """Verifica uso atual da VRAM."""
        try:
            if torch.cuda.is_available():
                vram_used = torch.cuda.memory_allocated() / (1024**3)  # GB
                return vram_used
            return 0.0
        except:
            return 0.0
    
    def create_task(self, task_type: str, description: str, context: str = "") -> Task:
        """Cria uma task específica para um agente."""
        
        if task_type == "ui":
            return Task(
                description=f"""
                UI/UX Task: {description}
                
                Context: {context}
                
                Requirements:
                - Design responsive UI components for 3440x1440 resolution
                - Implement intuitive Hour-Glass Initiative feedback
                - Ensure 60+ FPS performance
                - Follow Egyptian theme consistency
                - Include proper accessibility features
                
                Deliverables:
                - Python code with pygame components
                - Visual mockups if needed
                - Implementation notes
                """,
                agent=self.agents['ui'],
                expected_output="Complete UI implementation with code and documentation"
            )
        
        elif task_type == "code":
            return Task(
                description=f"""
                Development Task: {description}
                
                Context: {context}
                
                Requirements:
                - Implement Hour-Glass Initiative mechanics
                - Ensure cast time and queue systems work properly
                - Sand regeneration: 2 seconds per grain
                - Double-click card queueing
                - Proper error handling and logging
                - Performance optimization for 60+ FPS
                
                Deliverables:
                - Complete Python implementation
                - Docstrings and type hints
                - Unit tests where applicable
                """,
                agent=self.agents['code'],
                expected_output="Production-ready code with tests and documentation"
            )
        
        elif task_type == "qa":
            return Task(
                description=f"""
                QA Task: {description}
                
                Context: {context}
                
                Requirements:
                - Test Hour-Glass Initiative mechanics
                - Verify cast time and queue functionality
                - Check performance (60+ FPS @ 3440x1440)
                - Validate game balance and feel
                - Identify bugs and edge cases
                
                Deliverables:
                - Test results and bug reports
                - Performance analysis
                - Gameplay feedback
                - Improvement recommendations
                """,
                agent=self.agents['qa'],
                expected_output="Comprehensive QA report with actionable feedback"
            )
        
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    def execute_development_cycle(self, feature_description: str, context: str = "") -> Dict[str, Any]:
        """Executa um ciclo completo de desenvolvimento com os agentes."""
        
        print(f"\nIniciando ciclo de desenvolvimento: {feature_description}")
        
        # Verificar VRAM antes de começar
        vram_usage = self.check_vram_usage()
        if vram_usage > self.max_vram_gb:
            print(f"VRAM usage too high: {vram_usage:.1f}GB > {self.max_vram_gb}GB")
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                print("GPU cache cleared")
        
        # Criar tasks para cada agente
        tasks = [
            self.create_task("ui", f"UI implementation for: {feature_description}", context),
            self.create_task("code", f"Core implementation for: {feature_description}", context),
            self.create_task("qa", f"QA validation for: {feature_description}", context)
        ]
        
        # Criar crew com processo sequencial
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        print("Executando agentes em sequência...")
        start_time = time.time()
        
        try:
            result = crew.kickoff()
            execution_time = time.time() - start_time
            
            print(f"Ciclo completo em {execution_time:.1f}s")
            
            # Verificar VRAM final
            final_vram = self.check_vram_usage()
            print(f"VRAM final: {final_vram:.1f}GB")
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'vram_usage': final_vram,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Erro durante execução: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def quick_fix(self, issue_description: str, agent_type: str = "code") -> str:
        """Executa uma correção rápida com um agente específico."""
        
        print(f"Quick fix com agente {agent_type}: {issue_description}")
        
        task = self.create_task(agent_type, f"Quick fix: {issue_description}", "")
        
        # Crew com apenas um agente
        crew = Crew(
            agents=[self.agents[agent_type]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        try:
            result = crew.kickoff()
            print("Quick fix completo")
            return result
        except Exception as e:
            print(f"Erro no quick fix: {e}")
            return f"Error: {e}"


def main():
    """Função principal para testes do sistema de agentes."""
    
    print("Sands of Duat - Multi-Agent Development System")
    print("=" * 60)
    
    # Inicializar manager
    manager = AgentManager()
    
    # Exemplo de uso
    feature = "Fix Hour-Glass Initiative queue display and card selection issues"
    context = """
    Current issues:
    1. Cards not showing in queue after double-click
    2. Card information panel not displaying properly
    3. Sand regeneration rate needs to be 2 seconds per grain
    4. Need to implement in main game (not just test screen)
    
    Current files:
    - dynamic_combat_screen.py: Dynamic combat UI
    - action_queue.py: Queue system implementation
    - hourglass.py: Sand regeneration system
    - cards.py: Card data models
    """
    
    result = manager.execute_development_cycle(feature, context)
    
    if result['success']:
        print("\nRESULTADO:")
        print(result['result'])
    else:
        print(f"\nFALHA: {result['error']}")


if __name__ == "__main__":
    main()