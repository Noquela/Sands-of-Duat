"""
Card Animator - Hades-level card animation system.
Creates smooth, professional card animations for play, hover, and combat effects.
"""

import pygame
import math
from typing import Tuple, Optional, Callable, Dict, Any
from enum import Enum
from dataclasses import dataclass
from ...core.constants import Colors, Timing

class AnimationType(Enum):
    """Types of card animations."""
    HOVER = "hover"
    PLAY = "play"
    ATTACK = "attack"
    DAMAGE = "damage"
    DESTROY = "destroy"
    DRAW = "draw"
    DISCARD = "discard"
    BUFF = "buff"
    DEBUFF = "debuff"

class EasingType(Enum):
    """Animation easing types."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"

@dataclass
class CardAnimation:
    """Single card animation definition."""
    animation_type: AnimationType
    duration: float
    easing: EasingType
    start_values: Dict[str, float]
    end_values: Dict[str, float]
    completion_callback: Optional[Callable] = None
    loop: bool = False
    delay: float = 0.0

class CardAnimator:
    """Professional card animation system with Hades-level polish."""
    
    def __init__(self):
        # Active animations per card
        self.active_animations: Dict[str, Dict[str, Any]] = {}
        
        # Animation presets
        self._setup_animation_presets()
        
        # Performance settings
        self.max_simultaneous_animations = 20
        
    def _setup_animation_presets(self):
        """Setup predefined animation presets."""
        self.presets = {
            AnimationType.HOVER: CardAnimation(
                animation_type=AnimationType.HOVER,
                duration=0.2,
                easing=EasingType.EASE_OUT,
                start_values={'scale': 1.0, 'y_offset': 0, 'glow_intensity': 0},
                end_values={'scale': 1.1, 'y_offset': -15, 'glow_intensity': 0.8}
            ),
            
            AnimationType.PLAY: CardAnimation(
                animation_type=AnimationType.PLAY,
                duration=0.6,
                easing=EasingType.EASE_IN_OUT,
                start_values={'scale': 1.0, 'rotation': 0, 'alpha': 255},
                end_values={'scale': 1.3, 'rotation': 15, 'alpha': 200}
            ),
            
            AnimationType.ATTACK: CardAnimation(
                animation_type=AnimationType.ATTACK,
                duration=0.4,
                easing=EasingType.BOUNCE,
                start_values={'scale': 1.0, 'shake_x': 0, 'flash_intensity': 0},
                end_values={'scale': 1.2, 'shake_x': 10, 'flash_intensity': 1.0}
            ),
            
            AnimationType.DAMAGE: CardAnimation(
                animation_type=AnimationType.DAMAGE,
                duration=0.3,
                easing=EasingType.EASE_OUT,
                start_values={'shake_intensity': 0, 'red_tint': 0, 'scale': 1.0},
                end_values={'shake_intensity': 15, 'red_tint': 100, 'scale': 0.95}
            ),
            
            AnimationType.DESTROY: CardAnimation(
                animation_type=AnimationType.DESTROY,
                duration=0.8,
                easing=EasingType.EASE_IN,
                start_values={'scale': 1.0, 'rotation': 0, 'alpha': 255, 'particles': 0},
                end_values={'scale': 0.1, 'rotation': 180, 'alpha': 0, 'particles': 20}
            ),
            
            AnimationType.DRAW: CardAnimation(
                animation_type=AnimationType.DRAW,
                duration=0.5,
                easing=EasingType.ELASTIC,
                start_values={'scale': 0.3, 'alpha': 0, 'y_offset': 100},
                end_values={'scale': 1.0, 'alpha': 255, 'y_offset': 0}
            ),
            
            AnimationType.BUFF: CardAnimation(
                animation_type=AnimationType.BUFF,
                duration=1.0,
                easing=EasingType.EASE_IN_OUT,
                start_values={'glow_intensity': 0, 'golden_tint': 0},
                end_values={'glow_intensity': 1.0, 'golden_tint': 50},
                loop=True
            ),
            
            AnimationType.DEBUFF: CardAnimation(
                animation_type=AnimationType.DEBUFF,
                duration=1.2,
                easing=EasingType.EASE_IN_OUT,
                start_values={'purple_tint': 0, 'corrupt_effect': 0},
                end_values={'purple_tint': 60, 'corrupt_effect': 0.3},
                loop=True
            )
        }
    
    def start_animation(self, card_id: str, animation_type: AnimationType, 
                       custom_values: Optional[Dict[str, Any]] = None) -> bool:
        """
        Start an animation on a card.
        
        Args:
            card_id: Unique identifier for the card
            animation_type: Type of animation to play
            custom_values: Optional custom animation values
        
        Returns:
            True if animation started successfully
        """
        if card_id not in self.active_animations:
            self.active_animations[card_id] = {}
        
        # Don't start if too many animations are running
        total_animations = sum(len(anims) for anims in self.active_animations.values())
        if total_animations >= self.max_simultaneous_animations:
            return False
        
        # Get animation preset
        if animation_type not in self.presets:
            return False
        
        preset = self.presets[animation_type]
        
        # Create animation state
        animation_state = {
            'type': animation_type,
            'duration': preset.duration,
            'easing': preset.easing,
            'current_time': 0.0,
            'start_values': preset.start_values.copy(),
            'end_values': preset.end_values.copy(),
            'current_values': preset.start_values.copy(),
            'completion_callback': preset.completion_callback,
            'loop': preset.loop,
            'delay': preset.delay,
            'started': preset.delay <= 0.0
        }
        
        # Apply custom values if provided
        if custom_values:
            if 'duration' in custom_values:
                animation_state['duration'] = custom_values['duration']
            if 'start_values' in custom_values:
                animation_state['start_values'].update(custom_values['start_values'])
            if 'end_values' in custom_values:
                animation_state['end_values'].update(custom_values['end_values'])
                animation_state['current_values'].update(custom_values['start_values'])
        
        # Store animation
        anim_key = f"{animation_type.value}_{len(self.active_animations[card_id])}"
        self.active_animations[card_id][anim_key] = animation_state
        
        return True
    
    def stop_animation(self, card_id: str, animation_type: Optional[AnimationType] = None):
        """Stop animations on a card."""
        if card_id not in self.active_animations:
            return
        
        if animation_type is None:
            # Stop all animations on card
            self.active_animations[card_id].clear()
        else:
            # Stop specific animation type
            keys_to_remove = [k for k, v in self.active_animations[card_id].items() 
                            if v['type'] == animation_type]
            for key in keys_to_remove:
                del self.active_animations[card_id][key]
    
    def update(self, dt: float):
        """Update all active animations."""
        cards_to_remove = []
        
        for card_id, animations in self.active_animations.items():
            anims_to_remove = []
            
            for anim_key, anim_state in animations.items():
                # Handle delay
                if not anim_state['started']:
                    anim_state['delay'] -= dt
                    if anim_state['delay'] <= 0:
                        anim_state['started'] = True
                    continue
                
                # Update animation time
                anim_state['current_time'] += dt
                
                # Calculate progress
                progress = min(anim_state['current_time'] / anim_state['duration'], 1.0)
                eased_progress = self._apply_easing(progress, anim_state['easing'])
                
                # Update current values
                for key in anim_state['start_values']:
                    start_val = anim_state['start_values'][key]
                    end_val = anim_state['end_values'][key]
                    current_val = start_val + (end_val - start_val) * eased_progress
                    anim_state['current_values'][key] = current_val
                
                # Check for completion
                if progress >= 1.0:
                    if anim_state['loop']:
                        # Reset for loop
                        anim_state['current_time'] = 0.0
                    else:
                        # Mark for removal
                        anims_to_remove.append(anim_key)
                        
                        # Call completion callback
                        if anim_state['completion_callback']:
                            anim_state['completion_callback']()
            
            # Remove completed animations
            for key in anims_to_remove:
                del animations[key]
            
            # Mark empty animation sets for removal
            if not animations:
                cards_to_remove.append(card_id)
        
        # Remove empty card entries
        for card_id in cards_to_remove:
            del self.active_animations[card_id]
    
    def _apply_easing(self, progress: float, easing: EasingType) -> float:
        """Apply easing function to animation progress."""
        if easing == EasingType.LINEAR:
            return progress
        
        elif easing == EasingType.EASE_IN:
            return progress * progress
        
        elif easing == EasingType.EASE_OUT:
            return 1 - (1 - progress) * (1 - progress)
        
        elif easing == EasingType.EASE_IN_OUT:
            if progress < 0.5:
                return 2 * progress * progress
            else:
                return 1 - 2 * (1 - progress) * (1 - progress)
        
        elif easing == EasingType.BOUNCE:
            if progress < 0.5:
                return 2 * progress * progress
            else:
                p = (progress - 0.5) * 2
                return 0.5 + 0.5 * (4 * p * (1 - p))
        
        elif easing == EasingType.ELASTIC:
            if progress == 0 or progress == 1:
                return progress
            
            p = progress - 1
            return -(math.pow(2, 10 * p) * math.sin((p - 0.1) * (2 * math.pi) / 0.4))
        
        return progress
    
    def get_card_animation_values(self, card_id: str) -> Dict[str, float]:
        """Get current animation values for a card."""
        if card_id not in self.active_animations:
            return {}
        
        # Combine all animation values for this card
        combined_values = {}
        
        for anim_state in self.active_animations[card_id].values():
            for key, value in anim_state['current_values'].items():
                if key in combined_values:
                    # Combine values (additive for most properties)
                    if key in ['scale']:
                        combined_values[key] *= value  # Multiplicative for scale
                    else:
                        combined_values[key] += value  # Additive for others
                else:
                    combined_values[key] = value
        
        return combined_values
    
    def is_animating(self, card_id: str, animation_type: Optional[AnimationType] = None) -> bool:
        """Check if a card is currently animating."""
        if card_id not in self.active_animations:
            return False
        
        if animation_type is None:
            return len(self.active_animations[card_id]) > 0
        
        return any(anim['type'] == animation_type 
                  for anim in self.active_animations[card_id].values())
    
    def apply_animation_to_surface(self, surface: pygame.Surface, card_id: str, 
                                 base_rect: pygame.Rect) -> Tuple[pygame.Surface, pygame.Rect]:
        """
        Apply current animation values to a card surface.
        
        Args:
            surface: Original card surface
            card_id: Card identifier
            base_rect: Original card rectangle
        
        Returns:
            Tuple of (animated_surface, animated_rect)
        """
        values = self.get_card_animation_values(card_id)
        
        if not values:
            return surface, base_rect
        
        # Create animated surface
        animated_surface = surface.copy()
        animated_rect = base_rect.copy()
        
        # Apply scaling
        if 'scale' in values and values['scale'] != 1.0:
            scale = values['scale']
            new_width = int(surface.get_width() * scale)
            new_height = int(surface.get_height() * scale)
            animated_surface = pygame.transform.scale(animated_surface, (new_width, new_height))
            
            # Center the scaled surface
            animated_rect.width = new_width
            animated_rect.height = new_height
            animated_rect.center = base_rect.center
        
        # Apply rotation
        if 'rotation' in values and values['rotation'] != 0:
            rotation = values['rotation']
            animated_surface = pygame.transform.rotate(animated_surface, rotation)
            # Update rect to match rotated surface
            old_center = animated_rect.center
            animated_rect = animated_surface.get_rect()
            animated_rect.center = old_center
        
        # Apply position offsets
        if 'x_offset' in values:
            animated_rect.x += int(values['x_offset'])
        if 'y_offset' in values:
            animated_rect.y += int(values['y_offset'])
        
        # Apply shake effects
        if 'shake_x' in values:
            shake_x = math.sin(pygame.time.get_ticks() * 0.05) * values['shake_x']
            animated_rect.x += int(shake_x)
        if 'shake_intensity' in values:
            shake_time = pygame.time.get_ticks() * 0.1
            shake_x = math.sin(shake_time) * values['shake_intensity']
            shake_y = math.cos(shake_time * 1.3) * values['shake_intensity']
            animated_rect.x += int(shake_x)
            animated_rect.y += int(shake_y)
        
        # Apply alpha
        if 'alpha' in values and values['alpha'] != 255:
            alpha = max(0, min(255, int(values['alpha'])))
            animated_surface.set_alpha(alpha)
        
        # Apply color effects
        if 'red_tint' in values and values['red_tint'] > 0:
            red_overlay = pygame.Surface(animated_surface.get_size(), pygame.SRCALPHA)
            red_overlay.fill((*Colors.RED, int(values['red_tint'])))
            animated_surface.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
        
        if 'golden_tint' in values and values['golden_tint'] > 0:
            gold_overlay = pygame.Surface(animated_surface.get_size(), pygame.SRCALPHA)
            gold_overlay.fill((*Colors.GOLD, int(values['golden_tint'])))
            animated_surface.blit(gold_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
        
        if 'purple_tint' in values and values['purple_tint'] > 0:
            purple_overlay = pygame.Surface(animated_surface.get_size(), pygame.SRCALPHA)
            purple_overlay.fill((138, 43, 226, int(values['purple_tint'])))
            animated_surface.blit(purple_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
        
        return animated_surface, animated_rect
    
    def clear_all_animations(self):
        """Clear all active animations."""
        self.active_animations.clear()
    
    def get_animation_count(self) -> int:
        """Get total number of active animations."""
        return sum(len(anims) for anims in self.active_animations.values())

# Global card animator instance
card_animator = CardAnimator()