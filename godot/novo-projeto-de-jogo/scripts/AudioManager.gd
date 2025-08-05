extends Node
class_name AudioManager

# Sands of Duat - Audio Manager
# Handles music and sound effects

# Audio players
var music_player: AudioStreamPlayer
var sfx_player: AudioStreamPlayer
var ui_player: AudioStreamPlayer

# Audio settings
var master_volume: float = 1.0
var music_volume: float = 0.7
var sfx_volume: float = 0.8

# Current state
var current_music: String = ""
var is_music_playing: bool = false

func _ready():
	setup_audio_players()
	load_audio_settings()

func setup_audio_players():
	# Music player
	music_player = AudioStreamPlayer.new()
	music_player.name = "MusicPlayer"
	music_player.bus = "Music"
	add_child(music_player)
	
	# SFX player
	sfx_player = AudioStreamPlayer.new()
	sfx_player.name = "SFXPlayer"
	sfx_player.bus = "SFX"
	add_child(sfx_player)
	
	# UI player
	ui_player = AudioStreamPlayer.new()
	ui_player.name = "UIPlayer"
	ui_player.bus = "UI"
	add_child(ui_player)
	
	print("AudioManager: Audio players initialized")

func load_audio_settings():
	# Load settings from user preferences
	# For now, use defaults
	apply_volume_settings()

func apply_volume_settings():
	# Apply volume to audio buses
	var master_bus = AudioServer.get_bus_index("Master")
	var music_bus = AudioServer.get_bus_index("Music")
	var sfx_bus = AudioServer.get_bus_index("SFX")
	var ui_bus = AudioServer.get_bus_index("UI")
	
	AudioServer.set_bus_volume_db(master_bus, linear_to_db(master_volume))
	
	if music_bus >= 0:
		AudioServer.set_bus_volume_db(music_bus, linear_to_db(music_volume))
	
	if sfx_bus >= 0:
		AudioServer.set_bus_volume_db(sfx_bus, linear_to_db(sfx_volume))
	
	if ui_bus >= 0:
		AudioServer.set_bus_volume_db(ui_bus, linear_to_db(sfx_volume))

# Music functions
func play_music(track_name: String, fade_in: bool = true):
	if current_music == track_name and is_music_playing:
		return
	
	var music_path = get_music_path(track_name)
	var audio_stream = load(music_path)
	
	if not audio_stream:
		print("AudioManager: Music not found: %s" % track_name)
		return
	
	if fade_in and is_music_playing:
		fade_out_music()
		await get_tree().create_timer(0.5).timeout
	
	music_player.stream = audio_stream
	music_player.play()
	
	current_music = track_name
	is_music_playing = true
	
	if fade_in:
		fade_in_music()
	
	print("AudioManager: Playing music: %s" % track_name)

func stop_music(fade_out: bool = true):
	if not is_music_playing:
		return
	
	if fade_out:
		fade_out_music()
		await get_tree().create_timer(0.5).timeout
	
	music_player.stop()
	current_music = ""
	is_music_playing = false
	
	print("AudioManager: Music stopped")

func fade_in_music():
	var tween = create_tween()
	music_player.volume_db = -60
	tween.tween_property(music_player, "volume_db", 0, 0.5)

func fade_out_music():
	var tween = create_tween()
	tween.tween_property(music_player, "volume_db", -60, 0.5)

# Sound effects
func play_sound(sound_name: String):
	var sound_path = get_sound_path(sound_name)
	var audio_stream = load(sound_path)
	
	if not audio_stream:
		print("AudioManager: Sound not found: %s" % sound_name)
		return
	
	sfx_player.stream = audio_stream
	sfx_player.play()
	
	print("AudioManager: Playing sound: %s" % sound_name)

func play_ui_sound(sound_name: String):
	var sound_path = get_ui_sound_path(sound_name)
	var audio_stream = load(sound_path)
	
	if not audio_stream:
		print("AudioManager: UI sound not found: %s" % sound_name)
		return
	
	ui_player.stream = audio_stream
	ui_player.play()

# Path helpers
func get_music_path(track_name: String) -> String:
	match track_name:
		"menu_theme":
			return "res://audio/music/menu_theme.ogg"
		"combat_theme":
			return "res://audio/music/combat_theme.ogg"
		"exploration_theme":
			return "res://audio/music/exploration_theme.ogg"
		"victory_theme":
			return "res://audio/music/victory_theme.ogg"
		"boss_theme":
			return "res://audio/music/boss_theme.ogg"
		_:
			return "res://audio/music/default.ogg"

func get_sound_path(sound_name: String) -> String:
	match sound_name:
		"card_play":
			return "res://audio/sfx/card_play.ogg"
		"card_draw":
			return "res://audio/sfx/card_draw.ogg"
		"damage":
			return "res://audio/sfx/damage.ogg"
		"heal":
			return "res://audio/sfx/heal.ogg"
		"block":
			return "res://audio/sfx/block.ogg"
		"victory":
			return "res://audio/sfx/victory.ogg"
		"defeat":
			return "res://audio/sfx/defeat.ogg"
		"enemy_attack":
			return "res://audio/sfx/enemy_attack.ogg"
		"sand_gain":
			return "res://audio/sfx/sand_gain.ogg"
		_:
			return "res://audio/sfx/default.ogg"

func get_ui_sound_path(sound_name: String) -> String:
	match sound_name:
		"button_click":
			return "res://audio/ui/button_click.ogg"
		"button_hover":
			return "res://audio/ui/button_hover.ogg"
		"menu_open":
			return "res://audio/ui/menu_open.ogg"
		"menu_close":
			return "res://audio/ui/menu_close.ogg"
		_:
			return "res://audio/ui/default.ogg"

# Volume controls
func set_master_volume(volume: float):
	master_volume = clamp(volume, 0.0, 1.0)
	apply_volume_settings()

func set_music_volume(volume: float):
	music_volume = clamp(volume, 0.0, 1.0)
	apply_volume_settings()

func set_sfx_volume(volume: float):
	sfx_volume = clamp(volume, 0.0, 1.0)
	apply_volume_settings()

# Getters
func get_master_volume() -> float:
	return master_volume

func get_music_volume() -> float:
	return music_volume

func get_sfx_volume() -> float:
	return sfx_volume

func is_music_muted() -> bool:
	return music_volume <= 0.0

func is_sfx_muted() -> bool:
	return sfx_volume <= 0.0

# Save/Load settings
func save_audio_settings():
	var config = ConfigFile.new()
	config.set_value("audio", "master_volume", master_volume)
	config.set_value("audio", "music_volume", music_volume)
	config.set_value("audio", "sfx_volume", sfx_volume)
	config.save("user://audio_settings.cfg")

func load_audio_settings_from_file():
	var config = ConfigFile.new()
	var err = config.load("user://audio_settings.cfg")
	
	if err != OK:
		print("AudioManager: No audio settings file found, using defaults")
		return
	
	master_volume = config.get_value("audio", "master_volume", 1.0)
	music_volume = config.get_value("audio", "music_volume", 0.7)
	sfx_volume = config.get_value("audio", "sfx_volume", 0.8)
	
	apply_volume_settings()
	print("AudioManager: Audio settings loaded")