extends Node
class_name CombatManager

# Sands of Duat - Combat Manager
# Handles turn-based card combat

signal combat_started
signal combat_ended(victory: bool)
signal turn_started(is_player_turn: bool)
signal turn_ended(is_player_turn: bool)
signal card_played(card: Card)
signal sand_changed(new_amount: int)

enum CombatPhase {
	SETUP,
	PLAYER_TURN,
	ENEMY_TURN,
	ENDED
}

var current_phase: CombatPhase = CombatPhase.SETUP
var turn_number: int = 1

# Combat participants
var player: Character
var enemy: Character
var enemies: Array[Character] = []

# Player resources
var current_sand: int = 3
var max_sand: int = 6
var sand_per_turn: int = 1

# Card management
var deck: Array[Card] = []
var hand: Array[Card] = []
var discard_pile: Array[Card] = []
var exhaust_pile: Array[Card] = []

# Combat settings
var starting_hand_size: int = 5
var cards_per_turn: int = 1
var max_hand_size: int = 10

func _ready():
	setup_combat_manager()

func setup_combat_manager():
	print("CombatManager: Initialized")

func start_combat(player_deck: Array[Card], enemy_character: Character):
	print("CombatManager: Starting combat")
	
	# Setup deck and shuffle
	deck = player_deck.duplicate()
	shuffle_deck()
	
	# Set enemy
	enemy = enemy_character
	enemies = [enemy]
	
	# Reset piles
	hand.clear()
	discard_pile.clear()
	exhaust_pile.clear()
	
	# Reset resources
	current_sand = 3
	
	# Draw starting hand
	draw_cards(starting_hand_size)
	
	# Start combat
	current_phase = CombatPhase.PLAYER_TURN
	turn_number = 1
	
	combat_started.emit()
	start_player_turn()

func start_player_turn():
	print("CombatManager: Player turn %d started" % turn_number)
	current_phase = CombatPhase.PLAYER_TURN
	
	# Gain sand
	gain_sand(sand_per_turn)
	
	# Draw cards
	draw_cards(cards_per_turn)
	
	# Process player status effects
	if player:
		player.process_status_effects()
	
	turn_started.emit(true)

func end_player_turn():
	print("CombatManager: Player turn ended")
	
	# Discard hand
	for card in hand:
		if not card.is_retained:
			discard_pile.append(card)
	hand.clear()
	
	turn_ended.emit(true)
	start_enemy_turn()

func start_enemy_turn():
	print("CombatManager: Enemy turn started")
	current_phase = CombatPhase.ENEMY_TURN
	
	# Process enemy status effects
	for enemy_char in enemies:
		if enemy_char.is_alive():
			enemy_char.process_status_effects()
	
	turn_started.emit(false)
	
	# Execute enemy AI
	await execute_enemy_turn()
	
	end_enemy_turn()

func execute_enemy_turn():
	# Simple enemy AI - just attack the player
	for enemy_char in enemies:
		if enemy_char.is_alive() and player and player.is_alive():
			await perform_enemy_action(enemy_char)

func perform_enemy_action(enemy_char: Character):
	# Simple attack
	enemy_char.attack_animation()
	
	# Wait for animation
	await enemy_char.animation_finished
	
	# Deal damage to player
	if player:
		var damage = 8  # Base enemy damage
		player.take_damage(damage)
		
		# Check if player died
		if not player.is_alive():
			end_combat(false)

func end_enemy_turn():
	print("CombatManager: Enemy turn ended")
	turn_ended.emit(false)
	
	turn_number += 1
	start_player_turn()

func play_card(card: Card, target = null):
	if not can_play_card(card, target):
		print("CombatManager: Cannot play card %s" % card.name)
		return false
	
	print("CombatManager: Playing card %s" % card.name)
	
	# Pay cost
	spend_sand(card.sand_cost)
	
	# Remove from hand
	hand.erase(card)
	
	# Resolve card effects
	var resolved_effects = card.play(player, target)
	
	# Handle card destination
	if card.is_exhausted:
		exhaust_pile.append(card)
	else:
		discard_pile.append(card)
	
	card_played.emit(card)
	
	# Check win condition
	check_combat_end()
	
	return true

func can_play_card(card: Card, target = null) -> bool:
	if current_phase != CombatPhase.PLAYER_TURN:
		return false
	
	return card.can_play(current_sand, target)

func gain_sand(amount: int):
	current_sand = min(current_sand + amount, max_sand)
	sand_changed.emit(current_sand)
	print("CombatManager: Gained %d sand (total: %d)" % [amount, current_sand])

func spend_sand(amount: int) -> bool:
	if current_sand >= amount:
		current_sand -= amount
		sand_changed.emit(current_sand)
		print("CombatManager: Spent %d sand (remaining: %d)" % [amount, current_sand])
		return true
	return false

func draw_cards(count: int):
	for i in count:
		draw_card()

func draw_card():
	# Check if deck is empty, reshuffle discard
	if deck.is_empty():
		if discard_pile.is_empty():
			print("CombatManager: No cards to draw")
			return
		
		# Reshuffle discard into deck
		deck = discard_pile.duplicate()
		discard_pile.clear()
		shuffle_deck()
		print("CombatManager: Reshuffled discard pile into deck")
	
	# Check hand size limit
	if hand.size() >= max_hand_size:
		print("CombatManager: Hand is full, cannot draw")
		return
	
	# Draw top card
	var card = deck.pop_back()
	hand.append(card)
	print("CombatManager: Drew card %s" % card.name)

func shuffle_deck():
	# Simple shuffle algorithm
	for i in range(deck.size() - 1, 0, -1):
		var j = randi() % (i + 1)
		var temp = deck[i]
		deck[i] = deck[j]
		deck[j] = temp
	
	print("CombatManager: Shuffled deck (%d cards)" % deck.size())

func check_combat_end():
	# Check if all enemies are dead
	var all_enemies_dead = true
	for enemy_char in enemies:
		if enemy_char.is_alive():
			all_enemies_dead = false
			break
	
	if all_enemies_dead:
		end_combat(true)
		return
	
	# Check if player is dead
	if player and not player.is_alive():
		end_combat(false)
		return

func end_combat(victory: bool):
	print("CombatManager: Combat ended - %s" % ("Victory" if victory else "Defeat"))
	current_phase = CombatPhase.ENDED
	combat_ended.emit(victory)

# Card effect helpers - called by cards
func heal_player(amount: int):
	if player:
		player.heal(amount)

func damage_enemy(target: Character, amount: int):
	if target and target.is_alive():
		target.take_damage(amount)

func damage_all_enemies(amount: int):
	for enemy_char in enemies:
		if enemy_char.is_alive():
			enemy_char.take_damage(amount)

func gain_block(amount: int):
	if player:
		player.gain_block(amount)

func apply_status_to_enemy(target: Character, status_name: String, duration: int):
	if target:
		target.apply_status(status_name, duration)

func apply_status_to_player(status_name: String, duration: int):
	if player:
		player.apply_status(status_name, duration)

# Card effect queries - called by cards
func get_current_hour() -> int:
	# This would be connected to the game manager
	return 1  # Placeholder

func get_all_enemies() -> Array[Character]:
	return enemies.filter(func(enemy): return enemy.is_alive())

func get_hand_diversity() -> int:
	var types_seen = {}
	for card in hand:
		types_seen[card.card_type] = true
	return types_seen.size()

func get_missing_enemy_health(target: Character) -> int:
	if target:
		return target.get_missing_health()
	return 0

# Getters
func get_current_sand() -> int:
	return current_sand

func get_max_sand() -> int:
	return max_sand

func get_hand() -> Array[Card]:
	return hand.duplicate()

func get_deck_size() -> int:
	return deck.size()

func get_discard_size() -> int:
	return discard_pile.size()

func is_player_turn() -> bool:
	return current_phase == CombatPhase.PLAYER_TURN

func get_turn_number() -> int:
	return turn_number

# Debug functions
func print_combat_state():
	print("=== COMBAT STATE ===")
	print("Phase: %s" % CombatPhase.keys()[current_phase])
	print("Turn: %d" % turn_number)
	print("Sand: %d/%d" % [current_sand, max_sand])
	print("Hand: %d cards" % hand.size())
	print("Deck: %d cards" % deck.size())
	print("Discard: %d cards" % discard_pile.size())
	if player:
		print("Player: %d/%d HP, %d block" % [player.current_health, player.max_health, player.block])
	if enemy:
		print("Enemy: %d/%d HP, %d block" % [enemy.current_health, enemy.max_health, enemy.block])
	print("====================")