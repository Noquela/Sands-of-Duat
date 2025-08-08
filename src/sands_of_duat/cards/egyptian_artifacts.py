"""
Egyptian Artifact Cards - Sacred objects, weapons, and tools of power.
Artifacts provide permanent effects and synergize with gods and mortals.
"""

from pathlib import Path
from .card import (
    Card, CardType, CardRarity, CardElement, CardKeyword, 
    CardStats, CardEffect
)

# Asset base path
ASSETS_PATH = Path("assets/images/lora_training/final_dataset")


def create_ankh_of_life() -> Card:
    """Ankh of Life - Symbol of eternal life and divine protection."""
    return Card(
        card_id="artifact_ankh_01",
        name="Ankh of Eternal Life",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.RARE,
        element=CardElement.PROTECTION,
        stats=CardStats(
            attack=0,
            defense=0,
            health=5,
            mana_cost=3,
            sand_cost=1,
            ba_power=3,
            ka_power=5
        ),
        keywords={
            CardKeyword.ANKH_LIFE,
            CardKeyword.DIVINE_PROTECTION
        },
        effects=[
            CardEffect(
                name="Eternal Life Force",
                description="At the start of each turn, heal all your creatures for 1.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Divine Intervention",
                description="Once per turn, when a creature would be destroyed, you may prevent it.",
                effect_type="trigger",
                target="choice",
                conditions=["on_would_die"],
                cost={}
            )
        ],
        description="The sacred ankh, symbol of life itself, grants protection from death and channels the life force of the gods.",
        flavor_text="'Life eternal flows through this sacred symbol, connecting mortal flesh to divine essence.'",
        mythology_source="Egyptian Hieroglyphic texts",
        image_path=ASSETS_PATH / "egyptian_artifact_02_q77.png",
        image_quality=77
    )


def create_was_scepter() -> Card:
    """Was Scepter - Rod of divine authority and power."""
    return Card(
        card_id="artifact_was_01",
        name="Was Scepter of Command",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.EPIC,
        element=CardElement.ORDER,
        stats=CardStats(
            attack=3,
            defense=0,
            health=4,
            mana_cost=4,
            sand_cost=2,
            ba_power=2,
            ka_power=6
        ),
        keywords={
            CardKeyword.PHARAOH_BOND,
            CardKeyword.DIVINE_PROTECTION
        },
        effects=[
            CardEffect(
                name="Divine Authority",
                description="Your deity cards gain +2/+1 and their abilities cost 1 less.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Command the Faithful",
                description="Pay 2 mana: Give target creature Charge and +1/+1 until end of turn.",
                effect_type="activated",
                target="choice",
                cost={"mana": 2}
            )
        ],
        description="The was scepter represents divine power and dominion, carried by gods and pharaohs as a symbol of their authority.",
        flavor_text="'This rod carries the weight of divine command. Before it, even the mightiest bow.'",
        mythology_source="Egyptian royal iconography",
        image_path=ASSETS_PATH / "egyptian_artifact_04_q75.png",
        image_quality=75
    )


def create_djed_pillar() -> Card:
    """Djed Pillar - Symbol of stability and endurance."""
    return Card(
        card_id="artifact_djed_01",
        name="Djed Pillar of Stability",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.UNCOMMON,
        element=CardElement.EARTH,
        stats=CardStats(
            attack=0,
            defense=6,
            health=8,
            mana_cost=3,
            sand_cost=1,
            ba_power=1,
            ka_power=7
        ),
        keywords={
            CardKeyword.KA_BINDING,
            CardKeyword.GUARD
        },
        effects=[
            CardEffect(
                name="Pillar of Endurance",
                description="All your creatures gain +0/+2 and cannot have their stats reduced below 1.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Stability Aura",
                description="Creatures you control cannot be forced to move or change position.",
                effect_type="passive",
                target="all"
            )
        ],
        description="The djed pillar represents the backbone of Osiris and the stability of the eternal order.",
        flavor_text="'As the pillar supports the sky, so does stability support the realm of the living.'",
        mythology_source="Osiris mythology, Festival of Djed",
        image_path=ASSETS_PATH / "egyptian_artifact_07_q84.png",
        image_quality=84
    )


def create_eye_of_horus() -> Card:
    """Eye of Horus - Symbol of protection and royal power."""
    return Card(
        card_id="artifact_eye_horus_01",
        name="Eye of Horus Amulet",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.RARE,
        element=CardElement.AIR,
        stats=CardStats(
            attack=2,
            defense=2,
            health=3,
            mana_cost=2,
            sand_cost=1,
            ba_power=4,
            ka_power=3
        ),
        keywords={
            CardKeyword.PHARAOH_BOND,
            CardKeyword.PIERCE
        },
        effects=[
            CardEffect(
                name="All-Seeing Eye",
                description="You can see your opponent's hand. Your spells cannot be countered.",
                effect_type="passive",
                target="self"
            ),
            CardEffect(
                name="Falcon's Strike",
                description="Pay 1 mana: Deal 2 damage to any target. If you control Horus, deal 4 instead.",
                effect_type="activated",
                target="choice",
                cost={"mana": 1},
                conditions=["horus_bonus"]
            )
        ],
        description="The wadjet eye of Horus provides protection and insight, representing royal power and divine watchfulness.",
        flavor_text="'The eye that sees all, protects all. No enemy can hide from its piercing gaze.'",
        mythology_source="Horus mythology, protective amulets",
        image_path=ASSETS_PATH / "egyptian_artifact_09_q80.png",
        image_quality=80
    )


def create_scarab_amulet() -> Card:
    """Scarab Amulet - Symbol of rebirth and transformation."""
    return Card(
        card_id="artifact_scarab_01",
        name="Sacred Scarab of Rebirth",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.UNCOMMON,
        element=CardElement.SUN,
        stats=CardStats(
            attack=1,
            defense=1,
            health=2,
            mana_cost=2,
            sand_cost=0,
            ba_power=3,
            ka_power=2
        ),
        keywords={
            CardKeyword.AFTERLIFE,
            CardKeyword.REGENERATE
        },
        effects=[
            CardEffect(
                name="Cycle of Rebirth",
                description="When a creature dies, you may pay 1 sand to return it to your hand with -1/-1 counters removed.",
                effect_type="trigger",
                target="choice",
                conditions=["on_creature_death"],
                cost={"sand": 1}
            ),
            CardEffect(
                name="Solar Blessing",
                description="At dawn (start of turn), gain 1 mana and heal 1 damage.",
                effect_type="passive",
                target="self"
            )
        ],
        description="The scarab beetle pushes the sun across the sky and represents the cycle of death and rebirth.",
        flavor_text="'As the scarab rolls the sun to dawn, so does life emerge from death's shadow.'",
        mythology_source="Solar mythology, Khepri cult",
        image_path=ASSETS_PATH / "egyptian_artifact_10_q75.png",
        image_quality=75
    )


def create_book_of_the_dead() -> Card:
    """Book of the Dead - Ancient wisdom and spells."""
    return Card(
        card_id="artifact_book_dead_01",
        name="Book of Coming Forth by Day",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.MAGIC,
        stats=CardStats(
            attack=0,
            defense=0,
            health=6,
            mana_cost=5,
            sand_cost=2,
            ba_power=8,
            ka_power=4
        ),
        keywords={
            CardKeyword.HIEROGLYPH,
            CardKeyword.AFTERLIFE,
            CardKeyword.SOUL_LINK
        },
        effects=[
            CardEffect(
                name="Ancient Wisdom",
                description="Draw 2 cards at the start of each turn. You have no maximum hand size.",
                effect_type="passive",
                target="self"
            ),
            CardEffect(
                name="Spell of Coming Forth",
                description="Pay 3 mana: Return target creature from any discard pile to the battlefield under your control.",
                effect_type="activated",
                target="choice",
                cost={"mana": 3},
                ba_ka_interaction="afterlife"
            ),
            CardEffect(
                name="Sacred Formulae",
                description="All your spells gain 'Draw a card' and Hieroglyph keyword.",
                effect_type="passive",
                target="all"
            )
        ],
        description="The most sacred of texts, containing spells and knowledge needed to navigate the afterlife successfully.",
        flavor_text="'Within these hieroglyphs lies the wisdom of eternity, the words that guide souls to immortality.'",
        mythology_source="Book of the Dead papyri",
        image_path=ASSETS_PATH / "egyptian_object_01_q64.png",
        image_quality=64
    )


def create_canopic_jars() -> Card:
    """Canopic Jars - Vessels for preserved organs."""
    return Card(
        card_id="artifact_canopic_01",
        name="Four Sons Canopic Jars",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.RARE,
        element=CardElement.DEATH,
        stats=CardStats(
            attack=0,
            defense=4,
            health=6,
            mana_cost=4,
            sand_cost=1,
            ba_power=6,
            ka_power=6
        ),
        keywords={
            CardKeyword.AFTERLIFE,
            CardKeyword.SOUL_LINK,
            CardKeyword.BA_SEPARATION
        },
        effects=[
            CardEffect(
                name="Preserve the Essence",
                description="When a creature dies, store its Ba and Ka separately. You may redistribute them to other creatures.",
                effect_type="trigger",
                target="choice",
                conditions=["on_creature_death"],
                ba_ka_interaction="essence_storage"
            ),
            CardEffect(
                name="Four Sacred Guardians",
                description="Create four 1/1 Guardian tokens with different elements (one each of Human, Baboon, Jackal, Falcon).",
                effect_type="activated",
                target="self",
                cost={"mana": 3, "sand": 1}
            )
        ],
        description="Sacred jars guarded by the four sons of Horus, used to preserve the organs needed for resurrection.",
        flavor_text="'The body may perish, but the essence endures within these sacred vessels.'",
        mythology_source="Mummification rituals, Four Sons of Horus",
        image_path=ASSETS_PATH / "egyptian_object_02_q70.png",
        image_quality=70
    )


def create_sistrum() -> Card:
    """Sistrum - Musical instrument of Bastet and Hathor."""
    return Card(
        card_id="artifact_sistrum_01",
        name="Sacred Sistrum of Bastet",
        card_type=CardType.ARTIFACT,
        rarity=CardRarity.UNCOMMON,
        element=CardElement.PROTECTION,
        stats=CardStats(
            attack=0,
            defense=2,
            health=3,
            mana_cost=2,
            sand_cost=0,
            ba_power=4,
            ka_power=2
        ),
        keywords={
            CardKeyword.DIVINE_PROTECTION,
            CardKeyword.REGENERATE
        },
        effects=[
            CardEffect(
                name="Joyful Music",
                description="All your creatures gain +1/+0 and cannot be targeted by enemy abilities during your turn.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Ward Off Evil",
                description="Pay 1 mana: Prevent the next spell or ability that would target one of your creatures.",
                effect_type="activated",
                target="choice",
                cost={"mana": 1}
            )
        ],
        description="The sacred rattle of Bastet, its music drives away evil spirits and brings joy to the righteous.",
        flavor_text="'Its gentle melody carries the goddess's blessing, protecting all who hear its sacred song.'",
        mythology_source="Bastet cult, temple rituals",
        image_path=ASSETS_PATH / "egyptian_object_04_q74.png",
        image_quality=74
    )


# Collection of all artifact cards
EGYPTIAN_ARTIFACT_CARDS = {
    "artifact_ankh_01": create_ankh_of_life,
    "artifact_was_01": create_was_scepter,
    "artifact_djed_01": create_djed_pillar,
    "artifact_eye_horus_01": create_eye_of_horus,
    "artifact_scarab_01": create_scarab_amulet,
    "artifact_book_dead_01": create_book_of_the_dead,
    "artifact_canopic_01": create_canopic_jars,
    "artifact_sistrum_01": create_sistrum
}


def get_all_artifact_cards() -> list[Card]:
    """Get all Egyptian artifact cards."""
    return [card_func() for card_func in EGYPTIAN_ARTIFACT_CARDS.values()]


def get_artifact_by_id(card_id: str) -> Card | None:
    """Get a specific artifact card by ID."""
    card_func = EGYPTIAN_ARTIFACT_CARDS.get(card_id)
    return card_func() if card_func else None