"""
Enhanced Combat System Usage Example

Demonstrates how to integrate the enhanced enemy AI, visual effects,
and audio systems with the existing HourGlass Initiative combat system.

This example shows:
1. Setting up enhanced combat with all systems
2. Processing player and enemy actions with full feedback
3. Managing turn transitions and visual effects
4. Coordinating AI decision-making with player analysis
"""

import pygame
import time
import logging
from typing import Dict, Any

# Enhanced combat system imports
from ..core.enhanced_combat_integration import (
    get_combat_coordinator, 
    trigger_card_play, 
    trigger_damage, 
    trigger_healing,
    trigger_turn_change,
    trigger_status_effect
)
from ..core.hourglass import HourGlass
from ..core.combat_enhanced import EnhancedCombatEngine, ActionType
from ..ai.enemy_types import create_enemy_ai
from ..ui.combat_effects import CardType


def setup_enhanced_combat_example():
    """Set up an enhanced combat example with all systems."""
    
    # Initialize pygame for visual/audio systems
    pygame.init()
    pygame.mixer.init()
    
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Enhanced Combat Example - Sands of Duat")
    
    # Get the combat coordinator
    coordinator = get_combat_coordinator()
    
    # Create hourglass systems for player and enemy
    player_hourglass = HourGlass(
        entity_id="player",
        max_sand=5,
        regeneration_rate=1.0
    )
    
    enemy_hourglass = HourGlass(
        entity_id="enemy_mummy",
        max_sand=4,
        regeneration_rate=0.8
    )
    
    # Create enhanced combat engine
    combat_engine = EnhancedCombatEngine()
    combat_engine.register_combatant_hourglass("player", player_hourglass)
    combat_engine.register_combatant_hourglass("enemy_mummy", enemy_hourglass)
    
    # Set up combat participants
    player_data = {
        "id": "player",
        "type": "player",
        "health": 80,
        "max_health": 100,
        "sand": 3,
        "hourglass": player_hourglass
    }
    
    enemy_data = {
        "id": "enemy_mummy",
        "type": "mummy_warrior",  # Will create MummyWarriorAI
        "health": 60,
        "max_health": 60,
        "sand": 2,
        "hourglass": enemy_hourglass,
        "combat_engine": combat_engine
    }
    
    # Start enhanced combat
    coordinator.start_combat(player_data, enemy_data, location_type="tomb")
    
    return coordinator, screen, player_data, enemy_data, combat_engine


def demonstrate_card_play_effects(coordinator, player_data):
    """Demonstrate different card play effects."""
    
    print("\\n=== Demonstrating Card Play Effects ===")
    
    # Different card types for demonstration
    cards_to_play = [
        {
            "name": "Desert Strike",
            "type": "attack",
            "sand_cost": 2,
            "description": "Physical attack with fire damage"
        },
        {
            "name": "Anubis Blessing",
            "type": "skill", 
            "sand_cost": 3,
            "description": "Divine protection skill"
        },
        {
            "name": "Pharaoh's Power",
            "type": "power",
            "sand_cost": 2,
            "description": "Permanent strength enhancement"
        },
        {
            "name": "Curse of the Tomb",
            "type": "status",
            "sand_cost": 1,
            "description": "Apply weakness debuff"
        }
    ]
    
    # Player position for effects
    player_pos = (300, 400)
    
    for i, card in enumerate(cards_to_play):
        print(f"Playing {card['name']} ({card['type']})")
        
        # Trigger card play with full effects
        coordinator.process_card_play(card, player_pos)
        
        # Small delay to see each effect
        time.sleep(1.5)
        
        # Update player sand
        player_data["sand"] = max(0, player_data["sand"] - card["sand_cost"])


def demonstrate_damage_and_healing(coordinator):
    """Demonstrate damage and healing effects."""
    
    print("\\n=== Demonstrating Damage and Healing ===")
    
    enemy_pos = (900, 400)
    player_pos = (300, 400)
    
    # Different damage types
    damage_scenarios = [
        {"damage": 15, "type": "physical", "critical": False},
        {"damage": 12, "type": "fire", "critical": False},
        {"damage": 8, "type": "poison", "critical": False},
        {"damage": 20, "type": "divine", "critical": True},  # Critical hit
    ]
    
    for scenario in damage_scenarios:
        print(f"Dealing {scenario['damage']} {scenario['type']} damage" + 
              (" (CRITICAL)" if scenario['critical'] else ""))
        
        # Enemy attacks player
        coordinator.process_damage(
            attacker_id="enemy_mummy",
            target_id="player", 
            damage=scenario["damage"],
            damage_type=scenario["type"],
            position=player_pos,
            is_critical=scenario["critical"]
        )
        
        time.sleep(2.0)
    
    # Demonstrate healing
    print("Healing player with divine magic")
    coordinator.process_healing(
        healer_id="player",
        target_id="player",
        healing=25,
        healing_type="divine",
        position=player_pos
    )
    
    time.sleep(2.0)


def demonstrate_status_effects(coordinator):
    """Demonstrate status effect feedback."""
    
    print("\\n=== Demonstrating Status Effects ===")
    
    player_pos = (300, 400)
    enemy_pos = (900, 400)
    
    status_effects = [
        {"status": "strength", "applied": True, "target": "player"},
        {"status": "poison", "applied": True, "target": "enemy_mummy"},
        {"status": "defense", "applied": True, "target": "player"},
        {"status": "weak", "applied": True, "target": "enemy_mummy"},
        {"status": "poison", "applied": False, "target": "enemy_mummy"},  # Remove poison
    ]
    
    for effect in status_effects:
        action = "Applied" if effect["applied"] else "Removed"
        print(f"{action} {effect['status']} {'to' if effect['applied'] else 'from'} {effect['target']}")
        
        position = player_pos if effect["target"] == "player" else enemy_pos
        
        coordinator.process_status_effect(
            target_id=effect["target"],
            status_type=effect["status"],
            is_applied=effect["applied"],
            position=position
        )
        
        time.sleep(1.5)


def demonstrate_turn_transitions(coordinator):
    """Demonstrate turn transition effects."""
    
    print("\\n=== Demonstrating Turn Transitions ===")
    
    # Simulate several turn changes
    for turn_num in range(1, 4):
        print(f"Turn {turn_num} - Player Turn")
        coordinator.process_turn_change(is_now_player_turn=True)
        time.sleep(2.0)
        
        print(f"Turn {turn_num} - Enemy Turn")
        coordinator.process_turn_change(is_now_player_turn=False)
        time.sleep(2.0)


def demonstrate_ai_decision_making(coordinator):
    """Demonstrate AI decision making and player analysis."""
    
    print("\\n=== Demonstrating AI Decision Making ===")
    
    # Get the enemy AI
    enemy_ai = coordinator.ai_manager.get_ai("enemy_mummy")
    if not enemy_ai:
        print("No enemy AI found!")
        return
    
    print(f"Enemy AI Personality: {enemy_ai.personality.value}")
    print(f"Enemy AI Difficulty: {enemy_ai.difficulty.value}")
    
    # Simulate player actions for AI to analyze
    simulated_actions = [
        {"card_type": "attack", "sand_cost": 2},
        {"card_type": "attack", "sand_cost": 1}, 
        {"card_type": "skill", "sand_cost": 3},
        {"card_type": "attack", "sand_cost": 2},
    ]
    
    print("\\nSimulating player actions for AI analysis:")
    for action in simulated_actions:
        print(f"  Player plays {action['card_type']} card (cost: {action['sand_cost']})")
        
        # Inform AI about player action
        enemy_ai.observe_player_action(
            ActionType.PLAY_CARD,
            f"Test {action['card_type']} Card",
            action['card_type'],
            action['sand_cost'],
            80  # Player health
        )
    
    # Get AI analysis
    ai_status = enemy_ai.get_ai_status()
    player_analysis = ai_status.get('player_analysis', {})
    
    print("\\nAI Analysis Results:")
    print(f"  Player threat level: {player_analysis.get('threat_level', 'Unknown'):.2f}")
    print(f"  Predicted player moves: {player_analysis.get('predicted_moves', {})}")
    
    behavior = player_analysis.get('behavior_pattern', {})
    print(f"  Player preferred card type: {behavior.get('preferred_card_type', 'Unknown')}")
    print(f"  Player is aggressive: {behavior.get('is_aggressive', False)}")
    print(f"  Player is conservative: {behavior.get('is_conservative', False)}")
    print(f"  Average sand spending: {behavior.get('avg_sand_spending', 0):.1f}")


def run_enhanced_combat_example():
    """Run the complete enhanced combat example."""
    
    print("Starting Enhanced Combat System Example")
    print("=" * 50)
    
    # Setup
    coordinator, screen, player_data, enemy_data, combat_engine = setup_enhanced_combat_example()
    
    # Clock for timing
    clock = pygame.time.Clock()
    
    try:
        # Demonstrate different aspects of the enhanced system
        demonstrate_card_play_effects(coordinator, player_data)
        demonstrate_damage_and_healing(coordinator)
        demonstrate_status_effects(coordinator)
        demonstrate_turn_transitions(coordinator)
        demonstrate_ai_decision_making(coordinator)
        
        print("\\n=== Real-time Combat Simulation ===")
        print("Running real-time combat for 10 seconds...")
        
        # Run real-time simulation for 10 seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Update all systems
            coordinator.update(dt)
            
            # Render effects
            screen.fill((40, 20, 10))  # Dark background
            coordinator.render(screen)
            
            # Display system status
            status = coordinator.get_system_status()
            if status['effects_system']['active_effects'] > 0:
                print(f"Active effects: {status['effects_system']['active_effects']}")
            
            pygame.display.flip()
        
        print("\\nCombat simulation complete!")
        
        # End combat
        coordinator.end_combat(winner="player")
        time.sleep(3)  # Let victory effects play
        
    except Exception as e:
        logging.error(f"Error in combat example: {e}")
        print(f"Error occurred: {e}")
    
    finally:
        # Cleanup
        pygame.quit()
        print("\\nEnhanced Combat Example finished!")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Run the example
    run_enhanced_combat_example()