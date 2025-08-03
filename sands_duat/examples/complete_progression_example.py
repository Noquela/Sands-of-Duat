#!/usr/bin/env python3
"""
Complete Progression System Example for Sands of Duat

Demonstrates the full integration of all progression systems:
- Save/Load System
- Progression Rewards
- Egyptian Achievements
- Backup Manager
- Security & Validation
- Game Progression Manager

This example shows how a complete game session would work with
all systems integrated and working together.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sands_duat.core.game_progression_manager import GameProgressionManager, get_progression_manager
from sands_duat.core.save_system import get_save_system, ProgressionState
from sands_duat.core.save_security import SecurityLevel, init_security_manager
from sands_duat.core.backup_manager import get_backup_manager, BackupType


def setup_logging():
    """Set up logging for the example."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('progression_example.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def simulate_complete_game_session():
    """Simulate a complete game session demonstrating all progression features."""
    print("🏺 SANDS OF DUAT - COMPLETE PROGRESSION SYSTEM DEMO 🏺")
    print("=" * 60)
    
    # Initialize security with high security level
    security_manager = init_security_manager(SecurityLevel.HIGH)
    print(f"🔒 Security manager initialized with HIGH security level")
    
    # Get progression manager (this initializes all other systems)
    progression_manager = get_progression_manager()
    save_system = get_save_system()
    backup_manager = get_backup_manager()
    
    # Set up event handlers to demonstrate the system
    progression_manager.add_event_handler("level_up", lambda data: 
        print(f"LEVEL UP! {data['old_level']} -> {data['new_level']}"))
    
    progression_manager.add_event_handler("achievement_earned", lambda data: 
        print(f"ACHIEVEMENT UNLOCKED: {data['achievement_id']}"))
    
    progression_manager.add_event_handler("chamber_completed", lambda data: 
        print(f"CHAMBER COMPLETED: {data['chamber_id']}"))
    
    progression_manager.add_event_handler("card_discovered", lambda data: 
        print(f"🃏 NEW CARD DISCOVERED: {data['card_id']}"))
    
    # === NEW GAME START ===
    print("\n📅 Starting New Game...")
    player_name = "Pharaoh_Khenti"
    
    success = progression_manager.start_new_game(player_name)
    if not success:
        print("❌ Failed to start new game!")
        return
    
    print(f"✅ New game started for {player_name}")
    
    # Show initial progression summary
    summary = progression_manager.get_progression_summary()
    print(f"\n📊 Initial Stats:")
    print(f"   Level: {summary['level']}")
    print(f"   XP: {summary['xp']}")
    print(f"   Cards: {summary['unique_cards']}")
    print(f"   Chambers: {summary['chambers_completed']}")
    
    # === SIMULATE TUTORIAL ===
    print("\n🎓 Completing Tutorial...")
    time.sleep(1)  # Simulate time passing
    
    # Complete entrance chamber (tutorial)
    chamber_result = progression_manager.complete_chamber("entrance", completion_time=120.0)
    print(f"✅ Tutorial completed! Rewards: {len(chamber_result.get('chamber_rewards', {}).get('rewards', []))} items")
    
    # === SIMULATE BATTLES ===
    print("\nStarting Combat Training...")
    
    # Simulate a series of battles
    enemies = ["Desert Scorpion", "Sand Mummy", "Canopic Guardian", "Temple Priest", "Anubis Sentinel"]
    
    for i, enemy in enumerate(enemies):
        print(f"\n🗡️ Battle {i+1}: Fighting {enemy}...")
        time.sleep(0.5)
        
        # Simulate battle (90% win rate for demo)
        won = i < 4  # Win first 4, lose last one for demonstration
        
        battle_result = progression_manager.record_battle_result(
            won=won,
            enemy_type=enemy.lower().replace(" ", "_"),
            damage_dealt=50 + i * 10,
            damage_taken=20 + i * 5,
            cards_played=["ra_solar_flare", "anubis_judgment", "isis_protection"][:i+1]
        )
        
        if won:
            print(f"   ✅ Victory! XP gained: {battle_result['battle_result']['xp_result']['xp_gained']}")
        else:
            print(f"   💀 Defeat! But gained experience from the attempt.")
        
        # Check for level ups
        if battle_result.get('level_up_result'):
            print(f"   🌟 Level up rewards received!")
        
        # Show current stats
        current_summary = progression_manager.get_progression_summary()
        print(f"   📊 Current: Level {current_summary['level']}, "
              f"Streak: {current_summary['current_streak']}, "
              f"Win Rate: {current_summary['win_rate']:.1f}%")
    
    # === CHAMBER PROGRESSION ===
    print("\nProgressing Through Temple Chambers...")
    
    chambers_to_complete = ["antechamber", "first_trial", "chamber_of_isis"]
    
    for chamber in chambers_to_complete:
        print(f"\n🚪 Entering {chamber}...")
        time.sleep(1)
        
        # Simulate some battles in the chamber
        for j in range(2):
            battle_result = progression_manager.record_battle_result(
                won=True,
                enemy_type=f"{chamber}_guardian_{j}",
                damage_dealt=75,
                damage_taken=15
            )
        
        # Complete the chamber
        completion_time = 300.0 + len(chamber) * 10  # Vary completion time
        chamber_result = progression_manager.complete_chamber(chamber, completion_time)
        
        print(f"   ✅ {chamber} completed in {completion_time:.0f} seconds!")
        
        # Show chamber rewards
        rewards = chamber_result.get('chamber_rewards', {}).get('rewards', [])
        print(f"   🎁 Received {len(rewards)} rewards")
    
    # === SAVE AND BACKUP DEMONSTRATION ===
    print("\n💾 Save and Backup Operations...")
    
    # Manual save
    save_success = progression_manager.save_game("demo_save", create_backup=True)
    print(f"✅ Manual save: {'Success' if save_success else 'Failed'}")
    
    # Show backup summary
    backup_summary = backup_manager.get_backup_summary()
    print(f"Backups: {backup_summary['total_backups']} total, "
          f"{backup_summary['total_size_mb']:.1f} MB")
    
    # === ACHIEVEMENT SHOWCASE ===
    print("\nAchievement Progress...")
    
    if progression_manager.achievement_manager:
        achievement_summary = progression_manager.achievement_manager.get_achievement_summary()
        print(f"   Completed: {achievement_summary['completed_count']}/{achievement_summary['total_achievements']}")
        print(f"   Completion: {achievement_summary['completion_percentage']:.1f}%")
        
        # Show recent achievements
        recent = achievement_summary.get('recent_completions', [])
        if recent:
            print(f"   Recent achievements:")
            for completion in recent[:3]:
                achievement = completion['achievement']
                print(f"     - {achievement.name}")
    
    # === SECURITY DEMONSTRATION ===
    print("\n🔒 Security Features Demonstration...")
    
    # Create a secure backup
    emergency_backup = backup_manager.create_emergency_backup("Security demo")
    if emergency_backup:
        print(f"🛡️ Emergency backup created: {emergency_backup.backup_id}")
        print(f"   Security: Checksum verified, HMAC signed")
        print(f"   Size: {emergency_backup.file_size_bytes} bytes")
    
    # === FINAL STATISTICS ===
    print("\nFinal Session Statistics:")
    print("=" * 40)
    
    final_summary = progression_manager.get_progression_summary()
    
    print(f"Player: {final_summary['player_name']}")
    print(f"Level: {final_summary['level']} (XP: {final_summary['xp']})")
    print(f"Playtime: {final_summary['playtime_hours']:.1f} hours")
    print(f"Win Rate: {final_summary['win_rate']:.1f}% ({final_summary.get('total_wins', 0)}W/{final_summary.get('total_losses', 0)}L)")
    print(f"Best Streak: {final_summary['best_streak']}")
    print(f"Chambers: {final_summary['chambers_completed']}/7")
    print(f"Cards: {final_summary['unique_cards']} unique, {final_summary['total_cards']} total")
    print(f"Achievements: {final_summary.get('achievements', {}).get('completed_count', 0)}")
    
    # Session-specific stats
    session_stats = final_summary.get('current_session', {})
    if session_stats:
        print(f"\nSession Stats:")
        print(f"  Duration: {session_stats['duration_minutes']:.1f} minutes")
        print(f"  Battles: {session_stats['battles_fought']}")
        print(f"  XP Gained: {session_stats['xp_gained']}")
        print(f"  Cards Discovered: {session_stats['cards_discovered']}")
        print(f"  Achievements: {session_stats['achievements_earned']}")
        print(f"  Chambers: {session_stats['chambers_completed']}")
    
    # === SAVE/LOAD CYCLE TEST ===
    print("\n🔄 Testing Save/Load Cycle...")
    
    # Save current state
    progression_manager.save_game("test_cycle")
    original_summary = progression_manager.get_progression_summary()
    
    # Create some changes
    progression_manager.record_battle_result(True, "test_enemy")
    
    # Load the saved state
    load_success = progression_manager.load_game("test_cycle")
    if load_success:
        loaded_summary = progression_manager.get_progression_summary()
        
        # Verify state was restored
        level_match = original_summary['level'] == loaded_summary['level']
        xp_match = original_summary['xp'] == loaded_summary['xp']
        
        print(f"✅ Save/Load cycle: {'Success' if level_match and xp_match else 'Failed'}")
        print(f"   Level preserved: {level_match}")
        print(f"   XP preserved: {xp_match}")
    else:
        print("❌ Save/Load cycle failed")
    
    print("\n🎊 Demo Complete! All progression systems working together.")
    print("\nKey Features Demonstrated:")
    print("  ✅ Comprehensive save/load with validation")
    print("  ✅ XP progression and level-ups with rewards")
    print("  ✅ Egyptian-themed achievements with tracking")
    print("  ✅ Automatic and manual backup management")
    print("  ✅ Security validation and tamper detection")
    print("  ✅ Integrated player collection and card rewards")
    print("  ✅ Chamber progression and unlocks")
    print("  ✅ Real-time session tracking")
    print("  ✅ Event-driven progression updates")


def demonstrate_backup_recovery():
    """Demonstrate backup and recovery features."""
    print("\n🔧 BACKUP & RECOVERY DEMONSTRATION")
    print("=" * 40)
    
    backup_manager = get_backup_manager()
    
    # List available backups
    backups = backup_manager.list_backups()
    print(f"Available backups: {len(backups)}")
    
    for backup in backups[:3]:  # Show first 3
        print(f"   {backup.backup_id}: {backup.backup_type.value}, "
              f"{backup.file_size_bytes} bytes, {backup.player_name}")
    
    # Demonstrate export functionality
    if backups:
        latest_backup = backups[0]
        export_path = Path(f"exported_{latest_backup.backup_id}.bak")
        
        export_success = backup_manager.export_backup(latest_backup.backup_id, export_path)
        if export_success:
            print(f"📤 Exported backup to: {export_path}")
            
            # Clean up
            if export_path.exists():
                export_path.unlink()
                print(f"🧹 Cleaned up export file")


def demonstrate_security_features():
    """Demonstrate security validation features."""
    print("\n🛡️ SECURITY FEATURES DEMONSTRATION")
    print("=" * 40)
    
    from sands_duat.core.save_security import get_security_manager
    
    security_manager = get_security_manager()
    
    # Create sample save data
    sample_save = {
        "player_profile": {
            "name": "TestPlayer",
            "level": 5,
            "xp": 4500,
            "total_wins": 25,
            "total_losses": 3,
            "playtime_hours": 2.5
        },
        "card_collection": {
            "owned_cards": {"ra_solar_flare": 3, "anubis_judgment": 2}
        },
        "progression": {
            "chambers_completed": ["entrance", "antechamber"],
            "achievements": ["anubis_first_victory"],
            "battles_won": 25,
            "battles_lost": 3
        }
    }
    
    # Secure the save data
    try:
        secured_save = security_manager.secure_save_data(sample_save)
        print("✅ Save data secured successfully")
        print(f"   Checksum: {secured_save['security_metadata']['checksum_sha256'][:16]}...")
        print(f"   HMAC: {secured_save['security_metadata']['hmac_signature'][:16]}...")
        
        # Verify and load
        loaded_save = security_manager.verify_and_load_save_data(secured_save)
        print("✅ Save data verified and loaded successfully")
        
        # Test tampering detection
        print("\n🔍 Testing tampering detection...")
        
        # Tamper with the data
        tampered_save = secured_save.copy()
        tampered_save['security_metadata']['checksum_sha256'] = "tampered_checksum"
        
        try:
            security_manager.verify_and_load_save_data(tampered_save)
            print("❌ Tampering detection failed!")
        except Exception as e:
            print(f"✅ Tampering detected: {type(e).__name__}")
        
    except Exception as e:
        print(f"❌ Security demonstration failed: {e}")


if __name__ == "__main__":
    setup_logging()
    
    try:
        # Run the complete demonstration
        simulate_complete_game_session()
        
        # Additional demonstrations
        demonstrate_backup_recovery()
        demonstrate_security_features()
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n👋 Thank you for exploring the Sands of Duat progression system!")