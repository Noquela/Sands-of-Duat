"""
Hub Scene - The main lobby like Hades' Hall of Styx
Central area where player manages artifacts, upgrades, and starts runs
"""

import pygame
import math
from typing import Optional, Dict, Any, List
from .scene import Scene
from ecs import (
    EntityManager, create_player_entity, EntityBuilder,
    InputSystem, MovementSystem, AnimationSystem, RenderSystem,
    Transform, SpriteRenderer, Health, PlayerTag
)
from assets import get_sprite


class HubScene(Scene):
    """Hub scene - main lobby area like Hades."""
    
    def __init__(self, game):
        super().__init__(game)
        self.player_id: Optional[int] = None
        self.altars: List[int] = []
        self.npcs: List[int] = []
        self.portal_id: Optional[int] = None
        self.show_ui = True
        
        # Hub layout (Egyptian temple style)
        self.hub_width = 1200
        self.hub_height = 800
        self.center_x = self.hub_width // 2
        self.center_y = self.hub_height // 2
    
    def initialize(self) -> None:
        """Initialize the Hub scene."""
        print("Initializing Hub Scene (Hall of Anubis)...")
        
        # Setup ECS systems
        self.systems = [
            InputSystem(self.entity_manager),
            MovementSystem(self.entity_manager), 
            AnimationSystem(self.entity_manager),
            RenderSystem(self.entity_manager, self.game.screen)
        ]
        
        # Create player in center of hub
        self.create_player()
        
        # Create hub elements
        self.create_artifact_altars()
        self.create_npcs()
        self.create_arena_portal()
        
        print("Hub Scene initialized with altars, NPCs, and portal")
    
    def create_player(self) -> None:
        """Create or restore player in hub."""
        # Get player data from transition or create new
        transition_data = self.get_transition_data()
        player_health = transition_data.get('player_health', {'current': 100, 'max': 100})
        
        self.player_id = create_player_entity(
            self.entity_manager,
            x=self.center_x,
            y=self.center_y
        )
        
        # Restore health if returning from arena
        if 'player_health' in transition_data:
            health = self.entity_manager.get_component(self.player_id, Health)
            if health is not None:
                health.current_hp = player_health['current']
                health.max_hp = player_health['max']
        
        # Set player sprite
        player_sprite = self.entity_manager.get_component(self.player_id, SpriteRenderer)
        if player_sprite is not None:
            player_sprite.sprite_sheet = get_sprite("player_anubis")
    
    def create_artifact_altars(self) -> None:
        """Create artifact selection altars around the hub."""
        # 4 altars in cardinal directions (like Hades boons)
        altar_positions = [
            (self.center_x, self.center_y - 200, "Altar of Ra"),      # North
            (self.center_x + 200, self.center_y, "Altar of Thoth"),   # East  
            (self.center_x, self.center_y + 200, "Altar of Isis"),    # South
            (self.center_x - 200, self.center_y, "Altar of Ptah")     # West
        ]
        
        for x, y, altar_name in altar_positions:
            altar_id = self.create_altar(x, y, altar_name)
            self.altars.append(altar_id)
    
    def create_altar(self, x: float, y: float, name: str) -> int:
        """Create an artifact altar entity."""
        altar_id = (EntityBuilder(self.entity_manager)
                   .with_component(Transform(x=x, y=y))
                   .with_component(SpriteRenderer(
                       frame_width=64,
                       frame_height=64,
                       frames_per_row=1,
                       total_frames=1,
                       color_tint=(218, 165, 32)  # Golden
                   ))
                   .build())
        
        # Set altar sprite (placeholder for now)
        altar_sprite = self.entity_manager.get_component(altar_id, SpriteRenderer)
        if altar_sprite is not None:
            altar_sprite.sprite_sheet = get_sprite("scarab_enemy")  # Temporary
            altar_sprite.color_tint = (218, 165, 32)  # Golden tint
        
        return altar_id
    
    def create_npcs(self) -> None:
        """Create NPCs for upgrades (Mirror of Nyx style)."""
        # Egyptian NPCs for permanent upgrades
        npc_positions = [
            (self.center_x - 300, self.center_y - 100, "Mirror of Anubis"),
            (self.center_x + 300, self.center_y + 100, "Merchant of Memphis")
        ]
        
        for x, y, npc_name in npc_positions:
            npc_id = self.create_npc(x, y, npc_name)
            self.npcs.append(npc_id)
    
    def create_npc(self, x: float, y: float, name: str) -> int:
        """Create an NPC entity."""
        npc_id = (EntityBuilder(self.entity_manager)
                 .with_component(Transform(x=x, y=y))
                 .with_component(SpriteRenderer(
                     frame_width=48,
                     frame_height=64,
                     frames_per_row=1,
                     total_frames=1,
                     color_tint=(139, 69, 19)  # Brown/bronze
                 ))
                 .build())
        
        # Set NPC sprite
        npc_sprite = self.entity_manager.get_component(npc_id, SpriteRenderer)
        if npc_sprite is not None:
            npc_sprite.sprite_sheet = get_sprite("player_anubis")  # Temporary
            npc_sprite.color_tint = (139, 69, 19)  # Brown tint
        
        return npc_id
    
    def create_arena_portal(self) -> None:
        """Create portal to arena (like Hades' doorway)."""
        self.portal_id = (EntityBuilder(self.entity_manager)
                         .with_component(Transform(
                             x=self.center_x,
                             y=self.center_y + 300
                         ))
                         .with_component(SpriteRenderer(
                             frame_width=96,
                             frame_height=96,
                             frames_per_row=1,
                             total_frames=1,
                             color_tint=(138, 43, 226)  # Purple portal
                         ))
                         .build())
        
        # Set portal sprite
        portal_sprite = self.entity_manager.get_component(self.portal_id, SpriteRenderer)
        if portal_sprite is not None:
            portal_sprite.sprite_sheet = get_sprite("scarab_enemy")  # Temporary
            portal_sprite.color_tint = (138, 43, 226)  # Purple portal tint
    
    def update(self, dt: float) -> Optional[str]:
        """Update hub logic."""
        # Update ECS systems
        for system in self.systems:
            system.update(dt)
        
        # Check for interactions
        return self.check_interactions()
    
    def check_interactions(self) -> Optional[str]:
        """Check for player interactions with hub elements."""
        if self.player_id is None:
            return None
        
        player_transform = self.entity_manager.get_component(self.player_id, Transform)
        if player_transform is None:
            return None
        
        # Check portal interaction
        if self.portal_id is not None:
            portal_transform = self.entity_manager.get_component(self.portal_id, Transform)
            if portal_transform is not None:
                distance = math.sqrt(
                    (player_transform.x - portal_transform.x) ** 2 +
                    (player_transform.y - portal_transform.y) ** 2
                )
                
                # If close to portal and pressing E
                keys = pygame.key.get_pressed()
                if distance < 80 and keys[pygame.K_e]:
                    # Transition to arena
                    player_health = self.entity_manager.get_component(self.player_id, Health)
                    health_data = {
                        'current': player_health.current_hp if player_health else 100,
                        'max': player_health.max_hp if player_health else 100
                    }
                    
                    self.set_transition_data({
                        'player_health': health_data,
                        'artifacts': [],  # TODO: Add current artifacts
                        'from_scene': 'hub'
                    })
                    
                    return "arena"
        
        # TODO: Check altar and NPC interactions
        
        return None
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the hub scene."""
        # Clear with temple/tomb background color
        screen.fill((42, 35, 28))  # Dark sand/stone
        
        # Render all entities (handled by RenderSystem)
        
        # Draw hub UI
        if self.show_ui:
            self.draw_hub_ui(screen)
    
    def draw_hub_ui(self, screen: pygame.Surface) -> None:
        """Draw Hub-specific UI elements."""
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)
        
        # Title
        title = font.render("Hall of Anubis", True, (218, 165, 32))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "WASD: Move around the hall",
            "E: Enter Arena Portal (bottom)",
            "Approach altars to select artifacts",
            "Visit NPCs for permanent upgrades"
        ]
        
        y_offset = screen.get_height() - 150
        for instruction in instructions:
            text = small_font.render(instruction, True, (255, 215, 0))
            screen.blit(text, (20, y_offset))
            y_offset += 30
        
        # Show player health
        if self.player_id is not None:
            player_health = self.entity_manager.get_component(self.player_id, Health)
            if player_health is not None:
                health_text = f"Health: {player_health.current_hp}/{player_health.max_hp}"
                health_surface = small_font.render(health_text, True, (255, 0, 0) if player_health.current_hp < 30 else (0, 255, 0))
                screen.blit(health_surface, (20, 20))
        
        # Portal proximity indicator
        if self.player_id is not None and self.portal_id is not None:
            player_transform = self.entity_manager.get_component(self.player_id, Transform)
            portal_transform = self.entity_manager.get_component(self.portal_id, Transform)
            
            if player_transform and portal_transform:
                distance = math.sqrt(
                    (player_transform.x - portal_transform.x) ** 2 +
                    (player_transform.y - portal_transform.y) ** 2
                )
                
                if distance < 80:
                    prompt = font.render("Press E to Enter Arena", True, (255, 255, 255))
                    prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
                    
                    # Draw background
                    pygame.draw.rect(screen, (0, 0, 0), prompt_rect.inflate(20, 10))
                    pygame.draw.rect(screen, (218, 165, 32), prompt_rect.inflate(20, 10), 3)
                    screen.blit(prompt, prompt_rect)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle hub-specific events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.show_ui = not self.show_ui
            elif event.key == pygame.K_h:
                # Show help
                print("Hub Controls: WASD=Move, E=Interact, TAB=Toggle UI")