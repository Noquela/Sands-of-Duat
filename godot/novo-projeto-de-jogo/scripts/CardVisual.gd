extends Control
class_name CardVisual

# Sands of Duat - Card Visual Component
# Handles the visual representation and interactions of cards

signal card_selected(card: Card)
signal card_hovered(card: Card)
signal card_unhovered(card: Card)

@export var card_data: Card
@export var is_in_hand: bool = true
@export var is_playable: bool = true
@export var show_tooltip: bool = true

# Visual components
@onready var card_background: NinePatchRect = $CardBackground
@onready var card_image: TextureRect = $CardImage
@onready var card_title: Label = $CardTitle
@onready var cost_label: Label = $CostLabel
@onready var description_label: Label = $DescriptionLabel
@onready var type_label: Label = $TypeLabel
@onready var animation_player: AnimationPlayer = $AnimationPlayer

# Visual states
var is_hovered: bool = false
var is_selected: bool = false
var original_position: Vector2
var original_scale: Vector2 = Vector2.ONE
var tween: Tween

# Card dimensions
const CARD_SIZE = Vector2(200, 280)
const HOVER_SCALE = 1.1
const HOVER_OFFSET = Vector2(0, -20)

func _ready():
	setup_visual_components()
	setup_signals()
	if card_data:
		update_card_display()

func setup_visual_components():
	# Set card size
	custom_minimum_size = CARD_SIZE
	size = CARD_SIZE
	
	# Store original transform
	original_position = position
	original_scale = scale
	
	# Setup mouse detection
	mouse_entered.connect(_on_mouse_entered)
	mouse_exited.connect(_on_mouse_exited)

func setup_signals():
	# Connect GUI input for clicking
	gui_input.connect(_on_gui_input)

func set_card_data(new_card: Card):
	card_data = new_card
	if is_node_ready():
		update_card_display()

func update_card_display():
	if not card_data:
		return
	
	# Update text elements
	if card_title:
		card_title.text = card_data.name
	
	if cost_label:
		cost_label.text = str(card_data.sand_cost)
		# Color cost based on playability
		cost_label.modulate = Color.WHITE if is_playable else Color.RED
	
	if description_label:
		description_label.text = card_data.description
	
	if type_label:
		type_label.text = card_data.get_type_name()
	
	# Update card image
	if card_image and card_data.texture:
		card_image.texture = card_data.texture
	
	# Update background based on rarity
	update_rarity_visual()
	
	# Update playability visual
	update_playability_visual()

func update_rarity_visual():
	if not card_background:
		return
	
	match card_data.rarity:
		Card.CardRarity.COMMON:
			card_background.modulate = Color.WHITE
		Card.CardRarity.UNCOMMON:
			card_background.modulate = Color.GREEN
		Card.CardRarity.RARE:
			card_background.modulate = Color.BLUE
		Card.CardRarity.LEGENDARY:
			card_background.modulate = Color.GOLD

func update_playability_visual():
	var alpha = 1.0 if is_playable else 0.6
	modulate = Color(1, 1, 1, alpha)

func set_playable(playable: bool):
	is_playable = playable
	update_playability_visual()
	
	if cost_label:
		cost_label.modulate = Color.WHITE if is_playable else Color.RED

func _on_mouse_entered():
	if not is_playable:
		return
	
	is_hovered = true
	card_hovered.emit(card_data)
	
	animate_hover(true)
	
	if show_tooltip:
		show_card_tooltip()

func _on_mouse_exited():
	is_hovered = false
	card_unhovered.emit(card_data)
	
	animate_hover(false)
	hide_card_tooltip()

func _on_gui_input(event: InputEvent):
	if event is InputEventMouseButton:
		if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			if is_playable:
				card_selected.emit(card_data)
				animate_selection()

func animate_hover(hover: bool):
	if tween:
		tween.kill()
	tween = create_tween()
	tween.set_parallel(true)
	
	if hover:
		# Hover animation
		tween.tween_property(self, "scale", original_scale * HOVER_SCALE, 0.2)
		tween.tween_property(self, "position", original_position + HOVER_OFFSET, 0.2)
		tween.tween_property(self, "z_index", 10, 0.0)
	else:
		# Return to normal
		tween.tween_property(self, "scale", original_scale, 0.2)
		tween.tween_property(self, "position", original_position, 0.2)
		tween.tween_property(self, "z_index", 0, 0.2)

func animate_selection():
	if animation_player and animation_player.has_animation("select"):
		animation_player.play("select")
	else:
		# Fallback pulse animation
		if tween:
			tween.kill()
		tween = create_tween()
		tween.tween_property(self, "scale", original_scale * 0.95, 0.1)
		tween.tween_property(self, "scale", original_scale, 0.1)

func animate_play():
	if animation_player and animation_player.has_animation("play"):
		animation_player.play("play")
	else:
		# Fallback play animation
		if tween:
			tween.kill()
		tween = create_tween()
		tween.set_parallel(true)
		tween.tween_property(self, "modulate", Color.TRANSPARENT, 0.5)
		tween.tween_property(self, "scale", Vector2.ZERO, 0.5)
		tween.tween_callback(queue_free).set_delay(0.5)

func show_card_tooltip():
	if not card_data:
		return
	
	# Create tooltip (this would connect to a tooltip manager)
	var tooltip_text = card_data.get_tooltip_text()
	print("Tooltip: %s" % tooltip_text)  # Debug - replace with actual tooltip

func hide_card_tooltip():
	# Hide tooltip
	pass

func set_position_smoothly(new_position: Vector2, duration: float = 0.3):
	original_position = new_position
	
	if tween:
		tween.kill()
	tween = create_tween()
	tween.tween_property(self, "position", new_position, duration)

func set_scale_smoothly(new_scale: Vector2, duration: float = 0.3):
	original_scale = new_scale
	
	if tween:
		tween.kill()
	tween = create_tween()
	tween.tween_property(self, "scale", new_scale, duration)

# Drag and drop functionality
var is_dragging: bool = false
var drag_offset: Vector2

func start_drag():
	if not is_playable:
		return false
	
	is_dragging = true
	drag_offset = get_global_mouse_position() - global_position
	z_index = 100
	return true

func update_drag():
	if is_dragging:
		global_position = get_global_mouse_position() - drag_offset

func end_drag():
	if is_dragging:
		is_dragging = false
		z_index = 0
		
		# Snap back to original position if not dropped on valid target
		set_position_smoothly(original_position)

func _input(event):
	if is_dragging and event is InputEventMouseMotion:
		update_drag()
	elif is_dragging and event is InputEventMouseButton:
		if not event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			end_drag()

# Utility functions
func get_card_bounds() -> Rect2:
	return Rect2(global_position, size)

func is_point_over_card(point: Vector2) -> bool:
	return get_card_bounds().has_point(point)

func set_highlight(highlight: bool, color: Color = Color.YELLOW):
	if highlight:
		modulate = color
	else:
		modulate = Color.WHITE