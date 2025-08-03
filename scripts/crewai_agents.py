#!/usr/bin/env python3
"""
Sands of Duat CrewAI Multi-Agent Development System

Free local multi-agent setup for Egyptian roguelike game development.
Implements simultaneous collaboration between specialized agents.
"""

import os
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Configure local Ollama models for CrewAI
def get_local_llm(model_name):
    """Get local Ollama LLM instance for CrewAI."""
    try:
        # Try new langchain-ollama package first
        from langchain_ollama import OllamaLLM
        return OllamaLLM(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0.7,
            num_predict=2048,
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.1
        )
    except ImportError:
        # Fallback to langchain-community
        from langchain_community.llms import Ollama
        return Ollama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0.7,
            num_predict=2048,
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.1
        )

class SandsOfDuatAgentCrew:
    """Multi-agent crew for Sands of Duat development."""
    
    def __init__(self):
        # Initialize local LLMs with CrewAI-compatible configuration
        self.fast_llm = "ollama/llama3.1:8b"      # For UI/MCP agents
        self.smart_llm = "ollama/llama3.1:8b"     # For coordinator (will upgrade when 70B is available)
        self.code_llm = "ollama/llama3.1:8b"      # For code specialist (will use CodeLlama when available)
        
        # Initialize agents
        self.agents = self._create_agents()
        
        # Project context
        self.project_context = """
        Sands of Duat - Egyptian Roguelike Deck-Builder Game
        
        Current State:
        - Complete Egyptian-themed UI with warm sandstone palette
        - Interactive feedback system with golden glow effects
        - Information architecture reorganized with Egyptian temple chambers
        - Turn indicator as central obelisk with hieroglyphic symbols
        - Combat system with HourGlass Initiative timing
        - Deck building system with player collection management
        - Comprehensive accessibility features (colorblind support, font scaling)
        - MCP analysis integration for quality assurance
        
        Technology Stack:
        - Python 3.13 + Pygame for game engine
        - Ultrawide display support (3440x1440)
        - Component-based UI architecture
        - Egyptian theming with authentic cultural elements
        
        Development Philosophy:
        - Authentic Egyptian cultural representation
        - Accessibility-first design
        - MCP analysis for continuous quality improvement
        - Simultaneous multi-agent collaboration
        """
    
    def _create_agents(self):
        """Create specialized agents for Sands of Duat development."""
        
        # Egyptian UI/UX Specialist
        ui_specialist = Agent(
            role="Egyptian UI/UX Specialist",
            goal="Ensure authentic Egyptian theming and excellent user experience in Sands of Duat",
            backstory="""You are an expert in Egyptian art, architecture, and modern UI/UX design. 
            You have deep knowledge of hieroglyphic symbolism, temple architecture, and archaeological accuracy.
            Your specialty is creating immersive interfaces that respect Egyptian culture while providing 
            excellent usability. You understand the warm sandstone palette, obelisk turn indicators, 
            and canopic chamber information organization currently implemented.""",
            verbose=True,
            allow_delegation=False,
            llm=self.fast_llm,
            max_iter=3
        )
        
        # Gameplay Code Specialist
        code_specialist = Agent(
            role="Gameplay Code Specialist", 
            goal="Implement robust game mechanics and maintain high code quality for Sands of Duat",
            backstory="""You are a senior Python game developer with expertise in Pygame, 
            component-based architecture, and roguelike game mechanics. You understand the 
            HourGlass Initiative combat system, deck-building mechanics, and the importance 
            of performance optimization for ultrawide displays. You excel at writing clean, 
            maintainable code that integrates seamlessly with existing systems.""",
            verbose=True,
            allow_delegation=False,
            llm=self.code_llm,
            max_iter=3
        )
        
        # MCP Analysis Agent
        mcp_analyst = Agent(
            role="MCP Analysis Agent",
            goal="Provide continuous quality analysis and system integration oversight",
            backstory="""You are a quality assurance specialist focused on MCP (Model Context Protocol) 
            analysis for the Sands of Duat project. You analyze code quality, system integration, 
            performance metrics, and user experience consistency. You have deep knowledge of the 
            project's development history and excel at identifying optimization opportunities 
            and potential integration issues.""",
            verbose=True,
            allow_delegation=False,
            llm=self.fast_llm,
            max_iter=3
        )
        
        # Q&A Coordinator
        qa_coordinator = Agent(
            role="Q&A Coordinator",
            goal="Coordinate agent collaboration and synthesize recommendations for optimal development decisions",
            backstory="""You are the master coordinator for the Sands of Duat development team. 
            You excel at managing complex multi-agent workflows, resolving conflicts between 
            different perspectives, and synthesizing diverse expertise into actionable recommendations. 
            You understand the full scope of the Egyptian roguelike project and can balance 
            technical requirements with cultural authenticity and user experience goals.""",
            verbose=True,
            allow_delegation=True,
            llm=self.smart_llm,
            max_iter=5
        )
        
        return {
            'ui_specialist': ui_specialist,
            'code_specialist': code_specialist, 
            'mcp_analyst': mcp_analyst,
            'qa_coordinator': qa_coordinator
        }
    
    def create_development_task(self, user_request, task_type="general"):
        """Create a collaborative development task."""
        
        if task_type == "ui_enhancement":
            return self._create_ui_task(user_request)
        elif task_type == "code_development":
            return self._create_code_task(user_request)
        elif task_type == "analysis":
            return self._create_analysis_task(user_request)
        else:
            return self._create_general_task(user_request)
    
    def _create_ui_task(self, user_request):
        """Create UI enhancement task with agent collaboration."""
        
        # UI Specialist primary task
        ui_task = Task(
            description=f"""
            Analyze and plan UI enhancements for: {user_request}
            
            Context: {self.project_context}
            
            Your analysis should cover:
            1. Egyptian theming authenticity and consistency
            2. Visual hierarchy and information organization
            3. Accessibility considerations (colorblind support, font scaling)
            4. Integration with existing canopic chamber layout
            5. Cultural sensitivity and archaeological accuracy
            
            Provide specific recommendations with Egyptian design principles.
            """,
            agent=self.agents['ui_specialist'],
            expected_output="Detailed UI enhancement plan with Egyptian theming considerations"
        )
        
        # Code integration task
        code_task = Task(
            description=f"""
            Review UI enhancement plan and provide technical implementation strategy for: {user_request}
            
            Consider:
            1. Integration with existing component architecture
            2. Performance implications for ultrawide displays
            3. Compatibility with interactive feedback system
            4. Code maintainability and testing requirements
            
            Provide implementation roadmap and potential technical challenges.
            """,
            agent=self.agents['code_specialist'],
            expected_output="Technical implementation plan with code architecture considerations"
        )
        
        # Quality analysis task
        analysis_task = Task(
            description=f"""
            Conduct MCP analysis of proposed UI enhancements for: {user_request}
            
            Analyze:
            1. Quality metrics and improvement potential
            2. System integration implications
            3. User experience impact assessment
            4. Performance and accessibility compliance
            
            Provide quality assurance recommendations and metrics.
            """,
            agent=self.agents['mcp_analyst'],
            expected_output="Comprehensive quality analysis with metrics and recommendations"
        )
        
        # Coordination task
        coordination_task = Task(
            description=f"""
            Coordinate team recommendations for UI enhancement: {user_request}
            
            Synthesize input from:
            - UI Specialist: Egyptian theming and user experience analysis
            - Code Specialist: Technical implementation strategy
            - MCP Analyst: Quality metrics and integration assessment
            
            Provide:
            1. Unified implementation plan
            2. Priority recommendations
            3. Risk assessment and mitigation
            4. Final go/no-go decision with rationale
            
            Ensure all cultural, technical, and quality requirements are balanced.
            """,
            agent=self.agents['qa_coordinator'],
            expected_output="Coordinated implementation plan with prioritized recommendations"
        )
        
        return [ui_task, code_task, analysis_task, coordination_task]
    
    def _create_code_task(self, user_request):
        """Create code development task with agent collaboration."""
        
        # Code Specialist primary task
        code_task = Task(
            description=f"""
            Analyze and plan code implementation for: {user_request}
            
            Context: {self.project_context}
            
            Provide:
            1. Technical architecture design
            2. Integration with existing systems
            3. Performance optimization strategy
            4. Testing and validation approach
            
            Consider compatibility with Egyptian theming and UI components.
            """,
            agent=self.agents['code_specialist'],
            expected_output="Detailed technical implementation plan"
        )
        
        # UI integration review
        ui_task = Task(
            description=f"""
            Review code implementation plan from UI/UX perspective for: {user_request}
            
            Ensure:
            1. Compatibility with Egyptian theming system
            2. Proper integration with visual feedback
            3. Accessibility features maintained
            4. Cultural authenticity preserved
            
            Provide UI integration recommendations.
            """,
            agent=self.agents['ui_specialist'],
            expected_output="UI integration assessment and recommendations"
        )
        
        # Quality validation
        analysis_task = Task(
            description=f"""
            Validate code implementation plan through MCP analysis for: {user_request}
            
            Assess:
            1. Code quality and maintainability
            2. System architecture compliance
            3. Performance impact evaluation
            4. Integration risk assessment
            
            Provide validation metrics and recommendations.
            """,
            agent=self.agents['mcp_analyst'],
            expected_output="Code quality validation with metrics"
        )
        
        # Final coordination
        coordination_task = Task(
            description=f"""
            Coordinate technical implementation plan for: {user_request}
            
            Integrate feedback from:
            - Code Specialist: Technical architecture and implementation
            - UI Specialist: Visual integration and theming compatibility
            - MCP Analyst: Quality validation and risk assessment
            
            Deliver:
            1. Final implementation strategy
            2. Development sequence and priorities
            3. Quality gates and validation checkpoints
            4. Risk mitigation plan
            """,
            agent=self.agents['qa_coordinator'],
            expected_output="Final coordinated development plan"
        )
        
        return [code_task, ui_task, analysis_task, coordination_task]
    
    def _create_analysis_task(self, user_request):
        """Create analysis task with multi-perspective review."""
        
        # MCP Analyst primary task
        analysis_task = Task(
            description=f"""
            Conduct comprehensive MCP analysis for: {user_request}
            
            Context: {self.project_context}
            
            Analyze:
            1. Current system quality metrics
            2. Performance characteristics
            3. User experience indicators
            4. Technical debt assessment
            5. Optimization opportunities
            
            Provide detailed analysis with actionable recommendations.
            """,
            agent=self.agents['mcp_analyst'],
            expected_output="Comprehensive system analysis with metrics"
        )
        
        # UI perspective
        ui_review = Task(
            description=f"""
            Review analysis from UI/UX perspective for: {user_request}
            
            Focus on:
            1. Visual design effectiveness
            2. Egyptian theming consistency
            3. User experience optimization
            4. Accessibility compliance
            
            Provide UI-focused recommendations.
            """,
            agent=self.agents['ui_specialist'],
            expected_output="UI/UX analysis perspective"
        )
        
        # Technical perspective
        code_review = Task(
            description=f"""
            Review analysis from technical architecture perspective for: {user_request}
            
            Evaluate:
            1. Code architecture quality
            2. Performance optimization potential
            3. Maintainability factors
            4. Integration robustness
            
            Provide technical improvement recommendations.
            """,
            agent=self.agents['code_specialist'],
            expected_output="Technical architecture analysis"
        )
        
        # Coordinated synthesis
        coordination_task = Task(
            description=f"""
            Synthesize multi-perspective analysis for: {user_request}
            
            Integrate insights from:
            - MCP Analyst: System quality and performance metrics
            - UI Specialist: Visual design and user experience
            - Code Specialist: Technical architecture and maintainability
            
            Provide:
            1. Unified analysis summary
            2. Prioritized improvement recommendations
            3. Implementation roadmap
            4. Success metrics and validation criteria
            """,
            agent=self.agents['qa_coordinator'],
            expected_output="Synthesized multi-perspective analysis with action plan"
        )
        
        return [analysis_task, ui_review, code_review, coordination_task]
    
    def _create_general_task(self, user_request):
        """Create general collaborative task."""
        
        # General collaborative task
        main_task = Task(
            description=f"""
            Collaborative analysis and planning for: {user_request}
            
            Project Context: {self.project_context}
            
            Each agent should contribute their expertise:
            - UI Specialist: Egyptian theming and user experience
            - Code Specialist: Technical implementation and architecture
            - MCP Analyst: Quality metrics and system integration
            - Q&A Coordinator: Overall coordination and synthesis
            
            Provide comprehensive recommendations addressing all aspects.
            """,
            agent=self.agents['qa_coordinator'],
            expected_output="Comprehensive collaborative analysis and recommendations"
        )
        
        return [main_task]
    
    def run_collaborative_development(self, user_request, task_type="general"):
        """Execute collaborative development with simultaneous agents."""
        
        print(f"\n[START] Starting Sands of Duat Multi-Agent Development Session")
        print(f"[REQUEST] Request: {user_request}")
        print(f"[TYPE] Task Type: {task_type}")
        print(f"[AGENTS] Agents: UI Specialist, Code Specialist, MCP Analyst, Q&A Coordinator")
        print("=" * 70)
        
        # Create appropriate tasks
        tasks = self.create_development_task(user_request, task_type)
        
        # Create crew with all agents
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            verbose=True,
            process="sequential"
        )
        
        # Execute collaborative development
        try:
            result = crew.kickoff()
            
            print("\n" + "=" * 70)
            print("[COMPLETE] Multi-Agent Development Session Complete")
            print("[RESULTS] Results ready for implementation")
            
            return result
            
        except Exception as e:
            print(f"\n[ERROR] Error in multi-agent collaboration: {e}")
            return None

# Factory function for easy import
def create_sands_of_duat_crew():
    """Create and return a Sands of Duat development crew."""
    return SandsOfDuatAgentCrew()

if __name__ == "__main__":
    # Example usage
    crew = create_sands_of_duat_crew()
    
    # Test collaborative development
    result = crew.run_collaborative_development(
        "Enhance the deck builder screen with better card filtering and Egyptian-themed animations",
        task_type="ui_enhancement"
    )
    
    if result:
        print(f"\n[RESULT] Collaborative Result:\n{result}")