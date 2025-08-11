"""
Egyptian Lore & Narrative System
Professional storytelling system featuring authentic Egyptian mythology.
"""

import random
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from dataclasses import dataclass

class NarrativeType(Enum):
    """Types of narrative content."""
    INTRO = auto()          # Game introduction
    VICTORY = auto()        # After winning combat
    DEFEAT = auto()         # After losing combat
    GOD_ENCOUNTER = auto()  # Meeting a god
    LOCATION_ENTER = auto() # Entering new location
    CARD_LORE = auto()      # Individual card backstory
    EPILOGUE = auto()       # Game endings

class EgyptianGod(Enum):
    """Egyptian deities in the game."""
    RA = auto()
    ANUBIS = auto()
    ISIS = auto()
    OSIRIS = auto()
    SET = auto()
    THOTH = auto()
    HORUS = auto()
    BASTET = auto()
    PTAH = auto()
    SOBEK = auto()

@dataclass
class NarrativeEvent:
    """A single narrative event with Egyptian theming."""
    title: str
    text: str
    speaker: str
    god_associated: Optional[EgyptianGod] = None
    choices: Optional[List[str]] = None
    outcomes: Optional[List[str]] = None

class EgyptianLoreSystem:
    """
    Professional Egyptian mythology and narrative system.
    Provides authentic lore, character backgrounds, and immersive storytelling.
    """
    
    def __init__(self):
        """Initialize the lore system."""
        self.current_story_progress = 0
        self.encountered_gods = set()
        self.unlocked_lore = set()
        self.player_choices = []
        
        # Initialize all lore content
        self._initialize_god_lore()
        self._initialize_location_lore()
        self._initialize_card_lore()
        self._initialize_narrative_events()
        
        print("Egyptian Lore System initialized - The gods await your journey")
    
    def _initialize_god_lore(self):
        """Initialize detailed lore for each Egyptian god."""
        self.god_lore = {
            EgyptianGod.RA: {
                'name': 'Ra - The Sun God',
                'domain': 'Sun, Light, Creation',
                'description': 'The king of the gods, Ra travels across the sky in his solar barque, bringing light to the world. His greatest enemy is Apep, the serpent of chaos who threatens to devour the sun each night.',
                'backstory': 'Born from the primordial waters of Nun, Ra created himself and then brought forth all other gods. His tears became the first humans, and his word became divine law.',
                'powers': ['Solar Energy', 'Divine Authority', 'Creation', 'Rebirth'],
                'sacred_animals': ['Falcon', 'Scarab Beetle'],
                'symbols': ['Solar Disk', 'Uraeus Serpent', 'Ankh']
            },
            EgyptianGod.ANUBIS: {
                'name': 'Anubis - Judge of the Dead',
                'domain': 'Death, Mummification, Afterlife',
                'description': 'The jackal-headed god who guides souls through the underworld. He weighs hearts against the feather of Ma\'at to determine the fate of the deceased.',
                'backstory': 'Born of Osiris and Nephthys, Anubis was the first to mummify a body - that of his father Osiris. He became the guardian of the dead and master of the embalming arts.',
                'powers': ['Soul Judgment', 'Mummification', 'Underworld Navigation', 'Protection of Tombs'],
                'sacred_animals': ['Jackal', 'Black Dog'],
                'symbols': ['Scales of Justice', 'Canopic Jars', 'Flail']
            },
            EgyptianGod.ISIS: {
                'name': 'Isis - The Divine Mother',
                'domain': 'Magic, Healing, Motherhood',
                'description': 'The most powerful sorceress among the gods, Isis is the protector of the innocent and the mother of all pharaohs. Her love resurrected Osiris from death.',
                'backstory': 'Sister and wife to Osiris, Isis searched the world to gather his scattered remains after Set murdered him. Through her magic, she brought him back to life long enough to conceive Horus.',
                'powers': ['Healing Magic', 'Protection Spells', 'Resurrection', 'Divine Motherhood'],
                'sacred_animals': ['Kite Bird', 'Cow', 'Scorpion'],
                'symbols': ['Throne', 'Ankh', 'Tyet Knot']
            },
            EgyptianGod.SET: {
                'name': 'Set - God of Chaos',
                'domain': 'Storms, Desert, Chaos',
                'description': 'The red-eyed god of disorder and violence. Set murdered his brother Osiris out of jealousy and wages eternal war against order and harmony.',
                'backstory': 'Born from the sky goddess Nut, Set was always jealous of his brother Osiris. His murder of Osiris began the eternal struggle between order and chaos that defines existence.',
                'powers': ['Storm Control', 'Desert Mastery', 'Chaos Magic', 'Superhuman Strength'],
                'sacred_animals': ['Set Animal (Mythical)', 'Hippo', 'Crocodile'],
                'symbols': ['Was Scepter', 'Red Crown', 'Djed Pillar']
            },
            EgyptianGod.THOTH: {
                'name': 'Thoth - God of Wisdom',
                'domain': 'Wisdom, Writing, Moon',
                'description': 'The ibis-headed god of knowledge who invented writing and maintains the universe\'s equilibrium. He records the deeds of mortals and gods alike.',
                'backstory': 'Self-created through speech, Thoth spoke the world into existence alongside Ra. He serves as the scribe of the gods and mediator in their disputes.',
                'powers': ['Divine Knowledge', 'Magic Words', 'Time Control', 'Sacred Mathematics'],
                'sacred_animals': ['Ibis', 'Baboon'],
                'symbols': ['Papyrus Scroll', 'Reed Pen', 'Scales']
            },
            EgyptianGod.HORUS: {
                'name': 'Horus - The Sky God',
                'domain': 'Sky, Kingship, Protection',
                'description': 'The falcon-headed god whose eyes are the sun and moon. Son of Osiris and Isis, he avenged his father by defeating Set and became the prototype of all pharaohs.',
                'backstory': 'Hidden by his mother Isis after Osiris\'s murder, Horus grew up in secret until he was strong enough to challenge Set for the throne of Egypt.',
                'powers': ['Sky Mastery', 'Divine Sight', 'Royal Authority', 'Solar Power'],
                'sacred_animals': ['Falcon', 'Hawk'],
                'symbols': ['Eye of Horus', 'Double Crown', 'Winged Disk']
            }
        }
    
    def _initialize_location_lore(self):
        """Initialize lore for various Egyptian locations."""
        self.location_lore = {
            'Great Pyramid': {
                'description': 'The eternal resting place of the pharaohs, where mortal kings become gods and join Ra in his celestial journey.',
                'lore': 'Built as a stairway to heaven, each stone was blessed by the priests of Ra. The pyramid focuses divine energy, allowing the pharaoh\'s ka to ascend to the afterlife.',
                'dangers': 'Cursed guardians protect the sacred chambers from tomb robbers and the unworthy.'
            },
            'Temple of Karnak': {
                'description': 'The largest religious complex ever built, dedicated to the Theban Triad of Amun, Mut, and Khonsu.',
                'lore': 'For over 2000 years, pharaohs added to this temple, each trying to prove their devotion to the gods. The sacred lake within purifies all who enter.',
                'dangers': 'The temple\'s own divine energy can overwhelm those who lack proper spiritual preparation.'
            },
            'Valley of the Kings': {
                'description': 'The royal cemetery where pharaohs of the New Kingdom were laid to rest in elaborate tombs.',
                'lore': 'Hidden in the western desert, this valley was chosen because its peak resembles a pyramid. The setting sun here opens the gate to the Duat.',
                'dangers': 'Ancient curses and protective spirits guard against those who would disturb the eternal sleep of kings.'
            },
            'Duat - The Underworld': {
                'description': 'The realm of the dead, a complex landscape of caverns, lakes of fire, and celestial rivers.',
                'lore': 'Every night, Ra\'s solar barque travels through the Duat, battling Apep and bringing hope to the souls of the dead. The righteous join his crew, the wicked are devoured.',
                'dangers': 'Demons, serpents, and lakes of fire test every soul. Only those pure of heart can navigate its twelve regions.'
            }
        }
    
    def _initialize_card_lore(self):
        """Initialize lore for individual cards."""
        self.card_lore = {
            'EGYPTIAN WARRIOR': {
                'backstory': 'Elite soldiers trained in the temples of Montu, god of war. They serve both pharaoh and gods, sworn to protect Egypt from chaos.',
                'significance': 'These warriors believe that dying in battle guarantees a place in Ra\'s solar barque, fighting alongside the gods forever.',
                'historical_context': 'Based on the Medjai, Nubian warriors who served as the elite police and military force of ancient Egypt.'
            },
            'MUMMY GUARDIAN': {
                'backstory': 'Priests who volunteered to undergo the sacred mummification while still alive, becoming eternal guardians of holy places.',
                'significance': 'Their sacrifice grants them power over death itself, allowing them to rise again when their sacred duties call.',
                'historical_context': 'Inspired by the actual practice of voluntary mummification among certain high priests.'
            },
            'SPHINX GUARDIAN': {
                'backstory': 'Ancient beings created by the gods to test the wisdom and courage of mortals. They pose riddles that reflect cosmic truths.',
                'significance': 'To answer a sphinx\'s riddle correctly is to demonstrate divine wisdom; to fail means spiritual destruction.',
                'historical_context': 'The Great Sphinx of Giza was believed to be a guardian of sacred knowledge and the gateway to the afterlife.'
            },
            'PYRAMID POWER': {
                'backstory': 'The pyramid shape channels cosmic energy, connecting earth to heaven and focusing the power of the gods.',
                'significance': 'Each pyramid is a machine for transformation, turning mortal pharaohs into divine beings through sacred geometry.',
                'historical_context': 'Ancient Egyptians believed pyramids were resurrection machines that enabled the pharaoh\'s divine transformation.'
            }
        }
    
    def _initialize_narrative_events(self):
        """Initialize major narrative events and encounters."""
        self.narrative_events = {
            NarrativeType.INTRO: [
                NarrativeEvent(
                    title="The Weighing of Hearts",
                    speaker="Anubis",
                    text="Mortal soul, you stand at the threshold of eternity. In life, your deeds have been recorded by Thoth. Now, your heart shall be weighed against the feather of Ma'at. Are you prepared for judgment?",
                    god_associated=EgyptianGod.ANUBIS,
                    choices=["I am ready for judgment", "I seek to prove my worth through battle", "Grant me more time to prepare"],
                    outcomes=["The scales await your soul...", "Then face the trials of the gods in combat!", "Time moves differently in the realm of the dead..."]
                ),
                NarrativeEvent(
                    title="Ra's Dawn",
                    speaker="Ra",
                    text="Each dawn I emerge victorious from the underworld, having battled the serpent Apep through the night. You too must prove your strength against the forces of chaos. Will you join my eternal struggle?",
                    god_associated=EgyptianGod.RA,
                    choices=["I pledge myself to order and light", "I must first understand the nature of chaos", "What reward awaits those who serve?"],
                    outcomes=["Then take up arms in the name of justice!", "Wisdom seeks understanding before action...", "Eternal glory in the celestial realm..."]
                )
            ],
            NarrativeType.VICTORY: [
                NarrativeEvent(
                    title="Divine Favor",
                    speaker="Thoth",
                    text="Your victory has been recorded in the halls of eternity. The gods smile upon those who uphold Ma'at against the forces of isfet. What wisdom have you gained from this trial?",
                    god_associated=EgyptianGod.THOTH
                ),
                NarrativeEvent(
                    title="Isis's Blessing",
                    speaker="Isis",
                    text="Well fought, brave soul. As I once healed Horus's wounds in battle with Set, so do I bless you now. Your compassion in victory shows the divine nature within you.",
                    god_associated=EgyptianGod.ISIS
                )
            ],
            NarrativeType.DEFEAT: [
                NarrativeEvent(
                    title="Anubis's Counsel",
                    speaker="Anubis",
                    text="Death is but a doorway, not an ending. Even Ra must die each night to be reborn at dawn. Learn from this defeat - what weakness allowed chaos to triumph over order?",
                    god_associated=EgyptianGod.ANUBIS
                ),
                NarrativeEvent(
                    title="Osiris's Wisdom",
                    speaker="Osiris",
                    text="I too knew defeat at the hands of Set, yet through that death came greater understanding. Your failure today plants the seeds of tomorrow's victory.",
                    god_associated=EgyptianGod.OSIRIS
                )
            ]
        }
    
    def get_intro_narrative(self) -> NarrativeEvent:
        """Get an introduction narrative event."""
        return random.choice(self.narrative_events[NarrativeType.INTRO])
    
    def get_victory_narrative(self, defeated_enemy: str = None) -> NarrativeEvent:
        """Get a victory narrative event."""
        return random.choice(self.narrative_events[NarrativeType.VICTORY])
    
    def get_defeat_narrative(self) -> NarrativeEvent:
        """Get a defeat narrative event."""
        return random.choice(self.narrative_events[NarrativeType.DEFEAT])
    
    def get_god_lore(self, god: EgyptianGod) -> Dict:
        """Get detailed lore for a specific god."""
        return self.god_lore.get(god, {})
    
    def get_card_lore(self, card_name: str) -> Dict:
        """Get lore for a specific card."""
        return self.card_lore.get(card_name, {})
    
    def get_location_lore(self, location: str) -> Dict:
        """Get lore for a specific location."""
        return self.location_lore.get(location, {})
    
    def unlock_god_lore(self, god: EgyptianGod):
        """Unlock lore for a specific god after encounter."""
        self.encountered_gods.add(god)
        self.unlocked_lore.add(f"god_{god.name.lower()}")
        print(f"Unlocked lore: {self.god_lore[god]['name']}")
    
    def get_random_mythological_fact(self) -> str:
        """Get a random Egyptian mythology fact for loading screens, etc."""
        facts = [
            "The ancient Egyptians believed the heart, not the brain, was the center of intelligence and emotion.",
            "Ra's barque had to pass through twelve gates in the underworld, each guarded by a different demon.",
            "The djed pillar represents stability and was often placed in tombs to ensure the deceased's resurrection.",
            "Cats were sacred to Bastet and killing one, even accidentally, was punishable by death.",
            "The ankh symbolizes life, and gods were often depicted holding them to the noses of pharaohs to grant eternal life.",
            "Thoth was said to have created writing by watching cranes fly, their formations inspiring hieroglyphic shapes.",
            "The scarab beetle rolling its dung ball inspired the Egyptian vision of the sun god pushing the sun across the sky.",
            "Ancient Egyptians believed the soul had multiple parts: ka (life force), ba (personality), and akh (transfigured spirit).",
            "The weighing of the heart ceremony determined if one's sins outweighed their good deeds - literally.",
            "Set was not always evil; early Egyptians saw him as necessary balance to order, representing the harsh but vital desert."
        ]
        return random.choice(facts)
    
    def get_immersive_combat_intro(self, enemy_type: str = None) -> str:
        """Get an immersive combat introduction based on enemy type."""
        intros = {
            'desert_creature': [
                "The sands shift beneath your feet as ancient eyes watch from the dunes...",
                "Set's children emerge from the scorching wastes, bearing the fury of the storm god...",
                "The desert speaks in whispers of wind and the rattle of bone..."
            ],
            'undead': [
                "From the eternal silence of the tomb, the dead rise to test your worth...",
                "Anubis's servants emerge from the realm of shadows, their judgment absolute...",
                "The scent of natron and myrrh fills the air as bandaged forms approach..."
            ],
            'divine': [
                "The very air crackles with divine power as immortal beings manifest...",
                "You stand in the presence of those who walked with Ra before time began...",
                "The gods have descended to test whether you are worthy of their attention..."
            ],
            'default': [
                "The eternal struggle between order and chaos begins anew...",
                "In this sacred combat, your heart will reveal its true nature...",
                "The gods watch as mortals dance the ancient dance of battle..."
            ]
        }
        
        category = enemy_type if enemy_type in intros else 'default'
        return random.choice(intros[category])
    
    def create_dynamic_narrative(self, context: Dict) -> NarrativeEvent:
        """Create dynamic narrative based on game context."""
        # This would create narrative based on player actions, cards used, etc.
        # For now, return a generic event
        return NarrativeEvent(
            title="The Journey Continues",
            speaker="Narrator",
            text="Your path through the afterlife grows ever stranger, filled with wonders and terrors beyond mortal comprehension...",
            god_associated=None
        )

# Global lore system instance
egyptian_lore = EgyptianLoreSystem()