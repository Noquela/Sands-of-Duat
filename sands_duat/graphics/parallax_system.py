#!/usr/bin/env python3
"""
Parallax Background System for Sands of Duat
Creates atmospheric depth through layered backgrounds with Hades-style visual flair.
"""

import pygame
import math
from typing import List, Tuple, Optional
from pathlib import Path

class ParallaxLayer:
    """Individual parallax layer with independent movement and effects."""
    
    def __init__(self, image_path: str, scroll_speed: float, 
                 alpha: int = 255, blend_mode: int = pygame.BLEND_ALPHA_SDL2):
        """
        Initialize a parallax layer.
        
        Args:
            image_path: Path to the layer image
            scroll_speed: Movement speed (0.0 = static, 1.0 = normal speed)
            alpha: Transparency (0-255)
            blend_mode: Pygame blend mode for atmospheric effects
        """
        self.image_path = image_path
        self.scroll_speed = scroll_speed
        self.alpha = alpha
        self.blend_mode = blend_mode
        
        # Load and prepare image
        self.original_image = None
        self.image = None
        self.load_image()
        
        # Position and movement
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.auto_scroll_x = 0.0  # Automatic horizontal scrolling
        self.auto_scroll_y = 0.0  # Automatic vertical scrolling
        
        # Visual effects
        self.wave_amplitude = 0.0  # Vertical wave motion
        self.wave_frequency = 0.0  # Wave frequency
        self.wave_time = 0.0       # Wave animation time
    
    def load_image(self):
        """Load and prepare the layer image."""
        try:
            if Path(self.image_path).exists():
                self.original_image = pygame.image.load(self.image_path).convert_alpha()
                self.image = self.original_image.copy()
                self.image.set_alpha(self.alpha)
            else:
                # Create a placeholder if image doesn't exist
                self.original_image = pygame.Surface((1920, 1080), pygame.SRCALPHA)
                self.original_image.fill((0, 0, 0, 50))  # Semi-transparent black
                self.image = self.original_image.copy()
                print(f"Warning: Parallax layer image not found: {self.image_path}")
        except Exception as e:
            print(f"Error loading parallax layer {self.image_path}: {e}")
            self.original_image = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            self.image = self.original_image.copy()
    
    def update(self, dt: float, camera_x: float = 0, camera_y: float = 0):
        """Update layer position and effects."""
        # Camera-based parallax movement
        self.x_offset = camera_x * self.scroll_speed
        self.y_offset = camera_y * self.scroll_speed
        
        # Automatic scrolling (for atmospheric movement)
        self.x_offset += self.auto_scroll_x * dt
        self.y_offset += self.auto_scroll_y * dt
        
        # Wave motion for atmospheric effects
        if self.wave_amplitude > 0:
            self.wave_time += dt
            wave_offset = math.sin(self.wave_time * self.wave_frequency) * self.wave_amplitude
            self.y_offset += wave_offset
    
    def render(self, surface: pygame.Surface, screen_width: int, screen_height: int):
        """Render the parallax layer."""
        if not self.image:
            return
        
        layer_width = self.image.get_width()
        layer_height = self.image.get_height()
        
        # Calculate how many tiles we need to cover the screen
        tiles_x = math.ceil(screen_width / layer_width) + 1
        tiles_y = math.ceil(screen_height / layer_height) + 1
        
        # Calculate starting positions with wrapping
        start_x = -(self.x_offset % layer_width)
        start_y = -(self.y_offset % layer_height)
        
        # Render tiled background
        for y in range(tiles_y):
            for x in range(tiles_x):
                pos_x = start_x + (x * layer_width)
                pos_y = start_y + (y * layer_height)
                
                if self.blend_mode == pygame.BLEND_ALPHA_SDL2:
                    surface.blit(self.image, (pos_x, pos_y))
                else:
                    surface.blit(self.image, (pos_x, pos_y), special_flags=self.blend_mode)


class ParallaxSystem:
    """Complete parallax background system with multiple layers and effects."""
    
    def __init__(self, screen_width: int = 1920, screen_height: int = 1080):
        """Initialize the parallax system."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layers: List[ParallaxLayer] = []
        self.camera_x = 0.0
        self.camera_y = 0.0
        
        # Atmospheric effects
        self.fog_alpha = 0
        self.lighting_effects = True
        self.particle_drift = True
    
    def add_layer(self, image_path: str, scroll_speed: float, 
                  alpha: int = 255, blend_mode: int = pygame.BLEND_ALPHA_SDL2,
                  auto_scroll_x: float = 0.0, auto_scroll_y: float = 0.0,
                  wave_amplitude: float = 0.0, wave_frequency: float = 0.0) -> ParallaxLayer:
        """
        Add a new parallax layer.
        
        Args:
            image_path: Path to layer image
            scroll_speed: Parallax scroll speed (0.0-1.0)
            alpha: Layer transparency
            blend_mode: Pygame blend mode
            auto_scroll_x: Automatic horizontal scrolling speed
            auto_scroll_y: Automatic vertical scrolling speed
            wave_amplitude: Vertical wave motion amplitude
            wave_frequency: Wave motion frequency
        """
        layer = ParallaxLayer(image_path, scroll_speed, alpha, blend_mode)
        layer.auto_scroll_x = auto_scroll_x
        layer.auto_scroll_y = auto_scroll_y
        layer.wave_amplitude = wave_amplitude
        layer.wave_frequency = wave_frequency
        
        self.layers.append(layer)
        return layer
    
    def setup_egyptian_underworld_scene(self, assets_path: str):
        """Setup a complete Egyptian underworld parallax scene."""
        base_path = Path(assets_path)
        
        # Background layers (furthest to nearest)
        layers_config = [
            # Far background - distant pyramids and sky
            {
                "path": str(base_path / "environments" / "hades_quality" / "distant_pyramids.png"),
                "scroll_speed": 0.1,
                "alpha": 180,
                "auto_scroll_x": -2.0,  # Slow drift
                "wave_amplitude": 1.0,
                "wave_frequency": 0.3
            },
            # Mid background - sand dunes
            {
                "path": str(base_path / "environments" / "hades_quality" / "sand_dunes.png"),
                "scroll_speed": 0.3,
                "alpha": 200,
                "auto_scroll_x": -5.0,
                "wave_amplitude": 2.0,
                "wave_frequency": 0.5
            },
            # Atmospheric fog layer
            {
                "path": str(base_path / "effects" / "mystical_fog.png"),
                "scroll_speed": 0.2,
                "alpha": 100,
                "blend_mode": pygame.BLEND_ADD,
                "auto_scroll_x": -8.0,
                "wave_amplitude": 3.0,
                "wave_frequency": 0.4
            },
            # Foreground details - tomb structures
            {
                "path": str(base_path / "environments" / "hades_quality" / "tomb_structures.png"),
                "scroll_speed": 0.7,
                "alpha": 255,
                "auto_scroll_x": -10.0
            },
            # Particle effects layer
            {
                "path": str(base_path / "effects" / "floating_sand.png"),
                "scroll_speed": 0.4,
                "alpha": 150,
                "blend_mode": pygame.BLEND_ADD,
                "auto_scroll_x": -15.0,
                "auto_scroll_y": -3.0,
                "wave_amplitude": 5.0,
                "wave_frequency": 0.6
            }
        ]
        
        for config in layers_config:
            self.add_layer(**config)
    
    def setup_temple_library_scene(self, assets_path: str):
        """Setup parallax for the deck builder temple library scene."""
        base_path = Path(assets_path)
        
        layers_config = [
            # Background temple walls
            {
                "path": str(base_path / "environments" / "hades_quality" / "temple_walls.png"),
                "scroll_speed": 0.1,
                "alpha": 255
            },
            # Floating papyrus scrolls
            {
                "path": str(base_path / "effects" / "floating_scrolls.png"),
                "scroll_speed": 0.3,
                "alpha": 180,
                "auto_scroll_y": -5.0,
                "wave_amplitude": 2.0,
                "wave_frequency": 0.4
            },
            # Mystical light rays
            {
                "path": str(base_path / "effects" / "divine_light.png"),
                "scroll_speed": 0.2,
                "alpha": 120,
                "blend_mode": pygame.BLEND_ADD,
                "wave_amplitude": 1.0,
                "wave_frequency": 0.3
            },
            # Foreground columns
            {
                "path": str(base_path / "environments" / "hades_quality" / "temple_columns.png"),
                "scroll_speed": 0.8,
                "alpha": 255
            }
        ]
        
        for config in layers_config:
            self.add_layer(**config)
    
    def update_camera(self, x: float, y: float):
        """Update camera position for parallax effect."""
        self.camera_x = x
        self.camera_y = y
    
    def update(self, dt: float):
        """Update all parallax layers."""
        for layer in self.layers:
            layer.update(dt, self.camera_x, self.camera_y)
    
    def render(self, surface: pygame.Surface):
        """Render all parallax layers in order."""
        for layer in self.layers:
            layer.render(surface, self.screen_width, self.screen_height)
    
    def add_atmospheric_fog(self, alpha: int = 50):
        """Add atmospheric fog overlay."""
        fog_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        fog_surface.fill((139, 69, 19, alpha))  # Sandy brown fog
        return fog_surface
    
    def create_depth_gradient(self, start_color: Tuple[int, int, int, int],
                            end_color: Tuple[int, int, int, int]) -> pygame.Surface:
        """Create a depth gradient for atmospheric perspective."""
        gradient = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = [
                int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                for i in range(4)
            ]
            pygame.draw.line(gradient, color, (0, y), (self.screen_width, y))
        
        return gradient


# Example usage and testing
def create_test_parallax():
    """Create a test parallax system for demonstration."""
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    
    # Initialize parallax system
    parallax = ParallaxSystem()
    
    # Setup Egyptian underworld scene
    parallax.setup_egyptian_underworld_scene("game_assets")
    
    # Main loop
    running = True
    camera_x = 0
    
    while running:
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Simulate camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_x -= 100 * dt
        if keys[pygame.K_RIGHT]:
            camera_x += 100 * dt
        
        # Update parallax
        parallax.update_camera(camera_x, 0)
        parallax.update(dt)
        
        # Render
        screen.fill((20, 15, 10))  # Dark background
        parallax.render(screen)
        
        # Add atmospheric fog
        fog = parallax.add_atmospheric_fog(30)
        screen.blit(fog, (0, 0))
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    create_test_parallax()