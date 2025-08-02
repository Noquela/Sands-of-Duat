"""
ECS Systems for Sands of Duat
Core game logic systems that operate on components
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set
import pygame
import math
from .components import *
from .entity import EntityManager


class System(ABC):
    """Base class for all ECS systems."""
    
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager
        self.enabled = True
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update system logic."""
        pass


class InputSystem(System):
    """Handles player input and updates InputController components."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        keys = pygame.key.get_pressed()
        
        for entity_id in self.entity_manager.get_entities_with_component(InputController):
            input_comp = self.entity_manager.get_component(entity_id, InputController)
            if input_comp is None:
                continue
            
            # Reset input state
            input_comp.move_x = 0.0
            input_comp.move_y = 0.0
            input_comp.attack_light_pressed = False
            input_comp.attack_heavy_pressed = False
            input_comp.dash_pressed = False
            input_comp.interact_pressed = False
            
            # Check movement keys
            if keys[input_comp.move_left_key]:
                input_comp.move_x -= 1.0
            if keys[input_comp.move_right_key]:
                input_comp.move_x += 1.0
            if keys[input_comp.move_up_key]:
                input_comp.move_y -= 1.0
            if keys[input_comp.move_down_key]:
                input_comp.move_y += 1.0
            
            # Normalize diagonal movement
            if input_comp.move_x != 0.0 and input_comp.move_y != 0.0:
                length = math.sqrt(input_comp.move_x ** 2 + input_comp.move_y ** 2)
                input_comp.move_x /= length
                input_comp.move_y /= length
            
            # Check action keys
            if keys[input_comp.attack_light_key]:
                input_comp.attack_light_pressed = True
            if keys[input_comp.attack_heavy_key]:
                input_comp.attack_heavy_pressed = True
            if keys[input_comp.dash_key]:
                input_comp.dash_pressed = True
            if keys[input_comp.interact_key]:
                input_comp.interact_pressed = True


class MovementSystem(System):
    """Handles entity movement physics."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        for entity_id in self.entity_manager.get_entities_with_component(Movement):
            movement = self.entity_manager.get_component(entity_id, Movement)
            transform = self.entity_manager.get_component(entity_id, Transform)
            input_comp = self.entity_manager.get_component(entity_id, InputController)
            
            if movement is None or transform is None:
                continue
            
            # Get input direction
            input_x, input_y = 0.0, 0.0
            if input_comp is not None:
                input_x, input_y = input_comp.move_x, input_comp.move_y
            
            # Apply acceleration or friction
            if input_x != 0.0:
                movement.velocity_x += input_x * movement.acceleration * dt
            else:
                # Apply friction
                if movement.velocity_x > 0:
                    movement.velocity_x = max(0, movement.velocity_x - movement.friction * dt)
                elif movement.velocity_x < 0:
                    movement.velocity_x = min(0, movement.velocity_x + movement.friction * dt)
            
            if input_y != 0.0:
                movement.velocity_y += input_y * movement.acceleration * dt
            else:
                # Apply friction
                if movement.velocity_y > 0:
                    movement.velocity_y = max(0, movement.velocity_y - movement.friction * dt)
                elif movement.velocity_y < 0:
                    movement.velocity_y = min(0, movement.velocity_y + movement.friction * dt)
            
            # Clamp to max speed
            speed = math.sqrt(movement.velocity_x ** 2 + movement.velocity_y ** 2)
            if speed > movement.max_speed:
                movement.velocity_x = (movement.velocity_x / speed) * movement.max_speed
                movement.velocity_y = (movement.velocity_y / speed) * movement.max_speed
            
            # Update position
            transform.x += movement.velocity_x * dt
            transform.y += movement.velocity_y * dt


class AnimationSystem(System):
    """Handles sprite animation."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        for entity_id in self.entity_manager.get_entities_with_component(Animation):
            animation = self.entity_manager.get_component(entity_id, Animation)
            sprite = self.entity_manager.get_component(entity_id, SpriteRenderer)
            movement = self.entity_manager.get_component(entity_id, Movement)
            
            if animation is None or sprite is None:
                continue
            
            # Determine animation state
            new_animation = "idle"
            if movement is not None:
                speed = math.sqrt(movement.velocity_x ** 2 + movement.velocity_y ** 2)
                if speed > 10.0:  # Moving threshold
                    new_animation = "walk"
            
            # Change animation if needed
            if new_animation != animation.current_animation:
                animation.current_animation = new_animation
                animation.animation_time = 0.0
            
            # Update animation time
            if animation.playing:
                animation.animation_time += dt
                
                anim_data = animation.animations.get(animation.current_animation, {})
                frames = anim_data.get("frames", [0])
                frame_duration = anim_data.get("duration", 0.2)
                loop = anim_data.get("loop", True)
                
                # Calculate current frame
                total_duration = len(frames) * frame_duration
                if animation.animation_time >= total_duration:
                    if loop:
                        animation.animation_time = 0.0
                    else:
                        animation.animation_time = total_duration
                        animation.playing = False
                
                frame_index = min(int(animation.animation_time / frame_duration), len(frames) - 1)
                sprite.current_frame = frames[frame_index]


class RenderSystem(System):
    """Handles sprite rendering."""
    
    def __init__(self, entity_manager: EntityManager, screen: pygame.Surface):
        super().__init__(entity_manager)
        self.screen = screen
        self.camera_x = 0.0
        self.camera_y = 0.0
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        # Update camera position
        self._update_camera()
        
        # Render all sprites
        render_list = []
        for entity_id in self.entity_manager.get_entities_with_component(SpriteRenderer):
            transform = self.entity_manager.get_component(entity_id, Transform)
            sprite = self.entity_manager.get_component(entity_id, SpriteRenderer)
            
            if transform is None or sprite is None or not sprite.visible or sprite.sprite_sheet is None:
                continue
            
            render_list.append((entity_id, transform, sprite))
        
        # Sort by y position for proper depth
        render_list.sort(key=lambda x: x[1].y)
        
        # Render sprites
        for entity_id, transform, sprite in render_list:
            self._render_sprite(transform, sprite)
    
    def _update_camera(self) -> None:
        """Update camera to follow player."""
        for entity_id in self.entity_manager.get_entities_with_component(PlayerTag):
            transform = self.entity_manager.get_component(entity_id, Transform)
            if transform is not None:
                screen_center_x = self.screen.get_width() // 2
                screen_center_y = self.screen.get_height() // 2
                self.camera_x = transform.x - screen_center_x
                self.camera_y = transform.y - screen_center_y
                break
    
    def _render_sprite(self, transform: Transform, sprite: SpriteRenderer) -> None:
        """Render a single sprite."""
        # Get source rect for current frame
        source_rect = sprite.get_current_rect()
        
        # Calculate screen position
        screen_x = transform.x - self.camera_x
        screen_y = transform.y - self.camera_y
        
        # Create destination rect
        dest_rect = pygame.Rect(
            screen_x - sprite.frame_width // 2,
            screen_y - sprite.frame_height // 2,
            sprite.frame_width * transform.scale_x,
            sprite.frame_height * transform.scale_y
        )
        
        # Apply transformations to sprite
        sprite_surface = sprite.sprite_sheet.subsurface(source_rect).copy()
        
        # Apply color tint
        if sprite.color_tint != (255, 255, 255):
            sprite_surface.fill(sprite.color_tint, special_flags=pygame.BLEND_MULT)
        
        # Apply alpha
        if sprite.alpha < 255:
            sprite_surface.set_alpha(sprite.alpha)
        
        # Apply flipping
        if sprite.flip_x or sprite.flip_y:
            sprite_surface = pygame.transform.flip(sprite_surface, sprite.flip_x, sprite.flip_y)
        
        # Apply rotation
        if transform.rotation != 0.0:
            sprite_surface = pygame.transform.rotate(sprite_surface, transform.rotation)
            # Adjust position for rotated sprite
            old_center = dest_rect.center
            dest_rect = sprite_surface.get_rect()
            dest_rect.center = old_center
        
        # Render to screen
        self.screen.blit(sprite_surface, dest_rect)


class CameraSystem(System):
    """Handles camera movement and bounds."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        for entity_id in self.entity_manager.get_entities_with_component(Camera):
            camera = self.entity_manager.get_component(entity_id, Camera)
            if camera is None:
                continue
            
            # Find player to follow
            for player_id in self.entity_manager.get_entities_with_component(PlayerTag):
                player_transform = self.entity_manager.get_component(player_id, Transform)
                if player_transform is not None:
                    # Smooth camera following
                    target_x = player_transform.x + camera.offset_x
                    target_y = player_transform.y + camera.offset_y
                    
                    diff_x = target_x - camera.target_x
                    diff_y = target_y - camera.target_y
                    
                    camera.target_x += diff_x * camera.follow_speed * dt
                    camera.target_y += diff_y * camera.follow_speed * dt
                    
                    # Apply camera bounds
                    if camera.bounds_left is not None:
                        camera.target_x = max(camera.target_x, camera.bounds_left)
                    if camera.bounds_right is not None:
                        camera.target_x = min(camera.target_x, camera.bounds_right)
                    if camera.bounds_top is not None:
                        camera.target_y = max(camera.target_y, camera.bounds_top)
                    if camera.bounds_bottom is not None:
                        camera.target_y = min(camera.target_y, camera.bounds_bottom)
                    
                    break