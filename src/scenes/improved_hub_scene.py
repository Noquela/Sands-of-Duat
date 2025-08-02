"""
Improved Hub Scene - Enhanced Hall of Anubis with more visual content
Based on Hades' Hall of Styx design with Egyptian theming
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

class ImprovedHubScene(Scene):
    """Enhanced Hub scene with better visual layout and more content."""
    
    def __init__(self, game):
        super().__init__(game)
        self.player_id: Optional[int] = None
        self.altars: List[int] = []
        self.npcs: List[int] = []
        self.decorations: List[int] = []
        self.portal_id: Optional[int] = None
        self.show_ui = True
        
        # Enhanced hub layout (larger Egyptian temple)
        self.hub_width = 1600
        self.hub_height = 1200
        self.center_x = self.hub_width // 2
        self.center_y = self.hub_height // 2
        
        # Visual enhancement data
        self.background_tiles = []
        self.lighting_effects = []
        self.particle_systems = []
        
        print("Improved Hub Scene initialized with enhanced visuals")
    
    def initialize(self) -> None:
        """Initialize the enhanced Hub scene."""
        print("Initializing Enhanced Hub Scene (Hall of Anubis)...")
        
        # Setup ECS systems with improved rendering
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
        
        # Create enhanced hub elements
        self.create_background_elements()
        self.create_player()
        self.create_enhanced_altars()
        self.create_egyptian_npcs()
        self.create_decorative_elements()
        self.create_arena_portal()
        
        print("Enhanced Hub Scene initialized with Egyptian temple layout")
    
    def create_background_elements(self) -> None:
        """Create background visual elements for the temple."""
        # Create visual background data (not entities, just for rendering)
        
        # Temple floor pattern
        tile_size = 64
        for x in range(0, self.hub_width, tile_size):
            for y in range(0, self.hub_height, tile_size):
                # Alternating floor pattern
                tile_type = "dark" if (x // tile_size + y // tile_size) % 2 == 0 else "light"
                self.background_tiles.append({
                    "x": x, "y": y, "size": tile_size, "type": tile_type
                })
        
        # Pillars around the perimeter
        pillar_positions = [
            (200, 200), (200, 400), (200, 600), (200, 800), (200, 1000),
            (1400, 200), (1400, 400), (1400, 600), (1400, 800), (1400, 1000),
            (400, 150), (800, 150), (1200, 150),
            (400, 1050), (800, 1050), (1200, 1050)
        ]
        
        for x, y in pillar_positions:
            self.decorations.append({
                "type": "pillar", "x": x, "y": y, "width": 80, "height": 120
            })
        
        print("Background elements created: temple floor and pillars")
    
    def create_player(self) -> None:
        """Create player with enhanced positioning."""
        # Get player data from transition or create new
        transition_data = self.get_transition_data()
        player_health = transition_data.get('player_health', {'current': 100, 'max': 100})
        
        # Place player in center of main hall
        self.player_id = create_player_entity(
            self.entity_manager,
            x=self.center_x,
            y=self.center_y + 100  # Slightly below center for better view
        )
        
        # Restore health if returning from arena
        if 'player_health' in transition_data:
            health = self.entity_manager.get_component(self.player_id, Health)
            if health is not None:
                health.current_hp = player_health['current']
                health.max_hp = player_health['max']
        
        # Set player sprite (using organized assets)
        player_sprite = self.entity_manager.get_component(self.player_id, SpriteRenderer)
        if player_sprite is not None:
            player_sprite.sprite_sheet = get_sprite("player_anubis")
        
        print(f"Player created at enhanced position: ({self.center_x}, {self.center_y + 100})")
    
    def create_enhanced_altars(self) -> None:
        """Create Egyptian god altars in enhanced circular layout."""
        # Altars in a larger circle around the center
        altar_radius = 300
        altar_configs = [
            (0, "Ra", "Sun God - Damage & Divine Power"),      # North
            (math.pi/2, "Thoth", "Wisdom God - Knowledge & Magic"),   # East  
            (math.pi, "Isis", "Protection Goddess - Health & Defense"),    # South
            (3*math.pi/2, "Ptah", "Creator God - Crafting & Items")     # West
        ]
        
        for angle, god_type, description in altar_configs:
            x = self.center_x + int(altar_radius * math.cos(angle))
            y = self.center_y + int(altar_radius * math.sin(angle))
            
            altar_id = create_egyptian_altar(self.entity_manager, x, y, god_type)
            self.altars.append(altar_id)
            
            # Set altar sprite using organized assets
            altar_sprite = self.entity_manager.get_component(altar_id, SpriteRenderer)
            if altar_sprite is not None:
                sprite_name = f"altar_{god_type.lower()}"
                altar_sprite.sprite_sheet = get_sprite(sprite_name)
                print(f"Created {god_type} altar at ({x}, {y}) - {description}")
        
        print("Enhanced altar layout created in circular formation")
    
    def create_egyptian_npcs(self) -> None:
        """Create Egyptian NPCs in strategic positions."""
        # Enhanced NPC placement
        npc_configs = [
            # Mirror of Anubis - for upgrades (left side)
            (self.center_x - 400, self.center_y - 200, "mirror_anubis", "Divine Mirror - Permanent Upgrades"),
            
            # Merchant - for items (right side)  
            (self.center_x + 400, self.center_y + 200, "merchant", "Khenti-Kheti - Artifact Merchant"),
            
            # Oracle - for lore (upper area)
            (self.center_x, self.center_y - 350, "oracle", "Oracle of Thoth - Ancient Wisdom"),
            
            # Guard Captain - for combat training (lower area)
            (self.center_x, self.center_y + 400, "guard_captain", "Captain Khufti - Combat Training")
        ]
        
        for x, y, npc_type, description in npc_configs:
            npc_id = create_egyptian_npc(self.entity_manager, x, y, npc_type)
            self.npcs.append(npc_id)
            
            # Set NPC sprite
            npc_sprite = self.entity_manager.get_component(npc_id, SpriteRenderer)
            if npc_sprite is not None:
                sprite_name = f"npc_{npc_type}"
                sprite_surface = get_sprite(sprite_name)
                if sprite_surface:
                    npc_sprite.sprite_sheet = sprite_surface
                else:
                    # Create distinct placeholder for each NPC type
                    npc_sprite.sprite_sheet = self._create_npc_placeholder(npc_type)
                
                print(f"Created {npc_type} at ({x}, {y}) - {description}")
        
        print("Enhanced NPCs created with specialized roles")
    
    def _create_npc_placeholder(self, npc_type: str) -> pygame.Surface:
        """Create distinct placeholder sprites for different NPC types."""
        sprite = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Different colors for different NPC types
        npc_colors = {
            "mirror_anubis": (72, 61, 139),    # Dark slate blue
            "merchant": (184, 134, 11),        # Dark goldenrod
            "oracle": (138, 43, 226),          # Blue violet  
            "guard_captain": (139, 69, 19)     # Saddle brown
        }
        
        color = npc_colors.get(npc_type, (128, 128, 128))
        
        # Draw NPC shape
        pygame.draw.ellipse(sprite, color, (16, 16, 32, 48))  # Body
        pygame.draw.circle(sprite, color, (32, 20), 12)       # Head
        
        # Add distinguishing features
        if npc_type == "mirror_anubis":
            # Anubis ears
            pygame.draw.polygon(sprite, color, [(20, 15), (25, 5), (30, 15)])
            pygame.draw.polygon(sprite, color, [(34, 15), (39, 5), (44, 15)])
        elif npc_type == "merchant":
            # Merchant hat
            pygame.draw.rect(sprite, (255, 215, 0), (26, 8, 12, 8))
        elif npc_type == "oracle":
            # Mystical aura
            pygame.draw.circle(sprite, (255, 255, 255), (32, 32), 30, 2)
        
        return sprite
    
    def create_decorative_elements(self) -> None:
        """Create decorative elements to enhance the temple atmosphere."""
        # Torches around altars
        torch_positions = []
        altar_radius = 300
        for i in range(8):  # 8 torches around the altar circle
            angle = i * math.pi / 4
            x = self.center_x + int((altar_radius + 80) * math.cos(angle))
            y = self.center_y + int((altar_radius + 80) * math.sin(angle))
            torch_positions.append((x, y))
        
        for x, y in torch_positions:
            self.decorations.append({
                "type": "torch", "x": x, "y": y, "width": 16, "height": 32,
                "flame_offset": 0  # For animation
            })
        
        # Central brazier
        self.decorations.append({
            "type": "brazier", "x": self.center_x, "y": self.center_y - 50,
            "width": 48, "height": 48, "flame_offset": 0
        })
        
        # Sacred symbols on the floor
        symbol_positions = [
            (self.center_x - 150, self.center_y - 150, "ankh"),
            (self.center_x + 150, self.center_y - 150, "eye_of_horus"),
            (self.center_x - 150, self.center_y + 150, "scarab"),
            (self.center_x + 150, self.center_y + 150, "djed")
        ]
        
        for x, y, symbol_type in symbol_positions:
            self.decorations.append({
                "type": "floor_symbol", "x": x, "y": y, "width": 32, "height": 32,
                "symbol": symbol_type
            })
        
        print("Decorative elements added: torches, brazier, and sacred symbols")
    
    def create_arena_portal(self) -> None:
        """Create enhanced arena portal."""
        # Place portal in ceremonial position (south of center)
        portal_x = self.center_x
        portal_y = self.center_y + 450
        
        self.portal_id = create_arena_portal(self.entity_manager, portal_x, portal_y)
        
        # Set portal sprite using organized assets
        portal_sprite = self.entity_manager.get_component(self.portal_id, SpriteRenderer)
        if portal_sprite is not None:
            portal_surface = get_sprite("portal_arena")
            if portal_surface:
                portal_sprite.sprite_sheet = portal_surface
                print("Using organized portal sprite")
            else:
                # Enhanced placeholder portal
                portal_sprite.sprite_sheet = self._create_enhanced_portal_placeholder()
                print("Using enhanced placeholder portal sprite")
        
        print(f"Enhanced arena portal created at ({portal_x}, {portal_y})")
    
    def _create_enhanced_portal_placeholder(self) -> pygame.Surface:
        """Create an enhanced placeholder for the portal."""
        sprite = pygame.Surface((128, 128), pygame.SRCALPHA)
        
        # Portal archway
        pygame.draw.ellipse(sprite, (138, 43, 226), (16, 16, 96, 96), 8)  # Purple ring
        pygame.draw.ellipse(sprite, (75, 0, 130), (24, 24, 80, 80), 4)    # Inner ring
        
        # Energy swirl (simplified)
        center = (64, 64)
        for i in range(8):
            angle = i * math.pi / 4
            start_x = center[0] + int(30 * math.cos(angle))
            start_y = center[1] + int(30 * math.sin(angle))
            end_x = center[0] + int(20 * math.cos(angle + 0.5))
            end_y = center[1] + int(20 * math.sin(angle + 0.5))
            pygame.draw.line(sprite, (255, 215, 0), (start_x, start_y), (end_x, end_y), 3)
        
        return sprite
    
    def update(self, dt: float) -> Optional[str]:
        """Update enhanced hub logic."""
        # Update ECS systems
        for system in self.systems:
            system.update(dt)
        
        # Update decorative animations
        self._update_decorative_animations(dt)
        
        # Check for interactions
        return self.check_interactions()
    
    def _update_decorative_animations(self, dt: float) -> None:
        """Update animations for decorative elements."""
        # Animate torch flames and other decorative elements
        for decoration in self.decorations:
            if decoration["type"] in ["torch", "brazier"]:
                decoration["flame_offset"] += dt * 5  # Flame flicker speed
                if decoration["flame_offset"] > math.pi * 2:
                    decoration["flame_offset"] = 0
    
    def check_interactions(self) -> Optional[str]:
        """Enhanced interaction checking."""
        if self.player_id is None:
            return None
        
        player_transform = self.entity_manager.get_component(self.player_id, Transform)
        if player_transform is None:
            return None
        
        # Check portal interaction with enhanced feedback
        if self.portal_id is not None:
            portal_transform = self.entity_manager.get_component(self.portal_id, Transform)
            if portal_transform is not None:
                distance = math.sqrt(
                    (player_transform.x - portal_transform.x) ** 2 +
                    (player_transform.y - portal_transform.y) ** 2
                )
                
                # Enhanced interaction range and feedback
                keys = pygame.key.get_pressed()
                if distance < 100 and keys[pygame.K_e]:
                    # Transition to arena with enhanced data
                    player_health = self.entity_manager.get_component(self.player_id, Health)
                    player_inventory = self.entity_manager.get_component(self.player_id, ArtifactInventory)
                    
                    health_data = {
                        'current': player_health.current_hp if player_health else 100,
                        'max': player_health.max_hp if player_health else 100
                    }
                    
                    artifacts_data = []
                    if player_inventory:
                        artifacts_data = player_inventory.equipped_artifacts.copy()
                    
                    self.set_transition_data({
                        'player_health': health_data,
                        'artifacts': artifacts_data,
                        'from_scene': 'enhanced_hub',
                        'hub_visit_count': transition_data.get('hub_visit_count', 0) + 1
                    })
                    
                    return "arena"
        
        # Enhanced debug features
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:  # T for test artifact
            self.add_test_artifact()
        elif keys[pygame.K_r]:  # R for restore health
            self.restore_player_health()
        
        return None
    
    def add_test_artifact(self) -> None:
        """Enhanced test artifact system."""
        if self.player_id is None:
            return
        
        player_inventory = self.entity_manager.get_component(self.player_id, ArtifactInventory)
        if player_inventory is None:
            return
        
        # Enhanced test artifacts with Egyptian theming
        test_artifacts = [
            "Ra's Solar Blessing - +25% Damage",
            "Thoth's Wisdom Scroll - +15% Magic Power", 
            "Isis's Protective Charm - +20% Health",
            "Ptah's Crafting Hammer - +10% Item Quality",
            "Anubis's Judgment Scale - +Critical Hit Chance",
            "Horus's Eagle Eye - +Range & Accuracy"
        ]
        
        for artifact in test_artifacts:
            artifact_name = artifact.split(" - ")[0]  # Get name part only
            if artifact_name not in [a.split(" - ")[0] for a in player_inventory.equipped_artifacts]:
                if player_inventory.add_artifact(artifact):
                    print(f"DEBUG: Added {artifact} to inventory")
                    break
    
    def restore_player_health(self) -> None:
        """Restore player health for testing."""
        if self.player_id is None:
            return
        
        player_health = self.entity_manager.get_component(self.player_id, Health)
        if player_health is not None:
            player_health.current_hp = player_health.max_hp
            print("DEBUG: Player health restored")
    
    def render(self, screen: pygame.Surface) -> None:
        """Enhanced rendering with background elements."""
        # Clear with enhanced temple background
        screen.fill((28, 25, 23))  # Darker stone color
        
        # Render background elements first
        self._render_background_elements(screen)
        
        # Render decorative elements
        self._render_decorative_elements(screen)
        
        # Render all entities with SDXL assets
        self._render_sdxl_entities(screen)
        
        # Render enhanced UI
        if self.show_ui:
            self.draw_enhanced_hub_ui(screen)
        
        # Draw interaction prompts
        self.draw_interaction_prompts(screen)
    
    def _render_background_elements(self, screen: pygame.Surface) -> None:
        """Render background temple elements."""
        # Get camera offset from render system
        render_system = None
        for system in self.systems:
            if isinstance(system, RenderSystem):
                render_system = system
                break
        
        camera_x = render_system.camera_x if render_system else 0
        camera_y = render_system.camera_y if render_system else 0
        
        # Render floor tiles
        for tile in self.background_tiles:
            screen_x = tile["x"] - camera_x
            screen_y = tile["y"] - camera_y
            
            # Only render tiles visible on screen
            if -64 <= screen_x <= screen.get_width() and -64 <= screen_y <= screen.get_height():
                color = (45, 38, 35) if tile["type"] == "dark" else (52, 45, 40)
                pygame.draw.rect(screen, color, (screen_x, screen_y, tile["size"], tile["size"]))
                # Add subtle border
                pygame.draw.rect(screen, (35, 30, 25), (screen_x, screen_y, tile["size"], tile["size"]), 1)
    
    def _render_sdxl_entities(self, screen: pygame.Surface) -> None:
        """Render entities with SDXL assets directly"""
        # Get camera offset
        render_system = None
        for system in self.systems:
            if isinstance(system, RenderSystem):
                render_system = system
                break
        
        camera_x = render_system.camera_x if render_system else 0
        camera_y = render_system.camera_y if render_system else 0
        
        # Render player
        if self.player_id is not None:
            player_transform = self.entity_manager.get_component(self.player_id, Transform)
            if player_transform:
                player_sprite = get_sprite("player_anubis")
                if player_sprite:
                    screen_x = player_transform.x - camera_x - player_sprite.get_width() // 2
                    screen_y = player_transform.y - camera_y - player_sprite.get_height() // 2
                    screen.blit(player_sprite, (screen_x, screen_y))
        
        # Render altars
        for altar_id in self.altars:
            altar_transform = self.entity_manager.get_component(altar_id, Transform)
            if altar_transform:
                # Determine which altar this is based on position
                if abs(altar_transform.x - (self.center_x + 300)) < 50:  # Ra (east)
                    altar_sprite = get_sprite("altar_ra")
                elif abs(altar_transform.x - (self.center_x - 300)) < 50:  # Isis (west)
                    altar_sprite = get_sprite("altar_isis")
                elif abs(altar_transform.y - (self.center_y - 300)) < 50:  # Ptah (north)
                    altar_sprite = get_sprite("altar_ptah")
                else:  # Thoth (south)
                    altar_sprite = get_sprite("altar_thoth")
                
                if altar_sprite:
                    screen_x = altar_transform.x - camera_x - altar_sprite.get_width() // 2
                    screen_y = altar_transform.y - camera_y - altar_sprite.get_height() // 2
                    screen.blit(altar_sprite, (screen_x, screen_y))
        
        # Render portal
        if self.portal_id is not None:
            portal_transform = self.entity_manager.get_component(self.portal_id, Transform)
            if portal_transform:
                portal_sprite = get_sprite("portal_arena")
                if portal_sprite:
                    screen_x = portal_transform.x - camera_x - portal_sprite.get_width() // 2
                    screen_y = portal_transform.y - camera_y - portal_sprite.get_height() // 2
                    screen.blit(portal_sprite, (screen_x, screen_y))
    
    def _render_decorative_elements(self, screen: pygame.Surface) -> None:
        """Render decorative temple elements."""
        # Get camera offset
        render_system = None
        for system in self.systems:
            if isinstance(system, RenderSystem):
                render_system = system
                break
        
        camera_x = render_system.camera_x if render_system else 0
        camera_y = render_system.camera_y if render_system else 0
        
        for decoration in self.decorations:
            screen_x = decoration["x"] - camera_x
            screen_y = decoration["y"] - camera_y
            
            # Only render decorations visible on screen
            if -100 <= screen_x <= screen.get_width() and -100 <= screen_y <= screen.get_height():
                if decoration["type"] == "pillar":
                    # Egyptian stone pillar
                    pygame.draw.rect(screen, (139, 126, 102), 
                                   (screen_x, screen_y, decoration["width"], decoration["height"]))
                    pygame.draw.rect(screen, (160, 145, 115), 
                                   (screen_x, screen_y, decoration["width"], decoration["height"]), 3)
                    # Hieroglyphic details (simplified)
                    for i in range(3):
                        y_offset = decoration["height"] // 4 + i * decoration["height"] // 4
                        pygame.draw.line(screen, (101, 67, 33), 
                                       (screen_x + 10, screen_y + y_offset),
                                       (screen_x + decoration["width"] - 10, screen_y + y_offset), 2)
                
                elif decoration["type"] == "torch":
                    # Torch base
                    pygame.draw.rect(screen, (139, 69, 19), 
                                   (screen_x, screen_y + 16, 16, 16))
                    # Torch flame (animated)
                    flame_height = 16 + int(4 * math.sin(decoration["flame_offset"]))
                    flame_colors = [(255, 100, 0), (255, 200, 0), (255, 255, 100)]
                    for i, color in enumerate(flame_colors):
                        offset = i * 2
                        pygame.draw.ellipse(screen, color,
                                          (screen_x + 4 + offset, screen_y + 16 - flame_height + offset,
                                           8 - offset, flame_height - offset))
                
                elif decoration["type"] == "brazier":
                    # Central brazier
                    pygame.draw.ellipse(screen, (139, 126, 102),
                                      (screen_x, screen_y + 32, decoration["width"], 16))
                    # Large flame
                    flame_height = 32 + int(8 * math.sin(decoration["flame_offset"]))
                    flame_colors = [(255, 69, 0), (255, 140, 0), (255, 215, 0)]
                    for i, color in enumerate(flame_colors):
                        offset = i * 3
                        pygame.draw.ellipse(screen, color,
                                          (screen_x + 8 + offset, screen_y + 32 - flame_height + offset,
                                           32 - offset * 2, flame_height - offset))
                
                elif decoration["type"] == "floor_symbol":
                    # Sacred Egyptian symbols
                    symbol_colors = {
                        "ankh": (255, 215, 0),          # Gold
                        "eye_of_horus": (65, 105, 225), # Royal blue
                        "scarab": (34, 139, 34),        # Forest green
                        "djed": (138, 43, 226)          # Blue violet
                    }
                    color = symbol_colors.get(decoration["symbol"], (255, 255, 255))
                    
                    # Simple symbol representation
                    center_x = screen_x + decoration["width"] // 2
                    center_y = screen_y + decoration["height"] // 2
                    
                    if decoration["symbol"] == "ankh":
                        # Ankh symbol (simplified)
                        pygame.draw.circle(screen, color, (center_x, center_y - 8), 6, 2)
                        pygame.draw.line(screen, color, (center_x, center_y - 2), (center_x, center_y + 12), 3)
                        pygame.draw.line(screen, color, (center_x - 6, center_y + 4), (center_x + 6, center_y + 4), 3)
                    else:
                        # Other symbols as circles with inner patterns
                        pygame.draw.circle(screen, color, (center_x, center_y), 12, 2)
                        pygame.draw.circle(screen, color, (center_x, center_y), 6, 1)
    
    def draw_enhanced_hub_ui(self, screen: pygame.Surface) -> None:
        """Draw enhanced Hub UI with more information."""
        font = pygame.font.Font(None, 48)
        medium_font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Enhanced title with subtitle
        title = font.render("Hall of Anubis", True, (218, 165, 32))
        subtitle = medium_font.render("Sacred Temple of the Jackal God", True, (184, 134, 11))
        
        title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
        subtitle_rect = subtitle.get_rect(center=(screen.get_width() // 2, 85))
        
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        
        # Enhanced instructions with categories
        instruction_categories = [
            ("Movement:", ["WASD: Navigate the sacred halls"]),
            ("Interactions:", ["E: Enter Arena Portal", "E: Approach altars for blessings", "E: Speak with NPCs"]),
            ("Debug:", ["T: Test artifacts", "R: Restore health", "TAB: Toggle UI"])
        ]
        
        y_offset = screen.get_height() - 200
        for category, instructions in instruction_categories:
            # Category header
            category_text = medium_font.render(category, True, (255, 215, 0))
            screen.blit(category_text, (20, y_offset))
            y_offset += 30
            
            # Instructions
            for instruction in instructions:
                text = small_font.render(f"  {instruction}", True, (255, 255, 255))
                screen.blit(text, (20, y_offset))
                y_offset += 22
            
            y_offset += 10  # Space between categories
        
        # Enhanced player status display
        if self.player_id is not None:
            self._draw_enhanced_player_status(screen, small_font, medium_font)
    
    def _draw_enhanced_player_status(self, screen: pygame.Surface, small_font, medium_font) -> None:
        """Draw enhanced player status information."""
        player_health = self.entity_manager.get_component(self.player_id, Health)
        player_inventory = self.entity_manager.get_component(self.player_id, ArtifactInventory)
        
        # Health display with bar
        if player_health is not None:
            health_percent = player_health.current_hp / player_health.max_hp
            
            # Health text
            health_text = f"Anubis Warrior Health: {player_health.current_hp:.0f}/{player_health.max_hp:.0f}"
            health_color = (255, 0, 0) if health_percent < 0.3 else (255, 255, 0) if health_percent < 0.7 else (0, 255, 0)
            health_surface = small_font.render(health_text, True, health_color)
            screen.blit(health_surface, (20, 20))
            
            # Health bar
            bar_width = 200
            bar_height = 16
            bar_x, bar_y = 20, 45
            
            pygame.draw.rect(screen, (64, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, int(bar_width * health_percent), bar_height))
            pygame.draw.rect(screen, (255, 215, 0), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Enhanced artifact display
        if player_inventory is not None:
            artifacts_header = f"Divine Artifacts ({len(player_inventory.equipped_artifacts)}/{player_inventory.max_artifacts}):"
            artifacts_surface = small_font.render(artifacts_header, True, (218, 165, 32))
            screen.blit(artifacts_surface, (20, 70))
            
            # List artifacts with descriptions
            y_pos = 95
            for i, artifact in enumerate(player_inventory.equipped_artifacts[:6]):  # Show up to 6
                artifact_text = f"  {i+1}. {artifact}"
                artifact_surface = small_font.render(artifact_text, True, (255, 215, 0))
                screen.blit(artifact_surface, (20, y_pos))
                y_pos += 20
            
            if len(player_inventory.equipped_artifacts) > 6:
                more_text = f"  ... and {len(player_inventory.equipped_artifacts) - 6} more"
                more_surface = small_font.render(more_text, True, (184, 134, 11))
                screen.blit(more_surface, (20, y_pos))
    
    def draw_interaction_prompts(self, screen: pygame.Surface) -> None:
        """Draw enhanced interaction prompts."""
        # Portal proximity with enhanced feedback
        if self.player_id is not None and self.portal_id is not None:
            player_transform = self.entity_manager.get_component(self.player_id, Transform)
            portal_transform = self.entity_manager.get_component(self.portal_id, Transform)
            
            if player_transform and portal_transform:
                distance = math.sqrt(
                    (player_transform.x - portal_transform.x) ** 2 +
                    (player_transform.y - portal_transform.y) ** 2
                )
                
                if distance < 100:
                    font = pygame.font.Font(None, 42)
                    prompt = font.render("Press E to Enter the Arena of Trials", True, (255, 255, 255))
                    subtitle = pygame.font.Font(None, 28).render("Face the challenges of the Egyptian underworld", True, (218, 165, 32))
                    
                    prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 120))
                    subtitle_rect = subtitle.get_rect(center=(screen.get_width() // 2, screen.get_height() - 90))
                    
                    # Enhanced background with Egyptian styling
                    bg_rect = prompt_rect.inflate(40, 50)
                    bg_rect.union_ip(subtitle_rect.inflate(40, 20))
                    
                    pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
                    pygame.draw.rect(screen, (218, 165, 32), bg_rect, 3)
                    
                    # Golden corner decorations
                    corner_size = 8
                    corners = [bg_rect.topleft, (bg_rect.right - corner_size, bg_rect.top),
                              bg_rect.bottomleft, (bg_rect.right - corner_size, bg_rect.bottom - corner_size)]
                    for corner in corners:
                        pygame.draw.rect(screen, (255, 215, 0), (*corner, corner_size, corner_size))
                    
                    screen.blit(prompt, prompt_rect)
                    screen.blit(subtitle, subtitle_rect)
        
        # System interaction prompts
        system_prompt = self.interaction_system.get_interaction_prompt()
        if system_prompt is not None:
            font = pygame.font.Font(None, 32)
            prompt_text = system_prompt['text']
            prompt_pos = system_prompt['position']
            
            text_surface = font.render(prompt_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            
            # Convert world position to screen position
            render_system = None
            for system in self.systems:
                if isinstance(system, RenderSystem):
                    render_system = system
                    break
            
            if render_system:
                screen_x = prompt_pos[0] - render_system.camera_x
                screen_y = prompt_pos[1] - render_system.camera_y - 40  # Above entity
                text_rect.center = (screen_x, screen_y)
                
                # Enhanced interaction prompt background
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect)
                pygame.draw.rect(screen, (218, 165, 32), bg_rect, 2)
                screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle enhanced hub events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.show_ui = not self.show_ui
            elif event.key == pygame.K_h:
                # Enhanced help
                print("Enhanced Hub Controls:")
                print("  WASD = Navigate temple halls")
                print("  E = Interact with portals, altars, NPCs") 
                print("  TAB = Toggle UI display")
                print("  T = Add test artifact (debug)")
                print("  R = Restore health (debug)")
                print("  H = Show this help")