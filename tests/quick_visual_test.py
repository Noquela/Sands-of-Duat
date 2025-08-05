#!/usr/bin/env python3
"""
Quick Visual Test for Sands of Duat
Simulates what user would see in screenshots
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent / "sands_duat"
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all key imports that might be failing"""
    issues = []
    
    try:
        from sands_duat.graphics.background_loader import load_background
        print("+ Background loader import successful")
    except Exception as e:
        issues.append(f"- Background loader failed: {e}")
    
    try:
        from sands_duat.graphics.lighting_system import get_lighting_system
        print("+ Lighting system import successful")
    except Exception as e:
        issues.append(f"- Lighting system failed: {e}")
    
    try:
        from sands_duat.graphics.ai_effects_system import get_ai_effects
        print("+ AI effects system import successful") 
    except Exception as e:
        issues.append(f"- AI effects system failed: {e}")
    
    try:
        from sands_duat.graphics.sprite_animator import create_character_sprite
        print("+ Sprite animator import successful")
    except Exception as e:
        issues.append(f"- Sprite animator failed: {e}")
    
    try:
        from sands_duat.graphics.card_art_loader import load_card_art
        print("+ Card art loader import successful")
    except Exception as e:
        issues.append(f"- Card art loader failed: {e}")
    
    try:
        from sands_duat.ui.particle_system import ParticleSystem
        print("+ Particle system import successful")
    except Exception as e:
        issues.append(f"- Particle system failed: {e}")
    
    return issues

def test_asset_availability():
    """Test if required assets exist"""
    issues = []
    asset_root = Path("game_assets")
    
    # Check backgrounds
    menu_bg = asset_root / "environments" / "menu_background.png"
    combat_bg = asset_root / "environments" / "combat_background.png"
    
    if menu_bg.exists():
        print(f"+ Menu background found: {menu_bg}")
    else:
        issues.append(f"- Menu background missing: {menu_bg}")
    
    if combat_bg.exists():
        print(f"+ Combat background found: {combat_bg}")
    else:
        issues.append(f"- Combat background missing: {combat_bg}")
    
    # Check character sprites
    characters_dir = asset_root / "characters" / "sprites"
    if characters_dir.exists():
        sprites = list(characters_dir.glob("*.png"))
        print(f"+ Found {len(sprites)} character sprites")
        if len(sprites) < 5:
            issues.append(f"- Only {len(sprites)} character sprites found, expected more")
    else:
        issues.append(f"- Character sprites directory missing: {characters_dir}")
    
    # Check card art
    cards_dir = asset_root / "cards"
    if cards_dir.exists():
        cards = list(cards_dir.glob("*.png"))
        print(f"+ Found {len(cards)} card artworks")
        if len(cards) < 10:
            issues.append(f"- Only {len(cards)} card artworks found, expected more")
    else:
        issues.append(f"- Card art directory missing: {cards_dir}")
    
    return issues

def simulate_visual_state():
    """Simulate what each screen would show visually"""
    print("\n=== VISUAL STATE SIMULATION ===")
    
    # Menu Screen
    print("\n1. MAIN MENU SCREEN:")
    print("   Expected to show:")
    print("   - AI-generated desert/temple background")
    print("   - 'SANDS OF DUAT' title with gold glow effect")
    print("   - 'Hour-Glass Initiative' subtitle") 
    print("   - 5 menu buttons: New Game, Continue, Tutorial, Deck Builder, Exit")
    print("   - Animated sand particles falling")
    print("   - Version info in bottom right")
    print("   - Atmospheric lighting effects")
    
    # Combat Screen  
    print("\n2. COMBAT SCREEN:")
    print("   Expected to show:")
    print("   - AI-generated combat background (tomb/desert)")
    print("   - Player character sprite (animated)")
    print("   - Enemy character sprite (animated)")
    print("   - Hour-glass sand gauge (visual sand level)")
    print("   - Hand of 5+ cards with AI-generated artwork")
    print("   - 800+ particle effects for atmosphere")
    print("   - Combat hit effects and healing sparkles")
    print("   - Sand flow effects between hourglass")
    print("   - Health/block displays for both characters")
    print("   - 'SANDS OF DUAT' title at top")
    
    # Deck Builder
    print("\n3. DECK BUILDER SCREEN:")
    print("   Expected to show:")
    print("   - AI-generated background")
    print("   - Upper area: Available cards (collection)")
    print("   - Lower area: Current deck cards")
    print("   - Card previews with AI-generated artwork")
    print("   - Drag-and-drop visual feedback")
    print("   - Double-click to add/remove cards")
    print("   - Deck count and limits displayed")

def check_recent_issues():
    """Check for issues introduced in recent commits"""
    print("\n=== RECENT CHANGES ANALYSIS ===")
    
    # Check particle system issues
    try:
        from sands_duat.ui.particle_system import ParticleSystem, ParticleType
        print("+ New particle system available")
        
        # Test creating particles
        import pygame
        pygame.init()
        test_surface = pygame.Surface((100, 100))
        ps = ParticleSystem(max_particles=100)
        ps.emit_particles(ParticleType.SAND_GRAIN, 50, 50, 10)
        print("+ Particle system can create particles")
        
    except Exception as e:
        print(f"- Particle system has issues: {e}")
    
    # Check if lighting system causes performance issues
    try:
        from sands_duat.graphics.lighting_system import LightingSystem
        print("+ Lighting system available")
    except Exception as e:
        print(f"- Lighting system has issues: {e}")

def identify_potential_problems():
    """Identify specific issues that could cause 'nothing changed, it just got worse'"""
    print("\n=== POTENTIAL PROBLEMS ANALYSIS ===")
    
    problems = []
    
    # Check for import failures that would cause blank screens
    try:
        import pygame
        pygame.init()
        screen = pygame.Surface((1920, 1080))
        
        # Test menu screen creation
        from sands_duat.ui.menu_screen import MenuScreen
        menu = MenuScreen()
        menu.on_enter()
        print("+ Menu screen can be created")
        
    except Exception as e:
        problems.append(f"Menu screen creation fails: {e}")
    
    # Check for asset loading failures
    try:
        from sands_duat.graphics.background_loader import load_background
        bg = load_background('menu', (1920, 1080))
        if bg:
            print("+ Background loading works")
        else:
            problems.append("Background loading returns None")
    except Exception as e:
        problems.append(f"Background loading fails: {e}")
    
    # Check for particle system causing performance issues
    try:
        from sands_duat.ui.particle_system import ParticleSystem
        ps = ParticleSystem(max_particles=800)  # The mentioned 800+ particles
        if ps.max_particles > 500:
            problems.append("Particle system configured for 800+ particles - may cause lag")
        print(f"+ Particle system max particles: {ps.max_particles}")
    except Exception as e:
        problems.append(f"Particle system fails: {e}")
    
    return problems

if __name__ == "__main__":
    print("=== SANDS OF DUAT VISUAL STATE ANALYSIS ===")
    
    import_issues = test_imports()
    asset_issues = test_asset_availability()
    
    print(f"\n=== IMPORT ISSUES ({len(import_issues)}) ===")
    for issue in import_issues:
        print(issue)
    
    print(f"\n=== ASSET ISSUES ({len(asset_issues)}) ===")
    for issue in asset_issues:
        print(issue)
    
    simulate_visual_state()
    check_recent_issues()
    
    problems = identify_potential_problems()
    print(f"\n=== IDENTIFIED PROBLEMS ({len(problems)}) ===")
    for problem in problems:
        print(f"- {problem}")
    
    total_issues = len(import_issues) + len(asset_issues) + len(problems)
    if total_issues > 0:
        print(f"\nWARNING: TOTAL ISSUES FOUND: {total_issues}")
        print("These issues could explain why 'nothing changed, it just got worse'")
    else:
        print("\nSUCCESS: NO CRITICAL ISSUES FOUND - Game should work visually")