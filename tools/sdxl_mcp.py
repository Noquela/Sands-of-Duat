#!/usr/bin/env python3
"""
SDXL MCP Server
Provides tools for generating Egyptian-themed game assets using Stable Diffusion XL
"""

import asyncio
import base64
import io
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types


app = Server("sdxl-mcp")


@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="text2img",
            description="Generate image from text prompt using SDXL",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text prompt for image generation"
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "Negative prompt (what to avoid)",
                        "default": "blurry, low quality, distorted"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Image width",
                        "default": 1024
                    },
                    "height": {
                        "type": "integer",
                        "description": "Image height",
                        "default": 1024
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                        "default": -1
                    },
                    "steps": {
                        "type": "integer",
                        "description": "Number of denoising steps",
                        "default": 25
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path (default: assets/generated/)",
                        "default": ""
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="img2img",
            description="Generate image from existing image and text prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text prompt for image generation"
                    },
                    "input_image": {
                        "type": "string",
                        "description": "Path to input image"
                    },
                    "strength": {
                        "type": "number",
                        "description": "Transformation strength (0.0-1.0)",
                        "default": 0.7
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "Negative prompt",
                        "default": "blurry, low quality, distorted"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path",
                        "default": ""
                    }
                },
                "required": ["prompt", "input_image"]
            }
        ),
        Tool(
            name="sprite_sheet",
            description="Generate sprite sheet for game animations",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Base prompt for sprite generation"
                    },
                    "cols": {
                        "type": "integer",
                        "description": "Number of columns",
                        "default": 4
                    },
                    "rows": {
                        "type": "integer",
                        "description": "Number of rows",
                        "default": 4
                    },
                    "size": {
                        "type": "integer",
                        "description": "Size of each sprite frame",
                        "default": 512
                    },
                    "animation_type": {
                        "type": "string",
                        "description": "Animation type (idle, walk, attack, etc.)",
                        "default": "idle"
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed",
                        "default": -1
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path",
                        "default": ""
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="palette_reduce",
            description="Reduce color palette for pixel art style",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to input image"
                    },
                    "colors": {
                        "type": "integer",
                        "description": "Number of colors in palette",
                        "default": 16
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path",
                        "default": ""
                    }
                },
                "required": ["input_path"]
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "text2img":
            return await handle_text2img(arguments)
        elif name == "img2img":
            return await handle_img2img(arguments)
        elif name == "sprite_sheet":
            return await handle_sprite_sheet(arguments)
        elif name == "palette_reduce":
            return await handle_palette_reduce(arguments)
        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
            
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error in {name}: {str(e)}"
        )]


async def handle_text2img(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle text to image generation."""
    try:
        # Import here to avoid loading heavy libraries at startup
        import torch
        from diffusers import StableDiffusionXLPipeline
        
        prompt = arguments["prompt"]
        negative_prompt = arguments.get("negative_prompt", "blurry, low quality, distorted")
        width = arguments.get("width", 1024)
        height = arguments.get("height", 1024)
        seed = arguments.get("seed", -1)
        steps = arguments.get("steps", 25)
        output_path = arguments.get("output_path", "")
        
        # Setup device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load pipeline (this might take time on first run)
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_safetensors=True
        )
        pipe = pipe.to(device)
        
        # Set random seed if provided
        if seed != -1:
            torch.manual_seed(seed)
        
        # Generate image
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps
        ).images[0]
        
        # Save image
        if not output_path:
            os.makedirs("assets/generated", exist_ok=True)
            output_path = f"assets/generated/text2img_{hash(prompt) % 10000}.png"
        
        image.save(output_path)
        
        return [types.TextContent(
            type="text",
            text=f"Generated image saved to: {output_path}\nPrompt: {prompt}\nSize: {width}x{height}\nSteps: {steps}"
        )]
        
    except ImportError:
        return [types.TextContent(
            type="text",
            text="Error: Required libraries not installed. Install with: pip install diffusers transformers torch"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error generating image: {str(e)}"
        )]


async def handle_img2img(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle image to image generation."""
    return [types.TextContent(
        type="text",
        text="img2img tool not yet implemented. This requires the StableDiffusionXLImg2ImgPipeline."
    )]


async def handle_sprite_sheet(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle sprite sheet generation."""
    try:
        prompt = arguments["prompt"]
        cols = arguments.get("cols", 4)
        rows = arguments.get("rows", 4)
        size = arguments.get("size", 512)
        animation_type = arguments.get("animation_type", "idle")
        
        # Enhanced prompt for sprite generation
        enhanced_prompt = f"{prompt}, {animation_type} animation frames, sprite sheet, game asset, pixel art style, clean background, consistent character design, Egyptian mythology"
        
        # Generate using text2img with sprite-specific settings
        sprite_args = {
            "prompt": enhanced_prompt,
            "width": size * cols,
            "height": size * rows,
            "seed": arguments.get("seed", -1),
            "steps": 30,  # More steps for better quality
            "output_path": arguments.get("output_path", f"assets/generated/sprite_{animation_type}_{cols}x{rows}.png")
        }
        
        result = await handle_text2img(sprite_args)
        
        # Add sprite sheet specific information
        sprite_info = f"\nSprite Sheet Info:\n- Grid: {cols}x{rows}\n- Frame size: {size}x{size}\n- Animation: {animation_type}\n- Total frames: {cols * rows}"
        
        if result:
            result[0].text += sprite_info
        
        return result
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error generating sprite sheet: {str(e)}"
        )]


async def handle_palette_reduce(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle color palette reduction."""
    try:
        from PIL import Image
        import numpy as np
        
        input_path = arguments["input_path"]
        colors = arguments.get("colors", 16)
        output_path = arguments.get("output_path", "")
        
        if not os.path.exists(input_path):
            return [types.TextContent(
                type="text",
                text=f"Error: Input image '{input_path}' not found"
            )]
        
        # Load image
        image = Image.open(input_path).convert("RGB")
        
        # Reduce palette using PIL's quantize
        quantized = image.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
        result_image = quantized.convert("RGB")
        
        # Save result
        if not output_path:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"assets/generated/{base_name}_palette_{colors}.png"
        
        result_image.save(output_path)
        
        return [types.TextContent(
            type="text",
            text=f"Palette reduced image saved to: {output_path}\nColors: {colors}\nOriginal size: {image.size}"
        )]
        
    except ImportError:
        return [types.TextContent(
            type="text",
            text="Error: PIL (Pillow) not installed. Install with: pip install Pillow"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error reducing palette: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sdxl-mcp",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())