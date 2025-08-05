extends Node
class_name SpriteSheetAnimator

# Sands of Duat - SpriteSheet Animator
# Automatically configures AnimatedSprite2D nodes with spritesheet data

static func setup_character_animations(animated_sprite: AnimatedSprite2D, character_name: String):
	if not animated_sprite:
		print("SpriteSheetAnimator: No AnimatedSprite2D provided")
		return
	
	print("SpriteSheetAnimator: Setting up animations for %s" % character_name)
	
	# Create SpriteFrames resource
	var sprite_frames = SpriteFrames.new()
	animated_sprite.sprite_frames = sprite_frames
	
	# Load and configure animations based on available spritesheets
	match character_name.to_lower():
		"player":
			setup_player_animations(sprite_frames)
		"anubis_guardian":
			setup_enemy_animations(sprite_frames, "anubis_guardian")
		"desert_scorpion":
			setup_enemy_animations(sprite_frames, "desert_scorpion")
		"pharaoh_lich":
			setup_enemy_animations(sprite_frames, "pharaoh_lich")
		"temple_guardian":
			setup_enemy_animations(sprite_frames, "temple_guardian")
		_:
			print("Unknown character: %s, using default setup" % character_name)
			setup_default_animations(sprite_frames, character_name)
	
	# Set default animation
	animated_sprite.animation = "idle"
	animated_sprite.play()

static func setup_player_animations(sprite_frames: SpriteFrames):
	# Player has idle, walk, and attack animations
	
	# Idle animation
	var idle_texture = load("res://sprites/player_idle_spritesheet.png")
	if idle_texture:
		create_animation_from_spritesheet(sprite_frames, "idle", idle_texture, 4, 4, 12.0)
	
	# Walk animation
	var walk_texture = load("res://sprites/player_walk_spritesheet.png")
	if walk_texture:
		create_animation_from_spritesheet(sprite_frames, "walk", walk_texture, 4, 4, 12.0)
	
	# Attack animation
	var attack_texture = load("res://sprites/player_attack_spritesheet.png")
	if attack_texture:
		create_animation_from_spritesheet(sprite_frames, "attack", attack_texture, 3, 4, 15.0, false)
	
	print("SpriteSheetAnimator: Player animations configured")

static func setup_enemy_animations(sprite_frames: SpriteFrames, enemy_name: String):
	# Most enemies only have idle animation for now
	var idle_texture = load("res://sprites/%s_idle_spritesheet.png" % enemy_name)
	if idle_texture:
		create_animation_from_spritesheet(sprite_frames, "idle", idle_texture, 3, 4, 8.0)
		
		# Create attack animation by using same spritesheet at different speed
		create_animation_from_spritesheet(sprite_frames, "attack", idle_texture, 3, 4, 12.0, false)
		
		# Create hurt animation (subset of idle)
		create_animation_from_spritesheet(sprite_frames, "hurt", idle_texture, 2, 4, 15.0, false)
	
	print("SpriteSheetAnimator: %s animations configured" % enemy_name)

static func setup_default_animations(sprite_frames: SpriteFrames, character_name: String):
	# Try to load any available spritesheet for this character
	var possible_files = [
		"res://sprites/%s_idle_spritesheet.png" % character_name,
		"res://sprites/%s_spritesheet.png" % character_name,
		"res://characters/%s.png" % character_name
	]
	
	for file_path in possible_files:
		var texture = load(file_path)
		if texture:
			create_animation_from_spritesheet(sprite_frames, "idle", texture, 4, 4, 10.0)
			print("SpriteSheetAnimator: Default animation configured for %s" % character_name)
			return
	
	print("SpriteSheetAnimator: No spritesheet found for %s" % character_name)

static func create_animation_from_spritesheet(
	sprite_frames: SpriteFrames, 
	animation_name: String, 
	texture: Texture2D, 
	rows: int, 
	cols: int, 
	fps: float, 
	loop: bool = true
):
	if not texture:
		print("SpriteSheetAnimator: No texture provided for animation %s" % animation_name)
		return
	
	# Add animation to SpriteFrames
	sprite_frames.add_animation(animation_name)
	sprite_frames.set_animation_speed(animation_name, fps)
	sprite_frames.set_animation_loop(animation_name, loop)
	
	# Calculate frame dimensions
	var texture_size = texture.get_size()
	var frame_width = texture_size.x / cols
	var frame_height = texture_size.y / rows
	
	# Create frames from spritesheet
	var frame_count = 0
	for row in rows:
		for col in cols:
			var atlas_texture = AtlasTexture.new()
			atlas_texture.atlas = texture
			atlas_texture.region = Rect2(
				col * frame_width,
				row * frame_height,
				frame_width,
				frame_height
			)
			
			sprite_frames.add_frame(animation_name, atlas_texture)
			frame_count += 1
	
	print("SpriteSheetAnimator: Created animation '%s' with %d frames at %.1f fps" % [animation_name, frame_count, fps])

static func load_spritesheet_metadata(spritesheet_path: String) -> Dictionary:
	var metadata_path = spritesheet_path.replace(".png", "_metadata.json")
	
	if not FileAccess.file_exists(metadata_path):
		print("SpriteSheetAnimator: No metadata found at %s" % metadata_path)
		return {}
	
	var file = FileAccess.open(metadata_path, FileAccess.READ)
	if not file:
		print("SpriteSheetAnimator: Could not open metadata file %s" % metadata_path)
		return {}
	
	var json_string = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	var parse_result = json.parse(json_string)
	
	if parse_result != OK:
		print("SpriteSheetAnimator: Failed to parse metadata JSON")
		return {}
	
	return json.data

static func create_animation_from_metadata(sprite_frames: SpriteFrames, animation_name: String, texture: Texture2D, metadata: Dictionary):
	var rows = metadata.get("rows", 4)
	var cols = metadata.get("cols", 4)
	var fps = metadata.get("fps", 12.0)
	
	create_animation_from_spritesheet(sprite_frames, animation_name, texture, rows, cols, fps)

# Utility function to setup a character with animations
static func setup_character_with_metadata(character: Character):
	var animated_sprite = character.get_node("AnimatedSprite2D")
	if not animated_sprite:
		print("SpriteSheetAnimator: No AnimatedSprite2D found in character")
		return
	
	setup_character_animations(animated_sprite, character.character_name)