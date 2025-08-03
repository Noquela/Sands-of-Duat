#!/usr/bin/env python3
"""
Test CrewAI Setup for Sands of Duat

Simple test to verify the local multi-agent system is working.
"""

import sys
import os

# Add the scripts directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from crewai_agents import create_sands_of_duat_crew
    print("[OK] CrewAI agents imported successfully")
except ImportError as e:
    print(f"[ERROR] Error importing CrewAI agents: {e}")
    sys.exit(1)

def test_ollama_connection():
    """Test connection to local Ollama."""
    try:
        # Try new langchain-ollama package first
        try:
            from langchain_ollama import OllamaLLM
            llm = OllamaLLM(model="llama3.1:8b", base_url="http://localhost:11434")
        except ImportError:
            from langchain_community.llms import Ollama
            llm = Ollama(model="llama3.1:8b", base_url="http://localhost:11434")
        
        # Simple test prompt
        response = llm.invoke("Hello, this is a test. Please respond with 'Connection successful!'")
        print(f"[OK] Ollama connection test: {response}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Ollama connection failed: {e}")
        return False

def test_agent_creation():
    """Test agent creation."""
    try:
        crew = create_sands_of_duat_crew()
        
        agents = crew.agents
        print(f"[OK] Created {len(agents)} agents:")
        for name, agent in agents.items():
            print(f"   - {name}: {agent.role}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Agent creation failed: {e}")
        return False

def test_simple_collaboration():
    """Test simple multi-agent collaboration."""
    try:
        print("\n[TEST] Testing Simple Multi-Agent Collaboration...")
        
        crew = create_sands_of_duat_crew()
        
        # Simple test request
        result = crew.run_collaborative_development(
            "Analyze the current Egyptian theming quality in Sands of Duat",
            task_type="analysis"
        )
        
        if result:
            print("[OK] Multi-agent collaboration test successful")
            return True
        else:
            print("[ERROR] Multi-agent collaboration returned no result")
            return False
            
    except Exception as e:
        print(f"[ERROR] Multi-agent collaboration failed: {e}")
        return False

def main():
    """Run all tests."""
    print("[TEST] Testing CrewAI Setup for Sands of Duat")
    print("=" * 50)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Agent Creation", test_agent_creation),
        ("Simple Collaboration", test_simple_collaboration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n[RUN] Running {test_name} test...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"[CRASH] {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("[SUMMARY] Test Results Summary:")
    
    passed = 0
    for test_name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"   {status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n[OVERALL] Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("[SUCCESS] CrewAI setup is ready for Sands of Duat development!")
        return True
    else:
        print("[WARNING] Some tests failed. Please check the setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)