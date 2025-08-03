"""
Enhanced Progression UI for Sands of Duat

Comprehensive progression interface with Egyptian theming, statistics dashboard,
achievement tracking, and detailed player progress visualization.
"""

import pygame
import math
from typing import Dict, Any, Optional, List, Callable, Tuple
from datetime import datetime

from .base import UIScreen, UIComponent
from .theme import get_theme
from .animation_system import EasingType
from .menu_screen import MenuButton
from ..core.save_system import SaveSystem, get_save_system
from ..core.achievements import AchievementManager, Achievement, AchievementCategory
from ..core.backup_manager import BackupManager, get_backup_manager


class StatisticCard(UIComponent):
    """Individual statistic display card with Egyptian styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 title: str, value: str, icon: str = "", description: str = ""):
        super().__init__(x, y, width, height)
        self.title = title
        self.value = value
        self.icon = icon
        self.description = description
        
        # Colors
        self.bg_color = (45, 35, 25)  # Dark temple brown
        self.border_color = (139, 117, 93)  # Stone color
        self.gold_color = (255, 215, 0)
        self.text_color = (220, 200, 180)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 24)
        self.value_font = pygame.font.Font(None, 32)
        self.desc_font = pygame.font.Font(None, 18)
        
        # Animation
        self.hover_scale = 1.0
        self.target_scale = 1.0
    
    def update(self, delta_time: float) -> None:
        """Update animations."""
        if abs(self.hover_scale - self.target_scale) > 0.01:
            self.hover_scale += (self.target_scale - self.hover_scale) * delta_time * 10
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the statistic card."""
        if not self.visible:
            return
        
        # Scale for hover effect
        scaled_rect = pygame.Rect(self.rect)
        if self.hover_scale != 1.0:
            scale_diff = (self.hover_scale - 1.0) * 10
            scaled_rect.inflate_ip(scale_diff, scale_diff)
        
        # Background
        pygame.draw.rect(surface, self.bg_color, scaled_rect)
        pygame.draw.rect(surface, self.border_color, scaled_rect, 2)
        
        # Icon (if provided)
        icon_y = scaled_rect.y + 10
        if self.icon:
            icon_surface = self.title_font.render(self.icon, True, self.gold_color)
            icon_rect = icon_surface.get_rect()
            icon_rect.centerx = scaled_rect.centerx
            icon_rect.y = icon_y
            surface.blit(icon_surface, icon_rect)
            icon_y += icon_rect.height + 5
        
        # Title
        title_surface = self.title_font.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect()
        title_rect.centerx = scaled_rect.centerx
        title_rect.y = icon_y
        surface.blit(title_surface, title_rect)
        
        # Value
        value_surface = self.value_font.render(self.value, True, self.gold_color)
        value_rect = value_surface.get_rect()
        value_rect.centerx = scaled_rect.centerx
        value_rect.y = title_rect.bottom + 5
        surface.blit(value_surface, value_rect)
        
        # Description (if provided)
        if self.description:
            desc_surface = self.desc_font.render(self.description, True, self.text_color)
            desc_rect = desc_surface.get_rect()
            desc_rect.centerx = scaled_rect.centerx
            desc_rect.y = value_rect.bottom + 5
            surface.blit(desc_surface, desc_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle hover effects."""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.target_scale = 1.05
            else:
                self.target_scale = 1.0
        
        return False


class AchievementDisplay(UIComponent):
    """Display component for individual achievement."""
    
    def __init__(self, x: int, y: int, width: int, height: int, achievement: Achievement, 
                 is_completed: bool = False, progress_percentage: float = 0.0):
        super().__init__(x, y, width, height)
        self.achievement = achievement
        self.is_completed = is_completed
        self.progress_percentage = progress_percentage
        
        # Colors
        self.bg_color = (60, 50, 40) if is_completed else (40, 30, 20)
        self.border_color = (255, 215, 0) if is_completed else (139, 117, 93)
        self.text_color = (255, 255, 255) if is_completed else (200, 180, 160)
        self.progress_color = (255, 215, 0)
        self.progress_bg_color = (80, 70, 60)
        
        # Fonts
        self.name_font = pygame.font.Font(None, 22)
        self.desc_font = pygame.font.Font(None, 18)
        self.progress_font = pygame.font.Font(None, 16)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the achievement."""
        if not self.visible:
            return
        
        # Background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Achievement icon/symbol
        if self.achievement.hieroglyph_symbol:
            icon_surface = self.name_font.render(self.achievement.hieroglyph_symbol, True, self.border_color)
            icon_rect = icon_surface.get_rect()
            icon_rect.x = self.rect.x + 10
            icon_rect.y = self.rect.y + 10
            surface.blit(icon_surface, icon_rect)
            text_x = icon_rect.right + 10
        else:
            text_x = self.rect.x + 10
        
        # Achievement name
        name_surface = self.name_font.render(self.achievement.name, True, self.text_color)
        name_rect = name_surface.get_rect()
        name_rect.x = text_x
        name_rect.y = self.rect.y + 8
        surface.blit(name_surface, name_rect)
        
        # Achievement description
        desc_surface = self.desc_font.render(self.achievement.description, True, self.text_color)
        desc_rect = desc_surface.get_rect()
        desc_rect.x = text_x
        desc_rect.y = name_rect.bottom + 2
        surface.blit(desc_surface, desc_rect)
        
        # Progress bar (if not completed)
        if not self.is_completed and self.progress_percentage > 0:
            progress_rect = pygame.Rect(text_x, desc_rect.bottom + 5, self.rect.width - text_x - 20, 8)
            pygame.draw.rect(surface, self.progress_bg_color, progress_rect)
            
            progress_width = int(progress_rect.width * (self.progress_percentage / 100))
            if progress_width > 0:
                fill_rect = pygame.Rect(progress_rect.x, progress_rect.y, progress_width, progress_rect.height)
                pygame.draw.rect(surface, self.progress_color, fill_rect)
            
            # Progress text
            progress_text = f"{self.progress_percentage:.1f}%"
            progress_surface = self.progress_font.render(progress_text, True, self.text_color)
            progress_text_rect = progress_surface.get_rect()
            progress_text_rect.x = progress_rect.right + 5
            progress_text_rect.centery = progress_rect.centery
            surface.blit(progress_surface, progress_text_rect)
        
        # Completion indicator
        if self.is_completed:
            checkmark = "✓"
            check_surface = self.name_font.render(checkmark, True, (0, 255, 0))
            check_rect = check_surface.get_rect()
            check_rect.right = self.rect.right - 10
            check_rect.y = self.rect.y + 10
            surface.blit(check_surface, check_rect)


class ProgressionDashboard(UIComponent):
    """Main progression dashboard with multiple panels."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        
        self.save_system = get_save_system()
        self.backup_manager = get_backup_manager()
        
        # Panel dimensions
        self.panel_spacing = 20
        self.stat_card_width = 150
        self.stat_card_height = 100
        
        # Colors
        self.bg_color = (30, 20, 10)
        self.panel_color = (45, 35, 25)
        self.border_color = (139, 117, 93)
        self.gold_color = (255, 215, 0)
        self.text_color = (220, 200, 180)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.section_font = pygame.font.Font(None, 24)
        
        # UI Components
        self.stat_cards: List[StatisticCard] = []
        self.achievement_displays: List[AchievementDisplay] = []
        
        # Scrolling
        self.scroll_y = 0
        self.max_scroll = 0
        
        self._setup_components()
    
    def _setup_components(self) -> None:
        """Setup dashboard components."""
        if not self.save_system.current_save:
            return
        
        save_data = self.save_system.current_save
        profile = save_data.player_profile
        progression = save_data.progression
        collection = save_data.card_collection
        
        # Create statistic cards
        self.stat_cards.clear()
        
        stats = [
            ("Level", str(profile.level), "👑", f"XP: {profile.xp}"),
            ("Win Rate", f"{(profile.total_wins / max(1, profile.total_wins + profile.total_losses)) * 100:.1f}%", "⚔️", f"{profile.total_wins}W/{profile.total_losses}L"),
            ("Win Streak", str(profile.win_streak), "🔥", f"Best: {profile.best_win_streak}"),
            ("Playtime", f"{profile.playtime_hours:.1f}h", "⏰", "Total hours played"),
            ("Chambers", f"{len(progression.chambers_completed)}/7", "🏛️", "Completed chambers"),
            ("Cards", str(len(collection.owned_cards)), "🃏", f"Total: {sum(collection.owned_cards.values())}"),
            ("Achievements", str(len(progression.achievements)), "🏆", "Unlocked"),
            ("Daily Wins", str(progression.daily_wins), "☀️", "Today's victories")
        ]
        
        cards_per_row = 4
        card_x_start = self.rect.x + 20
        card_y_start = self.rect.y + 80
        
        for i, (title, value, icon, desc) in enumerate(stats):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = card_x_start + col * (self.stat_card_width + 15)
            y = card_y_start + row * (self.stat_card_height + 15)
            
            card = StatisticCard(x, y, self.stat_card_width, self.stat_card_height, title, value, icon, desc)
            self.stat_cards.append(card)
        
        # Setup achievement displays
        self._setup_achievement_displays()
    
    def _setup_achievement_displays(self) -> None:
        """Setup achievement display components."""
        # This would need access to the achievement manager
        # For now, create placeholder achievement displays
        
        achievement_y = self.rect.y + 300
        achievement_spacing = 60
        
        # Create sample achievement displays
        sample_achievements = [
            ("Anubis' First Blessing", "Win your first battle", True, 100.0),
            ("Ra's Eternal Flame", "Achieve a 10-win streak", False, 70.0),
            ("Temple Master", "Complete all chambers", False, 42.8),
            ("Card Collector", "Collect 100 unique cards", False, 15.3)
        ]
        
        self.achievement_displays.clear()
        
        for i, (name, desc, completed, progress) in enumerate(sample_achievements):
            y = achievement_y + i * achievement_spacing
            
            # Create a mock achievement object
            class MockAchievement:
                def __init__(self, name, description):
                    self.name = name
                    self.description = description
                    self.hieroglyph_symbol = "⭐"
            
            achievement = MockAchievement(name, desc)
            display = AchievementDisplay(
                self.rect.x + 20, y, self.rect.width - 40, 50,
                achievement, completed, progress
            )
            self.achievement_displays.append(display)
    
    def update(self, delta_time: float) -> None:
        """Update dashboard components."""
        # Update statistic cards
        for card in self.stat_cards:
            card.update(delta_time)
        
        # Update achievement displays
        for display in self.achievement_displays:
            display.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the progression dashboard."""
        if not self.visible:
            return
        
        # Create scrollable surface
        dashboard_surface = pygame.Surface((self.rect.width, self.rect.height + abs(self.scroll_y)))
        dashboard_surface.fill(self.bg_color)
        
        # Dashboard title
        title_text = "Progression Dashboard"
        title_surface = self.title_font.render(title_text, True, self.gold_color)
        title_rect = title_surface.get_rect()
        title_rect.centerx = dashboard_surface.get_width() // 2
        title_rect.y = 20
        dashboard_surface.blit(title_surface, title_rect)
        
        # Statistics section
        stats_title = "Statistics"
        stats_surface = self.section_font.render(stats_title, True, self.text_color)
        stats_rect = stats_surface.get_rect()
        stats_rect.x = 20
        stats_rect.y = 60
        dashboard_surface.blit(stats_surface, stats_rect)
        
        # Render statistic cards
        for card in self.stat_cards:
            card.render(dashboard_surface)
        
        # Achievements section
        achievements_title = "Achievements"
        achievements_surface = self.section_font.render(achievements_title, True, self.text_color)
        achievements_rect = achievements_surface.get_rect()
        achievements_rect.x = 20
        achievements_rect.y = 280
        dashboard_surface.blit(achievements_surface, achievements_rect)
        
        # Render achievement displays
        for display in self.achievement_displays:
            display.render(dashboard_surface)
        
        # Blit to main surface with scrolling
        surface.blit(dashboard_surface, (self.rect.x, self.rect.y + self.scroll_y))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for dashboard."""
        if not self.visible or not self.enabled:
            return False
        
        # Handle scrolling
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_y += event.y * 30
                self.scroll_y = max(-self.max_scroll, min(0, self.scroll_y))
                return True
        
        # Forward events to components
        handled = False
        
        for card in self.stat_cards:
            if card.handle_event(event):
                handled = True
        
        for display in self.achievement_displays:
            if display.handle_event(event):
                handled = True
        
        return handled


class EnhancedProgressionScreen(UIScreen):
    """
    Enhanced progression screen with comprehensive statistics and achievement tracking.
    """
    
    def __init__(self):
        super().__init__("enhanced_progression")
        self.save_system = get_save_system()
        self.backup_manager = get_backup_manager()
        
        # UI Components
        self.dashboard: Optional[ProgressionDashboard] = None
        self.temple_map = None  # Will reuse existing temple map if needed
        
        # View state
        self.current_view = "dashboard"  # dashboard, temple_map, achievements
        
    def on_enter(self) -> None:
        """Initialize enhanced progression screen."""
        self.logger.info("Entering enhanced progression screen")
        self._setup_ui_components()
    
    def on_exit(self) -> None:
        """Clean up enhanced progression screen."""
        self.logger.info("Exiting enhanced progression screen")
        self.clear_components()
    
    def _setup_ui_components(self) -> None:
        """Set up the enhanced progression UI."""
        theme = get_theme()
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
        # Navigation buttons
        button_width = 120
        button_height = 40
        button_y = 20
        
        dashboard_button = MenuButton(
            20, button_y, button_width, button_height,
            "Dashboard",
            lambda: self._switch_view("dashboard")
        )
        self.add_component(dashboard_button)
        
        temple_button = MenuButton(
            150, button_y, button_width, button_height,
            "Temple Map",
            lambda: self._switch_view("temple_map")
        )
        self.add_component(temple_button)
        
        achievements_button = MenuButton(
            280, button_y, button_width, button_height,
            "Achievements",
            lambda: self._switch_view("achievements")
        )
        self.add_component(achievements_button)
        
        # Back button
        back_button = MenuButton(
            screen_width - 140, button_y, button_width, button_height,
            "< Back",
            self._back_to_menu
        )
        self.add_component(back_button)
        
        # Create dashboard
        dashboard_y = 80
        dashboard_height = screen_height - dashboard_y - 20
        
        self.dashboard = ProgressionDashboard(
            0, dashboard_y, screen_width, dashboard_height
        )
        self.add_component(self.dashboard)
        
        # Auto-save status indicator
        self._create_save_status_indicator()
    
    def _create_save_status_indicator(self) -> None:
        """Create save status indicator."""
        # This would show auto-save status, backup information, etc.
        pass
    
    def _switch_view(self, view_name: str) -> None:
        """Switch between different views."""
        self.current_view = view_name
        
        # Hide/show components based on view
        if self.dashboard:
            self.dashboard.visible = (view_name == "dashboard")
        
        self.logger.info(f"Switched to view: {view_name}")
    
    def _back_to_menu(self) -> None:
        """Return to main menu."""
        self.logger.info("Returning to main menu from enhanced progression screen")
        if hasattr(self, 'ui_manager') and self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("menu", "slide_down")
        else:
            self._trigger_event("switch_screen", {"screen": "menu"})
    
    def update(self, delta_time: float) -> None:
        """Update enhanced progression screen."""
        super().update(delta_time)
        
        # Update dashboard if visible
        if self.dashboard and self.dashboard.visible:
            self.dashboard.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render enhanced progression screen."""
        # Egyptian temple background
        surface.fill((30, 20, 10))
        
        # Draw subtle background pattern
        self._draw_background_pattern(surface)
        
        # Render components
        super().render(surface)
    
    def _draw_background_pattern(self, surface: pygame.Surface) -> None:
        """Draw subtle Egyptian-themed background pattern."""
        # Draw subtle hieroglyphic patterns
        pattern_color = (40, 30, 20)
        
        # Simple geometric patterns
        for x in range(0, surface.get_width(), 100):
            for y in range(0, surface.get_height(), 100):
                pygame.draw.circle(surface, pattern_color, (x + 50, y + 50), 2)
                pygame.draw.rect(surface, pattern_color, (x + 45, y + 45, 10, 10), 1)