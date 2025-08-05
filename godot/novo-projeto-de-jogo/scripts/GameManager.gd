extends Node

# Sands of Duat - Game Manager
# Main controller for game state, progression, and scene management

signal game_state_changed(new_state)
signal sand_changed(new_amount)
signal hourglass_tick(current_hour)

enum GameState {
	MENU,
	COMBAT,
	MAP,
	DECK_BUILDER,
	VICTORY,
	DEFEAT
}

@export var current_state: GameState = GameState.MENU
@export var max_sand: int = 6
@export var current_sand: int = 3
@export var current_hour: int = 1
@export var max_hours: int = 12

# Game data
var player_deck: Array[Card] = []
var player_collection: Array[Card] = []
var current_enemy: Enemy
var game_progression: Dictionary = {}

# Singletons and managers
var audio_manager: AudioManager
var ui_manager: UIManager
var combat_manager: CombatManager
var card_loader: CardLoader

func _ready():
	print("GameManager: Initializing Sands of Duat")
	setup_managers()
	setup_signals()
	transition_to_state(GameState.MENU)

func setup_managers():
	# Initialize core managers
	audio_manager = AudioManager.new()
	add_child(audio_manager)
	
	ui_manager = UIManager.new()
	add_child(ui_manager)
	
	combat_manager = CombatManager.new()
	add_child(combat_manager)
	
	card_loader = CardLoader.new()
	add_child(card_loader)
	
	print("GameManager: All managers initialized")

func setup_signals():
	# Connect manager signals
	combat_manager.combat_ended.connect(_on_combat_ended)
	combat_manager.sand_changed.connect(_on_sand_changed)
	
	# Connect UI signals
	ui_manager.state_change_requested.connect(transition_to_state)

func transition_to_state(new_state: GameState):
	var old_state = current_state
	current_state = new_state
	
	print("GameManager: State transition: %s -> %s" % [GameState.keys()[old_state], GameState.keys()[new_state]])
	
	match current_state:
		GameState.MENU:
			show_main_menu()
		GameState.COMBAT:
			start_combat()
		GameState.MAP:
			show_map()
		GameState.DECK_BUILDER:
			show_deck_builder()
		GameState.VICTORY:
			show_victory()
		GameState.DEFEAT:
			show_defeat()
	
	game_state_changed.emit(current_state)

func show_main_menu():
	ui_manager.show_menu_screen()
	audio_manager.play_music("menu_theme")

func start_combat():
	if not current_enemy:
		print("GameManager: No enemy set for combat!")
		return
	
	ui_manager.show_combat_screen()
	combat_manager.start_combat(player_deck, current_enemy)
	audio_manager.play_music("combat_theme")

func show_map():
	ui_manager.show_map_screen()
	audio_manager.play_music("exploration_theme")

func show_deck_builder():
	ui_manager.show_deck_builder(player_collection, player_deck)

func show_victory():
	ui_manager.show_victory_screen()
	audio_manager.play_sound("victory")
	advance_progression()

func show_defeat():
	ui_manager.show_defeat_screen()
	audio_manager.play_sound("defeat")

func advance_progression():
	current_hour += 1
	hourglass_tick.emit(current_hour)
	
	if current_hour > max_hours:
		print("GameManager: Game completed!")
		# Handle game completion
	else:
		print("GameManager: Advanced to hour %d" % current_hour)

func add_sand(amount: int):
	current_sand = min(current_sand + amount, max_sand)
	sand_changed.emit(current_sand)

func spend_sand(amount: int) -> bool:
	if current_sand >= amount:
		current_sand -= amount
		sand_changed.emit(current_sand)
		return true
	return false

func set_enemy(enemy: Enemy):
	current_enemy = enemy
	print("GameManager: Enemy set: %s" % enemy.name)

func add_card_to_collection(card: Card):
	if card not in player_collection:
		player_collection.append(card)
		print("GameManager: Added card to collection: %s" % card.name)

func add_card_to_deck(card: Card):
	if card in player_collection and card not in player_deck:
		player_deck.append(card)
		print("GameManager: Added card to deck: %s" % card.name)

func remove_card_from_deck(card: Card):
	if card in player_deck:
		player_deck.erase(card)
		print("GameManager: Removed card from deck: %s" % card.name)

func save_game():
	var save_data = {
		"current_hour": current_hour,
		"current_sand": current_sand,
		"player_deck": serialize_cards(player_deck),
		"player_collection": serialize_cards(player_collection),
		"game_progression": game_progression
	}
	
	var save_file = FileAccess.open("user://savegame.save", FileAccess.WRITE)
	save_file.store_string(JSON.stringify(save_data))
	save_file.close()
	
	print("GameManager: Game saved")

func load_game():
	if not FileAccess.file_exists("user://savegame.save"):
		print("GameManager: No save file found")
		return
	
	var save_file = FileAccess.open("user://savegame.save", FileAccess.READ)
	var save_data = JSON.parse_string(save_file.get_as_text())
	save_file.close()
	
	current_hour = save_data.get("current_hour", 1)
	current_sand = save_data.get("current_sand", 3)
	player_deck = deserialize_cards(save_data.get("player_deck", []))
	player_collection = deserialize_cards(save_data.get("player_collection", []))
	game_progression = save_data.get("game_progression", {})
	
	print("GameManager: Game loaded")

func serialize_cards(cards: Array[Card]) -> Array:
	var serialized = []
	for card in cards:
		serialized.append(card.name)
	return serialized

func deserialize_cards(card_names: Array) -> Array[Card]:
	var cards: Array[Card] = []
	for name in card_names:
		var card = card_loader.get_card_by_name(name)
		if card:
			cards.append(card)
	return cards

# Signal callbacks
func _on_combat_ended(victory: bool):
	if victory:
		transition_to_state(GameState.VICTORY)
	else:
		transition_to_state(GameState.DEFEAT)

func _on_sand_changed(new_amount: int):
	current_sand = new_amount
	sand_changed.emit(current_sand)

# Utility functions
func get_current_state_name() -> String:
	return GameState.keys()[current_state]

func is_game_over() -> bool:
	return current_hour > max_hours

func reset_game():
	current_hour = 1
	current_sand = 3
	player_deck.clear()
	player_collection.clear()
	game_progression.clear()
	transition_to_state(GameState.MENU)
	print("GameManager: Game reset")