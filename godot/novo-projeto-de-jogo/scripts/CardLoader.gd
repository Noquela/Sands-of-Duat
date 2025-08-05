extends Node
class_name CardLoader

# Sands of Duat - Card Loader
# Loads and manages all cards in the game

var all_cards: Dictionary = {}
var starter_deck: Array[Card] = []

func _ready():
	load_all_cards()
	create_starter_deck()

func load_all_cards():
	print("CardLoader: Loading all cards...")
	
	# Load starter cards (matching Python definitions)
	create_desert_whisper()
	create_sand_grain()
	create_tomb_strike()
	create_ankh_blessing()
	create_scarab_swarm()
	create_papyrus_scroll()
	create_mummys_wrath()
	create_isis_grace()
	create_pyramid_power()
	create_thoths_wisdom()
	create_anubis_judgment()
	create_ras_solar_flare()
	create_pharaohs_resurrection()
	
	# Load Egyptian cards
	create_whisper_of_thoth()
	create_isis_protection()
	create_desert_meditation()
	create_ra_solar_flare_alt()
	create_mummification_ritual()
	create_ankh_of_life()
	
	print("CardLoader: Loaded %d cards" % all_cards.size())

func create_desert_whisper():
	var card = Card.new("Desert Whisper", "Draw a card. The desert spirits guide your hand.", 0)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/desert_whisper.png")
	
	var effect = CardEffect.new(Card.EffectType.DRAW_CARDS, Card.TargetType.SELF, 1)
	card.effects.append(effect)
	
	card.keywords = ["cantrip"]
	card.flavor_text = "The winds carry secrets from the ancient tombs."
	
	all_cards["desert_whisper"] = card

func create_sand_grain():
	var card = Card.new("Sand Grain", "Gain 1 sand. Every grain matters in the desert.", 0)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/sand_grain.png")
	
	var effect = CardEffect.new(Card.EffectType.GAIN_SAND, Card.TargetType.SELF, 1)
	card.effects.append(effect)
	
	card.flavor_text = "From small beginnings come great power."
	
	all_cards["sand_grain"] = card

func create_tomb_strike():
	var card = Card.new("Tomb Strike", "Deal 6 damage. Basic attack from the depths.", 1)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/tomb_strike.png")
	
	var effect = CardEffect.new(Card.EffectType.DAMAGE, Card.TargetType.ENEMY, 6)
	card.effects.append(effect)
	
	card.flavor_text = "Swift and silent, like the shadow of death."
	
	all_cards["tomb_strike"] = card

func create_ankh_blessing():
	var card = Card.new("Ankh Blessing", "Heal 5 health. Gain 3 block. The ankh protects.", 1)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/ankh_blessing.png")
	
	var heal_effect = CardEffect.new(Card.EffectType.HEAL, Card.TargetType.SELF, 5)
	var block_effect = CardEffect.new(Card.EffectType.GAIN_BLOCK, Card.TargetType.SELF, 3)
	card.effects.append(heal_effect)
	card.effects.append(block_effect)
	
	card.keywords = ["blessing"]
	card.flavor_text = "Life eternal flows through the sacred symbol."
	
	all_cards["ankh_blessing"] = card

func create_scarab_swarm():
	var card = Card.new("Scarab Swarm", "Deal 4 damage. Draw a card. Swarm tactics.", 2)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/scarab_swarm.png")
	
	var damage_effect = CardEffect.new(Card.EffectType.DAMAGE, Card.TargetType.ENEMY, 4)
	var draw_effect = CardEffect.new(Card.EffectType.DRAW_CARDS, Card.TargetType.SELF, 1)
	card.effects.append(damage_effect)
	card.effects.append(draw_effect)
	
	card.keywords = ["swarm"]
	card.flavor_text = "A thousand wings, a thousand bites."
	
	all_cards["scarab_swarm"] = card

func create_papyrus_scroll():
	var card = Card.new("Papyrus Scroll", "Draw 2 cards. Ancient knowledge unfolds.", 2)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/papyrus_scroll.png")
	
	var effect = CardEffect.new(Card.EffectType.DRAW_CARDS, Card.TargetType.SELF, 2)
	card.effects.append(effect)
	
	card.keywords = ["knowledge"]
	card.flavor_text = "Written by scribes, blessed by gods."
	
	all_cards["papyrus_scroll"] = card

func create_mummys_wrath():
	var card = Card.new("Mummy's Wrath", "Deal 8 damage. If enemy dies, gain 2 sand.", 3)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.UNCOMMON
	card.texture = load("res://cards/mummys_wrath.png")
	
	var effect = CardEffect.new(Card.EffectType.DAMAGE, Card.TargetType.ENEMY, 8)
	card.effects.append(effect)
	
	card.keywords = ["wrath", "conditional"]
	card.flavor_text = "Disturb not the eternal rest."
	
	all_cards["mummys_wrath"] = card

func create_isis_grace():
	var card = Card.new("Isis's Grace", "Heal to full health. Gain 5 block. Divine intervention.", 3)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.UNCOMMON
	card.texture = load("res://cards/isiss_grace.png")
	
	var heal_effect = CardEffect.new(Card.EffectType.HEAL, Card.TargetType.SELF, 999) # Full heal
	var block_effect = CardEffect.new(Card.EffectType.GAIN_BLOCK, Card.TargetType.SELF, 5)
	card.effects.append(heal_effect)
	card.effects.append(block_effect)
	
	card.keywords = ["divine", "blessing"]
	card.flavor_text = "The goddess watches over her faithful."
	
	all_cards["isis_grace"] = card

func create_pyramid_power():
	var card = Card.new("Pyramid Power", "Gain sand equal to current hour (max 3).", 4)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.RARE
	card.texture = load("res://cards/pyramid_power.png")
	
	var effect = CardEffect.new(Card.EffectType.SPECIAL, Card.TargetType.SELF, 0)
	card.effects.append(effect)
	
	card.keywords = ["pyramid", "scaling"]
	card.flavor_text = "As time passes, so grows the pyramid's might."
	
	all_cards["pyramid_power"] = card

func create_thoths_wisdom():
	var card = Card.new("Thoth's Wisdom", "Draw cards equal to card types in hand.", 4)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.RARE
	card.texture = load("res://cards/thoths_wisdom.png")
	
	var effect = CardEffect.new(Card.EffectType.SPECIAL, Card.TargetType.SELF, 0)
	card.effects.append(effect)
	
	card.keywords = ["wisdom", "scaling"]
	card.flavor_text = "Knowledge builds upon itself like the great libraries."
	
	all_cards["thoths_wisdom"] = card

func create_anubis_judgment():
	var card = Card.new("Anubis Judgment", "Deal damage equal to enemy's missing health.", 5)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.RARE
	card.texture = load("res://cards/anubis_judgment.png")
	
	var effect = CardEffect.new(Card.EffectType.SPECIAL, Card.TargetType.ENEMY, 0)
	card.effects.append(effect)
	
	card.keywords = ["judgment", "execute"]
	card.flavor_text = "The scales tip toward justice."
	
	all_cards["anubis_judgment"] = card

func create_ras_solar_flare():
	var card = Card.new("Ra's Solar Flare", "Deal 12 damage to all enemies. The sun's wrath.", 5)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.RARE
	card.texture = load("res://cards/ras_solar_flare.png")
	
	var effect = CardEffect.new(Card.EffectType.SPECIAL, Card.TargetType.ALL_ENEMIES, 12)
	card.effects.append(effect)
	
	card.keywords = ["solar", "aoe"]
	card.flavor_text = "The desert sun burns all who oppose it."
	
	all_cards["ras_solar_flare"] = card

func create_pharaohs_resurrection():
	var card = Card.new("Pharaoh's Resurrection", "Return from defeat with half health. Single use.", 6)
	card.card_type = Card.CardType.POWER
	card.rarity = Card.CardRarity.LEGENDARY
	card.texture = load("res://cards/pharaohs_resurrection.png")
	
	var effect = CardEffect.new(Card.EffectType.SPECIAL, Card.TargetType.SELF, 0)
	card.effects.append(effect)
	
	card.keywords = ["resurrection", "unique"]
	card.flavor_text = "Death is but a door to the pharaoh."
	
	all_cards["pharaohs_resurrection"] = card

# Egyptian cards from existing assets
func create_whisper_of_thoth():
	var card = Card.new("Whisper of Thoth", "Draw a card and gain 1 sand. Wisdom flows.", 1)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/whisper_of_thoth.png")
	
	var draw_effect = CardEffect.new(Card.EffectType.DRAW_CARDS, Card.TargetType.SELF, 1)
	var sand_effect = CardEffect.new(Card.EffectType.GAIN_SAND, Card.TargetType.SELF, 1)
	card.effects.append(draw_effect)
	card.effects.append(sand_effect)
	
	all_cards["whisper_of_thoth"] = card

func create_isis_protection():
	var card = Card.new("Isis Protection", "Gain 8 block. Divine shield.", 2)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/isis_protection.png")
	
	var effect = CardEffect.new(Card.EffectType.GAIN_BLOCK, Card.TargetType.SELF, 8)
	card.effects.append(effect)
	
	all_cards["isis_protection"] = card

func create_desert_meditation():
	var card = Card.new("Desert Meditation", "Heal 6 health. Draw a card.", 2)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.COMMON
	card.texture = load("res://cards/desert_meditation.png")
	
	var heal_effect = CardEffect.new(Card.EffectType.HEAL, Card.TargetType.SELF, 6)
	var draw_effect = CardEffect.new(Card.EffectType.DRAW_CARDS, Card.TargetType.SELF, 1)
	card.effects.append(heal_effect)
	card.effects.append(draw_effect)
	
	all_cards["desert_meditation"] = card

func create_ra_solar_flare_alt():
	var card = Card.new("Ra Solar Flare", "Deal 10 damage. Solar power.", 3)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.UNCOMMON
	card.texture = load("res://cards/ra_solar_flare.png")
	
	var effect = CardEffect.new(Card.EffectType.DAMAGE, Card.TargetType.ENEMY, 10)
	card.effects.append(effect)
	
	all_cards["ra_solar_flare_alt"] = card

func create_mummification_ritual():
	var card = Card.new("Mummification Ritual", "Deal 6 damage. If enemy dies, gain permanent health.", 4)
	card.card_type = Card.CardType.ATTACK
	card.rarity = Card.CardRarity.RARE
	card.texture = load("res://cards/mummification_ritual.png")
	
	var effect = CardEffect.new(Card.EffectType.DAMAGE, Card.TargetType.ENEMY, 6)
	card.effects.append(effect)
	
	all_cards["mummification_ritual"] = card

func create_ankh_of_life():
	var card = Card.new("Ankh of Life", "Heal 10 health. Gain 5 block. Life eternal.", 3)
	card.card_type = Card.CardType.SKILL
	card.rarity = Card.CardRarity.UNCOMMON
	card.texture = load("res://cards/ankh_of_life.png")
	
	var heal_effect = CardEffect.new(Card.EffectType.HEAL, Card.TargetType.SELF, 10)
	var block_effect = CardEffect.new(Card.EffectType.GAIN_BLOCK, Card.TargetType.SELF, 5)
	card.effects.append(heal_effect)
	card.effects.append(block_effect)
	
	all_cards["ankh_of_life"] = card

func create_starter_deck():
	# Create a balanced starter deck
	starter_deck.clear()
	
	# Add basic cards (matching Python starter deck)
	add_to_starter("tomb_strike", 4)      # Basic attack
	add_to_starter("ankh_blessing", 4)    # Basic defense/heal
	add_to_starter("desert_whisper", 2)   # Card draw
	add_to_starter("sand_grain", 2)       # Sand generation
	add_to_starter("scarab_swarm", 2)     # Efficient attack
	add_to_starter("papyrus_scroll", 1)   # Burst draw
	
	print("CardLoader: Created starter deck with %d cards" % starter_deck.size())

func add_to_starter(card_name: String, count: int):
	if card_name in all_cards:
		for i in count:
			starter_deck.append(all_cards[card_name].duplicate())

func get_card_by_name(card_name: String) -> Card:
	return all_cards.get(card_name.to_lower().replace(" ", "_").replace("'", ""))

func get_all_cards() -> Array[Card]:
	var cards: Array[Card] = []
	for card in all_cards.values():
		cards.append(card)
	return cards

func get_starter_deck() -> Array[Card]:
	var deck: Array[Card] = []
	for card in starter_deck:
		deck.append(card.duplicate())
	return deck

func get_cards_by_rarity(rarity: Card.CardRarity) -> Array[Card]:
	var cards: Array[Card] = []
	for card in all_cards.values():
		if card.rarity == rarity:
			cards.append(card)
	return cards

func get_cards_by_type(card_type: Card.CardType) -> Array[Card]:
	var cards: Array[Card] = []
	for card in all_cards.values():
		if card.card_type == card_type:
			cards.append(card)
	return cards