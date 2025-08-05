extends Resource
class_name CardEffect

# Sands of Duat - Card Effect Resource
# Represents individual effects that cards can have

@export var effect_type: Card.EffectType = Card.EffectType.DAMAGE
@export var target_type: Card.TargetType = Card.TargetType.ENEMY
@export var value: int = 1
@export var status_name: String = ""
@export var duration: int = 1

# Runtime properties
var actual_target: Node = null
var was_triggered: bool = false

func _init(type: Card.EffectType = Card.EffectType.DAMAGE, target: Card.TargetType = Card.TargetType.ENEMY, effect_value: int = 1):
	effect_type = type
	target_type = target
	value = effect_value

func get_description() -> String:
	match effect_type:
		Card.EffectType.DAMAGE:
			return "Deal %d damage" % value
		Card.EffectType.HEAL:
			return "Heal %d health" % value
		Card.EffectType.DRAW_CARDS:
			return "Draw %d card%s" % [value, "s" if value > 1 else ""]
		Card.EffectType.GAIN_SAND:
			return "Gain %d sand" % value
		Card.EffectType.GAIN_BLOCK:
			return "Gain %d block" % value
		Card.EffectType.APPLY_STATUS:
			return "Apply %s (%d)" % [status_name, value]
		Card.EffectType.SPECIAL:
			return "Special effect"
		_:
			return "Unknown effect"

func get_target_description() -> String:
	match target_type:
		Card.TargetType.SELF:
			return "Self"
		Card.TargetType.ENEMY:
			return "Enemy"
		Card.TargetType.ALL_ENEMIES:
			return "All enemies"
		Card.TargetType.ANY:
			return "Any target"
		_:
			return "Unknown target"

func duplicate() -> CardEffect:
	var new_effect = CardEffect.new()
	new_effect.effect_type = effect_type
	new_effect.target_type = target_type
	new_effect.value = value
	new_effect.status_name = status_name
	new_effect.duration = duration
	return new_effect