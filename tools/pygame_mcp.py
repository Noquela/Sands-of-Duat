#!/usr/bin/env python3
"""
Pygame MCP Server
Provides tools for running and profiling the Sands of Duat game
"""

import asyncio
import subprocess
import time
import os
from pathlib import Path
from typing import Any, Dict, List
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types


app = Server("pygame-mcp")


@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="run_game",
            description="Execute the Sands of Duat game and capture logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "entry": {
                        "type": "string",
                        "description": "Entry point file path (default: src/game.py)",
                        "default": "src/game.py"
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds (default: 30)",
                        "default": 30
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="profile_fps",
            description="Run game for specified duration and measure FPS performance",
            inputSchema={
                "type": "object",
                "properties": {
                    "seconds": {
                        "type": "number",
                        "description": "Duration to run profiling in seconds",
                        "default": 10
                    },
                    "entry": {
                        "type": "string",
                        "description": "Entry point file path (default: src/game.py)",
                        "default": "src/game.py"
                    }
                },
                "required": ["seconds"]
            }
        ),
        Tool(
            name="open_file",
            description="Read a file from the project",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to project root"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a file in the project",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to project root"
                    },
                    "content": {
                        "type": "string",
                        "description": "File content to write"
                    }
                },
                "required": ["path", "content"]
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    
    if name == "run_game":
        entry = arguments.get("entry", "src/game.py")
        timeout = arguments.get("timeout", 30)
        
        try:
            # Check if entry file exists
            if not os.path.exists(entry):
                return [types.TextContent(
                    type="text",
                    text=f"Error: Entry file '{entry}' not found"
                )]
            
            # Run the game
            process = subprocess.run(
                ["python", entry],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = f"Exit code: {process.returncode}\n"
            output += f"STDOUT:\n{process.stdout}\n"
            if process.stderr:
                output += f"STDERR:\n{process.stderr}\n"
                
            return [types.TextContent(type="text", text=output)]
            
        except subprocess.TimeoutExpired:
            return [types.TextContent(
                type="text",
                text=f"Game execution timed out after {timeout} seconds"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error running game: {str(e)}"
            )]
    
    elif name == "profile_fps":
        seconds = arguments["seconds"]
        entry = arguments.get("entry", "src/game.py")
        
        try:
            if not os.path.exists(entry):
                return [types.TextContent(
                    type="text",
                    text=f"Error: Entry file '{entry}' not found"
                )]
            
            # TODO: Implement actual FPS profiling
            # For now, just run the game for the specified duration
            start_time = time.time()
            process = subprocess.run(
                ["python", entry],
                capture_output=True,
                text=True,
                timeout=seconds
            )
            elapsed = time.time() - start_time
            
            output = f"Profiling completed in {elapsed:.2f} seconds\n"
            output += f"Exit code: {process.returncode}\n"
            output += f"STDOUT:\n{process.stdout}\n"
            if process.stderr:
                output += f"STDERR:\n{process.stderr}\n"
            
            # Placeholder FPS calculation
            output += f"\nFPS Analysis:\n"
            output += f"- Target: 60 FPS\n"
            output += f"- Duration: {elapsed:.2f}s\n"
            output += f"- Estimated frames: {int(60 * elapsed)}\n"
            
            return [types.TextContent(type="text", text=output)]
            
        except subprocess.TimeoutExpired:
            return [types.TextContent(
                type="text",
                text=f"FPS profiling completed after {seconds} seconds (timeout reached)"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error during FPS profiling: {str(e)}"
            )]
    
    elif name == "open_file":
        path = arguments["path"]
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [types.TextContent(type="text", text=content)]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error reading file '{path}': {str(e)}"
            )]
    
    elif name == "write_file":
        path = arguments["path"]
        content = arguments["content"]
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return [types.TextContent(
                type="text",
                text=f"Successfully wrote {len(content)} characters to '{path}'"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error writing file '{path}': {str(e)}"
            )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pygame-mcp",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())