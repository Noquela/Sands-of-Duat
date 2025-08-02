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
        
        # Apply transformations to sprite with error handling
        try:
            sprite_surface = sprite.sprite_sheet.subsurface(source_rect).copy()
        except ValueError as e:
            # Create a fallback surface to prevent crashes
            sprite_surface = pygame.Surface((sprite.frame_width, sprite.frame_height), pygame.SRCALPHA)
            sprite_surface.fill((255, 0, 255))  # Magenta for error debugging
            
            # Log error only once per sprite to avoid spam
            sprite_id = id(sprite.sprite_sheet)
            if not hasattr(self, '_logged_errors'):
                self._logged_errors = set()
            if sprite_id not in self._logged_errors:
                print(f"WARNING: Sprite dimension mismatch!")
                print(f"  Expected frame: {sprite.frame_width}x{sprite.frame_height}")
                print(f"  Sprite sheet: {sprite.sprite_sheet.get_size()}")
                print(f"  Using magenta placeholder")
                self._logged_errors.add(sprite_id)
        
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


class AttackSystem(System):
    """Handles combat attacks and damage."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Handle attack input
        for entity_id in self.entity_manager.get_entities_with_components(InputController, Combat):
            input_comp = self.entity_manager.get_component(entity_id, InputController)
            combat = self.entity_manager.get_component(entity_id, Combat)
            animation = self.entity_manager.get_component(entity_id, Animation)
            attack_hitbox = self.entity_manager.get_component(entity_id, AttackHitbox)
            
            if input_comp is None or combat is None:
                continue
            
            # Check for attack input
            can_attack = combat.can_attack(current_time)
            attack_requested = input_comp.attack_light_pressed or input_comp.attack_heavy_pressed
            
            if attack_requested and can_attack:
                # Start attack
                combat.is_attacking = True
                combat.last_attack_time = current_time
                
                # Set attack animation
                if animation is not None:
                    if input_comp.attack_heavy_pressed:
                        animation.current_animation = "attack_heavy"
                        if attack_hitbox is not None:
                            attack_hitbox.damage = combat.attack_damage * 2
                    else:
                        animation.current_animation = "attack_light"
                        if attack_hitbox is not None:
                            attack_hitbox.damage = combat.attack_damage
                    
                    animation.animation_time = 0.0
                    animation.playing = True
                
                # Activate attack hitbox
                if attack_hitbox is not None:
                    attack_hitbox.active = True
                    attack_hitbox.duration = 0.0
                    attack_hitbox.hit_entities.clear()
        
        # Update attack hitboxes
        for entity_id in self.entity_manager.get_entities_with_component(AttackHitbox):
            attack_hitbox = self.entity_manager.get_component(entity_id, AttackHitbox)
            if attack_hitbox is None or not attack_hitbox.active:
                continue
            
            attack_hitbox.duration += dt
            
            # Deactivate after duration
            if attack_hitbox.duration >= attack_hitbox.max_duration:
                attack_hitbox.active = False
                
                # Stop attacking
                combat = self.entity_manager.get_component(entity_id, Combat)
                if combat is not None:
                    combat.is_attacking = False


class CollisionSystem(System):
    """Handles collision detection and damage."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        # Check attack hitbox vs enemy hitbox collisions
        attackers = []
        for entity_id in self.entity_manager.get_entities_with_components(Transform, AttackHitbox):
            transform = self.entity_manager.get_component(entity_id, Transform)
            attack_hitbox = self.entity_manager.get_component(entity_id, AttackHitbox)
            
            if transform is None or attack_hitbox is None or not attack_hitbox.active:
                continue
            
            attackers.append((entity_id, transform, attack_hitbox))
        
        # Get all entities with hitboxes
        targets = []
        for entity_id in self.entity_manager.get_entities_with_components(Transform, Hitbox, Health):
            transform = self.entity_manager.get_component(entity_id, Transform)
            hitbox = self.entity_manager.get_component(entity_id, Hitbox)
            health = self.entity_manager.get_component(entity_id, Health)
            
            if transform is None or hitbox is None or health is None or not hitbox.active:
                continue
            
            targets.append((entity_id, transform, hitbox, health))
        
        # Check collisions
        for attacker_id, attacker_transform, attack_hitbox in attackers:
            attack_rect = attack_hitbox.get_rect(attacker_transform)
            
            for target_id, target_transform, target_hitbox, target_health in targets:
                # Don't hit self
                if attacker_id == target_id:
                    continue
                
                # Skip if already hit this target
                if target_id in attack_hitbox.hit_entities:
                    continue
                
                # Check if invulnerable
                if target_health.invulnerable:
                    continue
                
                target_rect = target_hitbox.get_rect(target_transform)
                
                if attack_rect.colliderect(target_rect):
                    # Deal damage
                    self._deal_damage(target_id, target_health, attack_hitbox.damage)
                    attack_hitbox.hit_entities.add(target_id)
                    
                    # Create hit particles
                    self._create_hit_effect(target_transform.x, target_transform.y)
    
    def _deal_damage(self, entity_id: int, health: Health, damage: int) -> None:
        """Deal damage to an entity."""
        health.current_hp = max(0, health.current_hp - damage)
        
        # Set invulnerability frames
        health.invulnerable = True
        health.invulnerability_time = 0.5
        
        print(f"Entity {entity_id} took {damage} damage! HP: {health.current_hp}/{health.max_hp}")
        
        # Check if entity died
        if health.current_hp <= 0:
            print(f"Entity {entity_id} died!")
            # TODO: Add death handling
    
    def _create_hit_effect(self, x: float, y: float) -> None:
        """Create hit effect particles."""
        # TODO: Implement particle creation
        pass


class AISystem(System):
    """Handles enemy AI behavior."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        # Find player for targeting
        player_entity = None
        player_transform = None
        for entity_id in self.entity_manager.get_entities_with_component(PlayerTag):
            player_entity = entity_id
            player_transform = self.entity_manager.get_component(entity_id, Transform)
            break
        
        if player_entity is None or player_transform is None:
            return
        
        # Update all AI entities
        for entity_id in self.entity_manager.get_entities_with_components(Transform, AIController, Movement):
            transform = self.entity_manager.get_component(entity_id, Transform)
            ai = self.entity_manager.get_component(entity_id, AIController)
            movement = self.entity_manager.get_component(entity_id, Movement)
            health = self.entity_manager.get_component(entity_id, Health)
            
            if transform is None or ai is None or movement is None:
                continue
            
            # Skip if dead
            if health is not None and health.current_hp <= 0:
                ai.state = "dead"
                movement.velocity_x = 0
                movement.velocity_y = 0
                continue
            
            # Update state timer
            ai.state_timer += dt
            
            # Calculate distance to player
            dx = player_transform.x - transform.x
            dy = player_transform.y - transform.y
            distance_to_player = math.sqrt(dx * dx + dy * dy)
            
            # AI state machine
            if ai.state == "idle" or ai.state == "patrol":
                # Check if player is in detection range
                if distance_to_player <= ai.detection_range:
                    ai.state = "chase"
                    ai.target_entity = player_entity
                    ai.last_seen_x = player_transform.x
                    ai.last_seen_y = player_transform.y
                    ai.state_timer = 0.0
                elif ai.state == "idle" and ai.state_timer > 2.0:
                    # Start patrolling
                    ai.state = "patrol"
                    ai.patrol_center_x = transform.x
                    ai.patrol_center_y = transform.y
                    ai.state_timer = 0.0
                
                # Patrol movement
                if ai.state == "patrol":
                    ai.patrol_angle += dt * 0.5  # Slow rotation
                    target_x = ai.patrol_center_x + math.cos(ai.patrol_angle) * ai.patrol_radius
                    target_y = ai.patrol_center_y + math.sin(ai.patrol_angle) * ai.patrol_radius
                    
                    # Move towards patrol point
                    patrol_dx = target_x - transform.x
                    patrol_dy = target_y - transform.y
                    patrol_distance = math.sqrt(patrol_dx * patrol_dx + patrol_dy * patrol_dy)
                    
                    if patrol_distance > 10.0:
                        movement.velocity_x = (patrol_dx / patrol_distance) * ai.patrol_speed
                        movement.velocity_y = (patrol_dy / patrol_distance) * ai.patrol_speed
                    else:
                        movement.velocity_x = 0
                        movement.velocity_y = 0
            
            elif ai.state == "chase":
                # Update last seen position
                if distance_to_player <= ai.detection_range * 1.2:  # Slightly larger range to avoid flickering
                    ai.last_seen_x = player_transform.x
                    ai.last_seen_y = player_transform.y
                
                # Check if close enough to attack
                if distance_to_player <= ai.attack_range:
                    ai.state = "attack"
                    ai.state_timer = 0.0
                else:
                    # Chase towards last seen position
                    chase_dx = ai.last_seen_x - transform.x
                    chase_dy = ai.last_seen_y - transform.y
                    chase_distance = math.sqrt(chase_dx * chase_dx + chase_dy * chase_dy)
                    
                    if chase_distance > 5.0:
                        movement.velocity_x = (chase_dx / chase_distance) * ai.chase_speed
                        movement.velocity_y = (chase_dy / chase_distance) * ai.chase_speed
                    else:
                        # Lost player, return to patrol
                        ai.state = "idle"
                        ai.target_entity = None
                        ai.state_timer = 0.0
                        movement.velocity_x = 0
                        movement.velocity_y = 0
            
            elif ai.state == "attack":
                # Stop moving during attack
                movement.velocity_x = 0
                movement.velocity_y = 0
                
                # TODO: Trigger attack animation and damage
                
                if ai.state_timer > 1.0:  # Attack duration
                    # Return to chase or idle
                    if distance_to_player <= ai.detection_range:
                        ai.state = "chase"
                    else:
                        ai.state = "idle"
                    ai.state_timer = 0.0


class HealthSystem(System):
    """Handles health updates and invulnerability."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        for entity_id in self.entity_manager.get_entities_with_component(Health):
            health = self.entity_manager.get_component(entity_id, Health)
            if health is None:
                continue
            
            # Update invulnerability
            if health.invulnerable:
                health.invulnerability_time -= dt
                if health.invulnerability_time <= 0:
                    health.invulnerable = False
                    health.invulnerability_time = 0.0


class ArtifactSystem(System):
    """Handles Egyptian artifact effects and stat modifications."""
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        # Update all entities with artifact inventories
        for entity_id in self.entity_manager.get_entities_with_components(ArtifactInventory, Stats):
            inventory = self.entity_manager.get_component(entity_id, ArtifactInventory)
            stats = self.entity_manager.get_component(entity_id, Stats)
            
            if inventory is None or stats is None:
                continue
            
            # Reset multipliers to base
            stats.damage_multiplier = 1.0
            stats.speed_multiplier = 1.0
            stats.health_multiplier = 1.0
            stats.crit_chance_bonus = 0.0
            
            # Apply all equipped artifacts
            for artifact_name in inventory.equipped_artifacts:
                artifact_effects = self._get_artifact_effects(artifact_name)
                
                # Apply stat modifications
                stats.damage_multiplier *= artifact_effects.get('damage_multiplier', 1.0)
                stats.speed_multiplier *= artifact_effects.get('speed_multiplier', 1.0)
                stats.health_multiplier *= artifact_effects.get('health_multiplier', 1.0)
                stats.crit_chance_bonus += artifact_effects.get('crit_chance_bonus', 0.0)
            
            # Update actual component stats based on modified stats
            self._apply_stats_to_components(entity_id, stats)
    
    def _get_artifact_effects(self, artifact_name: str) -> Dict[str, float]:
        """Get the effects for a specific artifact."""
        # Egyptian artifact database
        artifact_db = {
            # Ra Artifacts (Fire/Damage)
            "Solar Blessing": {
                "damage_multiplier": 1.15,
                "description": "Ra's solar power increases attack damage by 15%"
            },
            "Pharaoh's Crown": {
                "damage_multiplier": 1.25,
                "crit_chance_bonus": 0.1,
                "description": "Divine authority grants 25% damage and 10% crit chance"
            },
            "Desert Storm": {
                "damage_multiplier": 1.35,
                "description": "Devastating sandstorm increases damage by 35%"
            },
            
            # Thoth Artifacts (Wisdom/Speed)
            "Wisdom of Ages": {
                "speed_multiplier": 1.2,
                "crit_chance_bonus": 0.05,
                "description": "Ancient knowledge grants 20% speed and 5% crit chance"
            },
            "Scribe's Quill": {
                "speed_multiplier": 1.15,
                "description": "Swift as the written word, 15% movement speed"
            },
            "Knowledge Keeper": {
                "speed_multiplier": 1.3,
                "damage_multiplier": 1.1,
                "description": "30% speed and 10% damage from divine intellect"
            },
            
            # Isis Artifacts (Protection/Health)
            "Mother's Protection": {
                "health_multiplier": 1.25,
                "description": "Maternal blessing increases health by 25%"
            },
            "Magic Ward": {
                "health_multiplier": 1.2,
                "speed_multiplier": 1.1,
                "description": "Magical protection grants 20% health and 10% speed"
            },
            "Healing Touch": {
                "health_multiplier": 1.4,
                "description": "Divine healing increases health by 40%"
            },
            
            # Ptah Artifacts (Creation/Balanced)
            "Creator's Hammer": {
                "damage_multiplier": 1.2,
                "health_multiplier": 1.15,
                "description": "Divine craftsmanship: 20% damage, 15% health"
            },
            "Divine Craft": {
                "damage_multiplier": 1.1,
                "speed_multiplier": 1.1,
                "health_multiplier": 1.1,
                "description": "Perfect balance: 10% to all stats"
            },
            "Builder's Strength": {
                "health_multiplier": 1.3,
                "damage_multiplier": 1.15,
                "description": "Construction prowess: 30% health, 15% damage"
            }
        }
        
        return artifact_db.get(artifact_name, {})
    
    def _apply_stats_to_components(self, entity_id: int, stats: Stats) -> None:
        """Apply stat modifications to actual game components."""
        # Update movement speed
        movement = self.entity_manager.get_component(entity_id, Movement)
        if movement is not None:
            movement.max_speed = stats.get_total_speed()
        
        # Update combat damage and crit
        combat = self.entity_manager.get_component(entity_id, Combat)
        if combat is not None:
            combat.attack_damage = stats.get_total_damage()
            combat.crit_chance = stats.get_total_crit_chance()
        
        # Update health (only increase max, don't decrease current)
        health = self.entity_manager.get_component(entity_id, Health)
        if health is not None:
            old_max = health.max_hp
            new_max = stats.get_total_health()
            if new_max > old_max:
                # Increase current health proportionally
                health.current_hp += (new_max - old_max)
            health.max_hp = new_max


class InteractionSystem(System):
    """Handles player interactions with altars, NPCs, and portals."""
    
    def __init__(self, entity_manager: EntityManager):
        super().__init__(entity_manager)
        self.interaction_prompt = None
        self.active_interactions = set()
    
    def update(self, dt: float) -> None:
        if not self.enabled:
            return
        
        # Find player
        player_entity = None
        player_transform = None
        player_input = None
        
        for entity_id in self.entity_manager.get_entities_with_component(PlayerTag):
            player_entity = entity_id
            player_transform = self.entity_manager.get_component(entity_id, Transform)
            player_input = self.entity_manager.get_component(entity_id, InputController)
            break
        
        if player_entity is None or player_transform is None:
            return
        
        # Clear previous interaction prompts
        self.interaction_prompt = None
        
        # Check for nearby interactables
        nearby_interactables = []
        for entity_id in self.entity_manager.get_entities_with_component(Interactable):
            interactable = self.entity_manager.get_component(entity_id, Interactable)
            transform = self.entity_manager.get_component(entity_id, Transform)
            
            if interactable is None or transform is None or not interactable.can_interact:
                continue
            
            # Check distance
            distance = math.sqrt(
                (player_transform.x - transform.x) ** 2 + 
                (player_transform.y - transform.y) ** 2
            )
            
            if distance <= interactable.interaction_range:
                nearby_interactables.append((entity_id, interactable, transform, distance))
        
        # Sort by distance and get closest
        if nearby_interactables:
            nearby_interactables.sort(key=lambda x: x[3])
            closest_entity, closest_interactable, closest_transform, _ = nearby_interactables[0]
            
            # Show interaction prompt
            self.interaction_prompt = {
                'text': closest_interactable.prompt_text,
                'position': (closest_transform.x, closest_transform.y - 40),
                'entity_id': closest_entity
            }
            
            # Handle interaction input
            if player_input and player_input.interact_pressed:
                self._handle_interaction(player_entity, closest_entity, closest_interactable)
    
    def _handle_interaction(self, player_id: int, target_id: int, interactable: Interactable) -> None:
        """Handle different types of interactions."""
        if interactable.interaction_type == "altar":
            self._handle_altar_interaction(player_id, target_id, interactable)
        elif interactable.interaction_type == "portal":
            self._handle_portal_interaction(player_id, target_id)
        elif interactable.interaction_type == "npc":
            self._handle_npc_interaction(player_id, target_id, interactable)
    
    def _handle_altar_interaction(self, player_id: int, altar_id: int, interactable: Interactable) -> None:
        """Handle Egyptian god altar interactions."""
        player_inventory = self.entity_manager.get_component(player_id, ArtifactInventory)
        egyptian_god = self.entity_manager.get_component(altar_id, EgyptianGod)
        
        if player_inventory is None or egyptian_god is None:
            return
        
        # Get available artifacts for this god
        god_artifacts = egyptian_god.god_artifacts.get(interactable.god_type, [])
        if not god_artifacts:
            print(f"No artifacts available for {interactable.god_type}")
            return
        
        # Check if player has room for more artifacts
        if len(player_inventory.equipped_artifacts) >= player_inventory.max_artifacts:
            print(f"Artifact inventory full! ({len(player_inventory.equipped_artifacts)}/{player_inventory.max_artifacts})")
            return
        
        # Select a random artifact from the god's pool
        import random
        selected_artifact = random.choice(god_artifacts)
        
        # Add artifact to inventory
        if player_inventory.add_artifact(selected_artifact):
            print(f"\n=== BLESSING RECEIVED ===\nGod: {interactable.god_type}\nArtifact: {selected_artifact}\n")
            
            # Increase blessing count and favor
            egyptian_god.blessing_count += 1
            if egyptian_god.blessing_count % 3 == 0:
                egyptian_god.favor_level += 1
                print(f"{interactable.god_type}'s favor increased to level {egyptian_god.favor_level}!")
            
            # Disable altar temporarily (like in Hades)
            interactable.can_interact = False
            # TODO: Re-enable after leaving and returning to hub
    
    def _handle_portal_interaction(self, player_id: int, portal_id: int) -> None:
        """Handle portal scene transitions."""
        portal = self.entity_manager.get_component(portal_id, Portal)
        if portal is None:
            return
        
        print(f"Entering portal to {portal.destination_scene}...")
        # TODO: Trigger scene transition
        # This would typically send an event to the scene manager
    
    def _handle_npc_interaction(self, player_id: int, npc_id: int, interactable: Interactable) -> None:
        """Handle NPC dialogue interactions."""
        npc_tag = self.entity_manager.get_component(npc_id, NPCTag)
        if npc_tag is None:
            return
        
        # Simple dialogue system
        dialogues = {
            "mirror_anubis": [
                "Greetings, fellow guardian of the afterlife.",
                "The gods watch your progress with interest.",
                "Your artifacts grow in power... as do you."
            ],
            "merchant": [
                "Welcome, traveler! I have rare goods from across the realm.",
                "Perhaps some divine artifacts interest you?",
                "The gods have blessed my wares today."
            ]
        }
        
        dialogue_lines = dialogues.get(npc_tag.npc_type, ["..."]) 
        import random
        selected_line = random.choice(dialogue_lines)
        print(f"\n[{npc_tag.npc_type.replace('_', ' ').title()}]: {selected_line}\n")
    
    def get_interaction_prompt(self) -> Optional[Dict[str, Any]]:
        """Get current interaction prompt for UI rendering."""
        return self.interaction_prompt