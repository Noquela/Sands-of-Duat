extends Resource
class_name Card

# Sands of Duat - Card Resource
# Represents a card in the game with all its properties and effects

enum CardType {
	ATTACK,
	SKILL,
	POWER
}

enum CardRarity {
	COMMON,
	UNCOMMON,
	RARE,
	LEGENDARY
}

enum EffectType {
	DAMAGE,
	HEAL,
	DRAW_CARDS,
	GAIN_SAND,
	GAIN_BLOCK,
	APPLY_STATUS,
	SPECIAL
}

enum TargetType {
	SELF,
	ENEMY,
	ALL_ENEMIES,
	ANY
}

@export var name: String = ""
@export var description: String = ""
@export var sand_cost: int = 1
@export var card_type: CardType = CardType.ATTACK
@export var rarity: CardRarity = CardRarity.COMMON
@export var texture: Texture2D
@export var effects: Array[CardEffect] = []
@export var keywords: Array[String] = []
@export var flavor_text: String = ""

# Visual properties
@export var is_exhausted: bool = false
@export var is_retained: bool = false
@export var is_innate: bool = false

func _init(card_name: String = "", card_description: String = "", cost: int = 1):
	name = card_name
	description = card_description
	sand_cost = cost

func can_play(current_sand: int, target = null) -> bool:
	if current_sand < sand_cost:
		return false
	
	# Check if card requires a target
	for effect in effects:
		if effect.target_type == TargetType.ENEMY and not target:
			return false
	
	return true

func play(caster, target = null) -> Array[CardEffect]:
	print("Playing card: %s" % name)
	
	var resolved_effects: Array[CardEffect] = []
	
	for effect in effects:
		var resolved_effect = resolve_effect(effect, caster, target)
		if resolved_effect:
			resolved_effects.append(resolved_effect)
	
	return resolved_effects

func resolve_effect(effect: CardEffect, caster, target) -> CardEffect:
	var resolved = effect.duplicate()
	
	match effect.effect_type:
		EffectType.DAMAGE:
			if target and target.has_method("take_damage"):
				target.take_damage(effect.value)
				resolved.actual_target = target
		
		EffectType.HEAL:
			if caster and caster.has_method("heal"):
				caster.heal(effect.value)
				resolved.actual_target = caster
		
		EffectType.DRAW_CARDS:
			if caster and caster.has_method("draw_cards"):
				caster.draw_cards(effect.value)
				resolved.actual_target = caster
		
		EffectType.GAIN_SAND:
			if caster and caster.has_method("gain_sand"):
				caster.gain_sand(effect.value)
				resolved.actual_target = caster
		
		EffectType.GAIN_BLOCK:
			if caster and caster.has_method("gain_block"):
				caster.gain_block(effect.value)
				resolved.actual_target = caster
		
		EffectType.APPLY_STATUS:
			var status_target = target if effect.target_type == TargetType.ENEMY else caster
			if status_target and status_target.has_method("apply_status"):
				status_target.apply_status(effect.status_name, effect.value)
				resolved.actual_target = status_target
		
		EffectType.SPECIAL:
			# Handle special card effects
			resolved = handle_special_effect(effect, caster, target)
	
	return resolved

func handle_special_effect(effect: CardEffect, caster, target) -> CardEffect:
	# Handle special card mechanics specific to Sands of Duat
	var resolved = effect.duplicate()
	
	match name:
		"Desert Whisper":
			# Draw a card
			if caster and caster.has_method("draw_cards"):
				caster.draw_cards(1)
		
		"Pyramid Power":
			# Gain sand based on current hour
			if caster and caster.has_method("get_current_hour"):
				var hour = caster.get_current_hour()
				var sand_gained = min(hour, 3)
				if caster.has_method("gain_sand"):
					caster.gain_sand(sand_gained)
				resolved.value = sand_gained
		
		"Anubis Judgment":
			# Deal damage equal to enemy's missing health
			if target and target.has_method("get_missing_health"):
				var missing_health = target.get_missing_health()
				var damage = min(missing_health, 10) # Cap at 10
				if target.has_method("take_damage"):
					target.take_damage(damage)
				resolved.value = damage
		
		"Ra's Solar Flare":
			# Deal damage to all enemies
			if caster and caster.has_method("get_all_enemies"):
				var enemies = caster.get_all_enemies()
				for enemy in enemies:
					if enemy.has_method("take_damage"):
						enemy.take_damage(effect.value)
		
		"Thoth's Wisdom":
			# Draw cards equal to the number of different card types in hand
			if caster and caster.has_method("get_hand_diversity"):
				var diversity = caster.get_hand_diversity()
				if caster.has_method("draw_cards"):
					caster.draw_cards(diversity)
				resolved.value = diversity
	
	resolved.actual_target = target if target else caster
	return resolved

func get_display_cost() -> String:
	return str(sand_cost)

func get_type_name() -> String:
	return CardType.keys()[card_type]

func get_rarity_name() -> String:
	return CardRarity.keys()[rarity]

func get_tooltip_text() -> String:
	var tooltip = "%s\nCost: %d Sand\nType: %s\n\n%s" % [name, sand_cost, get_type_name(), description]
	
	if not keywords.is_empty():
		tooltip += "\n\nKeywords: " + ", ".join(keywords)
	
	if flavor_text != "":
		tooltip += "\n\n" + flavor_text
	
	return tooltip

func duplicate() -> Card:
	var new_card = Card.new()
	new_card.name = name
	new_card.description = description
	new_card.sand_cost = sand_cost
	new_card.card_type = card_type
	new_card.rarity = rarity
	new_card.texture = texture
	new_card.effects = effects.duplicate()
	new_card.keywords = keywords.duplicate()
	new_card.flavor_text = flavor_text
	new_card.is_exhausted = is_exhausted
	new_card.is_retained = is_retained
	new_card.is_innate = is_innate
	return new_card

func is_valid() -> bool:
	return name != "" and description != "" and sand_cost >= 0

# Comparison for sorting
func compare_by_cost(other: Card) -> bool:
	return sand_cost < other.sand_cost

func compare_by_name(other: Card) -> bool:
	return name < other.name

func compare_by_type(other: Card) -> bool:
	return card_type < other.card_type