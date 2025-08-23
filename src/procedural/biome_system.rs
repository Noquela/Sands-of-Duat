use bevy::prelude::*;
use bevy::audio::Volume;
use super::room_types::BiomeType;

#[derive(Resource)]
pub struct BiomeAssets {
    // Desert biome
    pub desert_floor_texture: Handle<Image>,
    pub desert_wall_texture: Handle<Image>,
    pub desert_ambient_music: Handle<AudioSource>,
    pub sand_dune_model: Handle<Scene>,
    pub palm_tree_model: Handle<Scene>,
    pub desert_ruins_model: Handle<Scene>,
    
    // Temple biome
    pub temple_floor_texture: Handle<Image>,
    pub temple_wall_texture: Handle<Image>,
    pub temple_ambient_music: Handle<AudioSource>,
    pub pillar_model: Handle<Scene>,
    pub hieroglyph_wall_model: Handle<Scene>,
    pub altar_model: Handle<Scene>,
    
    // Underworld biome
    pub underworld_floor_texture: Handle<Image>,
    pub underworld_wall_texture: Handle<Image>,
    pub underworld_ambient_music: Handle<AudioSource>,
    pub bone_pile_model: Handle<Scene>,
    pub soul_crystal_model: Handle<Scene>,
    pub shadow_portal_model: Handle<Scene>,
}

#[derive(Resource)]
pub struct CurrentBiomeSettings {
    pub biome_type: BiomeType,
    pub ambient_light: Color,
    pub fog_color: Color,
    pub fog_density: f32,
    pub particle_system: Option<Entity>,
    pub music_volume: f32,
    pub transition_progress: f32, // 0.0 to 1.0 for smooth transitions
}

impl Default for CurrentBiomeSettings {
    fn default() -> Self {
        Self {
            biome_type: BiomeType::Desert,
            ambient_light: Color::rgb(1.0, 0.9, 0.6),
            fog_color: Color::rgb(0.9, 0.8, 0.6),
            fog_density: 0.02,
            particle_system: None,
            music_volume: 0.3,
            transition_progress: 1.0,
        }
    }
}

#[derive(Component)]
pub struct BiomeEnvironment {
    pub biome_type: BiomeType,
}

#[derive(Component)]
pub struct BiomeParticleSystem;

#[derive(Component)]
pub struct BiomeDecoration {
    pub decoration_type: String,
}

#[derive(Event)]
pub struct BiomeTransitionEvent {
    pub from_biome: BiomeType,
    pub to_biome: BiomeType,
    pub transition_duration: f32,
}

pub struct BiomeSystemPlugin;

impl Plugin for BiomeSystemPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<CurrentBiomeSettings>()
            .add_event::<BiomeTransitionEvent>()
            .add_systems(Startup, load_biome_assets)
            .add_systems(Update, (
                handle_biome_transitions,
                update_biome_lighting,
                manage_biome_particles,
                update_ambient_audio,
                spawn_biome_decorations,
            ));
    }
}

fn load_biome_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("🎨 Loading biome assets...");
    
    let biome_assets = BiomeAssets {
        // Desert assets
        desert_floor_texture: asset_server.load("textures/biomes/desert_sand_floor.png"),
        desert_wall_texture: asset_server.load("textures/biomes/desert_sandstone_wall.png"),
        desert_ambient_music: asset_server.load("audio/ambient/desert_winds.ogg"),
        sand_dune_model: asset_server.load("models/environment/sand_dune.glb#Scene0"),
        palm_tree_model: asset_server.load("models/environment/desert_palm.glb#Scene0"),
        desert_ruins_model: asset_server.load("models/environment/desert_ruins.glb#Scene0"),
        
        // Temple assets
        temple_floor_texture: asset_server.load("textures/biomes/temple_marble_floor.png"),
        temple_wall_texture: asset_server.load("textures/biomes/temple_hieroglyph_wall.png"),
        temple_ambient_music: asset_server.load("audio/ambient/temple_echoes.ogg"),
        pillar_model: asset_server.load("models/environment/egyptian_pillar.glb#Scene0"),
        hieroglyph_wall_model: asset_server.load("models/environment/hieroglyph_wall.glb#Scene0"),
        altar_model: asset_server.load("models/environment/sacrifice_altar.glb#Scene0"),
        
        // Underworld assets
        underworld_floor_texture: asset_server.load("textures/biomes/underworld_bone_floor.png"),
        underworld_wall_texture: asset_server.load("textures/biomes/underworld_shadow_wall.png"),
        underworld_ambient_music: asset_server.load("audio/ambient/underworld_whispers.ogg"),
        bone_pile_model: asset_server.load("models/environment/bone_pile.glb#Scene0"),
        soul_crystal_model: asset_server.load("models/environment/soul_crystal.glb#Scene0"),
        shadow_portal_model: asset_server.load("models/environment/shadow_portal.glb#Scene0"),
    };
    
    commands.insert_resource(biome_assets);
    info!("✅ Biome assets loaded");
}

fn handle_biome_transitions(
    mut commands: Commands,
    mut transition_events: EventReader<BiomeTransitionEvent>,
    mut biome_settings: ResMut<CurrentBiomeSettings>,
    time: Res<Time>,
    existing_env_query: Query<Entity, With<BiomeEnvironment>>,
    biome_assets: Res<BiomeAssets>,
) {
    for event in transition_events.read() {
        info!("🌍 Starting biome transition: {} -> {}", 
              event.from_biome.get_display_name(),
              event.to_biome.get_display_name());
        
        // Clean up existing biome environment
        for entity in existing_env_query.iter() {
            commands.entity(entity).despawn_recursive();
        }
        
        // Update settings for new biome
        apply_biome_settings(&mut biome_settings, event.to_biome);
        
        // Start transition animation
        biome_settings.transition_progress = 0.0;
        
        // Spawn new biome environment
        spawn_biome_environment(&mut commands, event.to_biome, &biome_assets);
    }
    
    // Update transition progress
    if biome_settings.transition_progress < 1.0 {
        biome_settings.transition_progress += time.delta_seconds() * 2.0; // 0.5 second transition
        biome_settings.transition_progress = biome_settings.transition_progress.min(1.0);
    }
}

fn apply_biome_settings(settings: &mut CurrentBiomeSettings, biome: BiomeType) {
    settings.biome_type = biome;
    
    match biome {
        BiomeType::Desert => {
            settings.ambient_light = Color::rgb(1.0, 0.9, 0.6);
            settings.fog_color = Color::rgb(0.9, 0.8, 0.6);
            settings.fog_density = 0.02;
        },
        BiomeType::Temple => {
            settings.ambient_light = Color::rgb(0.8, 0.7, 0.5);
            settings.fog_color = Color::rgb(0.7, 0.6, 0.4);
            settings.fog_density = 0.015;
        },
        BiomeType::Underworld => {
            settings.ambient_light = Color::rgb(0.4, 0.3, 0.6);
            settings.fog_color = Color::rgb(0.3, 0.2, 0.4);
            settings.fog_density = 0.04;
        },
    }
}

fn spawn_biome_environment(
    commands: &mut Commands,
    biome: BiomeType,
    biome_assets: &BiomeAssets,
) {
    let environment_entity = commands.spawn((
        BiomeEnvironment { biome_type: biome },
        Transform::from_translation(Vec3::ZERO),
        GlobalTransform::default(),
        Name::new(format!("{} Environment", biome.get_display_name())),
    )).id();
    
    // Spawn biome-specific decorations
    commands.entity(environment_entity).with_children(|parent| {
        match biome {
            BiomeType::Desert => spawn_desert_decorations(parent, biome_assets),
            BiomeType::Temple => spawn_temple_decorations(parent, biome_assets),
            BiomeType::Underworld => spawn_underworld_decorations(parent, biome_assets),
        }
    });
    
    info!("🏗️ Spawned {} environment", biome.get_display_name());
}

fn spawn_desert_decorations(parent: &mut ChildBuilder, biome_assets: &BiomeAssets) {
    // Sand dunes
    for i in 0..5 {
        let angle = (i as f32 / 5.0) * std::f32::consts::TAU;
        let radius = 15.0 + (i as f32 * 2.0);
        let position = Vec3::new(
            angle.cos() * radius,
            0.0,
            angle.sin() * radius,
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.sand_dune_model.clone(),
                transform: Transform::from_translation(position)
                    .with_rotation(Quat::from_rotation_y(angle))
                    .with_scale(Vec3::splat(0.8 + (i as f32 * 0.1))),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "sand_dune".to_string(),
            },
            Name::new(format!("Sand Dune {}", i + 1)),
        ));
    }
    
    // Palm trees (sparse)
    for i in 0..3 {
        let position = Vec3::new(
            (i as f32 - 1.0) * 8.0,
            0.0,
            12.0 + (i as f32 * 3.0),
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.palm_tree_model.clone(),
                transform: Transform::from_translation(position),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "palm_tree".to_string(),
            },
            Name::new(format!("Palm Tree {}", i + 1)),
        ));
    }
    
    // Ancient ruins
    parent.spawn((
        SceneBundle {
            scene: biome_assets.desert_ruins_model.clone(),
            transform: Transform::from_translation(Vec3::new(-10.0, 0.0, -8.0))
                .with_rotation(Quat::from_rotation_y(0.7)),
            ..default()
        },
        BiomeDecoration {
            decoration_type: "ruins".to_string(),
        },
        Name::new("Desert Ruins"),
    ));
}

fn spawn_temple_decorations(parent: &mut ChildBuilder, biome_assets: &BiomeAssets) {
    // Pillars around the room
    for i in 0..8 {
        let angle = (i as f32 / 8.0) * std::f32::consts::TAU;
        let radius = 12.0;
        let position = Vec3::new(
            angle.cos() * radius,
            0.0,
            angle.sin() * radius,
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.pillar_model.clone(),
                transform: Transform::from_translation(position),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "pillar".to_string(),
            },
            Name::new(format!("Temple Pillar {}", i + 1)),
        ));
    }
    
    // Central altar
    parent.spawn((
        SceneBundle {
            scene: biome_assets.altar_model.clone(),
            transform: Transform::from_translation(Vec3::new(0.0, 0.0, 0.0)),
            ..default()
        },
        BiomeDecoration {
            decoration_type: "altar".to_string(),
        },
        Name::new("Temple Altar"),
    ));
    
    // Hieroglyph walls
    for i in 0..4 {
        let angle = (i as f32 / 4.0) * std::f32::consts::TAU;
        let radius = 18.0;
        let position = Vec3::new(
            angle.cos() * radius,
            0.0,
            angle.sin() * radius,
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.hieroglyph_wall_model.clone(),
                transform: Transform::from_translation(position)
                    .with_rotation(Quat::from_rotation_y(angle + std::f32::consts::PI)),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "hieroglyph_wall".to_string(),
            },
            Name::new(format!("Hieroglyph Wall {}", i + 1)),
        ));
    }
}

fn spawn_underworld_decorations(parent: &mut ChildBuilder, biome_assets: &BiomeAssets) {
    // Bone piles scattered around
    for i in 0..12 {
        let angle = (i as f32 / 12.0) * std::f32::consts::TAU;
        let radius = 8.0 + (i as f32 % 3.0) * 4.0;
        let position = Vec3::new(
            angle.cos() * radius,
            0.0,
            angle.sin() * radius,
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.bone_pile_model.clone(),
                transform: Transform::from_translation(position)
                    .with_rotation(Quat::from_rotation_y(angle * 1.7))
                    .with_scale(Vec3::splat(0.5 + ((i % 4) as f32 * 0.25))),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "bone_pile".to_string(),
            },
            Name::new(format!("Bone Pile {}", i + 1)),
        ));
    }
    
    // Soul crystals (glowing)
    for i in 0..6 {
        let angle = (i as f32 / 6.0) * std::f32::consts::TAU;
        let radius = 15.0;
        let position = Vec3::new(
            angle.cos() * radius,
            2.0,
            angle.sin() * radius,
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.soul_crystal_model.clone(),
                transform: Transform::from_translation(position),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "soul_crystal".to_string(),
            },
            Name::new(format!("Soul Crystal {}", i + 1)),
        ));
    }
    
    // Shadow portals
    for i in 0..2 {
        let position = Vec3::new(
            if i == 0 { -12.0 } else { 12.0 },
            0.0,
            if i == 0 { 8.0 } else { -8.0 },
        );
        
        parent.spawn((
            SceneBundle {
                scene: biome_assets.shadow_portal_model.clone(),
                transform: Transform::from_translation(position),
                ..default()
            },
            BiomeDecoration {
                decoration_type: "shadow_portal".to_string(),
            },
            Name::new(format!("Shadow Portal {}", i + 1)),
        ));
    }
}

fn update_biome_lighting(
    biome_settings: Res<CurrentBiomeSettings>,
    mut ambient_light: ResMut<AmbientLight>,
) {
    if biome_settings.is_changed() || biome_settings.transition_progress < 1.0 {
        let progress = biome_settings.transition_progress;
        
        // Smooth ambient light transition
        ambient_light.color = biome_settings.ambient_light;
        ambient_light.brightness = 0.3 + (progress * 0.7);
        
        // Note: Fog settings would be handled by a separate fog system
        // if available in this version of Bevy
    }
}

fn manage_biome_particles(
    mut commands: Commands,
    biome_settings: Res<CurrentBiomeSettings>,
    existing_particles: Query<Entity, With<BiomeParticleSystem>>,
) {
    if biome_settings.is_changed() && biome_settings.transition_progress > 0.8 {
        // Clean up old particles
        for entity in existing_particles.iter() {
            commands.entity(entity).despawn_recursive();
        }
        
        // Spawn new particle system based on biome
        let particle_entity = match biome_settings.biome_type {
            BiomeType::Desert => {
                // Sand particles
                commands.spawn((
                    BiomeParticleSystem,
                    Transform::from_translation(Vec3::new(0.0, 5.0, 0.0)),
                    GlobalTransform::default(),
                    Name::new("Desert Sand Particles"),
                )).id()
            },
            BiomeType::Temple => {
                // Dust motes in sunbeams
                commands.spawn((
                    BiomeParticleSystem,
                    Transform::from_translation(Vec3::new(0.0, 8.0, 0.0)),
                    GlobalTransform::default(),
                    Name::new("Temple Dust Particles"),
                )).id()
            },
            BiomeType::Underworld => {
                // Floating souls/wisps
                commands.spawn((
                    BiomeParticleSystem,
                    Transform::from_translation(Vec3::new(0.0, 3.0, 0.0)),
                    GlobalTransform::default(),
                    Name::new("Underworld Soul Particles"),
                )).id()
            },
        };
        
        // Note: BiomeType could be added as a marker component if needed
    }
}

fn update_ambient_audio(
    biome_settings: Res<CurrentBiomeSettings>,
    biome_assets: Res<BiomeAssets>,
    mut commands: Commands,
    audio_query: Query<Entity, With<AudioSink>>,
) {
    if biome_settings.is_changed() && biome_settings.transition_progress > 0.5 {
        // Stop existing ambient audio
        for entity in audio_query.iter() {
            commands.entity(entity).despawn();
        }
        
        // Start new ambient audio
        let ambient_source = match biome_settings.biome_type {
            BiomeType::Desert => biome_assets.desert_ambient_music.clone(),
            BiomeType::Temple => biome_assets.temple_ambient_music.clone(),
            BiomeType::Underworld => biome_assets.underworld_ambient_music.clone(),
        };
        
        commands.spawn(AudioBundle {
            source: ambient_source,
            settings: PlaybackSettings::LOOP.with_volume(Volume::new(biome_settings.music_volume)),
        });
    }
}

fn spawn_biome_decorations(
    mut commands: Commands,
    biome_settings: Res<CurrentBiomeSettings>,
    time: Res<Time>,
    mut decoration_query: Query<&mut Transform, With<BiomeDecoration>>,
) {
    // Animate certain decorations
    for mut transform in decoration_query.iter_mut() {
        match biome_settings.biome_type {
            BiomeType::Desert => {
                // Gentle swaying for palm trees
                let sway = (time.elapsed_seconds() * 0.5).sin() * 0.05;
                transform.rotation = Quat::from_rotation_z(sway);
            },
            BiomeType::Temple => {
                // Subtle scaling breathing effect for altar
                let scale = 1.0 + (time.elapsed_seconds() * 1.5).sin() * 0.02;
                if transform.scale.x > 0.99 && transform.scale.x < 1.01 {
                    transform.scale = Vec3::splat(scale);
                }
            },
            BiomeType::Underworld => {
                // Floating motion for soul crystals
                let float_offset = (time.elapsed_seconds() * 2.0).sin() * 0.5;
                if transform.translation.y > 1.5 && transform.translation.y < 3.0 {
                    transform.translation.y = 2.0 + float_offset;
                }
            },
        }
    }
}

// Public API for triggering biome transitions
impl CurrentBiomeSettings {
    pub fn transition_to(&self, new_biome: BiomeType) -> BiomeTransitionEvent {
        BiomeTransitionEvent {
            from_biome: self.biome_type,
            to_biome: new_biome,
            transition_duration: 1.0,
        }
    }
    
    pub fn is_transitioning(&self) -> bool {
        self.transition_progress < 1.0
    }
}