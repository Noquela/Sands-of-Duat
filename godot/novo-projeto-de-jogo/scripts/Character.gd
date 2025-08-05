extends CharacterBody2D
class_name Character

# Sands of Duat - Character Base Class
# Handles character animations, stats, and combat behaviors

signal health_changed(new_health, max_health)
signal died
signal status_applied(status_name, duration)
signal animation_finished(animation_name)

@export var character_name: String = "Unknown"
@export var max_health: int = 100
@export var current_health: int = 100
@export var block: int = 0
@export var is_player: bool = false

# Animation components
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var health_bar: ProgressBar = $HealthBar
@onready var block_label: Label = $BlockLabel
@onready var damage_numbers: Node2D = $DamageNumbers
@onready var status_effects: Node2D = $StatusEffects

# Character states
enum CharacterState {
	IDLE,
	ATTACKING,
	TAKING_DAMAGE,
	DYING,
	CASTING
}

var current_state: CharacterState = CharacterState.IDLE
var status_effects_dict: Dictionary = {}

# Animation configuration
var animation_config: Dictionary = {
	"idle": {"frames": 16, "fps": 12, "loop": true},
	"attack": {"frames": 12, "fps": 15, "loop": false},
	"hurt": {"frames": 8, "fps": 12, "loop": false},
	"death": {"frames": 8, "fps": 10, "loop": false}
}

func _ready():
	setup_character()
	setup_animations()
	play_animation("idle")

func setup_character():
	current_health = max_health
	update_health_display()
	update_block_display()

func setup_animations():
	if not animated_sprite:
		print("Warning: No AnimatedSprite2D found for character %s" % character_name)
		return
	
	# Connect animation finished signal
	if animated_sprite.animation_finished.connect(_on_animation_finished):
		print("Animation finished signal connected for %s" % character_name)

func play_animation(anim_name: String, force: bool = false):
	if not animated_sprite:
		return
	
	if not force and animated_sprite.animation == anim_name and animated_sprite.is_playing():
		return
	
	if animated_sprite.sprite_frames and animated_sprite.sprite_frames.has_animation(anim_name):
		animated_sprite.play(anim_name)
		print("%s: Playing animation %s" % [character_name, anim_name])
	else:
		print("Warning: Animation %s not found for %s" % [anim_name, character_name])
		# Fallback to idle if available
		if animated_sprite.sprite_frames and animated_sprite.sprite_frames.has_animation("idle"):
			animated_sprite.play("idle")

func take_damage(damage: int):
	var actual_damage = max(0, damage - block)
	var blocked_damage = damage - actual_damage
	
	# Apply damage
	current_health = max(0, current_health - actual_damage)
	
	# Reduce block
	block = max(0, block - damage)
	
	# Visual feedback
	show_damage_number(actual_damage, blocked_damage)
	play_animation("hurt")
	flash_red()
	
	# Update UI
	update_health_display()
	update_block_display()
	
	# Emit signals
	health_changed.emit(current_health, max_health)
	
	# Check for death
	if current_health <= 0:
		die()
	
	print("%s took %d damage (%d blocked)" % [character_name, actual_damage, blocked_damage])

func heal(amount: int):
	var old_health = current_health
	current_health = min(max_health, current_health + amount)
	var actual_heal = current_health - old_health
	
	if actual_heal > 0:
		show_heal_number(actual_heal)
		flash_green()
		update_health_display()
		health_changed.emit(current_health, max_health)
		print("%s healed for %d" % [character_name, actual_heal])

func gain_block(amount: int):
	block += amount
	update_block_display()
	show_block_number(amount)
	print("%s gained %d block" % [character_name, amount])

func apply_status(status_name: String, duration: int):
	status_effects_dict[status_name] = duration
	update_status_display()
	status_applied.emit(status_name, duration)
	print("%s applied status: %s (%d turns)" % [character_name, status_name, duration])

func remove_status(status_name: String):
	if status_name in status_effects_dict:
		status_effects_dict.erase(status_name)
		update_status_display()
		print("%s removed status: %s" % [character_name, status_name])

func has_status(status_name: String) -> bool:
	return status_name in status_effects_dict

func get_status_duration(status_name: String) -> int:
	return status_effects_dict.get(status_name, 0)

func process_status_effects():
	# Process status effects at start of turn
	var statuses_to_remove = []
	
	for status_name in status_effects_dict.keys():
		var duration = status_effects_dict[status_name]
		
		# Apply status effect
		apply_status_effect(status_name)
		
		# Reduce duration
		duration -= 1
		if duration <= 0:
			statuses_to_remove.append(status_name)
		else:
			status_effects_dict[status_name] = duration
	
	# Remove expired statuses
	for status in statuses_to_remove:
		remove_status(status)

func apply_status_effect(status_name: String):
	match status_name:
		"poison":
			take_damage(3)
		"regeneration":
			heal(5)
		"weakness":
			# Handled in damage calculation
			pass
		"strength":
			# Handled in damage calculation
			pass

func die():
	current_state = CharacterState.DYING
	play_animation("death")
	print("%s has died" % character_name)
	died.emit()

func attack_animation():
	current_state = CharacterState.ATTACKING
	play_animation("attack")

func cast_animation():
	current_state = CharacterState.CASTING
	play_animation("cast", true)

func _on_animation_finished():
	match current_state:
		CharacterState.ATTACKING:
			current_state = CharacterState.IDLE
			play_animation("idle")
		CharacterState.TAKING_DAMAGE:
			current_state = CharacterState.IDLE
			play_animation("idle")
		CharacterState.CASTING:
			current_state = CharacterState.IDLE
			play_animation("idle")
		CharacterState.DYING:
			# Stay in death animation
			pass
	
	animation_finished.emit(animated_sprite.animation)

# Visual effects
func flash_red():
	var tween = create_tween()
	tween.tween_property(animated_sprite, "modulate", Color.RED, 0.1)
	tween.tween_property(animated_sprite, "modulate", Color.WHITE, 0.1)

func flash_green():
	var tween = create_tween()
	tween.tween_property(animated_sprite, "modulate", Color.GREEN, 0.1)
	tween.tween_property(animated_sprite, "modulate", Color.WHITE, 0.1)

func show_damage_number(damage: int, blocked: int = 0):
	if damage_numbers:
		var damage_text = str(damage)
		if blocked > 0:
			damage_text += " (%d blocked)" % blocked
		create_floating_text(damage_text, Color.RED)

func show_heal_number(heal: int):
	if damage_numbers:
		create_floating_text("+" + str(heal), Color.GREEN)

func show_block_number(block_amount: int):
	if damage_numbers:
		create_floating_text("+" + str(block_amount) + " block", Color.BLUE)

func create_floating_text(text: String, color: Color):
	var label = Label.new()
	label.text = text
	label.modulate = color
	label.add_theme_font_size_override("font_size", 24)
	
	damage_numbers.add_child(label)
	
	var tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(label, "position", label.position + Vector2(0, -50), 1.0)
	tween.tween_property(label, "modulate:a", 0.0, 1.0)
	tween.tween_callback(label.queue_free).set_delay(1.0)

func update_health_display():
	if health_bar:
		health_bar.max_value = max_health
		health_bar.value = current_health
		
		# Color health bar based on health percentage
		var health_percent = float(current_health) / float(max_health)
		if health_percent > 0.6:
			health_bar.modulate = Color.GREEN
		elif health_percent > 0.3:
			health_bar.modulate = Color.YELLOW
		else:
			health_bar.modulate = Color.RED

func update_block_display():
	if block_label:
		if block > 0:
			block_label.text = str(block)
			block_label.visible = true
		else:
			block_label.visible = false

func update_status_display():
	# Update status effect icons (simplified)
	if status_effects:
		# Clear existing status displays
		for child in status_effects.get_children():
			child.queue_free()
		
		# Add status icons
		var x_offset = 0
		for status_name in status_effects_dict.keys():
			var status_icon = Label.new()
			status_icon.text = status_name[0].to_upper()  # First letter as icon
			status_icon.position.x = x_offset
			status_effects.add_child(status_icon)
			x_offset += 20

# Getters for card effects
func get_missing_health() -> int:
	return max_health - current_health

func get_current_health() -> int:
	return current_health

func get_max_health() -> int:
	return max_health

func get_block_amount() -> int:
	return block

func is_alive() -> bool:
	return current_health > 0

# Utility functions
func reset_character():
	current_health = max_health
	block = 0
	status_effects_dict.clear()
	current_state = CharacterState.IDLE
	update_health_display()
	update_block_display()
	update_status_display()
	play_animation("idle")

func set_max_health(new_max: int):
	max_health = new_max
	current_health = min(current_health, max_health)
	update_health_display()
	health_changed.emit(current_health, max_health)