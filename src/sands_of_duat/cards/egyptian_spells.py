"""
Egyptian Spell Cards - Magic, incantations, and divine powers.
Spells provide immediate effects and ongoing magical powers.
"""

from pathlib import Path
from .card import (
    Card, CardType, CardRarity, CardElement, CardKeyword, 
    CardStats, CardEffect
)

# Asset base path
ASSETS_PATH = Path("assets/images/lora_training/final_dataset")


def create_words_of_power() -> Card:
    """Words of Power - Ancient Egyptian incantation."""
    return Card(
        card_id="spell_words_power_01",
        name="Words of Power",
        card_type=CardType.SPELL,
        rarity=CardRarity.COMMON,
        element=CardElement.MAGIC,
        stats=CardStats(
            mana_cost=2,
            sand_cost=0,
            ba_power=3,
            ka_power=1
        ),
        keywords={
            CardKeyword.HIEROGLYPH
        },
        effects=[
            CardEffect(
                name="Hieroglyphic Incantation",
                description="Deal 3 damage to target creature or player. If you control Thoth, draw a card.",
                effect_type="activated",
                target="choice",
                conditions=["thoth_bonus"]
            )
        ],
        description="Sacred hieroglyphs spoken aloud channel the power of creation itself.",
        flavor_text="'The words that created the world can also destroy those who oppose divine will.'",
        mythology_source="Pyramid Texts, Coffin Texts",
        image_path=ASSETS_PATH / "egyptian_myth_01_q81.png",
        image_quality=81
    )


def create_mummification_rite() -> Card:
    """Mummification Rite - Preserve and empower the dead."""
    return Card(
        card_id="spell_mummify_01",
        name="Sacred Mummification",
        card_type=CardType.SPELL,
        rarity=CardRarity.UNCOMMON,
        element=CardElement.DEATH,
        stats=CardStats(
            mana_cost=3,
            sand_cost=1,
            ba_power=2,
            ka_power=4
        ),
        keywords={
            CardKeyword.AFTERLIFE,
            CardKeyword.RITUAL
        },
        effects=[
            CardEffect(
                name="Preserve the Dead",
                description="Target creature in any discard pile gains +2/+2, Afterlife, and returns to the battlefield.",
                effect_type="activated",
                target="choice",
                ba_ka_interaction="afterlife_enhancement"
            )
        ],
        description="The sacred ritual that preserves the body and soul for the journey to the afterlife.",
        flavor_text="'Death is but a doorway. Through sacred rites, the departed join the eternal guardians.'",
        mythology_source="Mummification texts, Anubis rituals",
        image_path=ASSETS_PATH / "egyptian_myth_03_q77.png",
        image_quality=77
    )


def create_solar_blessing() -> Card:
    """Solar Blessing - Ra's divine light."""
    return Card(
        card_id="spell_solar_blessing_01",
        name="Blessing of the Sun God",
        card_type=CardType.SPELL,
        rarity=CardRarity.RARE,
        element=CardElement.SUN,
        stats=CardStats(
            mana_cost=4,
            sand_cost=2,
            ba_power=5,
            ka_power=3
        ),
        keywords={
            CardKeyword.DIVINE_PROTECTION
        },
        effects=[
            CardEffect(
                name="Solar Radiance",
                description="Heal all your creatures to full health and give them +2/+2 until end of turn. If you control Ra, they gain Divine Protection permanently.",
                effect_type="activated",
                target="all",
                conditions=["ra_bonus"]
            )
        ],
        description="The sun god's blessing brings healing light and divine protection to the faithful.",
        flavor_text="'Let Ra's golden light banish darkness and strengthen the hearts of the righteous.'",
        mythology_source="Solar hymns, Ra worship",
        image_path=ASSETS_PATH / "egyptian_myth_04_q79.png",
        image_quality=79
    )


def create_curse_of_set() -> Card:
    """Curse of Set - Chaotic destructive magic."""
    return Card(
        card_id="spell_curse_set_01",
        name="Curse of the Storm God",
        card_type=CardType.SPELL,
        rarity=CardRarity.UNCOMMON,
        element=CardElement.CHAOS,
        stats=CardStats(
            mana_cost=3,
            sand_cost=1,
            ba_power=1,
            ka_power=5
        ),
        keywords={
            CardKeyword.BA_SEPARATION
        },
        effects=[
            CardEffect(
                name="Chaotic Destruction",
                description="Deal 5 damage randomly distributed among all creatures. Then, randomly swap the positions of all remaining creatures.",
                effect_type="activated",
                target="all"
            )
        ],
        description="Set's chaotic power brings destructive storms and unpredictable upheaval.",
        flavor_text="'The desert wind brings change, and change brings destruction to the old order.'",
        mythology_source="Set mythology, storm magic",
        image_path=ASSETS_PATH / "egyptian_myth_06_q74.png",
        image_quality=74
    )


def create_judgment_of_anubis() -> Card:
    """Judgment of Anubis - Divine judgment spell."""
    return Card(
        card_id="spell_judgment_anubis_01",
        name="Judgment of the Jackal God",
        card_type=CardType.SPELL,
        rarity=CardRarity.EPIC,
        element=CardElement.DEATH,
        stats=CardStats(
            mana_cost=5,
            sand_cost=2,
            ba_power=7,
            ka_power=3
        ),
        keywords={
            CardKeyword.JUDGMENT,
            CardKeyword.BA_SEPARATION,
            CardKeyword.AFTERLIFE
        },
        effects=[
            CardEffect(
                name="Weighing of Hearts",
                description="Examine all creatures. Destroy those with more Ka than Ba. Creatures with more Ba than Ka gain +2/+2 and Afterlife.",
                effect_type="activated",
                target="all",
                ba_ka_interaction="mass_judgment"
            )
        ],
        description="Anubis weighs the hearts of all beings against the feather of Ma'at, determining their fate.",
        flavor_text="'The scales do not lie. Let the worthy ascend and the corrupt be devoured.'",
        mythology_source="Book of the Dead, Judgment of Osiris",
        image_path=ASSETS_PATH / "egyptian_myth_07_q79.png",
        image_quality=79
    )


def create_isis_healing() -> Card:
    """Isis Healing - Powerful restoration magic."""
    return Card(
        card_id="spell_isis_healing_01",
        name="Isis's Divine Healing",
        card_type=CardType.SPELL,
        rarity=CardRarity.RARE,
        element=CardElement.MAGIC,
        stats=CardStats(
            mana_cost=4,
            sand_cost=1,
            ba_power=4,
            ka_power=4
        ),
        keywords={
            CardKeyword.ANKH_LIFE,
            CardKeyword.SOUL_LINK
        },
        effects=[
            CardEffect(
                name="Words of Life",
                description="Choose up to 3 targets. Heal them to full health and remove all negative status effects. Link their souls together.",
                effect_type="activated",
                target="choice",
                ba_ka_interaction="soul_linking"
            )
        ],
        description="Isis's healing magic can restore life even from the brink of death and bind souls in eternal bonds.",
        flavor_text="'My magic flows through the words of power, bringing healing where there was harm.'",
        mythology_source="Isis magic, healing spells",
        image_path=ASSETS_PATH / "egyptian_myth_08_q75.png",
        image_quality=75
    )


def create_pharaohs_command() -> Card:
    """Pharaoh's Command - Royal authority spell."""
    return Card(
        card_id="spell_pharaoh_command_01",
        name="Divine Command of the Pharaoh",
        card_type=CardType.SPELL,
        rarity=CardRarity.UNCOMMON,
        element=CardElement.ORDER,
        stats=CardStats(
            mana_cost=3,
            sand_cost=1,
            ba_power=2,
            ka_power=4
        ),
        keywords={
            CardKeyword.PHARAOH_BOND
        },
        effects=[
            CardEffect(
                name="Royal Decree",
                description="All your creatures gain +1/+1 and Charge until end of turn. If you control a pharaoh, they also gain Pierce.",
                effect_type="activated",
                target="all",
                conditions=["pharaoh_bonus"]
            )
        ],
        description="The pharaoh's word is law, inspiring troops to fight with divine authority.",
        flavor_text="'The pharaoh speaks with the voice of the gods. Let all creation obey!'",
        mythology_source="Pharaonic texts, royal authority",
        image_path=ASSETS_PATH / "egyptian_myth_09_q84.png",
        image_quality=84
    )


def create_nile_flood() -> Card:
    """Nile Flood - Fertility and renewal spell."""
    return Card(
        card_id="spell_nile_flood_01",
        name="Great Flood of the Nile",
        card_type=CardType.SPELL,
        rarity=CardRarity.RARE,
        element=CardElement.WATER,
        stats=CardStats(
            mana_cost=5,
            sand_cost=2,
            ba_power=3,
            ka_power=6
        ),
        keywords={
            CardKeyword.REGENERATE
        },
        effects=[
            CardEffect(
                name="Fertile Waters",
                description="Heal all creatures for 4. Then, create a 2/2 Farmer token for each creature healed to full health.",
                effect_type="activated",
                target="all"
            ),
            CardEffect(
                name="Life-Giving Flood",
                description="For the next 3 turns, all creatures gain +1/+1 at the start of each turn and Regenerate 1.",
                effect_type="activated",
                target="all"
            )
        ],
        description="The annual flood brings fertility and life to the land of Egypt, blessing all with abundance.",
        flavor_text="'When the great river rises, Egypt blooms. Life springs eternal from the sacred waters.'",
        mythology_source="Nile flood mythology, Khnum worship",
        image_path=ASSETS_PATH / "egyptian_myth_10_q78.png",
        image_quality=78
    )


# Collection of all spell cards
EGYPTIAN_SPELL_CARDS = {
    "spell_words_power_01": create_words_of_power,
    "spell_mummify_01": create_mummification_rite,
    "spell_solar_blessing_01": create_solar_blessing,
    "spell_curse_set_01": create_curse_of_set,
    "spell_judgment_anubis_01": create_judgment_of_anubis,
    "spell_isis_healing_01": create_isis_healing,
    "spell_pharaoh_command_01": create_pharaohs_command,
    "spell_nile_flood_01": create_nile_flood
}


def get_all_spell_cards() -> list[Card]:
    """Get all Egyptian spell cards."""
    return [card_func() for card_func in EGYPTIAN_SPELL_CARDS.values()]


def get_spell_by_id(card_id: str) -> Card | None:
    """Get a specific spell card by ID."""
    card_func = EGYPTIAN_SPELL_CARDS.get(card_id)
    return card_func() if card_func else None