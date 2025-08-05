extends Node
class_name UIManager

# Sands of Duat - UI Manager
# Manages all UI screens and transitions

signal state_change_requested(new_state)
signal card_played(card: Card)
signal target_selected(target)

# UI Screens
var current_screen: Control
var screens: Dictionary = {}

# Screen names
const MENU_SCREEN = "menu"
const COMBAT_SCREEN = "combat"
const MAP_SCREEN = "map"
const DECK_BUILDER_SCREEN = "deck_builder"
const VICTORY_SCREEN = "victory"
const DEFEAT_SCREEN = "defeat"

# UI Components
var main_container: Control
var hud: Control
var tooltip: Control

# Egyptian UI Theme
var egyptian_theme: Theme

func _ready():
	setup_ui_theme()
	setup_main_container()
	create_screens()

func setup_ui_theme():
	egyptian_theme = Theme.new()
	
	# Egyptian color palette (sandstone theme)
	var primary_color = Color("#8B4513")    # Saddle brown
	var secondary_color = Color("#DAA520")  # Goldenrod
	var accent_color = Color("#CD853F")     # Peru
	var background_color = Color("#2C1810") # Dark brown
	
	# Setup theme resources would go here
	# For now, we'll apply colors manually to UI elements

func setup_main_container():
	main_container = Control.new()
	main_container.name = "MainContainer"
	main_container.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(main_container)
	
	# Setup HUD (always visible)
	setup_hud()

func setup_hud():
	hud = Control.new()
	hud.name = "HUD"
	hud.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	main_container.add_child(hud)
	
	# Sand counter
	var sand_container = HBoxContainer.new()
	sand_container.position = Vector2(20, 20)
	hud.add_child(sand_container)
	
	var sand_icon = Label.new()
	sand_icon.text = "🏺"
	sand_icon.add_theme_font_size_override("font_size", 24)
	sand_container.add_child(sand_icon)
	
	var sand_label = Label.new()
	sand_label.name = "SandLabel"
	sand_label.text = "3/6"
	sand_label.add_theme_font_size_override("font_size", 20)
	sand_container.add_child(sand_label)
	
	# Hour counter
	var hour_container = HBoxContainer.new()
	hour_container.position = Vector2(150, 20)
	hud.add_child(hour_container)
	
	var hour_icon = Label.new()
	hour_icon.text = "⧗"
	hour_icon.add_theme_font_size_override("font_size", 24)
	hour_container.add_child(hour_icon)
	
	var hour_label = Label.new()
	hour_label.name = "HourLabel"
	hour_label.text = "Hour 1/12"
	hour_label.add_theme_font_size_override("font_size", 20)
	hour_container.add_child(hour_label)

func create_screens():
	create_menu_screen()
	create_combat_screen()
	create_map_screen()
	create_deck_builder_screen()
	create_victory_screen()
	create_defeat_screen()

func create_menu_screen():
	var menu = Control.new()
	menu.name = MENU_SCREEN
	menu.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	menu.visible = false
	
	# Background
	var bg = ColorRect.new()
	bg.color = Color("#2C1810")
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	menu.add_child(bg)
	
	# Title
	var title = Label.new()
	title.text = "SANDS OF DUAT"
	title.add_theme_font_size_override("font_size", 48)
	title.add_theme_color_override("font_color", Color("#DAA520"))
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.position = Vector2(get_viewport().size.x / 2 - 200, 150)
	menu.add_child(title)
	
	# Subtitle
	var subtitle = Label.new()
	subtitle.text = "Egyptian Card Combat Adventure"
	subtitle.add_theme_font_size_override("font_size", 20)
	subtitle.add_theme_color_override("font_color", Color("#CD853F"))
	subtitle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	subtitle.position = Vector2(get_viewport().size.x / 2 - 150, 220)
	menu.add_child(subtitle)
	
	# Menu buttons
	var button_container = VBoxContainer.new()
	button_container.position = Vector2(get_viewport().size.x / 2 - 100, 300)
	menu.add_child(button_container)
	
	var start_button = Button.new()
	start_button.text = "Start Adventure"
	start_button.custom_minimum_size = Vector2(200, 50)
	start_button.pressed.connect(func(): state_change_requested.emit(GameManager.GameState.MAP))
	button_container.add_child(start_button)
	
	var deck_button = Button.new()
	deck_button.text = "Deck Builder"
	deck_button.custom_minimum_size = Vector2(200, 50)
	deck_button.pressed.connect(func(): state_change_requested.emit(GameManager.GameState.DECK_BUILDER))
	button_container.add_child(deck_button)
	
	var quit_button = Button.new()
	quit_button.text = "Quit Game"
	quit_button.custom_minimum_size = Vector2(200, 50)
	quit_button.pressed.connect(func(): get_tree().quit())
	button_container.add_child(quit_button)
	
	screens[MENU_SCREEN] = menu
	main_container.add_child(menu)

func create_combat_screen():
	var combat = Control.new()
	combat.name = COMBAT_SCREEN
	combat.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	combat.visible = false
	
	# Background
	var bg = ColorRect.new()
	bg.color = Color("#2C1810")
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	combat.add_child(bg)
	
	# Player area
	var player_area = Control.new()
	player_area.name = "PlayerArea"
	player_area.position = Vector2(50, 400)
	player_area.size = Vector2(300, 200)
	combat.add_child(player_area)
	
	# Enemy area
	var enemy_area = Control.new()
	enemy_area.name = "EnemyArea"
	enemy_area.position = Vector2(600, 200)
	enemy_area.size = Vector2(300, 200)
	combat.add_child(enemy_area)
	
	# Hand area
	var hand_area = Control.new()
	hand_area.name = "HandArea"
	hand_area.position = Vector2(100, get_viewport().size.y - 180)
	hand_area.size = Vector2(get_viewport().size.x - 200, 160)
	combat.add_child(hand_area)
	
	# End turn button
	var end_turn_button = Button.new()
	end_turn_button.name = "EndTurnButton"
	end_turn_button.text = "End Turn"
	end_turn_button.position = Vector2(get_viewport().size.x - 150, get_viewport().size.y - 60)
	end_turn_button.size = Vector2(120, 40)
	combat.add_child(end_turn_button)
	
	screens[COMBAT_SCREEN] = combat
	main_container.add_child(combat)

func create_map_screen():
	var map = Control.new()
	map.name = MAP_SCREEN
	map.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	map.visible = false
	
	# Background
	var bg = ColorRect.new()
	bg.color = Color("#8B4513")
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	map.add_child(bg)
	
	# Title
	var title = Label.new()
	title.text = "Desert Map"
	title.add_theme_font_size_override("font_size", 36)
	title.position = Vector2(50, 50)
	map.add_child(title)
	
	# Combat button
	var combat_button = Button.new()
	combat_button.text = "Enter Combat"
	combat_button.position = Vector2(200, 200)
	combat_button.size = Vector2(150, 50)
	combat_button.pressed.connect(func(): state_change_requested.emit(GameManager.GameState.COMBAT))
	map.add_child(combat_button)
	
	screens[MAP_SCREEN] = map
	main_container.add_child(map)

func create_deck_builder_screen():
	var deck_builder = Control.new()
	deck_builder.name = DECK_BUILDER_SCREEN
	deck_builder.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	deck_builder.visible = false
	
	# Background
	var bg = ColorRect.new()
	bg.color = Color("#2C1810")
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	deck_builder.add_child(bg)
	
	# Title
	var title = Label.new()
	title.text = "Deck Builder"
	title.add_theme_font_size_override("font_size", 36)
	title.position = Vector2(50, 50)
	deck_builder.add_child(title)
	
	# Collection area
	var collection_scroll = ScrollContainer.new()
	collection_scroll.name = "CollectionScroll"
	collection_scroll.position = Vector2(50, 120)
	collection_scroll.size = Vector2(400, 400)
	deck_builder.add_child(collection_scroll)
	
	var collection_grid = GridContainer.new()
	collection_grid.name = "CollectionGrid"
	collection_grid.columns = 3
	collection_scroll.add_child(collection_grid)
	
	# Deck area
	var deck_scroll = ScrollContainer.new()
	deck_scroll.name = "DeckScroll"
	deck_scroll.position = Vector2(500, 120)
	deck_scroll.size = Vector2(400, 400)
	deck_builder.add_child(deck_scroll)
	
	var deck_grid = GridContainer.new()
	deck_grid.name = "DeckGrid"
	deck_grid.columns = 3
	deck_scroll.add_child(deck_grid)
	
	# Back button
	var back_button = Button.new()
	back_button.text = "Back to Menu"
	back_button.position = Vector2(50, get_viewport().size.y - 100)
	back_button.pressed.connect(func(): state_change_requested.emit(GameManager.GameState.MENU))
	deck_builder.add_child(back_button)
	
	screens[DECK_BUILDER_SCREEN] = deck_builder
	main_container.add_child(deck_builder)

func create_victory_screen():
	var victory = create_result_screen("VICTORY!", Color.GREEN, func(): state_change_requested.emit(GameManager.GameState.MAP))
	victory.name = VICTORY_SCREEN
	screens[VICTORY_SCREEN] = victory
	main_container.add_child(victory)

func create_defeat_screen():
	var defeat = create_result_screen("DEFEAT", Color.RED, func(): state_change_requested.emit(GameManager.GameState.MENU))
	defeat.name = DEFEAT_SCREEN
	screens[DEFEAT_SCREEN] = defeat
	main_container.add_child(defeat)

func create_result_screen(result_text: String, color: Color, continue_callback: Callable) -> Control:
	var screen = Control.new()
	screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	screen.visible = false
	
	# Semi-transparent background
	var bg = ColorRect.new()
	bg.color = Color(0, 0, 0, 0.7)
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	screen.add_child(bg)
	
	# Result panel
	var panel = Panel.new()
	panel.position = Vector2(get_viewport().size.x / 2 - 200, get_viewport().size.y / 2 - 150)
	panel.size = Vector2(400, 300)
	screen.add_child(panel)
	
	# Result text
	var title = Label.new()
	title.text = result_text
	title.add_theme_font_size_override("font_size", 48)
	title.add_theme_color_override("font_color", color)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.position = Vector2(0, 50)
	title.size = Vector2(400, 60)
	panel.add_child(title)
	
	# Continue button
	var continue_button = Button.new()
	continue_button.text = "Continue"
	continue_button.position = Vector2(150, 200)
	continue_button.size = Vector2(100, 40)
	continue_button.pressed.connect(continue_callback)
	panel.add_child(continue_button)
	
	return screen

# Screen management
func show_screen(screen_name: String):
	# Hide current screen
	if current_screen:
		current_screen.visible = false
	
	# Show new screen
	if screen_name in screens:
		current_screen = screens[screen_name]
		current_screen.visible = true
		print("UIManager: Showing screen %s" % screen_name)
	else:
		print("UIManager: Screen %s not found" % screen_name)

func show_menu_screen():
	show_screen(MENU_SCREEN)

func show_combat_screen():
	show_screen(COMBAT_SCREEN)
	# Additional combat screen setup would go here

func show_map_screen():
	show_screen(MAP_SCREEN)

func show_deck_builder(collection: Array[Card] = [], deck: Array[Card] = []):
	show_screen(DECK_BUILDER_SCREEN)
	populate_deck_builder(collection, deck)

func show_victory_screen():
	show_screen(VICTORY_SCREEN)

func show_defeat_screen():
	show_screen(DEFEAT_SCREEN)

# Update HUD elements
func update_sand_display(current: int, max_sand: int):
	var sand_label = hud.get_node("SandLabel")
	if sand_label:
		sand_label.text = "%d/%d" % [current, max_sand]

func update_hour_display(current_hour: int, max_hours: int):
	var hour_label = hud.get_node("HourLabel")
	if hour_label:
		hour_label.text = "Hour %d/%d" % [current_hour, max_hours]

# Deck builder functionality
func populate_deck_builder(collection: Array[Card], deck: Array[Card]):
	var collection_grid = screens[DECK_BUILDER_SCREEN].get_node("CollectionScroll/CollectionGrid")
	var deck_grid = screens[DECK_BUILDER_SCREEN].get_node("DeckScroll/DeckGrid")
	
	# Clear existing cards
	for child in collection_grid.get_children():
		child.queue_free()
	for child in deck_grid.get_children():
		child.queue_free()
	
	# Populate collection
	for card in collection:
		var card_visual = create_deck_builder_card(card, true)
		collection_grid.add_child(card_visual)
	
	# Populate deck
	for card in deck:
		var card_visual = create_deck_builder_card(card, false)
		deck_grid.add_child(card_visual)

func create_deck_builder_card(card: Card, is_collection: bool) -> Control:
	var card_container = Control.new()
	card_container.custom_minimum_size = Vector2(120, 160)
	
	# Card background
	var bg = ColorRect.new()
	bg.color = Color.WHITE
	bg.size = Vector2(120, 160)
	card_container.add_child(bg)
	
	# Card image
	if card.texture:
		var image = TextureRect.new()
		image.texture = card.texture
		image.size = Vector2(120, 120)
		image.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
		card_container.add_child(image)
	
	# Card name
	var name_label = Label.new()
	name_label.text = card.name
	name_label.position = Vector2(5, 125)
	name_label.size = Vector2(110, 20)
	name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_label.add_theme_font_size_override("font_size", 10)
	card_container.add_child(name_label)
	
	# Cost
	var cost_label = Label.new()
	cost_label.text = str(card.sand_cost)
	cost_label.position = Vector2(100, 5)
	cost_label.size = Vector2(15, 15)
	cost_label.add_theme_font_size_override("font_size", 12)
	cost_label.add_theme_color_override("font_color", Color.BLUE)
	card_container.add_child(cost_label)
	
	return card_container

# Tooltip system
func show_tooltip(text: String, position: Vector2):
	# Implementation for tooltip display
	pass

func hide_tooltip():
	# Implementation for tooltip hiding
	pass