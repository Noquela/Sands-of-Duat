/*!
🏺 HADES-STYLE 3D RENDERING SYSTEM
Modern 3D rendering with dramatic lighting and Hades visual style
*/

use bevy::prelude::*;
use bevy::pbr::{DirectionalLightShadowMap, PointLightShadowMap};
use bevy::render::camera::Projection;

#[derive(Component)]
pub struct HadesCharacter {
    pub character_type: String,
    pub health: f32,
    pub max_health: f32,
}

#[derive(Component)]
pub struct MainCharacter;

#[derive(Resource)]
pub struct Hades3DAssets {
    pub pharaoh_hero: Handle<Scene>,
    pub anubis_boss: Handle<Scene>,
    pub mummy_enemy: Handle<Scene>,
    pub isis_npc: Handle<Scene>,
}

pub struct Hades3DPlugin;

impl Plugin for Hades3DPlugin {
    fn build(&self, app: &mut App) {
        app
            .add_systems(Startup, (
                load_3d_assets,
                // setup_3d_camera, // Disabled: Using HadesVisualPolishPlugin camera
                // setup_dramatic_lighting, // Disabled: Using HadesVisualPolishPlugin lighting
            ))
            .add_systems(Update, (
                spawn_pharaoh_hero,
                animate_characters,
                // update_camera_follow, // Disabled: Using HadesVisualPolishPlugin camera
            ));
    }
}

fn load_3d_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading Hades-style 3D assets...");
    
    let assets = Hades3DAssets {
        pharaoh_hero: asset_server.load("3d/hades_quality/pharaoh_hero_hades.glb#Scene0"),
        anubis_boss: asset_server.load("3d/hades_quality/anubis_boss_hades.glb#Scene0"),
        mummy_enemy: asset_server.load("3d/hades_quality/mummy_enemy_hades.glb#Scene0"),
        isis_npc: asset_server.load("3d/hades_quality/isis_npc_hades.glb#Scene0"),
    };
    
    commands.insert_resource(assets);
    info!("3D assets loading initiated");
}

fn setup_3d_camera(mut commands: Commands) {
    info!("Setting up 3D isometric camera...");
    
    // Create isometric-style 3D camera
    commands.spawn((
        Camera3dBundle {
            transform: Transform::from_xyz(10.0, 15.0, 10.0)
                .looking_at(Vec3::ZERO, Vec3::Y),
            projection: Projection::Orthographic(OrthographicProjection {
                scale: 10.0,
                ..default()
            }),
            ..default()
        },
        Name::new("Main 3D Camera"),
    ));
}

fn setup_dramatic_lighting(mut commands: Commands) {
    info!("Setting up Hades-style dramatic lighting...");
    
    // Key light (warm, from above-front)
    commands.spawn((
        DirectionalLightBundle {
            directional_light: DirectionalLight {
                color: Color::rgb(1.0, 0.9, 0.7), // Warm golden
                illuminance: 10000.0,
                shadows_enabled: true,
                ..default()
            },
            transform: Transform::from_xyz(4.0, 8.0, 4.0)
                .looking_at(Vec3::ZERO, Vec3::Y),
            ..default()
        },
        Name::new("Key Light"),
    ));
    
    // Fill light (cooler, from side)
    commands.spawn((
        PointLightBundle {
            point_light: PointLight {
                color: Color::rgb(0.5, 0.7, 1.0), // Cool blue
                intensity: 2000.0,
                range: 20.0,
                shadows_enabled: true,
                ..default()
            },
            transform: Transform::from_xyz(-5.0, 5.0, 5.0),
            ..default()
        },
        Name::new("Fill Light"),
    ));
    
    // Rim light (purple/magenta for mystical feel)
    commands.spawn((
        PointLightBundle {
            point_light: PointLight {
                color: Color::rgb(0.8, 0.3, 0.8), // Mystical purple
                intensity: 1500.0,
                range: 15.0,
                ..default()
            },
            transform: Transform::from_xyz(0.0, 3.0, -8.0),
            ..default()
        },
        Name::new("Rim Light"),
    ));
    
    // Ambient light (very low)
    commands.insert_resource(AmbientLight {
        color: Color::rgb(0.1, 0.1, 0.15),
        brightness: 0.02,
    });
    
    // Configure shadow maps for better quality
    commands.insert_resource(DirectionalLightShadowMap { size: 2048 });
    commands.insert_resource(PointLightShadowMap { size: 1024 });
}

fn spawn_pharaoh_hero(
    mut commands: Commands,
    assets: Res<Hades3DAssets>,
    asset_server: Res<AssetServer>,
    mut spawned: Local<bool>,
) {
    if *spawned {
        return;
    }
    
    // Check if asset is loaded
    let load_state = asset_server.get_load_state(&assets.pharaoh_hero);
    match load_state {
        Some(bevy::asset::LoadState::Loaded) => {
            info!("✅ Pharaoh hero GLB loaded successfully, spawning...");
        }
        Some(bevy::asset::LoadState::Loading) => {
            info!("⏳ Pharaoh hero GLB still loading...");
            return;
        }
        Some(bevy::asset::LoadState::Failed) => {
            info!("❌ Failed to load pharaoh hero GLB!");
            return;
        }
        Some(bevy::asset::LoadState::NotLoaded) => {
            info!("⚠️ Pharaoh hero GLB not loaded yet...");
            return;
        }
        None => {
            info!("⚠️ Pharaoh hero GLB not found in asset server!");
            return;
        }
    }
    
    info!("Spawning pharaoh hero character...");
    
    commands.spawn((
        SceneBundle {
            scene: assets.pharaoh_hero.clone(),
            transform: Transform::from_xyz(0.0, 0.0, 0.0)
                .with_scale(Vec3::splat(2.0)), // Make it bigger so we can see it
            ..default()
        },
        HadesCharacter {
            character_type: "pharaoh_hero".to_string(),
            health: 100.0,
            max_health: 100.0,
        },
        MainCharacter,
        crate::Player, // Make compatible with existing movement system
        crate::Stats {
            max_health: 100.0,
            current_health: 100.0,
            max_stamina: 100.0,
            current_stamina: 100.0,
            speed: 8.0,
            stamina_regen_rate: 50.0,
        },
        crate::Dash::default(),
        crate::Combat::default(), // Add combat component for combat system
        Name::new("Pharaoh Hero"),
    ));
    
    *spawned = true;
    info!("Pharaoh hero spawned successfully");
}

fn animate_characters(
    time: Res<Time>,
    mut query: Query<&mut Transform, With<HadesCharacter>>,
) {
    // Simple breathing/idle animation
    let breathing = (time.elapsed_seconds() * 2.0).sin() * 0.02;
    
    for mut transform in query.iter_mut() {
        // Subtle breathing animation
        let original_scale = 1.0;
        transform.scale.y = original_scale + breathing * 0.1;
        
        // Very slight rotation for life
        transform.rotation = Quat::from_rotation_y((time.elapsed_seconds() * 0.5).sin() * 0.05);
    }
}

/// Spawn Hades-quality 3D enemy
pub fn spawn_hades_enemy(
    commands: &mut Commands,
    assets: &Hades3DAssets,
    enemy_type: crate::EnemyType,
    position: Vec3,
    ai: crate::AI,
    stats: crate::Stats,
) {
    let (scene_handle, character_name) = match enemy_type {
        crate::EnemyType::Chaser => (assets.mummy_enemy.clone(), "mummy_enemy"),
        crate::EnemyType::Shooter => (assets.anubis_boss.clone(), "anubis_boss"),
        crate::EnemyType::Tank => (assets.anubis_boss.clone(), "anubis_boss"),
    };
    
    info!("🔥 Spawning Hades enemy with scene: {:?}", scene_handle);
    commands.spawn((
        SceneBundle {
            scene: scene_handle,
            transform: Transform::from_translation(position)
                .with_scale(Vec3::splat(3.0)), // Make enemies much larger so we can see them
            ..default()
        },
        HadesCharacter {
            character_type: character_name.to_string(),
            health: stats.current_health,
            max_health: stats.max_health,
        },
        crate::Enemy,
        ai,
        stats,
        Name::new(format!("Hades Enemy: {}", character_name)),
    ));
    
    info!("Spawned Hades-style enemy: {} at position {:?}", character_name, position);
}

fn update_camera_follow(
    mut camera_query: Query<&mut Transform, (With<Camera3d>, Without<MainCharacter>)>,
    character_query: Query<&Transform, (With<MainCharacter>, Without<Camera3d>)>,
) {
    if let (Ok(mut camera_transform), Ok(character_transform)) = 
        (camera_query.get_single_mut(), character_query.get_single()) {
        
        // Follow the main character with smooth interpolation
        let target_position = character_transform.translation + Vec3::new(10.0, 15.0, 10.0);
        camera_transform.translation = camera_transform.translation.lerp(target_position, 0.02);
        
        // Always look at the character
        camera_transform.look_at(character_transform.translation, Vec3::Y);
    }
}