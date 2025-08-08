#!/usr/bin/env python3
"""
Export complete Egyptian card database to JSON format.
Creates a comprehensive card database file for easy inspection and integration.
"""

import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from sands_of_duat.cards import get_card_database


def export_cards_to_json():
    """Export all Egyptian cards to JSON format."""
    print("Exporting Egyptian card database to JSON...")
    
    db = get_card_database()
    
    # Export to JSON file
    output_path = project_root / "egyptian_cards_database.json"
    
    if db.export_to_json(output_path):
        print(f"Successfully exported cards to: {output_path}")
        
        # Show file size
        file_size = output_path.stat().st_size
        print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        
        # Show summary
        stats = db.get_card_statistics()
        print(f"\nExported {stats['total_cards']} cards:")
        for card_type, count in stats['by_type'].items():
            if count > 0:
                print(f"  - {count} {card_type} cards")
        
        return True
    else:
        print("Failed to export cards to JSON")
        return False


if __name__ == "__main__":
    success = export_cards_to_json()
    sys.exit(0 if success else 1)