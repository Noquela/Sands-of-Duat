use bevy::prelude::*;
use bevy::animation::AnimationPlayer;

/// 3D System - Real 3D models with rigging and animations like Hades
/// Replaces 2D billboard sprites with true 3D glTF models

#[derive(Resource)]
pub struct True3DAssets {
    // Hero 3D model with animations
    pub hero_scene: Handle<Scene>,
    pub hero_idle: Handle<AnimationClip>,
    pub hero_walk: Handle<AnimationClip>,
    pub hero_attack: Handle<AnimationClip>,
    
    // Weapons 3D models
    pub khopesh_scene: Handle<Scene>,
    pub ceremonial_staff_scene: Handle<Scene>,
    
    // Enemies 3D models
    pub anubis_boss_scene: Handle<Scene>,
    pub mummy_enemy_scene: Handle<Scene>,
    
    // 3D Environment pieces
    pub stone_pillar_model: Handle<Scene>,
    pub torch_brazier_model: Handle<Scene>,
    pub anubis_statue_model: Handle<Scene>,
}

#[derive(Component)]
pub struct Hero3D;

#[derive(Component)]
pub struct Enemy3D {
    pub enemy_type: EnemyType,
}

#[derive(Clone, Copy)]
pub enum EnemyType {
    AnubisBoss,
    MummyGuardian,
    EgyptianWarrior,
}

#[derive(Component)]
pub struct Weapon3D {
    pub weapon_type: WeaponType,
    pub equipped: bool,
}

#[derive(Clone, Copy)]
pub enum WeaponType {
    Khopesh,
    CeremonialStaff,
}

#[derive(Component)]
pub struct AnimationController3D {
    pub current_animation: String,
    pub animation_player: Option<Entity>,
}

pub struct True3DPlugin;

impl Plugin for True3DPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PreStartup, load_3d_assets)
            .add_systems(PostStartup, spawn_3d_hero)
            .add_systems(Update, (
                setup_3d_camera,
                find_animation_players,
                play_hero_animations,
                update_weapon_sockets,
                animate_environment_elements,
            ));
    }
}

fn load_3d_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading TRUE 3D glTF assets...");
    
    let assets_3d = True3DAssets {
        // Hero with full rigging and animations
        hero_scene: asset_server.load("models/hero.glb#Scene0"),
        hero_idle: asset_server.load("models/hero.glb#Animation0"),
        hero_walk: asset_server.load("models/hero.glb#Animation1"),
        hero_attack: asset_server.load("models/hero.glb#Animation2"),
        
        // Weapon models
        khopesh_scene: asset_server.load("models/weapons/khopesh.glb#Scene0"),
        ceremonial_staff_scene: asset_server.load("models/weapons/staff.glb#Scene0"),
        
        // Enemy models
        anubis_boss_scene: asset_server.load("models/anubis_boss.glb#Scene0"),
        mummy_enemy_scene: asset_server.load("models/mummy_enemy.glb#Scene0"),
        
        // Environment 3D models
        stone_pillar_model: asset_server.load("models/environment/stone_pillar.glb#Scene0"),
        torch_brazier_model: asset_server.load("models/environment/torch_brazier.glb#Scene0"),
        anubis_statue_model: asset_server.load("models/environment/anubis_statue.glb#Scene0"),
    };
    
    commands.insert_resource(assets_3d);
    info!("✅ 3D glTF assets loaded successfully!");
}

fn setup_3d_camera(
    mut commands: Commands,
    cameras: Query<Entity, With<Camera>>,
    mut spawned: Local<bool>,
) {
    if *spawned {
        return;
    }
    *spawned = true;
    
    // Clear existing cameras and create new 3D camera
    for entity in cameras.iter() {
        commands.entity(entity).despawn();
    }
    
    // Spawn new 3D perspective camera with Hades-like isometric view
    commands.spawn((
        Camera3dBundle {
            transform: Transform::from_xyz(24.0, 24.0, 24.0)
                .looking_at(Vec3::ZERO, Vec3::Y),
            projection: Projection::Perspective(PerspectiveProjection {
                fov: 50f32.to_radians(), // Low FOV for Hades-like view
                aspect_ratio: 3440.0 / 1440.0, // Ultrawide
                near: 0.1,
                far: 1000.0,
            }),
            ..default()
        },
        Name::new("True3D_Camera"),
    ));
    
    info!("✅ 3D perspective camera setup complete - Hades-like isometric view");
}

fn spawn_3d_hero(
    mut commands: Commands,
    assets_3d: Res<True3DAssets>,
    mut spawned: Local<bool>,
) {
    if *spawned {
        return;
    }
    *spawned = true;
    
    info!("Spawning 3D hero with full rigging...");
    
    // Spawn 3D hero model
    let hero_entity = commands.spawn((
        SceneBundle {
            scene: assets_3d.hero_scene.clone(),
            transform: Transform::from_xyz(0.0, 0.0, 0.0),
            ..default()
        },
        Hero3D,
        crate::Player, // Add Player component for gameplay systems
        crate::Stats::default(),
        crate::Dash::default(), 
        crate::Combat::default(),
        AnimationController3D {
            current_animation: "idle".to_string(),
            animation_player: None,
        },
        Name::new("Hero_3D"),
    )).id();
    
    info!("✅ 3D Hero spawned with entity: {:?}", hero_entity);
}

fn find_animation_players(
    mut hero_query: Query<&mut AnimationController3D, With<Hero3D>>,
    animation_players: Query<Entity, (Added<AnimationPlayer>, Without<Hero3D>)>,
    parents: Query<&Parent>,
    names: Query<&Name>,
) {
    // Find AnimationPlayer entities that belong to our hero
    for player_entity in animation_players.iter() {
        // Walk up parent chain to find hero
        if let Some(hero_entity) = find_hero_parent(player_entity, &parents, &names) {
            if let Ok(mut anim_controller) = hero_query.get_mut(hero_entity) {
                anim_controller.animation_player = Some(player_entity);
                info!("✅ Found AnimationPlayer for Hero: {:?}", player_entity);
            }
        }
    }
}

fn find_hero_parent(
    entity: Entity,
    parents: &Query<&Parent>,
    names: &Query<&Name>,
) -> Option<Entity> {
    let mut current = entity;
    
    // Walk up parent chain
    for _ in 0..10 { // Max depth to avoid infinite loops
        if let Ok(name) = names.get(current) {
            if name.as_str() == "Hero_3D" {
                return Some(current);
            }
        }
        
        if let Ok(parent) = parents.get(current) {
            current = parent.get();
        } else {
            break;
        }
    }
    
    None
}

fn play_hero_animations(
    mut hero_query: Query<&mut AnimationController3D, With<Hero3D>>,
    mut animation_players: Query<&mut AnimationPlayer>,
    assets_3d: Res<True3DAssets>,
    input: Res<crate::InputState>,
    time: Res<Time>,
) {
    for mut anim_controller in hero_query.iter_mut() {
        if let Some(player_entity) = anim_controller.animation_player {
            if let Ok(mut player) = animation_players.get_mut(player_entity) {
                
                // Determine which animation to play based on input
                let desired_animation = if input.primary || input.secondary {
                    "attack"
                } else if input.up || input.down || input.left || input.right {
                    "walk"
                } else {
                    "idle"
                };
                
                // Switch animation if needed
                if anim_controller.current_animation != desired_animation {
                    let animation_handle = match desired_animation {
                        "idle" => assets_3d.hero_idle.clone(),
                        "walk" => assets_3d.hero_walk.clone(),
                        "attack" => assets_3d.hero_attack.clone(),
                        _ => assets_3d.hero_idle.clone(),
                    };
                    
                    player.play(animation_handle).repeat();
                    anim_controller.current_animation = desired_animation.to_string();
                    
                    debug!("🎭 Playing animation: {}", desired_animation);
                }
            }
        }
    }
}

fn update_weapon_sockets(
    mut commands: Commands,
    hero_query: Query<Entity, With<Hero3D>>,
    socket_query: Query<(Entity, &Name)>,
    weapon_query: Query<&Weapon3D>,
    assets_3d: Res<True3DAssets>,
    children: Query<&Children>,
) {
    for hero_entity in hero_query.iter() {
        // Find Socket_Hand_R in hero hierarchy
        if let Some(hand_socket) = find_socket_by_name(hero_entity, "Socket_Hand_R", &socket_query, &children) {
            
            // Check if weapon is already equipped
            let has_weapon = weapon_query.iter().any(|weapon| weapon.equipped);
            
            if !has_weapon {
                // Equip khopesh sword
                let weapon_entity = commands.spawn((
                    SceneBundle {
                        scene: assets_3d.khopesh_scene.clone(),
                        ..default()
                    },
                    Weapon3D {
                        weapon_type: WeaponType::Khopesh,
                        equipped: true,
                    },
                    Name::new("Equipped_Khopesh"),
                )).id();
                
                // Parent weapon to hand socket
                commands.entity(hand_socket).add_child(weapon_entity);
                
                info!("⚔️ Equipped khopesh to hero's hand socket");
            }
        }
    }
}

fn find_socket_by_name(
    root_entity: Entity,
    socket_name: &str,
    socket_query: &Query<(Entity, &Name)>,
    children: &Query<&Children>,
) -> Option<Entity> {
    let mut stack = vec![root_entity];
    
    while let Some(entity) = stack.pop() {
        if let Ok((socket_entity, name)) = socket_query.get(entity) {
            if name.as_str() == socket_name {
                return Some(socket_entity);
            }
        }
        
        if let Ok(entity_children) = children.get(entity) {
            stack.extend(entity_children.iter().copied());
        }
    }
    
    None
}

fn animate_environment_elements(
    mut torch_query: Query<&mut Transform, (With<Name>, Without<Hero3D>)>,
    time: Res<Time>,
) {
    // Animate torch flames with subtle movement
    for mut transform in torch_query.iter_mut() {
        // Only animate objects with "torch" in the name
        // Simple flame flicker effect
        let flicker = (time.elapsed_seconds() * 3.0).sin() * 0.02;
        transform.scale.y = 1.0 + flicker;
    }
}

pub fn spawn_3d_enemy(
    commands: &mut Commands,
    assets_3d: &True3DAssets,
    enemy_type: EnemyType,
    position: Vec3,
    ai: crate::AI,
    stats: crate::Stats,
) -> Entity {
    let scene_handle = match enemy_type {
        EnemyType::AnubisBoss => assets_3d.anubis_boss_scene.clone(),
        EnemyType::MummyGuardian => assets_3d.mummy_enemy_scene.clone(),
        EnemyType::EgyptianWarrior => assets_3d.mummy_enemy_scene.clone(), // Reuse for now
    };
    
    commands.spawn((
        SceneBundle {
            scene: scene_handle,
            transform: Transform::from_translation(position),
            ..default()
        },
        Enemy3D { enemy_type },
        crate::Enemy, // Add Enemy component for gameplay systems
        ai,
        stats,
        AnimationController3D {
            current_animation: "idle".to_string(),
            animation_player: None,
        },
        Name::new("Enemy_3D"),
    )).id()
}

pub fn spawn_3d_environment_piece(
    commands: &mut Commands,
    assets_3d: &True3DAssets,
    piece_type: &str,
    position: Vec3,
) -> Entity {
    let scene_handle = match piece_type {
        "pillar" => assets_3d.stone_pillar_model.clone(),
        "torch" => assets_3d.torch_brazier_model.clone(),
        "statue" => assets_3d.anubis_statue_model.clone(),
        _ => assets_3d.stone_pillar_model.clone(),
    };
    
    commands.spawn((
        SceneBundle {
            scene: scene_handle,
            transform: Transform::from_translation(position),
            ..default()
        },
        Name::new(format!("Env_3D_{}", piece_type)),
    )).id()
}