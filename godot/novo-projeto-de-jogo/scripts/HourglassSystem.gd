extends Node
class_name HourglassSystem

# Sands of Duat - Hourglass System
# Manages the 12-hour progression system

signal hour_changed(new_hour: int)
signal hourglass_turned
signal day_cycle_completed

@export var current_hour: int = 1
@export var max_hours: int = 12
@export var sand_per_hour: int = 1

# Hour effects and modifiers
var hour_modifiers: Dictionary = {}
var hour_rewards: Dictionary = {}

# Egyptian time theming
var hour_names: Array[String] = [
	"Dawn of Ra",           # Hour 1
	"Morning Light",        # Hour 2
	"Growing Strength",     # Hour 3
	"Midday Power",         # Hour 4
	"Peak of Sun",          # Hour 5
	"Blazing Zenith",       # Hour 6
	"Afternoon Glory",      # Hour 7
	"Waning Light",         # Hour 8
	"Evening Shadows",      # Hour 9
	"Twilight Descent",     # Hour 10
	"Night's Embrace",      # Hour 11
	"Darkness Falls"        # Hour 12
]

var hour_descriptions: Array[String] = [
	"The sun rises over the dunes, bringing new hope.",
	"Morning warmth spreads across the desert sands.",
	"The sun climbs higher, strengthening your resolve.",
	"Midday approaches with burning determination.",
	"The sun reaches its peak, power flows through you.",
	"At zenith, the desert reveals its hidden secrets.",
	"Afternoon light guides your path forward.",
	"The sun begins its descent, time grows short.",
	"Evening shadows lengthen across the land.",
	"Twilight brings ancient powers to life.",
	"Night falls, and darker forces stir.",
	"In the final hour, all is decided."
]

func _ready():
	setup_hour_system()

func setup_hour_system():
	current_hour = 1
	setup_hour_modifiers()
	setup_hour_rewards()
	print("HourglassSystem: Initialized at Hour %d" % current_hour)

func setup_hour_modifiers():
	# Define how each hour affects gameplay
	hour_modifiers = {
		1: {"sand_gain": 1, "card_draw": 0, "damage_bonus": 0},
		2: {"sand_gain": 1, "card_draw": 0, "damage_bonus": 0},
		3: {"sand_gain": 1, "card_draw": 1, "damage_bonus": 0},
		4: {"sand_gain": 2, "card_draw": 0, "damage_bonus": 1},
		5: {"sand_gain": 2, "card_draw": 0, "damage_bonus": 1},
		6: {"sand_gain": 2, "card_draw": 1, "damage_bonus": 2},  # Peak hour
		7: {"sand_gain": 2, "card_draw": 0, "damage_bonus": 1},
		8: {"sand_gain": 1, "card_draw": 1, "damage_bonus": 1},
		9: {"sand_gain": 1, "card_draw": 0, "damage_bonus": 0},
		10: {"sand_gain": 1, "card_draw": 1, "damage_bonus": -1},
		11: {"sand_gain": 1, "card_draw": 0, "damage_bonus": -1},
		12: {"sand_gain": 0, "card_draw": 2, "damage_bonus": -2}   # Final hour
	}

func setup_hour_rewards():
	# Define rewards for reaching each hour
	hour_rewards = {
		3: {"type": "card", "value": "sand_grain"},
		6: {"type": "upgrade", "value": "pyramid_power"},
		9: {"type": "relic", "value": "ankh_of_protection"},
		12: {"type": "victory", "value": "game_complete"}
	}

func advance_hour():
	if current_hour >= max_hours:
		print("HourglassSystem: Already at final hour")
		return false
	
	current_hour += 1
	print("HourglassSystem: Advanced to Hour %d - %s" % [current_hour, get_hour_name()])
	
	hour_changed.emit(current_hour)
	
	# Apply hour rewards
	if current_hour in hour_rewards:
		apply_hour_reward(hour_rewards[current_hour])
	
	# Check for completion
	if current_hour >= max_hours:
		day_cycle_completed.emit()
	
	return true

func turn_hourglass():
	# Special mechanic - turn the hourglass to gain benefits
	print("HourglassSystem: Hourglass turned!")
	hourglass_turned.emit()
	
	# Gain extra sand and card draw this turn
	return {
		"sand_bonus": 2,
		"draw_bonus": 1,
		"description": "The sands of time flow in your favor"
	}

func get_current_hour_modifier(modifier_type: String) -> int:
	var modifiers = hour_modifiers.get(current_hour, {})
	return modifiers.get(modifier_type, 0)

func get_sand_gain_modifier() -> int:
	return get_current_hour_modifier("sand_gain")

func get_card_draw_modifier() -> int:
	return get_current_hour_modifier("card_draw")

func get_damage_bonus() -> int:
	return get_current_hour_modifier("damage_bonus")

func apply_hour_reward(reward: Dictionary):
	print("HourglassSystem: Applying hour reward: %s" % reward)
	
	match reward.type:
		"card":
			# Award a specific card
			var card_name = reward.value
			print("Rewarded with card: %s" % card_name)
			# This would connect to the game manager to add the card
		
		"upgrade":
			# Upgrade a specific card
			var card_name = reward.value
			print("Card upgraded: %s" % card_name)
			# This would connect to upgrade system
		
		"relic":
			# Award a relic/artifact
			var relic_name = reward.value
			print("Rewarded with relic: %s" % relic_name)
			# This would connect to relic system
		
		"victory":
			print("Game completed successfully!")
			# This would trigger victory condition

func get_hour_name(hour: int = current_hour) -> String:
	if hour < 1 or hour > hour_names.size():
		return "Unknown Hour"
	return hour_names[hour - 1]

func get_hour_description(hour: int = current_hour) -> String:
	if hour < 1 or hour > hour_descriptions.size():
		return "Time flows through the hourglass..."
	return hour_descriptions[hour - 1]

func get_progress_percentage() -> float:
	return float(current_hour) / float(max_hours) * 100.0

func get_remaining_hours() -> int:
	return max_hours - current_hour

func is_final_hour() -> bool:
	return current_hour >= max_hours

func is_peak_hour() -> bool:
	return current_hour == 6  # Noon - peak of the sun

func is_dawn() -> bool:
	return current_hour <= 2

func is_dusk() -> bool:
	return current_hour >= 10

func get_time_period() -> String:
	if current_hour <= 2:
		return "Dawn"
	elif current_hour <= 5:
		return "Morning"
	elif current_hour <= 7:
		return "Noon"
	elif current_hour <= 9:
		return "Afternoon"
	elif current_hour <= 11:
		return "Evening"
	else:
		return "Night"

# Visual and UI helpers
func get_hourglass_fill_percentage() -> float:
	# Returns how full the hourglass appears (inverted for visual effect)
	return 1.0 - (float(current_hour - 1) / float(max_hours - 1))

func get_sun_position() -> float:
	# Returns sun position for background visuals (0.0 = sunrise, 1.0 = sunset)
	return float(current_hour - 1) / float(max_hours - 1)

func get_hour_color() -> Color:
	# Returns color theme for the current hour
	var progress = get_sun_position()
	
	if progress <= 0.2:  # Dawn
		return Color.ORANGE.lerp(Color.YELLOW, progress * 5)
	elif progress <= 0.5:  # Morning to Noon
		return Color.YELLOW.lerp(Color.WHITE, (progress - 0.2) * 3.33)
	elif progress <= 0.8:  # Afternoon
		return Color.WHITE.lerp(Color.ORANGE, (progress - 0.5) * 3.33)
	else:  # Evening to Night
		return Color.ORANGE.lerp(Color.DARK_BLUE, (progress - 0.8) * 5)

# Save/Load system
func get_save_data() -> Dictionary:
	return {
		"current_hour": current_hour,
		"max_hours": max_hours
	}

func load_save_data(data: Dictionary):
	current_hour = data.get("current_hour", 1)
	max_hours = data.get("max_hours", 12)
	hour_changed.emit(current_hour)
	print("HourglassSystem: Loaded save data - Hour %d" % current_hour)

# Debug functions
func skip_to_hour(target_hour: int):
	if target_hour < 1 or target_hour > max_hours:
		print("HourglassSystem: Invalid hour %d" % target_hour)
		return
	
	current_hour = target_hour
	hour_changed.emit(current_hour)
	print("HourglassSystem: Skipped to Hour %d" % current_hour)

func reset_hourglass():
	current_hour = 1
	hour_changed.emit(current_hour)
	print("HourglassSystem: Reset to Hour 1")

func print_hour_info():
	print("=== HOURGLASS INFO ===")
	print("Current Hour: %d/%d" % [current_hour, max_hours])
	print("Hour Name: %s" % get_hour_name())
	print("Description: %s" % get_hour_description())
	print("Time Period: %s" % get_time_period())
	print("Progress: %.1f%%" % get_progress_percentage())
	print("Sand Gain: +%d" % get_sand_gain_modifier())
	print("Card Draw: +%d" % get_card_draw_modifier())
	print("Damage Bonus: %+d" % get_damage_bonus())
	print("=====================")