"""
Egyptian God Cards - Authentic mythology-based implementations.
Each god card is balanced according to their mythological significance and powers.
"""

from pathlib import Path
from .card import (
    Card, CardType, CardRarity, CardElement, CardKeyword, 
    CardStats, CardEffect, BaKaSystem
)

# Asset base path
ASSETS_PATH = Path("assets/images/lora_training/final_dataset")


def create_ra_card() -> Card:
    """
    Ra - Supreme Sun God, King of the Gods
    The most powerful deity card, representing the sun's life-giving and destructive power.
    """
    return Card(
        card_id="god_ra_01",
        name="Ra, King of Gods",
        card_type=CardType.DEITY,
        rarity=CardRarity.DIVINE,
        element=CardElement.SUN,
        stats=CardStats(
            attack=12,
            defense=10,
            health=15,
            mana_cost=8,
            sand_cost=3,
            ba_power=10,
            ka_power=8
        ),
        keywords={
            CardKeyword.DIVINE_PROTECTION,
            CardKeyword.PHARAOH_BOND,
            CardKeyword.BA_SEPARATION,
            CardKeyword.CHARGE
        },
        effects=[
            CardEffect(
                name="Solar Barque Journey",
                description="At dawn, deal 3 damage to all enemies. At dusk, heal all allies for 2.",
                effect_type="passive",
                target="all",
                ba_ka_interaction="require_ba"
            ),
            CardEffect(
                name="Divine Judgment",
                description="Destroy target card with health 5 or less. If Ba is separated, affects any health.",
                effect_type="activated",
                target="choice",
                cost={"mana": 4, "sand": 1},
                ba_ka_interaction="enhance_if_ba_separated"
            ),
            CardEffect(
                name="Sun Disk Ascension",
                description="When summoned, gain +2/+2 for each other deity you control.",
                effect_type="trigger",
                target="self",
                conditions=["on_summon"]
            )
        ],
        description="The supreme sun god who travels across the sky in his solar barque, bringing life and light to Egypt while judging the dead in the underworld.",
        flavor_text="'I am Ra, the sun god, the king of gods. My light banishes darkness, my fire purifies souls.'",
        mythology_source="Pyramid Texts, Book of the Dead",
        image_path=ASSETS_PATH / "egyptian_god_ra_01_q81.png",
        image_quality=81
    )


def create_anubis_card() -> Card:
    """
    Anubis - God of Death, Mummification, and the Afterlife
    Specializes in Ba-Ka manipulation and judgment effects.
    """
    return Card(
        card_id="god_anubis_02",
        name="Anubis, Guardian of the Dead",
        card_type=CardType.DEITY,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.DEATH,
        stats=CardStats(
            attack=8,
            defense=12,
            health=12,
            mana_cost=6,
            sand_cost=2,
            ba_power=12,
            ka_power=6
        ),
        keywords={
            CardKeyword.AFTERLIFE,
            CardKeyword.JUDGMENT,
            CardKeyword.BA_SEPARATION,
            CardKeyword.SOUL_LINK,
            CardKeyword.GUARD
        },
        effects=[
            CardEffect(
                name="Weighing of the Heart",
                description="Judge target creature. If its Ba power < its Ka power, destroy it. Otherwise, heal it to full.",
                effect_type="activated",
                target="choice",
                cost={"mana": 3},
                ba_ka_interaction="judgment"
            ),
            CardEffect(
                name="Mummification Process",
                description="When a creature dies, you may pay 2 sand to return it as a mummy with +0/+2 and Afterlife keyword.",
                effect_type="trigger",
                target="choice",
                conditions=["on_creature_death"],
                cost={"sand": 2}
            ),
            CardEffect(
                name="Guide to the Underworld",
                description="All your creatures with Afterlife gain +2 Ba power and can attack from the underworld.",
                effect_type="passive",
                target="all",
                ba_ka_interaction="afterlife_enhancement"
            )
        ],
        description="The jackal-headed god who guides souls through death and judges their worthiness for the afterlife.",
        flavor_text="'Death is not the end, but a transformation. I shall guide you safely to your eternal rest.'",
        mythology_source="Book of the Dead, Pyramid Texts",
        image_path=ASSETS_PATH / "egyptian_god_anubis_02_q75.png",
        image_quality=75
    )


def create_isis_card() -> Card:
    """
    Isis - Goddess of Magic, Motherhood, and Healing
    Master of magical effects and protective abilities.
    """
    return Card(
        card_id="god_isis_04",
        name="Isis, Lady of Magic",
        card_type=CardType.DEITY,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.MAGIC,
        stats=CardStats(
            attack=6,
            defense=8,
            health=10,
            mana_cost=5,
            sand_cost=2,
            ba_power=9,
            ka_power=9
        ),
        keywords={
            CardKeyword.HIEROGLYPH,
            CardKeyword.ANKH_LIFE,
            CardKeyword.SOUL_LINK,
            CardKeyword.REGENERATE,
            CardKeyword.DIVINE_PROTECTION
        },
        effects=[
            CardEffect(
                name="Words of Power",
                description="Draw a card. If it's a spell, reduce its cost by 2 and give it Hieroglyph.",
                effect_type="activated",
                target="self",
                cost={"mana": 2},
                ba_ka_interaction="enhance_if_high_ba"
            ),
            CardEffect(
                name="Resurrection of Osiris",
                description="Return target creature from your discard pile to the battlefield with full health.",
                effect_type="activated",
                target="choice",
                cost={"mana": 4, "sand": 2},
                ba_ka_interaction="require_both"
            ),
            CardEffect(
                name="Protective Ward",
                description="At the start of each turn, choose an ally to gain Divine Protection until your next turn.",
                effect_type="passive",
                target="choice"
            )
        ],
        description="The most powerful goddess of magic, wife of Osiris, and devoted mother who used her magic to heal and protect.",
        flavor_text="'My magic flows through the very hieroglyphs. I am the protector of the innocent and healer of the wounded.'",
        mythology_source="Osiris Myth, Metternich Stela",
        image_path=ASSETS_PATH / "egyptian_god_isis_04_q76.png",
        image_quality=76
    )


def create_osiris_card() -> Card:
    """
    Osiris - God of the Dead, Underworld, and Resurrection
    Powerful afterlife effects and resurrection abilities.
    """
    return Card(
        card_id="god_osiris_05",
        name="Osiris, Lord of the Underworld",
        card_type=CardType.DEITY,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.DEATH,
        stats=CardStats(
            attack=10,
            defense=6,
            health=14,
            mana_cost=7,
            sand_cost=2,
            ba_power=8,
            ka_power=10
        ),
        keywords={
            CardKeyword.AFTERLIFE,
            CardKeyword.JUDGMENT,
            CardKeyword.KA_BINDING,
            CardKeyword.REGENERATE
        },
        effects=[
            CardEffect(
                name="Ruler of the Dead",
                description="All creatures in the underworld gain +2/+2 and can attack any target.",
                effect_type="passive",
                target="all",
                ba_ka_interaction="afterlife_enhancement"
            ),
            CardEffect(
                name="Green Flesh Revival",
                description="When Osiris dies, create a 4/4 Mummy token for each creature that died this game.",
                effect_type="trigger",
                target="self",
                conditions=["on_death"]
            ),
            CardEffect(
                name="Scales of Justice",
                description="Judge all creatures. Those with more Ba than Ka are blessed (+1/+1), others are cursed (-1/-1).",
                effect_type="activated",
                target="all",
                cost={"mana": 5},
                ba_ka_interaction="mass_judgment"
            )
        ],
        description="The green-skinned lord of the underworld, judge of the dead, and symbol of resurrection and eternal life.",
        flavor_text="'Death came to me through treachery, yet I rose to rule the realm beyond. All souls pass through my domain.'",
        mythology_source="Osiris Myth, Coffin Texts",
        image_path=ASSETS_PATH / "egyptian_god_osiris_05_q76.png",
        image_quality=76
    )


def create_horus_card() -> Card:
    """
    Horus - God of the Sky, War, and Protection
    Aggressive deity with pharaoh synergies and aerial combat.
    """
    return Card(
        card_id="god_horus_06",
        name="Horus, Sky God of Vengeance",
        card_type=CardType.DEITY,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.AIR,
        stats=CardStats(
            attack=11,
            defense=7,
            health=11,
            mana_cost=6,
            sand_cost=2,
            ba_power=7,
            ka_power=8
        ),
        keywords={
            CardKeyword.CHARGE,
            CardKeyword.PHARAOH_BOND,
            CardKeyword.PIERCE,
            CardKeyword.DIVINE_PROTECTION
        },
        effects=[
            CardEffect(
                name="Eye of Horus",
                description="Deal damage equal to Horus's attack to target creature or player. If a pharaoh is present, deal double damage.",
                effect_type="activated",
                target="choice",
                cost={"mana": 3},
                conditions=["pharaoh_bonus"]
            ),
            CardEffect(
                name="Falcon's Swoop",
                description="When Horus attacks, he can target any enemy regardless of guards or stealth.",
                effect_type="passive",
                target="self"
            ),
            CardEffect(
                name="Rightful Heir",
                description="If you control a pharaoh, Horus gains +3/+3 and all your creatures gain Charge.",
                effect_type="passive",
                target="all",
                conditions=["pharaoh_present"]
            )
        ],
        description="The falcon-headed god of the sky and divine kingship, avenger of his father Osiris and rightful ruler of Egypt.",
        flavor_text="'I am the living pharaoh, the sky itself! My talons strike with the fury of justice!'",
        mythology_source="Horus and Set Myth, Edfu Temple Texts",
        image_path=ASSETS_PATH / "egyptian_god_horus_06_q77.png",
        image_quality=77
    )


def create_set_card() -> Card:
    """
    Set - God of Chaos, Storms, and the Desert
    Powerful but unpredictable effects that embody chaos.
    """
    return Card(
        card_id="god_set_06",
        name="Set, Lord of Chaos",
        card_type=CardType.DEITY,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.CHAOS,
        stats=CardStats(
            attack=13,
            defense=5,
            health=10,
            mana_cost=6,
            sand_cost=3,
            ba_power=6,
            ka_power=11
        ),
        keywords={
            CardKeyword.CHARGE,
            CardKeyword.PIERCE,
            CardKeyword.BA_SEPARATION
        },
        effects=[
            CardEffect(
                name="Storm of Chaos",
                description="Deal 2 damage to all creatures. Then, randomly distribute 6 more damage among all creatures.",
                effect_type="activated",
                target="all",
                cost={"mana": 4, "sand": 1}
            ),
            CardEffect(
                name="Desert Winds",
                description="At the end of each turn, randomly move one creature to a different position on the battlefield.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Fraternal Rivalry",
                description="Set deals double damage to creatures with Order or Death elements and takes double damage from them.",
                effect_type="passive",
                target="self",
                ba_ka_interaction="elemental_chaos"
            )
        ],
        description="The red-haired god of chaos and storms, brother and enemy of Osiris, representing the necessary but destructive forces of nature.",
        flavor_text="'Order is stagnation! I bring the storm that clears the old to make way for the new!'",
        mythology_source="Set and Osiris Myth, Papyrus Chester Beatty",
        image_path=ASSETS_PATH / "egyptian_god_set_06_q73.png",
        image_quality=73
    )


def create_thoth_card() -> Card:
    """
    Thoth - God of Wisdom, Writing, and Magic
    Card draw, knowledge effects, and hieroglyph synergies.
    """
    return Card(
        card_id="god_thoth_03",
        name="Thoth, Scribe of the Gods",
        card_type=CardType.DEITY,
        rarity=CardRarity.LEGENDARY,
        element=CardElement.MAGIC,
        stats=CardStats(
            attack=5,
            defense=10,
            health=12,
            mana_cost=5,
            sand_cost=1,
            ba_power=11,
            ka_power=7
        ),
        keywords={
            CardKeyword.HIEROGLYPH,
            CardKeyword.JUDGMENT,
            CardKeyword.SOUL_LINK
        },
        effects=[
            CardEffect(
                name="Sacred Scrolls",
                description="Draw 2 cards. If you have 7+ cards in hand, draw 1 more and gain 2 mana.",
                effect_type="activated",
                target="self",
                cost={"mana": 3}
            ),
            CardEffect(
                name="Hieroglyphic Wisdom",
                description="All your spells with Hieroglyph cost 1 less and draw a card when played.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Record of Deeds",
                description="When any creature dies, you may pay 1 sand to look at the top 3 cards of your deck and put one in your hand.",
                effect_type="trigger",
                target="self",
                conditions=["on_any_death"],
                cost={"sand": 1}
            )
        ],
        description="The ibis-headed god of wisdom and writing, keeper of divine records and judge of the dead alongside Anubis.",
        flavor_text="'Knowledge is the greatest power. I record all deeds, both noble and corrupt, in the eternal scrolls.'",
        mythology_source="Book of the Dead, Pyramid Texts",
        image_path=ASSETS_PATH / "egyptian_god_thoth_03_q74.png",
        image_quality=74
    )


def create_bastet_card() -> Card:
    """
    Bastet - Goddess of Protection, Cats, and Joy
    Protective abilities and synergy with creature protection.
    """
    return Card(
        card_id="god_bastet_08",
        name="Bastet, Protector Goddess",
        card_type=CardType.DEITY,
        rarity=CardRarity.EPIC,
        element=CardElement.PROTECTION,
        stats=CardStats(
            attack=7,
            defense=9,
            health=11,
            mana_cost=4,
            sand_cost=1,
            ba_power=8,
            ka_power=8
        ),
        keywords={
            CardKeyword.DIVINE_PROTECTION,
            CardKeyword.GUARD,
            CardKeyword.ANKH_LIFE,
            CardKeyword.REGENERATE
        },
        effects=[
            CardEffect(
                name="Feline Grace",
                description="All your creatures gain +0/+2 and cannot be targeted by enemy spells.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Sacred Cat Blessing",
                description="When a creature you control would be destroyed, you may pay 2 mana to prevent it and heal it for 3.",
                effect_type="trigger",
                target="choice",
                conditions=["on_ally_would_die"],
                cost={"mana": 2}
            ),
            CardEffect(
                name="Joyful Dance",
                description="Heal all creatures for 2. Creatures healed to full health gain +1/+1 until end of turn.",
                effect_type="activated",
                target="all",
                cost={"mana": 3}
            )
        ],
        description="The cat goddess who protects the home, brings joy, and guards against evil spirits and disease.",
        flavor_text="'I am the gentle protector, the dancing flame that warms the hearth and guards the innocent.'",
        mythology_source="Temple of Bubastis texts",
        image_path=ASSETS_PATH / "egyptian_god_bastet_08_q73.png",
        image_quality=73
    )


def create_sobek_card() -> Card:
    """
    Sobek - Crocodile God of the Nile, Strength, and Fertility
    Water-based effects with powerful physical presence.
    """
    return Card(
        card_id="god_sobek_10",
        name="Sobek, Lord of the Nile",
        card_type=CardType.DEITY,
        rarity=CardRarity.EPIC,
        element=CardElement.WATER,
        stats=CardStats(
            attack=10,
            defense=8,
            health=13,
            mana_cost=5,
            sand_cost=2,
            ba_power=6,
            ka_power=9
        ),
        keywords={
            CardKeyword.CHARGE,
            CardKeyword.REGENERATE,
            CardKeyword.PIERCE
        },
        effects=[
            CardEffect(
                name="Nile's Fury",
                description="Deal 4 damage to target creature. If it dies, heal Sobek for 4 and draw a card.",
                effect_type="activated",
                target="choice",
                cost={"mana": 3}
            ),
            CardEffect(
                name="Crocodile Ambush",
                description="When a creature enters the battlefield, Sobek may immediately attack it.",
                effect_type="trigger",
                target="choice",
                conditions=["on_creature_summon"]
            ),
            CardEffect(
                name="River's Blessing",
                description="At the start of each turn, all creatures gain +1/+1 if you control more water-element cards than any opponent.",
                effect_type="passive",
                target="all",
                conditions=["water_dominance"]
            )
        ],
        description="The fierce crocodile god of the life-giving Nile, representing both the river's fertility and its dangerous power.",
        flavor_text="'The Nile flows through my veins. I am both the life-giver and the lurking death beneath the waters.'",
        mythology_source="Fayyum Crocodile Cult texts",
        image_path=ASSETS_PATH / "egyptian_god_sobek_10_q74.png",
        image_quality=74
    )


def create_ptah_card() -> Card:
    """
    Ptah - Creator God, Craftsman, and Builder
    Creates artifacts and enhances other cards.
    """
    return Card(
        card_id="god_ptah_12",
        name="Ptah, Divine Craftsman",
        card_type=CardType.DEITY,
        rarity=CardRarity.EPIC,
        element=CardElement.EARTH,
        stats=CardStats(
            attack=6,
            defense=11,
            health=12,
            mana_cost=5,
            sand_cost=1,
            ba_power=7,
            ka_power=10
        ),
        keywords={
            CardKeyword.KA_BINDING,
            CardKeyword.RITUAL,
            CardKeyword.TEMPLE_POWER
        },
        effects=[
            CardEffect(
                name="Divine Forge",
                description="Create a random artifact card and add it to your hand. It costs 2 less mana.",
                effect_type="activated",
                target="self",
                cost={"mana": 4, "sand": 1}
            ),
            CardEffect(
                name="Master Craftsman",
                description="All artifacts you control gain +2/+2 and their effects trigger twice.",
                effect_type="passive",
                target="all"
            ),
            CardEffect(
                name="Word of Creation",
                description="When Ptah is summoned, you may pay 3 mana to summon a random creature with cost 4 or less.",
                effect_type="trigger",
                target="self",
                conditions=["on_summon"],
                cost={"mana": 3}
            )
        ],
        description="The creator god who spoke the world into existence and patron of craftsmen, builders, and architects.",
        flavor_text="'Through word and will, through craft and creation, I shape the very foundations of existence.'",
        mythology_source="Memphite Theology, Shabaka Stone",
        image_path=ASSETS_PATH / "egyptian_god_ptah_12_q74.png",
        image_quality=74
    )


# Collection of all Egyptian god cards
EGYPTIAN_GOD_CARDS = {
    "god_ra_01": create_ra_card,
    "god_anubis_02": create_anubis_card,
    "god_isis_04": create_isis_card,
    "god_osiris_05": create_osiris_card,
    "god_horus_06": create_horus_card,
    "god_set_06": create_set_card,
    "god_thoth_03": create_thoth_card,
    "god_bastet_08": create_bastet_card,
    "god_sobek_10": create_sobek_card,
    "god_ptah_12": create_ptah_card
}


def get_all_god_cards() -> list[Card]:
    """Get all Egyptian god cards."""
    return [card_func() for card_func in EGYPTIAN_GOD_CARDS.values()]


def get_god_card_by_id(card_id: str) -> Card | None:
    """Get a specific god card by ID."""
    card_func = EGYPTIAN_GOD_CARDS.get(card_id)
    return card_func() if card_func else None


def get_gods_by_element(element: CardElement) -> list[Card]:
    """Get all god cards of a specific element."""
    return [card for card in get_all_god_cards() if card.element == element]


def get_gods_by_rarity(rarity: CardRarity) -> list[Card]:
    """Get all god cards of a specific rarity."""
    return [card for card in get_all_god_cards() if card.rarity == rarity]