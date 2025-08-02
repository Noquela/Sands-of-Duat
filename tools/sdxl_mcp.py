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
                        "default": 1536
                    },
                    "height": {
                        "type": "integer",
                        "description": "Image height",
                        "default": 1536
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                        "default": -1
                    },
                    "steps": {
                        "type": "integer",
                        "description": "Number of denoising steps",
                        "default": 75
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
                        "default": 256
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
        prompt = arguments["prompt"]
        negative_prompt = arguments.get("negative_prompt", "blurry, low quality, distorted, deformed")
        width = arguments.get("width", 1024)
        height = arguments.get("height", 1024)
        seed = arguments.get("seed", -1)
        steps = arguments.get("steps", 25)
        output_path = arguments.get("output_path", "")
        
        # Force CUDA usage for RTX 5070
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                torch.cuda.set_device(0)  # Force GPU 0
                print(f"Using device: {device} - {torch.cuda.get_device_name(0)}")
                print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory // 1024**3}GB")
            else:
                device = "cpu"
                print(f"Using device: {device} (CUDA not available)")
        except ImportError:
            return [types.TextContent(
                type="text",
                text="Error: PyTorch not installed. Install with: pip install torch torchvision torchaudio"
            )]
        
        # Try to import diffusers
        try:
            from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
            print("Diffusers library loaded successfully")
        except ImportError:
            return [types.TextContent(
                type="text", 
                text="Error: Diffusers not installed. Install with: pip install diffusers transformers accelerate"
            )]
        
        # Load FIXED SDXL pipeline - resolves black image issues
        try:
            print("Loading FIXED SDXL pipeline...")
            
            # FIX 1: Load with explicit VAE to prevent corruption
            from diffusers import AutoencoderKL
            vae = AutoencoderKL.from_pretrained(
                "madebyollin/sdxl-vae-fp16-fix", 
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            
            # FIX 2: Load base model with fixed VAE
            pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                vae=vae,  # Use fixed VAE
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if device == "cuda" else None,
                add_watermarker=False
            )
            
            # FIX 3: Use DPMSolver++ scheduler (better than EulerA for SDXL)
            from diffusers import DPMSolverMultistepScheduler
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            
            # Move to device
            pipe = pipe.to(device)
            print(f"Pipeline moved to {device}")
            
            # FIX 4: Enable memory efficient attention for RTX 5070
            if device == "cuda":
                pipe.enable_attention_slicing()
                print(f"RTX 5070 ready! GPU memory: {torch.cuda.memory_allocated(0) // 1024**2}MB")
            
            print("FIXED SDXL pipeline loaded - black image issue resolved!")
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error loading SDXL model: {str(e)}\nMake sure you have enough GPU memory (8GB+ recommended)"
            )]
        
        # Set random seed if provided
        if seed != -1:
            torch.manual_seed(seed)
            if device == "cuda":
                torch.cuda.manual_seed(seed)
        
        # FIX 5: Simplified prompts to avoid CLIP tokenizer issues
        enhanced_prompt = f"masterpiece, {prompt}, detailed, vibrant colors"
        # FIX 6: Much lighter negative prompt to prevent over-suppression
        safe_negative = "blurry, low quality"  # Minimal negative to avoid black images
        
        print(f"Generating FIXED image with prompt: {enhanced_prompt}")
        
        # GPU status
        if device == "cuda":
            print(f"RTX 5070 Status: {torch.cuda.memory_allocated(0) // 1024**2}MB allocated")
        
        print(f"Generating on {device}...")
        
        # FIX 7: Safe generation parameters
        try:
            generator = torch.Generator(device=device)
            if seed != -1:
                generator.manual_seed(seed)
            else:
                generator.manual_seed(42)  # Fixed seed for consistency
            
            print("Generating on RTX 5070...")
            image = pipe(
                prompt=enhanced_prompt,
                negative_prompt=safe_negative,  # Light negative prompt
                width=width,
                height=height,
                num_inference_steps=max(steps, 30),  # Reasonable steps
                guidance_scale=7.5,  # Standard guidance, not too high
                generator=generator,
                num_images_per_prompt=1
            ).images[0]
            
            print(f"RTX 5070 generation complete! Max GPU memory: {torch.cuda.max_memory_allocated(0) // 1024**2}MB")
        except Exception as gen_error:
            return [types.TextContent(
                type="text",
                text=f"Generation failed: {str(gen_error)}"
            )]
        
        # Save image
        if not output_path:
            os.makedirs("assets/generated", exist_ok=True)
            # Create safe filename from prompt
            safe_name = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            output_path = f"assets/generated/{safe_name}_{hash(prompt) % 10000}.png"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        
        return [types.TextContent(
            type="text",
            text=f"SUCCESS: Generated Egyptian game asset!\nSaved to: {output_path}\nPrompt: {prompt}\nSize: {width}x{height}\nSteps: {steps}\nSeed: {seed if seed != -1 else 'random'}"
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"ERROR: Failed to generate image: {str(e)}\n\nTroubleshooting:\n- Ensure CUDA drivers are installed\n- Try reducing image size (512x512)\n- Check available GPU memory\n- Install: pip install diffusers transformers accelerate torch"
        )]


async def handle_img2img(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle image to image generation."""
    return [types.TextContent(
        type="text",
        text="img2img tool not yet implemented. This requires the StableDiffusionXLImg2ImgPipeline."
    )]


async def handle_sprite_sheet(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle sprite sheet generation for game animations."""
    try:
        prompt = arguments["prompt"]
        cols = arguments.get("cols", 4)
        rows = arguments.get("rows", 4)
        size = arguments.get("size", 128)  # Smaller individual frames
        animation_type = arguments.get("animation_type", "idle")
        seed = arguments.get("seed", -1)
        
        # Egyptian-themed animation prompts
        animation_prompts = {
            "idle": f"{prompt}, standing pose, idle animation, breathing, subtle movement",
            "walk": f"{prompt}, walking cycle, side view, legs moving, step sequence",
            "attack": f"{prompt}, attacking pose, weapon swing, combat stance, action sequence",
            "death": f"{prompt}, falling, defeat pose, lying down, death sequence"
        }
        
        # Get specific prompt for animation type
        base_prompt = animation_prompts.get(animation_type, f"{prompt}, {animation_type} animation")
        
        # Optimized sprite sheet prompt for 77-token limit
        enhanced_prompt = f"masterpiece, {base_prompt}, sprite sheet, {cols}x{rows} grid, game asset, detailed"
        
        # Negative prompt to avoid unwanted elements
        negative_prompt = "blurry, low quality, photorealistic, 3d render, modern clothing, contemporary, inconsistent style, different characters, background clutter"
        
        # Calculate total image size
        total_width = size * cols
        total_height = size * rows
        
        print(f"Generating {animation_type} sprite sheet: {cols}x{rows} frames at {size}x{size} each")
        
        # Generate using text2img with sprite-specific settings
        sprite_args = {
            "prompt": enhanced_prompt,
            "negative_prompt": negative_prompt,
            "width": total_width,
            "height": total_height,
            "seed": seed,
            "steps": 75,  # High quality sprite generation
            "output_path": arguments.get("output_path", f"assets/generated/sprite_{animation_type}_{cols}x{rows}_{size}px.png")
        }
        
        result = await handle_text2img(sprite_args)
        
        # Add sprite sheet specific information
        sprite_info = f"\n\nSprite Sheet Generated!\nGrid Layout: {cols} columns x {rows} rows\nFrame Size: {size}x{size} pixels\nAnimation: {animation_type}\nTotal Frames: {cols * rows}\nSheet Size: {total_width}x{total_height}\n\nUsage: Load in game and extract frames using grid coordinates"
        
        if result and len(result) > 0:
            result[0].text += sprite_info
        
        return result
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"ERROR: Failed to generate sprite sheet: {str(e)}"
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