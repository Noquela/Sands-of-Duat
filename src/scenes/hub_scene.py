"""
Hub Scene - The main lobby like Hades' Hall of Styx
Central area where player manages artifacts, upgrades, and starts runs
"""

import pygame
import math
from typing import Optional, Dict, Any, List
from .scene import Scene
from ecs import (
    EntityManager, create_player_entity, create_egyptian_altar, 
    create_egyptian_npc, create_arena_portal, EntityBuilder,
    InputSystem, MovementSystem, AnimationSystem, RenderSystem,
    ArtifactSystem, InteractionSystem, HealthSystem,
    Transform, SpriteRenderer, Health, PlayerTag, ArtifactInventory
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
        
        # Setup ECS systems including Egyptian artifact and interaction systems
        self.interaction_system = InteractionSystem(self.entity_manager)
        self.systems = [
            InputSystem(self.entity_manager),
            MovementSystem(self.entity_manager), 
            AnimationSystem(self.entity_manager),
            ArtifactSystem(self.entity_manager),
            self.interaction_system,
            HealthSystem(self.entity_manager),
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
        """Create Egyptian god altars around the hub."""
        # 4 Egyptian god altars in cardinal directions
        altar_configs = [
            (self.center_x, self.center_y - 200, "Ra"),      # North - Sun God
            (self.center_x + 200, self.center_y, "Thoth"),   # East - Wisdom God
            (self.center_x, self.center_y + 200, "Isis"),    # South - Protection Goddess
            (self.center_x - 200, self.center_y, "Ptah")     # West - Creator God
        ]
        
        for x, y, god_type in altar_configs:
            altar_id = create_egyptian_altar(self.entity_manager, x, y, god_type)
            self.altars.append(altar_id)
            
            # Set altar sprite
            altar_sprite = self.entity_manager.get_component(altar_id, SpriteRenderer)
            if altar_sprite is not None:
                sprite_name = f"altar_{god_type.lower()}"
                altar_sprite.sprite_sheet = get_sprite(sprite_name)
                print(f"Created {god_type} altar at ({x}, {y})")
    
    
    def create_npcs(self) -> None:
        """Create Egyptian NPCs for upgrades and dialogue."""
        # Egyptian NPCs for permanent upgrades and lore
        npc_configs = [
            (self.center_x - 300, self.center_y - 100, "mirror_anubis"),
            (self.center_x + 300, self.center_y + 100, "merchant")
        ]
        
        for x, y, npc_type in npc_configs:
            npc_id = create_egyptian_npc(self.entity_manager, x, y, npc_type)
            self.npcs.append(npc_id)
            
            # Set NPC sprite
            npc_sprite = self.entity_manager.get_component(npc_id, SpriteRenderer)
            if npc_sprite is not None:
                sprite_name = f"npc_{npc_type}"
                npc_sprite.sprite_sheet = get_sprite(sprite_name)
                print(f"Created {npc_type} NPC at ({x}, {y})")
    
    
    def create_arena_portal(self) -> None:
        """Create portal to arena (like Hades' doorway)."""
        self.portal_id = create_arena_portal(
            self.entity_manager,
            self.center_x,
            self.center_y + 300
        )
        
        # Set portal sprite
        portal_sprite = self.entity_manager.get_component(self.portal_id, SpriteRenderer)
        if portal_sprite is not None:
            # Try to use AI-generated portal sprite, fallback to placeholder
            ai_portal = get_sprite("portal_arena")
            if ai_portal:
                portal_sprite.sprite_sheet = ai_portal
                print("Using AI-generated portal sprite (32x32 scaled from 128x128)")
            else:
                portal_sprite.sprite_sheet = get_sprite("scarab_enemy")  # Fallback
                print("Using placeholder portal sprite")
    
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
        
        # Check if interaction system has a scene transition request
        # This would be triggered by portal interactions
        # The InteractionSystem handles the UI prompts and interactions
        
        # Check for debug artifact adding
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:  # T for test artifact
            self.add_test_artifact()
        
        # TODO: Handle portal scene transitions from interaction system
        
        return None
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the hub scene."""
        # Clear with temple/tomb background color
        screen.fill((42, 35, 28))  # Dark sand/stone
        
        # Render all entities (handled by RenderSystem)
        
        # Draw hub UI and interaction prompts
        if self.show_ui:
            self.draw_hub_ui(screen)
        
        # Draw interaction prompts from InteractionSystem
        self.draw_interaction_prompts(screen)
    
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
        
        # Show player health and artifacts
        if self.player_id is not None:
            player_health = self.entity_manager.get_component(self.player_id, Health)
            player_inventory = self.entity_manager.get_component(self.player_id, ArtifactInventory)
            
            if player_health is not None:
                health_text = f"Health: {player_health.current_hp:.0f}/{player_health.max_hp:.0f}"
                health_surface = small_font.render(health_text, True, (255, 0, 0) if player_health.current_hp < 30 else (0, 255, 0))
                screen.blit(health_surface, (20, 20))
            
            # Show equipped artifacts
            if player_inventory is not None and player_inventory.equipped_artifacts:
                artifact_text = f"Artifacts: {len(player_inventory.equipped_artifacts)}/{player_inventory.max_artifacts}"
                artifact_surface = small_font.render(artifact_text, True, (218, 165, 32))
                screen.blit(artifact_surface, (20, 50))
                
                # List first few artifacts
                y_pos = 80
                for i, artifact in enumerate(player_inventory.equipped_artifacts[:3]):
                    if i < 3:  # Show only first 3
                        artifact_line = small_font.render(f"- {artifact}", True, (255, 215, 0))
                        screen.blit(artifact_line, (30, y_pos))
                        y_pos += 25
        
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
    
    def draw_interaction_prompts(self, screen: pygame.Surface) -> None:
        """Draw interaction prompts from the InteractionSystem."""
        prompt = self.interaction_system.get_interaction_prompt()
        if prompt is None:
            return
        
        font = pygame.font.Font(None, 36)
        prompt_text = prompt['text']
        prompt_pos = prompt['position']
        
        # Render prompt text
        text_surface = font.render(prompt_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        
        # Convert world position to screen position (accounting for camera)
        render_system = None
        for system in self.systems:
            if isinstance(system, RenderSystem):
                render_system = system
                break
        
        if render_system:
            screen_x = prompt_pos[0] - render_system.camera_x
            screen_y = prompt_pos[1] - render_system.camera_y
            text_rect.center = (screen_x, screen_y)
            
            # Draw background
            pygame.draw.rect(screen, (0, 0, 0, 180), text_rect.inflate(20, 10))
            pygame.draw.rect(screen, (218, 165, 32), text_rect.inflate(20, 10), 2)
            screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle hub-specific events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.show_ui = not self.show_ui
            elif event.key == pygame.K_h:
                # Show help
                print("Hub Controls: WASD=Move, E=Interact, TAB=Toggle UI, T=Test Artifact")
    
    def add_test_artifact(self) -> None:
        """Add a test artifact for debugging."""
        if self.player_id is None:
            return
        
        player_inventory = self.entity_manager.get_component(self.player_id, ArtifactInventory)
        if player_inventory is None:
            return
        
        # Test artifacts from different gods
        test_artifacts = ["Solar Blessing", "Wisdom of Ages", "Mother's Protection", "Creator's Hammer"]
        
        for artifact in test_artifacts:
            if artifact not in player_inventory.equipped_artifacts:
                if player_inventory.add_artifact(artifact):
                    print(f"DEBUG: Added {artifact} to inventory")
                    break