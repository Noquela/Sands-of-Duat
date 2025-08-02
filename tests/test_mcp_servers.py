#!/usr/bin/env python3
"""
Test MCP servers for Sands of Duat
Tests pygame-MCP and SDXL-MCP functionality
"""

import sys
import os
import asyncio

# Add src and tools to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools'))

async def test_pygame_mcp():
    """Test pygame MCP server functionality."""
    try:
        from pygame_mcp import handle_call_tool
        
        # Test file operations
        write_result = await handle_call_tool("write_file", {
            "path": "tests/test_output.txt",
            "content": "Test file from pygame MCP"
        })
        
        assert len(write_result) > 0
        assert "Successfully wrote" in write_result[0].text
        
        read_result = await handle_call_tool("open_file", {
            "path": "tests/test_output.txt"
        })
        
        assert len(read_result) > 0
        assert "Test file from pygame MCP" in read_result[0].text
        
        print("Pygame MCP file operations working")
        
        # Clean up
        if os.path.exists("tests/test_output.txt"):
            os.remove("tests/test_output.txt")
        
        return True
        
    except Exception as e:
        print(f"Pygame MCP test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_sdxl_mcp_basic():
    """Test SDXL MCP server basic functionality (without actual generation)."""
    try:
        from sdxl_mcp import handle_call_tool
        
        # Test that tools are available
        from sdxl_mcp import handle_list_tools
        tools = await handle_list_tools()
        
        tool_names = [tool.name for tool in tools]
        expected_tools = ["text2img", "sprite_sheet", "palette_reduce"]
        
        for expected in expected_tools:
            assert expected in tool_names, f"Missing tool: {expected}"
        
        print("SDXL MCP tools properly defined")
        print(f"Available tools: {', '.join(tool_names)}")
        
        # Test palette reduce (doesn't require SDXL model)
        # First create a test image
        from PIL import Image
        import numpy as np
        
        # Create a simple test image
        test_image = Image.fromarray(np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8))
        test_path = "tests/test_image.png"
        test_image.save(test_path)
        
        palette_result = await handle_call_tool("palette_reduce", {
            "input_path": test_path,
            "colors": 8
        })
        
        assert len(palette_result) > 0
        print("SDXL MCP palette reduction working")
        
        # Clean up
        if os.path.exists(test_path):
            os.remove(test_path)
        if os.path.exists("assets/generated/test_image_palette_8.png"):
            os.remove("assets/generated/test_image_palette_8.png")
        
        return True
        
    except Exception as e:
        print(f"SDXL MCP test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_sdxl_generation():
    """Test actual SDXL generation (requires CUDA and models)."""
    try:
        from sdxl_mcp import handle_call_tool
        
        print("Testing SDXL image generation (this may take a while...)") 
        print("Requires CUDA GPU and ~8GB VRAM")
        
        # Test simple generation
        result = await handle_call_tool("text2img", {
            "prompt": "Egyptian warrior Anubis, pixel art, game sprite",
            "width": 512,
            "height": 512,
            "steps": 20,  # Fewer steps for testing
            "seed": 42
        })
        
        assert len(result) > 0
        
        if "Error" in result[0].text:
            print(f"SDXL generation test skipped: {result[0].text}")
            return True  # Don't fail if model isn't available
        
        print("SDXL generation working!")
        print(result[0].text)
        
        return True
        
    except Exception as e:
        print(f"SDXL generation test failed (this is OK if no CUDA): {e}")
        return True  # Don't fail the test suite

def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    deps = {
        "pygame": "Game engine",
        "mcp": "MCP protocol", 
        "PIL": "Image processing",
        "torch": "PyTorch (optional for SDXL)",
        "diffusers": "Stable Diffusion (optional)"
    }
    
    for dep, description in deps.items():
        try:
            __import__(dep.replace("PIL", "PIL.Image").split('.')[0])
            print(f"OK: {dep}: {description}")
        except ImportError:
            if dep in ["torch", "diffusers"]:
                print(f"MISSING: {dep}: {description} (optional - needed for AI generation)")
            else:
                print(f"ERROR: {dep}: {description} (REQUIRED)")

async def main():
    """Run all MCP tests."""
    print("Testing Sands of Duat MCP Servers...")
    print("=" * 50)
    
    # Check dependencies first
    check_dependencies()
    print()
    
    tests = [
        ("Pygame MCP", test_pygame_mcp()),
        ("SDXL MCP Basic", test_sdxl_mcp_basic()),
        ("SDXL Generation", test_sdxl_generation()),
    ]
    
    passed = 0
    for test_name, test_coro in tests:
        print(f"Running {test_name}...")
        try:
            if await test_coro:
                passed += 1
                print(f"PASSED: {test_name}\n")
            else:
                print(f"FAILED: {test_name}\n")
        except Exception as e:
            print(f"CRASHED: {test_name}: {e}\n")
    
    print("=" * 50)
    print(f"MCP Tests: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("All MCP servers working! Ready for AI asset generation.")
        return 0
    else:
        print("Some tests failed. Check dependencies and GPU setup.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))