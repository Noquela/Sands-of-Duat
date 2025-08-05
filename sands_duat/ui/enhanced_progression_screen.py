"""
Enhanced Progression Screen - Egyptian Underworld Map Interface

Provides an immersive temple map experience with Egyptian theming,
atmospheric effects, and improved visual storytelling.
"""

import pygame
import math
import random
from typing import Dict, List, Optional, Tuple, Any
from .base import UIScreen, UIComponent
from .hades_theme import HadesEgyptianTheme
from .progression_screen import TempleChambersMap


class EnhancedTempleMap(UIComponent):
    """Enhanced temple map with improved Egyptian underworld theming."""
    
    def __init__(self, x: int, y: int, width: int, height: int, hades_theme: HadesEgyptianTheme):
        super().__init__(x, y, width, height)
        self.hades_theme = hades_theme
        
        # Enhanced chamber system with better progression flow
        self.chambers = self._create_enhanced_chamber_layout()
        self.selected_chamber = None
        self.hover_chamber = None
        
        # Visual enhancements
        self.map_time = 0.0
        self.torch_flames = []
        self.floating_spirits = []
        self.sand_streams = []
        
        # Camera system for large maps
        self.camera_x = 0
        self.camera_y = 0
        self.target_camera_x = 0
        self.target_camera_y = 0
        self.zoom_level = 1.0
        
        # Initialize atmospheric elements
        self._initialize_atmospheric_elements()
    
    def _create_enhanced_chamber_layout(self) -> Dict[str, Dict[str, Any]]:
        """Create enhanced chamber layout with better visual progression."""
        chambers = {
            # ENTRANCE HALLS - Tutorial and Introduction
            "desert_threshold": {
                "name": "Desert's Threshold",
                "position": (150, 450),
                "size": "large",
                "chamber_type": "entrance",
                "unlocked": True,
                "completed": False,
                "description": "Where the living world meets the realm of the dead",
                "visual_style": "sandstone_gateway",
                "connections": ["anubis_judgment"],
                "rewards": ["starter_deck", "basic_tutorial"],
                "difficulty": 1,
                "atmospheric_effects": ["swirling_sand", "distant_hymns"]
            },
            
            "anubis_judgment": {
                "name": "Hall of Two Truths",
                "position": (350, 400),
                "size": "large",
                "chamber_type": "judgment",
                "unlocked": False,
                "completed": False,
                "description": "Anubis weighs your heart against the feather of Ma'at",
                "visual_style": "judgment_hall",
                "connections": ["osiris_chamber", "ra_trial"],
                "rewards": ["anubis_blessing", "judgment_cards"],
                "difficulty": 2,
                "atmospheric_effects": ["golden_scales", "spirit_whispers"],
                "boss": "Anubis_Guardian"
            },
            
            # MAIN PROGRESSION PATHS
            "osiris_chamber": {
                "name": "Osiris' Domain",
                "position": (250, 300),
                "size": "massive",
                "chamber_type": "divine_trial",
                "unlocked": False,
                "completed": False,
                "description": "Face the Lord of the Underworld himself",
                "visual_style": "throne_chamber",
                "connections": ["final_judgment"],
                "rewards": ["osiris_power", "legendary_cards"],
                "difficulty": 5,
                "atmospheric_effects": ["divine_light", "resurrection_energy"],
                "boss": "Osiris_Lord_of_Duat"
            },
            
            "ra_trial": {
                "name": "Solar Barque Journey",
                "position": (450, 350),
                "size": "large",
                "chamber_type": "journey",
                "unlocked": False,
                "completed": False,
                "description": "Navigate the treacherous solar boat through the night",
                "visual_style": "solar_boat",
                "connections": ["apophis_encounter", "sky_goddess_temple"],
                "rewards": ["solar_blessing", "navigation_skills"],
                "difficulty": 3,
                "atmospheric_effects": ["flowing_river", "celestial_light"]
            },
            
            "apophis_encounter": {
                "name": "Serpent's Coils",
                "position": (550, 280),
                "size": "large", 
                "chamber_type": "monster_lair",
                "unlocked": False,
                "completed": False,
                "description": "Confront the great serpent of chaos, Apophis",
                "visual_style": "serpent_cavern",
                "connections": ["chaos_realm"],
                "rewards": ["chaos_mastery", "serpent_cards"],
                "difficulty": 4,
                "atmospheric_effects": ["coiling_shadows", "chaos_energy"],
                "boss": "Apophis_Chaos_Serpent"
            },
            
            # SECRET AND OPTIONAL AREAS
            "hidden_library": {
                "name": "Thoth's Hidden Archive",
                "position": (150, 250),
                "size": "medium",
                "chamber_type": "secret",
                "unlocked": False,
                "completed": False,
                "description": "Ancient wisdom hidden from mortal eyes",
                "visual_style": "mystical_library",
                "connections": ["wisdom_trial"],
                "rewards": ["ancient_knowledge", "thoth_spells"],
                "difficulty": 3,
                "atmospheric_effects": ["floating_scrolls", "magical_runes"],
                "requirements": ["solve_riddle", "collect_wisdom_tokens"]
            },
            
            "sky_goddess_temple": {
                "name": "Nut's Starry Embrace",
                "position": (450, 200),
                "size": "large",
                "chamber_type": "divine_blessing",
                "unlocked": False,
                "completed": False,
                "description": "Receive the blessing of the sky goddess",
                "visual_style": "starry_temple",
                "connections": ["celestial_realm"],
                "rewards": ["stellar_power", "night_cards"],
                "difficulty": 3,
                "atmospheric_effects": ["falling_stars", "cosmic_wind"]
            },
            
            # FINAL CHAMBERS
            "final_judgment": {
                "name": "The Final Weighing",
                "position": (350, 150),
                "size": "massive",
                "chamber_type": "final_boss",
                "unlocked": False,
                "completed": False,
                "description": "The ultimate test of your worthiness for eternal life",
                "visual_style": "cosmic_judgment",
                "connections": [],
                "rewards": ["eternal_life", "game_completion"],
                "difficulty": 6,
                "atmospheric_effects": ["cosmic_scales", "divine_judgment"],
                "boss": "Ma_at_Final_Judge"
            }
        }
        
        return chambers
    
    def _initialize_atmospheric_elements(self):
        """Initialize atmospheric visual elements."""
        # Torch flames at key locations
        for chamber_id, chamber in self.chambers.items():
            if chamber["chamber_type"] in ["entrance", "divine_trial", "final_boss"]:
                torch_pos = (chamber["position"][0] - 30, chamber["position"][1] - 40)
                self.torch_flames.append({
                    "position": torch_pos,
                    "intensity": random.uniform(0.8, 1.2),
                    "flicker_time": random.uniform(0, 2 * math.pi)
                })
        
        # Floating spirit orbs
        for _ in range(8):
            self.floating_spirits.append({
                "x": random.randint(50, self.rect.width - 50),
                "y": random.randint(50, self.rect.height - 50),
                "vx": random.uniform(-10, 10),
                "vy": random.uniform(-10, 10),
                "alpha": random.randint(50, 150),
                "size": random.randint(3, 8),
                "glow_time": random.uniform(0, 2 * math.pi)
            })
        
        # Sand streams between connected chambers
        for chamber_id, chamber in self.chambers.items():
            for connection in chamber.get("connections", []):
                if connection in self.chambers:
                    start_pos = chamber["position"]
                    end_pos = self.chambers[connection]["position"]
                    self.sand_streams.append({
                        "start": start_pos,
                        "end": end_pos,
                        "particles": self._create_stream_particles(start_pos, end_pos),
                        "active": chamber["unlocked"]
                    })
    
    def _create_stream_particles(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> List[Dict]:
        """Create particle stream between two positions."""
        particles = []
        distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        num_particles = max(5, int(distance // 20))
        
        for i in range(num_particles):
            t = i / num_particles
            x = start_pos[0] + t * (end_pos[0] - start_pos[0])
            y = start_pos[1] + t * (end_pos[1] - start_pos[1])
            
            particles.append({
                "x": x + random.uniform(-5, 5),
                "y": y + random.uniform(-5, 5),
                "life": random.uniform(1.0, 3.0),
                "max_life": 3.0,
                "size": random.randint(1, 3),
                "speed": random.uniform(0.5, 1.5)
            })
        
        return particles
    
    def update(self, delta_time: float) -> None:
        """Update map animations and effects."""
        super().update(delta_time)
        self.map_time += delta_time
        
        # Update camera smoothing
        self.camera_x += (self.target_camera_x - self.camera_x) * delta_time * 3
        self.camera_y += (self.target_camera_y - self.camera_y) * delta_time * 3
        
        # Update torch flames
        for torch in self.torch_flames:
            torch["flicker_time"] += delta_time * 3
            torch["intensity"] = 0.8 + 0.4 * abs(math.sin(torch["flicker_time"]))
        
        # Update floating spirits
        for spirit in self.floating_spirits:
            spirit["x"] += spirit["vx"] * delta_time
            spirit["y"] += spirit["vy"] * delta_time
            spirit["glow_time"] += delta_time * 2
            
            # Wrap around screen
            if spirit["x"] < 0 or spirit["x"] > self.rect.width:
                spirit["vx"] *= -1
            if spirit["y"] < 0 or spirit["y"] > self.rect.height:
                spirit["vy"] *= -1
            
            spirit["x"] = max(0, min(self.rect.width, spirit["x"]))
            spirit["y"] = max(0, min(self.rect.height, spirit["y"]))
        
        # Update sand streams
        for stream in self.sand_streams:
            if stream["active"]:
                for particle in stream["particles"]:
                    particle["life"] -= delta_time
                    if particle["life"] <= 0:
                        particle["life"] = particle["max_life"]
    
    def render(self, surface: pygame.Surface) -> None:
        """Render enhanced temple map with atmospheric effects."""
        if not self.visible:
            return
        
        # Create map surface for camera effects
        map_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        # Draw background atmosphere
        self._draw_background_atmosphere(map_surface)
        
        # Draw sand streams (connections)
        self._draw_sand_streams(map_surface)
        
        # Draw torch flames
        self._draw_torch_flames(map_surface)
        
        # Draw chamber nodes
        self._draw_chamber_nodes(map_surface)
        
        # Draw floating spirits
        self._draw_floating_spirits(map_surface)
        
        # Draw chamber labels and info
        self._draw_chamber_labels(map_surface)
        
        # Apply camera transform and blit to main surface
        camera_rect = pygame.Rect(-self.camera_x, -self.camera_y, 
                                self.rect.width, self.rect.height)
        surface.blit(map_surface, self.rect.topleft, camera_rect)
        
        # Draw UI overlay (always on top)
        self._draw_ui_overlay(surface)
    
    def _draw_background_atmosphere(self, surface: pygame.Surface):
        """Draw atmospheric background effects."""
        # Mystical fog gradient
        fog_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        for y in range(0, surface.get_height(), 10):
            fog_alpha = int(30 + 20 * abs(math.sin(self.map_time * 0.5 + y * 0.01)))
            fog_color = (*self.hades_theme.get_color('night_blue'), fog_alpha)
            
            fog_rect = pygame.Rect(0, y, surface.get_width(), 10)
            fog_surface.fill(fog_color, fog_rect)
        
        surface.blit(fog_surface, (0, 0))
        
        # Mystical energy lines
        self._draw_energy_lines(surface)
    
    def _draw_energy_lines(self, surface: pygame.Surface):
        """Draw mystical energy lines across the map."""
        energy_color = (*self.hades_theme.get_color('sacred_turquoise'), 80)
        
        # Horizontal energy flows
        for i in range(3):
            y = (i + 1) * surface.get_height() // 4
            wave_offset = math.sin(self.map_time * 2 + i) * 20
            
            points = []
            for x in range(0, surface.get_width(), 20):
                wave_y = y + wave_offset * math.sin(x * 0.02 + self.map_time)
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                pygame.draw.lines(surface, energy_color, False, points, 2)
    
    def _draw_sand_streams(self, surface: pygame.Surface):
        """Draw flowing sand streams between chambers."""
        for stream in self.sand_streams:
            if not stream["active"]:
                continue
            
            # Draw stream path
            stream_color = self.hades_theme.get_color('desert_amber')
            pygame.draw.line(surface, stream_color, stream["start"], stream["end"], 3)
            
            # Draw flowing particles
            for particle in stream["particles"]:
                if particle["life"] > 0:
                    alpha = int(255 * (particle["life"] / particle["max_life"]))
                    particle_color = (*stream_color, alpha)
                    
                    particle_surface = pygame.Surface((particle["size"]*2, particle["size"]*2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, particle_color, 
                                     (particle["size"], particle["size"]), particle["size"])
                    surface.blit(particle_surface, (int(particle["x"]), int(particle["y"])))
    
    def _draw_torch_flames(self, surface: pygame.Surface):
        """Draw animated torch flames."""
        for torch in self.torch_flames:
            pos = torch["position"]
            intensity = torch["intensity"]
            
            # Flame colors
            base_color = self.hades_theme.get_color('desert_amber')
            tip_color = self.hades_theme.get_color('underworld_crimson')
            
            # Flame size based on intensity
            flame_height = int(20 * intensity)
            flame_width = int(8 * intensity)
            
            # Draw flame base (wider, amber)
            base_rect = pygame.Rect(pos[0] - flame_width//2, pos[1] - flame_height//3, 
                                  flame_width, flame_height//2)
            pygame.draw.ellipse(surface, base_color, base_rect)
            
            # Draw flame tip (narrower, red)
            tip_rect = pygame.Rect(pos[0] - flame_width//3, pos[1] - flame_height, 
                                 flame_width//1.5, flame_height//1.5)
            pygame.draw.ellipse(surface, tip_color, tip_rect)
            
            # Add glow effect
            glow_surface = pygame.Surface((flame_width*3, flame_height*2), pygame.SRCALPHA)
            glow_alpha = int(intensity * 100)
            glow_color = (*base_color, glow_alpha)
            pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect())
            surface.blit(glow_surface, (pos[0] - flame_width*1.5, pos[1] - flame_height*1.5))
    
    def _draw_chamber_nodes(self, surface: pygame.Surface):
        """Draw chamber nodes with enhanced visuals."""
        for chamber_id, chamber in self.chambers.items():
            pos = chamber["position"]
            size = self._get_chamber_size(chamber["size"])
            chamber_type = chamber["chamber_type"]
            
            # Base node appearance
            node_color = self._get_chamber_color(chamber_type, chamber["unlocked"], chamber["completed"])
            
            # Draw chamber base with depth
            shadow_offset = 3
            shadow_rect = pygame.Rect(pos[0] - size//2 + shadow_offset, 
                                    pos[1] - size//2 + shadow_offset, size, size)
            pygame.draw.ellipse(surface, self.hades_theme.get_color('shadow_black'), shadow_rect)
            
            # Main chamber circle
            chamber_rect = pygame.Rect(pos[0] - size//2, pos[1] - size//2, size, size)
            pygame.draw.ellipse(surface, node_color, chamber_rect)
            
            # Chamber border
            border_color = self._get_chamber_border_color(chamber_type, chamber["unlocked"])
            pygame.draw.ellipse(surface, border_color, chamber_rect, 4)
            
            # Special effects for different chamber types
            self._draw_chamber_special_effects(surface, chamber, pos, size)
            
            # Selection/hover effects
            if chamber_id == self.selected_chamber:
                self._draw_selection_effect(surface, pos, size)
            elif chamber_id == self.hover_chamber:
                self._draw_hover_effect(surface, pos, size)
    
    def _get_chamber_size(self, size_category: str) -> int:
        """Get chamber visual size based on category."""
        sizes = {
            "small": 30,
            "medium": 40, 
            "large": 50,
            "massive": 70
        }
        return sizes.get(size_category, 40)
    
    def _get_chamber_color(self, chamber_type: str, unlocked: bool, completed: bool) -> Tuple[int, int, int]:
        """Get chamber color based on type and state."""
        if completed:
            return self.hades_theme.get_color('success_green')
        elif not unlocked:
            return self.hades_theme.get_color('disabled_gray')
        
        type_colors = {
            "entrance": self.hades_theme.get_color('desert_amber'),
            "judgment": self.hades_theme.get_color('duat_gold'),
            "divine_trial": self.hades_theme.get_color('royal_purple'),
            "journey": self.hades_theme.get_color('sacred_turquoise'),
            "monster_lair": self.hades_theme.get_color('underworld_crimson'),
            "secret": self.hades_theme.get_color('hieroglyph_green'),
            "divine_blessing": self.hades_theme.get_color('papyrus_cream'),
            "final_boss": self.hades_theme.get_color('hover_gold')
        }
        
        return type_colors.get(chamber_type, self.hades_theme.get_color('pharaoh_bronze'))
    
    def _get_chamber_border_color(self, chamber_type: str, unlocked: bool) -> Tuple[int, int, int]:
        """Get chamber border color."""
        if not unlocked:
            return self.hades_theme.get_color('obsidian_black')
        
        if chamber_type in ["divine_trial", "final_boss"]:
            return self.hades_theme.get_color('hover_gold')
        elif chamber_type == "secret":
            return self.hades_theme.get_color('sacred_turquoise')
        else:
            return self.hades_theme.get_color('pharaoh_bronze')
    
    def _draw_chamber_special_effects(self, surface: pygame.Surface, chamber: Dict, 
                                    pos: Tuple[int, int], size: int):
        """Draw special visual effects for different chamber types."""
        chamber_type = chamber["chamber_type"]
        
        if chamber_type == "divine_trial":
            # Divine light rays
            ray_color = (*self.hades_theme.get_color('hover_gold'), 100)
            for i in range(8):
                angle = i * (2 * math.pi / 8) + self.map_time
                end_x = pos[0] + (size + 20) * math.cos(angle)
                end_y = pos[1] + (size + 20) * math.sin(angle)
                pygame.draw.line(surface, ray_color, pos, (int(end_x), int(end_y)), 2)
        
        elif chamber_type == "monster_lair":
            # Menacing aura
            aura_intensity = 0.5 + 0.5 * abs(math.sin(self.map_time * 3))
            aura_color = (*self.hades_theme.get_color('underworld_crimson'), int(aura_intensity * 150))
            aura_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, aura_color, (size, size), size)
            surface.blit(aura_surface, (pos[0] - size, pos[1] - size))
        
        elif chamber_type == "secret":
            # Mystical runes orbiting
            for i in range(4):
                angle = i * (2 * math.pi / 4) + self.map_time * 2
                rune_x = pos[0] + (size//2 + 15) * math.cos(angle)
                rune_y = pos[1] + (size//2 + 15) * math.sin(angle)
                
                rune_color = (*self.hades_theme.get_color('sacred_turquoise'), 200)
                self.hades_theme._draw_transition_ankh(surface, (int(rune_x), int(rune_y)), 4, rune_color)
    
    def _draw_selection_effect(self, surface: pygame.Surface, pos: Tuple[int, int], size: int):
        """Draw selection effect around chamber."""
        selection_color = self.hades_theme.get_color('hover_gold')
        
        # Pulsing ring
        pulse = 0.8 + 0.2 * abs(math.sin(self.map_time * 4))
        ring_size = int((size + 15) * pulse)
        
        pygame.draw.circle(surface, selection_color, pos, ring_size, 4)
        
        # Corner decorations
        for i in range(4):
            angle = i * (math.pi / 2) + self.map_time
            corner_x = pos[0] + ring_size * math.cos(angle)
            corner_y = pos[1] + ring_size * math.sin(angle)
            
            self.hades_theme._draw_corner_decorations(surface, 
                pygame.Rect(corner_x-5, corner_y-5, 10, 10), selection_color)
    
    def _draw_hover_effect(self, surface: pygame.Surface, pos: Tuple[int, int], size: int):
        """Draw hover effect around chamber."""
        hover_color = (*self.hades_theme.get_color('papyrus_cream'), 150)
        
        # Subtle glow
        glow_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, hover_color, (size, size), size)
        surface.blit(glow_surface, (pos[0] - size, pos[1] - size))
    
    def _draw_floating_spirits(self, surface: pygame.Surface):
        """Draw floating spirit orbs."""
        for spirit in self.floating_spirits:
            # Pulsing glow
            glow_intensity = 0.5 + 0.5 * abs(math.sin(spirit["glow_time"]))
            alpha = int(spirit["alpha"] * glow_intensity)
            
            spirit_color = (*self.hades_theme.get_color('sacred_turquoise'), alpha)
            
            # Draw spirit with trail
            spirit_surface = pygame.Surface((spirit["size"]*4, spirit["size"]*4), pygame.SRCALPHA)
            pygame.draw.circle(spirit_surface, spirit_color, 
                             (spirit["size"]*2, spirit["size"]*2), spirit["size"])
            
            pos = (int(spirit["x"]) - spirit["size"]*2, int(spirit["y"]) - spirit["size"]*2)
            surface.blit(spirit_surface, pos)
    
    def _draw_chamber_labels(self, surface: pygame.Surface):
        """Draw chamber names and information."""
        font = pygame.font.Font(None, 16)
        
        for chamber_id, chamber in self.chambers.items():
            if not chamber["unlocked"] and chamber_id != self.hover_chamber:
                continue
            
            pos = chamber["position"]
            chamber_name = chamber["name"]
            
            # Draw label background
            text_surface = font.render(chamber_name, True, self.hades_theme.get_color('papyrus_cream'))
            label_rect = text_surface.get_rect(center=(pos[0], pos[1] + 40))
            
            # Background panel
            bg_rect = label_rect.inflate(10, 4)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((*self.hades_theme.get_color('obsidian_black'), 180))
            surface.blit(bg_surface, bg_rect)
            
            # Label text
            surface.blit(text_surface, label_rect)
            
            # Show additional info on hover
            if chamber_id == self.hover_chamber:
                self._draw_chamber_tooltip(surface, chamber, pos)
    
    def _draw_chamber_tooltip(self, surface: pygame.Surface, chamber: Dict, pos: Tuple[int, int]):
        """Draw detailed chamber information tooltip."""
        tooltip_font = pygame.font.Font(None, 14)
        
        # Tooltip content
        lines = [
            chamber["description"],
            f"Difficulty: {chamber.get('difficulty', 1)}/6",
            f"Type: {chamber['chamber_type'].replace('_', ' ').title()}"
        ]
        
        if chamber.get("boss"):
            lines.append(f"Boss: {chamber['boss'].replace('_', ' ')}")
        
        # Calculate tooltip size
        line_height = 16
        max_width = max(tooltip_font.size(line)[0] for line in lines)
        tooltip_height = len(lines) * line_height + 10
        
        # Position tooltip
        tooltip_x = pos[0] + 60
        tooltip_y = pos[1] - tooltip_height // 2
        
        # Keep tooltip on screen
        if tooltip_x + max_width + 20 > surface.get_width():
            tooltip_x = pos[0] - max_width - 80
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, max_width + 20, tooltip_height)
        
        # Draw tooltip background
        self.hades_theme.draw_ornate_button(surface, tooltip_rect, "", "normal")
        
        # Draw tooltip text
        for i, line in enumerate(lines):
            text_surface = tooltip_font.render(line, True, self.hades_theme.get_color('papyrus_cream'))
            text_y = tooltip_y + 5 + i * line_height
            surface.blit(text_surface, (tooltip_x + 10, text_y))
    
    def _draw_ui_overlay(self, surface: pygame.Surface):
        """Draw UI overlay elements (minimap, controls, etc.)."""
        # Minimap in corner
        minimap_size = 120
        minimap_rect = pygame.Rect(surface.get_width() - minimap_size - 10, 10, 
                                 minimap_size, minimap_size)
        
        # Minimap background
        minimap_bg = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
        minimap_bg.fill((*self.hades_theme.get_color('obsidian_black'), 150))
        surface.blit(minimap_bg, minimap_rect)
        
        # Minimap chambers (simplified)
        scale_x = minimap_size / self.rect.width
        scale_y = minimap_size / self.rect.height
        
        for chamber in self.chambers.values():
            if chamber["unlocked"]:
                mini_x = minimap_rect.x + int(chamber["position"][0] * scale_x)
                mini_y = minimap_rect.y + int(chamber["position"][1] * scale_y)
                mini_color = self.hades_theme.get_color('duat_gold') if chamber["completed"] else self.hades_theme.get_color('papyrus_cream')
                pygame.draw.circle(surface, mini_color, (mini_x, mini_y), 3)
        
        # Camera viewport indicator
        viewport_x = minimap_rect.x + int(self.camera_x * scale_x)
        viewport_y = minimap_rect.y + int(self.camera_y * scale_y)
        viewport_w = int(self.rect.width * scale_x * self.zoom_level)
        viewport_h = int(self.rect.height * scale_y * self.zoom_level)
        
        viewport_rect = pygame.Rect(viewport_x, viewport_y, viewport_w, viewport_h)
        pygame.draw.rect(surface, self.hades_theme.get_color('sacred_turquoise'), viewport_rect, 2)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle map interaction events."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check chamber clicks
            mouse_pos = pygame.mouse.get_pos()
            # Adjust for camera position
            world_pos = (mouse_pos[0] + self.camera_x, mouse_pos[1] + self.camera_y)
            
            for chamber_id, chamber in self.chambers.items():
                if not chamber["unlocked"]:
                    continue
                
                chamber_pos = chamber["position"]
                size = self._get_chamber_size(chamber["size"])
                
                distance = math.sqrt((world_pos[0] - chamber_pos[0])**2 + 
                                   (world_pos[1] - chamber_pos[1])**2)
                
                if distance <= size // 2:
                    self.selected_chamber = chamber_id
                    self._trigger_event("chamber_selected", {"chamber_id": chamber_id, "chamber": chamber})
                    return True
        
        elif event.type == pygame.MOUSEMOTION:
            # Check chamber hover
            mouse_pos = pygame.mouse.get_pos()
            world_pos = (mouse_pos[0] + self.camera_x, mouse_pos[1] + self.camera_y)
            
            previous_hover = self.hover_chamber
            self.hover_chamber = None
            
            for chamber_id, chamber in self.chambers.items():
                chamber_pos = chamber["position"]
                size = self._get_chamber_size(chamber["size"])
                
                distance = math.sqrt((world_pos[0] - chamber_pos[0])**2 + 
                                   (world_pos[1] - chamber_pos[1])**2)
                
                if distance <= size // 2:
                    self.hover_chamber = chamber_id
                    break
            
            if self.hover_chamber != previous_hover:
                if self.hover_chamber:
                    self._trigger_event("chamber_hover", {"chamber_id": self.hover_chamber})
                else:
                    self._trigger_event("chamber_hover_end", {})
        
        return False