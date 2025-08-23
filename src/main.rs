use bevy::prelude::*;
use bevy::window::{WindowResolution, PresentMode};

mod asset_loader;
mod sprite_animation;
mod true_3d_system;
mod placeholder_3d_models;
use asset_loader::{AssetLoaderPlugin, GameAssets};
use sprite_animation::SpriteAnimationPlugin;
use true_3d_system::True3DPlugin;
use placeholder_3d_models::Placeholder3DPlugin;

// 🔧 Controles estilo Hades (Mouse + R/Q)
// * Mover: WASD
// * Dash: Espaço (com i-frames)
// * Ataque principal: Mouse Esquerdo
// * Ataque secundário (especial leve): Mouse Direito
// * Habilidade principal: R (explosão/AoE curta)
// * Habilidade extra: Q (cast/projétil)
// * Interagir/Avançar: E
// * Menu: Esc

#[derive(Resource, Default, Clone, Copy)]
pub struct InputState {
    pub up: bool,
    pub down: bool,
    pub left: bool,
    pub right: bool,
    pub dash: bool,
    pub interact: bool,
    // Remapeamentos Hades-like:
    pub primary: bool,    // Mouse Esquerdo: ataque principal
    pub secondary: bool,  // Mouse Direito: ataque secundário (especial leve)
    pub ability_q: bool,  // Q: habilidade extra (cast)
    pub ability_r: bool,  // R: habilidade principal (AoE)
    pub mouse_world_pos: Vec3, // Posição do mouse no mundo 3D
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Sands of Duat - Hades-like Egyptian Roguelike".into(),
                resolution: WindowResolution::new(3440.0, 1440.0),
                present_mode: PresentMode::AutoNoVsync, // For 120fps benchmark
                resizable: false,
                ..default()
            }),
            ..default()
        }))
        .add_plugins(bevy::diagnostic::FrameTimeDiagnosticsPlugin)
        .add_plugins(AssetLoaderPlugin)
        .add_plugins(SpriteAnimationPlugin) // Load RTX-generated 3D isometric assets  
        .add_plugins(True3DPlugin) // NEW: True 3D system with glTF models and rigging
        // .add_plugins(Placeholder3DPlugin) // Disabled: Now using real 3D models
        .add_event::<SpawnParticlesEvent>()
        .add_event::<AudioEvent>()
        .init_resource::<InputState>()
        .init_resource::<AudioHandles>()
        .insert_resource(GameState {
            current_room: 0,
            rooms_cleared: 0,
            total_rooms: 3,
            previous_room: 0,
            enemies_spawned: vec![false, false, false], // No enemies spawned initially
        })
        .add_systems(Startup, setup)
        .add_systems(Update, (
            read_input,
            fps_counter_system,
            dash_ui_system,
            combat_ui_system,
            health_stamina_ui_system,
            player_movement_system,
            stamina_regen_system,
            ai_system,
            hades_combat_system,
            (projectile_movement_system, projectile_collision_system).chain(),
            hit_effect_system,
            particle_spawn_system,
            particle_system,
            room_transition_system,
            room_clear_system,
            room_enemy_spawn_system,
            audio_system,
        ))
        .run();
}

#[derive(Component)]
struct Player;

#[derive(Component)]
struct Enemy;

#[derive(Component)]
enum EnemyType {
    Chaser,    // Basic enemy that chases player
    Shooter,   // Ranged enemy that shoots projectiles
    Tank,      // Heavy enemy with lots of health, moves slowly
}

#[derive(Component)]
struct AI {
    target_range: f32,
    chase_speed: f32,
    attack_cooldown: f32,
    attack_timer: f32,
}

#[derive(Component)]
struct FpsText;

#[derive(Component)]
struct DashText;

#[derive(Component)]
struct CombatText;

#[derive(Component)]
struct HealthBar;

#[derive(Component)]
struct StaminaBar;

#[derive(Component)]
struct HitEffect {
    timer: f32,
    duration: f32,
    original_scale: Vec3,
}

impl Default for HitEffect {
    fn default() -> Self {
        Self {
            timer: 0.0,
            duration: 0.3,
            original_scale: Vec3::splat(0.8),
        }
    }
}

#[derive(Component)]
struct Stats {
    max_health: f32,
    current_health: f32,
    max_stamina: f32,
    current_stamina: f32,
    speed: f32,
    stamina_regen_rate: f32,
}

impl Default for Stats {
    fn default() -> Self {
        Self {
            max_health: 100.0,
            current_health: 100.0,
            max_stamina: 100.0,
            current_stamina: 100.0,
            speed: 9.5, // Faster like Hades
            stamina_regen_rate: 25.0, // Stamina per second
        }
    }
}

#[derive(Component)]
struct Dash {
    cooldown: f32,
    cooldown_timer: f32,
    distance: f32,
    i_frames: f32,
    i_timer: f32,
    is_dashing: bool,
    dash_timer: f32,
    dash_direction: Vec3,
    stamina_cost: f32,
}

impl Default for Dash {
    fn default() -> Self {
        Self {
            cooldown: 0.9,
            cooldown_timer: 0.0,
            distance: 5.5,
            i_frames: 0.15,
            i_timer: 0.0,
            is_dashing: false,
            dash_timer: 0.0,
            dash_direction: Vec3::ZERO,
            stamina_cost: 25.0, // Dash costs 25% stamina
        }
    }
}

#[derive(Component)]
struct Combat {
    base_damage: i32,
    // primário (mouse esq) – chain de 3
    atk_cd: f32,
    atk_timer: f32,
    chain_step: u8,
    // secundário (mouse dir) – especial leve
    special_cd: f32,
    special_timer: f32,
    // Q – cast/projétil
    q_cd: f32,
    q_timer: f32,
    // R – habilidade principal (AoE)
    r_cd: f32,
    r_timer: f32,
}

impl Default for Combat {
    fn default() -> Self {
        Self {
            base_damage: 10,
            atk_cd: 0.25,
            atk_timer: 0.0,
            chain_step: 0,
            special_cd: 3.0,
            special_timer: 0.0,
            q_cd: 1.2,
            q_timer: 0.0,
            r_cd: 8.0,
            r_timer: 0.0,
        }
    }
}

#[derive(Component, Copy, Clone)]
struct Projectile {
    damage: i32,
    velocity: Vec3,
    ttl: f32,
    from_enemy: bool, // Track if projectile is from enemy
}

#[derive(Component)]
struct EnemyProjectile;

#[derive(Component)]
struct Particle {
    velocity: Vec3,
    ttl: f32,
    fade_speed: f32,
    initial_scale: Vec3,
}

#[derive(Component)]
struct ParticleSystem {
    spawn_rate: f32,
    spawn_timer: f32,
    particle_lifetime: f32,
    spawn_radius: f32,
    velocity_range: f32,
    color: Color,
    size: f32,
}

// Event for spawning particles
#[derive(Event)]
struct SpawnParticlesEvent {
    position: Vec3,
    color: Color,
    count: usize,
}

// Audio events for combat feedback
#[derive(Event, Debug)]
enum AudioEvent {
    AttackPrimary,
    AttackSecondary,
    AbilityQ,
    AbilityR,
    ProjectileHit,
    EnemyHit,
    Dash,
    EnemyDeath,
}

// Room system components
#[derive(Component)]
struct Room {
    id: usize,
    size: Vec2,
    center: Vec2,
    cleared: bool,
    room_type: RoomType,
}

#[derive(Clone, Copy, Debug)]
enum RoomType {
    Combat,
    Treasure,
    Boss,
    Start,
}

#[derive(Component)]
struct RoomTransition {
    from_room: usize,
    to_room: usize,
    position: Vec3,
    size: Vec3,
    active: bool,
}

#[derive(Resource)]
struct GameState {
    current_room: usize,
    rooms_cleared: usize,
    total_rooms: usize,
    previous_room: usize,
    enemies_spawned: Vec<bool>, // Track which rooms have spawned enemies
}

#[derive(Resource, Default)]
struct AudioHandles {
    attack_primary: Handle<AudioSource>,
    attack_secondary: Handle<AudioSource>,
    ability_q: Handle<AudioSource>,
    ability_r: Handle<AudioSource>,
    projectile_hit: Handle<AudioSource>,
    enemy_hit: Handle<AudioSource>,
    dash: Handle<AudioSource>,
    enemy_death: Handle<AudioSource>,
}

fn setup(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    asset_server: Res<AssetServer>,
    game_assets: Option<Res<GameAssets>>,
    _audio_handles: ResMut<AudioHandles>,
) {
    // Load audio assets (using procedural sound generation since we don't have audio files)
    // These will be placeholder handles since we don't have actual audio files
    // In a real game, you would load actual audio files here
    
    // Light
    commands.insert_resource(AmbientLight {
        color: Color::rgb(1.0, 0.9, 0.7),
        brightness: 400.0,
    });
    
    // Directional light (sun-like for Egyptian theme)
    commands.spawn(DirectionalLightBundle {
        directional_light: DirectionalLight {
            color: Color::rgb(1.0, 0.9, 0.6),
            illuminance: 10000.0,
            ..default()
        },
        transform: Transform::from_rotation(Quat::from_euler(EulerRot::XYZ, -0.8, 0.8, 0.0)),
        ..default()
    });

    // Camera - Isometric view (45°/45°)
    commands.spawn(Camera3dBundle {
        transform: Transform::from_xyz(10.0, 10.0, 10.0)
            .looking_at(Vec3::ZERO, Vec3::Y),
        ..default()
    });

    // Ground plane (sand)
    commands.spawn(PbrBundle {
        mesh: meshes.add(Plane3d::default().mesh().size(20.0, 20.0)),
        material: materials.add(StandardMaterial {
            base_color: Color::rgb(0.8, 0.7, 0.4), // Sandy color
            ..default()
        }),
        ..default()
    });

    // NOTE: Player spawning now handled by Placeholder3DPlugin
    // Old 2D sprite player disabled in favor of 3D placeholder hero

    // FPS Counter UI
    commands.spawn((
        TextBundle::from_sections([
            TextSection::new(
                "FPS: ",
                TextStyle {
                    font_size: 32.0,
                    color: Color::WHITE,
                    ..default()
                },
            ),
            TextSection::from_style(TextStyle {
                font_size: 32.0,
                color: Color::GOLD,
                ..default()
            }),
        ])
        .with_style(Style {
            position_type: PositionType::Absolute,
            top: Val::Px(10.0),
            left: Val::Px(10.0),
            ..default()
        }),
        FpsText,
    ));

    // Dash status UI
    commands.spawn((
        TextBundle::from_sections([
            TextSection::new(
                "DASH: ",
                TextStyle {
                    font_size: 28.0,
                    color: Color::WHITE,
                    ..default()
                },
            ),
            TextSection::from_style(TextStyle {
                font_size: 28.0,
                color: Color::CYAN,
                ..default()
            }),
        ])
        .with_style(Style {
            position_type: PositionType::Absolute,
            top: Val::Px(60.0),
            left: Val::Px(10.0),
            ..default()
        }),
        DashText,
    ));

    // Combat status UI
    commands.spawn((
        TextBundle::from_sections([
            TextSection::new(
                "COMBAT: ",
                TextStyle {
                    font_size: 28.0,
                    color: Color::WHITE,
                    ..default()
                },
            ),
            TextSection::from_style(TextStyle {
                font_size: 28.0,
                color: Color::ORANGE_RED,
                ..default()
            }),
        ])
        .with_style(Style {
            position_type: PositionType::Absolute,
            top: Val::Px(110.0),
            left: Val::Px(10.0),
            ..default()
        }),
        CombatText,
    ));

    // Health Bar
    commands.spawn((
        NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                left: Val::Px(10.0),
                top: Val::Px(160.0),
                width: Val::Px(300.0),
                height: Val::Px(20.0),
                border: UiRect::all(Val::Px(2.0)),
                ..default()
            },
            background_color: Color::rgb(0.2, 0.2, 0.2).into(),
            border_color: Color::rgb(0.8, 0.8, 0.8).into(),
            ..default()
        },
    )).with_children(|parent| {
        parent.spawn((
            NodeBundle {
                style: Style {
                    width: Val::Percent(100.0),
                    height: Val::Percent(100.0),
                    ..default()
                },
                background_color: Color::rgb(0.8, 0.2, 0.2).into(),
                ..default()
            },
            HealthBar,
        ));
    });

    // Stamina Bar
    commands.spawn((
        NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                left: Val::Px(10.0),
                top: Val::Px(190.0),
                width: Val::Px(300.0),
                height: Val::Px(15.0),
                border: UiRect::all(Val::Px(2.0)),
                ..default()
            },
            background_color: Color::rgb(0.2, 0.2, 0.2).into(),
            border_color: Color::rgb(0.8, 0.8, 0.8).into(),
            ..default()
        },
    )).with_children(|parent| {
        parent.spawn((
            NodeBundle {
                style: Style {
                    width: Val::Percent(100.0),
                    height: Val::Percent(100.0),
                    ..default()
                },
                background_color: Color::rgb(0.2, 0.6, 0.8).into(),
                ..default()
            },
            StaminaBar,
        ));
    });

    // Controls help - Hades style
    commands.spawn(
        TextBundle::from_section(
            "WASD: Move | SPACE: Dash | LMB: Attack | RMB: Special | Q: Cast | R: AoE | E: Interact",
            TextStyle {
                font_size: 22.0,
                color: Color::rgb(0.7, 0.7, 0.7),
                ..default()
            },
        )
        .with_style(Style {
            position_type: PositionType::Absolute,
            bottom: Val::Px(10.0),
            left: Val::Px(10.0),
            ..default()
        }),
    );

    // Create rooms layout with RTX-generated environments
    let game_assets_ref = game_assets.as_ref().map(|a| a.as_ref());
    setup_rooms(&mut commands, &mut meshes, &mut materials, game_assets_ref);

    // NOTE: Enemy spawning now handled by room_enemy_spawn_system
    // Initial enemies will spawn when entering Combat rooms
    
    // Old static enemy spawning disabled:
    /*
    let enemy_spawns = [
        (Vec3::new(5.0, 0.5, 3.0), EnemyType::Chaser),
        (Vec3::new(-4.0, 0.5, -2.0), EnemyType::Shooter),
    ];

    for (pos, enemy_type) in enemy_spawns {
        let (mesh, material, ai, stats) = match enemy_type {
            EnemyType::Chaser => {
                // Fast, weak chaser - RTX-generated Anubis sprite
                (
                    meshes.add(Plane3d::default().mesh().size(2.0, 2.0)), // Billboard for 3D sprite
                    if let Some(assets) = &game_assets {
                        info!("✅ Using RTX-generated Anubis Judge sprite for chaser enemy");
                        materials.add(StandardMaterial {
                            base_color_texture: Some(assets.anubis_judge.clone()),
                            alpha_mode: AlphaMode::Blend,
                            unlit: true,
                            double_sided: true,
                            base_color: Color::WHITE,
                            ..default()
                        })
                    } else {
                        info!("⚠️ Assets not loaded, using red fallback for chaser");
                        materials.add(StandardMaterial {
                            base_color: Color::rgb(0.8, 0.2, 0.2),
                            emissive: Color::rgb(0.4, 0.1, 0.1).into(),
                            ..default()
                        })
                    },
                    AI {
                        target_range: 12.0,
                        chase_speed: 4.0,
                        attack_cooldown: 0.0,
                        attack_timer: 0.0,
                    },
                    Stats {
                        max_health: 30.0,
                        current_health: 30.0,
                        max_stamina: 0.0,
                        current_stamina: 0.0,
                        speed: 4.0,
                        stamina_regen_rate: 0.0,
                    },
                )
            },
            EnemyType::Shooter => {
                // Ranged shooter - RTX-generated Mummy Guardian sprite
                (
                    meshes.add(Plane3d::default().mesh().size(2.0, 2.0)), // Billboard for 3D sprite
                    if let Some(assets) = &game_assets {
                        materials.add(StandardMaterial {
                            base_color_texture: Some(assets.mummy_guardian.clone()),
                            alpha_mode: AlphaMode::Blend,
                            unlit: true,
                            double_sided: true,
                            ..default()
                        })
                    } else {
                        materials.add(StandardMaterial {
                            base_color: Color::rgb(0.2, 0.8, 0.2),
                            emissive: Color::rgb(0.1, 0.4, 0.1).into(),
                            ..default()
                        })
                    },
                    AI {
                        target_range: 15.0,
                        chase_speed: 1.5,
                        attack_cooldown: 2.0,
                        attack_timer: 0.0,
                    },
                    Stats {
                        max_health: 40.0,
                        current_health: 40.0,
                        max_stamina: 0.0,
                        current_stamina: 0.0,
                        speed: 1.5,
                        stamina_regen_rate: 0.0,
                    },
                )
            },
            EnemyType::Tank => {
                // Slow, heavy tank - RTX-generated Set Chaos sprite  
                (
                    meshes.add(Plane3d::default().mesh().size(2.5, 2.5)), // Larger billboard for tank
                    if let Some(assets) = &game_assets {
                        materials.add(StandardMaterial {
                            base_color_texture: Some(assets.set_chaos.clone()),
                            alpha_mode: AlphaMode::Blend,
                            unlit: true,
                            double_sided: true,
                            ..default()
                        })
                    } else {
                        materials.add(StandardMaterial {
                            base_color: Color::rgb(0.6, 0.6, 0.2),
                            emissive: Color::rgb(0.3, 0.3, 0.1).into(),
                            ..default()
                        })
                    },
                    AI {
                        target_range: 8.0,
                        chase_speed: 1.0,
                        attack_cooldown: 0.0,
                        attack_timer: 0.0,
                    },
                    Stats {
                        max_health: 120.0,
                        current_health: 120.0,
                        max_stamina: 0.0,
                        current_stamina: 0.0,
                        speed: 1.0,
                        stamina_regen_rate: 0.0,
                    },
                )
            },
        };

        commands.spawn((
            PbrBundle {
                mesh,
                material,
                transform: Transform::from_translation(pos)
                    .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_4)), // Face camera for 3D effect
                ..default()
            },
            Enemy,
            enemy_type,
            ai,
            stats,
        ));
    }
    */
}

fn read_input(
    kb: Res<ButtonInput<KeyCode>>,
    mouse: Res<ButtonInput<MouseButton>>,
    mut input_state: ResMut<InputState>,
    windows: Query<&Window>,
    cameras: Query<(&Camera, &GlobalTransform)>,
) {
    // Continuous inputs
    input_state.up = kb.pressed(KeyCode::KeyW);
    input_state.down = kb.pressed(KeyCode::KeyS);
    input_state.left = kb.pressed(KeyCode::KeyA);
    input_state.right = kb.pressed(KeyCode::KeyD);

    // Pulse inputs (just_pressed)
    input_state.dash = kb.just_pressed(KeyCode::Space);
    input_state.interact = kb.just_pressed(KeyCode::KeyE);

    // Hades-style remapped controls
    input_state.primary = mouse.just_pressed(MouseButton::Left);
    input_state.secondary = mouse.just_pressed(MouseButton::Right);
    input_state.ability_q = kb.just_pressed(KeyCode::KeyQ);
    input_state.ability_r = kb.just_pressed(KeyCode::KeyR);
    
    // Mouse world position calculation
    if let Ok(window) = windows.get_single() {
        if let Some(cursor_position) = window.cursor_position() {
            if let Ok((camera, camera_transform)) = cameras.get_single() {
                // Convert screen coordinates to world ray
                if let Some(ray) = camera.viewport_to_world(camera_transform, cursor_position) {
                    // Project ray onto ground plane (y = 0)
                    let distance = -ray.origin.y / ray.direction.y;
                    input_state.mouse_world_pos = ray.origin + ray.direction * distance;
                }
            }
        }
    }
}

fn fps_counter_system(
    diagnostics: Res<bevy::diagnostic::DiagnosticsStore>,
    mut query: Query<&mut Text, With<FpsText>>,
) {
    for mut text in &mut query {
        if let Some(fps) = diagnostics.get(&bevy::diagnostic::FrameTimeDiagnosticsPlugin::FPS) {
            if let Some(value) = fps.smoothed() {
                text.sections[1].value = format!("{:.0}", value);
            }
        }
    }
}

fn dash_ui_system(
    player_query: Query<&Dash, With<Player>>,
    mut dash_text_query: Query<&mut Text, With<DashText>>,
) {
    if let Ok(dash) = player_query.get_single() {
        for mut text in &mut dash_text_query {
            if dash.is_dashing {
                text.sections[1].value = "DASHING!".to_string();
                text.sections[1].style.color = Color::YELLOW;
            } else if dash.cooldown_timer > 0.0 {
                text.sections[1].value = format!("{:.1}s", dash.cooldown_timer);
                text.sections[1].style.color = Color::RED;
            } else {
                text.sections[1].value = "READY".to_string();
                text.sections[1].style.color = Color::GREEN;
            }
        }
    }
}

fn combat_ui_system(
    player_query: Query<&Combat, With<Player>>,
    mut combat_text_query: Query<&mut Text, With<CombatText>>,
) {
    if let Ok(combat) = player_query.get_single() {
        for mut text in &mut combat_text_query {
            let mut status = String::new();
            
            // Show chain step for primary attack
            if combat.atk_timer > 0.0 {
                status = format!("Chain {}", combat.chain_step + 1);
                text.sections[1].style.color = Color::YELLOW;
            } else if combat.special_timer > 0.0 {
                status = format!("Special: {:.1}s", combat.special_timer);
                text.sections[1].style.color = Color::PURPLE;
            } else if combat.r_timer > 0.0 {
                status = format!("AoE: {:.1}s", combat.r_timer);
                text.sections[1].style.color = Color::RED;
            } else if combat.q_timer > 0.0 {
                status = format!("Cast: {:.1}s", combat.q_timer);
                text.sections[1].style.color = Color::CYAN;
            } else {
                status = "READY".to_string();
                text.sections[1].style.color = Color::GREEN;
            }
            
            text.sections[1].value = status;
        }
    }
}

fn player_movement_system(
    time: Res<Time>,
    input: Res<InputState>,
    mut player_query: Query<(&mut Transform, &mut Stats, &mut Dash), With<Player>>,
    mut audio_events: EventWriter<AudioEvent>,
) {
    let (mut transform, mut stats, mut dash) = player_query.single_mut();
    let dt = time.delta_seconds();

    // Continuous movement
    let mut dir = Vec3::ZERO;
    if input.up { dir.z -= 1.0; }
    if input.down { dir.z += 1.0; }
    if input.left { dir.x -= 1.0; }
    if input.right { dir.x += 1.0; }
    dir = dir.normalize_or_zero();

    // Update cooldowns
    dash.cooldown_timer = (dash.cooldown_timer - dt).max(0.0);
    dash.i_timer = (dash.i_timer - dt).max(0.0);

    // Handle dash input (requires stamina)
    if input.dash && dash.cooldown_timer <= 0.0 && !dash.is_dashing && stats.current_stamina >= dash.stamina_cost {
        let dash_dir = if dir.length_squared() > 0.0 { dir } else { Vec3::new(0.0, 0.0, -1.0) };
        dash.is_dashing = true;
        dash.dash_timer = 0.2; // dash duration
        dash.dash_direction = dash_dir;
        dash.cooldown_timer = dash.cooldown;
        dash.i_timer = dash.i_frames;
        
        // Consume stamina
        stats.current_stamina -= dash.stamina_cost;
        stats.current_stamina = stats.current_stamina.max(0.0);
        
        // Play dash audio
        audio_events.send(AudioEvent::Dash);
    }

    // Handle dash movement
    if dash.is_dashing {
        dash.dash_timer -= dt;
        if dash.dash_timer > 0.0 {
            // Dash movement (instant distance)
            let dash_speed = dash.distance / 0.2;
            transform.translation += dash.dash_direction * dash_speed * dt;
        } else {
            dash.is_dashing = false;
            dash.dash_direction = Vec3::ZERO;
        }
    } else if dir != Vec3::ZERO {
        // Normal movement
        transform.translation += dir * stats.speed * dt;
    }

    // Keep player above ground
    transform.translation.y = 0.5;
}

fn stamina_regen_system(
    time: Res<Time>,
    mut player_query: Query<&mut Stats, With<Player>>,
) {
    let mut stats = player_query.single_mut();
    let dt = time.delta_seconds();
    
    // Regenerate stamina over time
    if stats.current_stamina < stats.max_stamina {
        stats.current_stamina += stats.stamina_regen_rate * dt;
        stats.current_stamina = stats.current_stamina.min(stats.max_stamina);
    }
}

fn health_stamina_ui_system(
    player_query: Query<&Stats, With<Player>>,
    mut health_bar_query: Query<&mut Style, (With<HealthBar>, Without<StaminaBar>)>,
    mut stamina_bar_query: Query<&mut Style, (With<StaminaBar>, Without<HealthBar>)>,
) {
    if let Ok(stats) = player_query.get_single() {
        // Update health bar
        if let Ok(mut style) = health_bar_query.get_single_mut() {
            let health_percent = (stats.current_health / stats.max_health) * 100.0;
            style.width = Val::Percent(health_percent);
        }
        
        // Update stamina bar
        if let Ok(mut style) = stamina_bar_query.get_single_mut() {
            let stamina_percent = (stats.current_stamina / stats.max_stamina) * 100.0;
            style.width = Val::Percent(stamina_percent);
        }
    }
}

fn ai_system(
    time: Res<Time>,
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut player_query: Query<(&Transform, &mut Stats, &Dash), With<Player>>,
    mut enemy_query: Query<(&mut Transform, &mut AI, &Stats, &EnemyType), (With<Enemy>, Without<Player>)>,
) {
    let (player_transform, mut player_stats, dash) = player_query.single_mut();
    let dt = time.delta_seconds();

    for (mut enemy_transform, mut ai, enemy_stats, enemy_type) in &mut enemy_query {
        let distance = player_transform.translation.distance(enemy_transform.translation);
        
        // Update attack timer
        ai.attack_timer = (ai.attack_timer - dt).max(0.0);
        
        match enemy_type {
            EnemyType::Chaser => {
                // Move towards player aggressively
                if distance < ai.target_range && distance > 1.0 {
                    let direction = (player_transform.translation - enemy_transform.translation).normalize();
                    enemy_transform.translation += direction * enemy_stats.speed * dt;
                    enemy_transform.translation.y = 0.5;
                }
                
                // Damage player if touching
                if distance <= 1.0 && dash.i_timer <= 0.0 {
                    player_stats.current_health -= 25.0 * dt;
                    player_stats.current_health = player_stats.current_health.max(0.0);
                }
            },
            
            EnemyType::Shooter => {
                // Keep distance and shoot projectiles
                if distance < ai.target_range {
                    if distance > 6.0 {
                        // Too far - move closer
                        let direction = (player_transform.translation - enemy_transform.translation).normalize();
                        enemy_transform.translation += direction * enemy_stats.speed * dt;
                        enemy_transform.translation.y = 0.5;
                    } else if distance < 4.0 {
                        // Too close - back away
                        let direction = (enemy_transform.translation - player_transform.translation).normalize();
                        enemy_transform.translation += direction * enemy_stats.speed * dt;
                        enemy_transform.translation.y = 0.5;
                    }
                    
                    // Shoot at player
                    if ai.attack_timer <= 0.0 {
                        let direction = (player_transform.translation - enemy_transform.translation).normalize();
                        commands.spawn((
                            PbrBundle {
                                mesh: meshes.add(Sphere::new(0.1)),
                                material: materials.add(StandardMaterial {
                                    base_color: Color::rgb(0.8, 0.1, 0.1),
                                    emissive: Color::rgb(2.0, 0.5, 0.5).into(),
                                    ..default()
                                }),
                                transform: Transform::from_translation(enemy_transform.translation + direction * 0.5),
                                ..default()
                            },
                            Projectile {
                                damage: 15,
                                velocity: direction * 8.0,
                                ttl: 3.0,
                                from_enemy: true,
                            },
                            EnemyProjectile,
                        ));
                        ai.attack_timer = ai.attack_cooldown;
                    }
                }
            },
            
            EnemyType::Tank => {
                // Slow but heavy damage
                if distance < ai.target_range && distance > 1.5 {
                    let direction = (player_transform.translation - enemy_transform.translation).normalize();
                    enemy_transform.translation += direction * enemy_stats.speed * dt;
                    enemy_transform.translation.y = 0.5;
                }
                
                // Heavy damage if touching
                if distance <= 1.5 && dash.i_timer <= 0.0 {
                    player_stats.current_health -= 40.0 * dt;
                    player_stats.current_health = player_stats.current_health.max(0.0);
                }
            },
        }
    }
}

fn hades_combat_system(
    time: Res<Time>,
    input: Res<InputState>,
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut player_query: Query<(&Transform, &mut Combat), With<Player>>,
    mut enemy_query: Query<(Entity, &Transform, &mut Stats), (With<Enemy>, Without<Player>)>,
    mut particle_events: EventWriter<SpawnParticlesEvent>,
    mut audio_events: EventWriter<AudioEvent>,
) {
    let (player_transform, mut combat) = player_query.single_mut();
    let dt = time.delta_seconds();

    // Update cooldowns
    combat.atk_timer = (combat.atk_timer - dt).max(0.0);
    combat.special_timer = (combat.special_timer - dt).max(0.0);
    combat.q_timer = (combat.q_timer - dt).max(0.0);
    combat.r_timer = (combat.r_timer - dt).max(0.0);

    const HIT_RANGE: f32 = 1.6;

    // PRIMARY ATTACK (Mouse Left) - Chain 3 hits
    if input.primary && combat.atk_timer <= 0.0 {
        let mut hits = 0;
        for (entity, enemy_transform, mut enemy_stats) in &mut enemy_query {
            if player_transform.translation.distance(enemy_transform.translation) <= HIT_RANGE {
                let damage = combat.base_damage + (combat.chain_step as i32 * 2);
                enemy_stats.current_health -= damage as f32;
                
                // Add hit effect
                commands.entity(entity).insert(HitEffect {
                    timer: 0.0,
                    duration: 0.3,
                    original_scale: enemy_transform.scale,
                });
                
                // Spawn impact particles
                particle_events.send(SpawnParticlesEvent {
                    position: enemy_transform.translation,
                    color: Color::rgb(1.0, 0.8, 0.2),
                    count: 8,
                });
                
                hits += 1;
                if enemy_stats.current_health <= 0.0 {
                    commands.entity(entity).despawn();
                    // Play enemy death audio
                    audio_events.send(AudioEvent::EnemyDeath);
                } else {
                    // Play enemy hit audio
                    audio_events.send(AudioEvent::EnemyHit);
                }
            }
        }
        
        if hits > 0 {
            combat.chain_step = (combat.chain_step + 1) % 3;
            combat.atk_timer = combat.atk_cd;
            // Play primary attack audio
            audio_events.send(AudioEvent::AttackPrimary);
        }
    }

    // SECONDARY ATTACK (Mouse Right) - Special attack
    if input.secondary && combat.special_timer <= 0.0 {
        let range = HIT_RANGE * 1.35;
        let mut hits = 0;
        for (entity, enemy_transform, mut enemy_stats) in &mut enemy_query {
            if player_transform.translation.distance(enemy_transform.translation) <= range {
                let damage = (combat.base_damage as f32 * 1.8) as i32;
                enemy_stats.current_health -= damage as f32;
                
                // Add stronger hit effect
                commands.entity(entity).insert(HitEffect {
                    timer: 0.0,
                    duration: 0.5,
                    original_scale: enemy_transform.scale,
                });
                
                // Spawn special attack particles (purple)
                particle_events.send(SpawnParticlesEvent {
                    position: enemy_transform.translation,
                    color: Color::rgb(0.8, 0.3, 1.0),
                    count: 12,
                });
                
                hits += 1;
                if enemy_stats.current_health <= 0.0 {
                    commands.entity(entity).despawn();
                    // Play enemy death audio
                    audio_events.send(AudioEvent::EnemyDeath);
                } else {
                    // Play enemy hit audio
                    audio_events.send(AudioEvent::EnemyHit);
                }
            }
        }
        
        if hits > 0 {
            combat.special_timer = combat.special_cd;
            // Play secondary attack audio
            audio_events.send(AudioEvent::AttackSecondary);
        }
    }

    // Q ABILITY - Cast projectile (follows mouse direction)
    if input.ability_q && combat.q_timer <= 0.0 {
        // Calculate direction from player to mouse position
        let direction = (input.mouse_world_pos - player_transform.translation).normalize_or_zero();
        
        // Fallback to forward direction if mouse position is invalid
        let direction = if direction.length_squared() > 0.01 {
            direction
        } else {
            Vec3::new(0.0, 0.0, -1.0)
        };
        
        commands.spawn((
            PbrBundle {
                mesh: meshes.add(Sphere::new(0.15)),
                material: materials.add(StandardMaterial {
                    base_color: Color::rgb(0.3, 0.8, 1.0),
                    emissive: Color::rgb(2.0, 4.0, 6.0).into(),
                    ..default()
                }),
                transform: Transform::from_translation(player_transform.translation + direction * 0.8),
                ..default()
            },
            Projectile {
                damage: 12,
                velocity: direction * 20.0,
                ttl: 2.5,
                from_enemy: false,
            },
        ));
        combat.q_timer = combat.q_cd;
        // Play ability Q audio
        audio_events.send(AudioEvent::AbilityQ);
    }

    // R ABILITY - AoE attack
    if input.ability_r && combat.r_timer <= 0.0 {
        let radius = 2.6;
        let mut hits = 0;
        for (entity, enemy_transform, mut enemy_stats) in &mut enemy_query {
            if player_transform.translation.distance(enemy_transform.translation) <= radius {
                let damage = (combat.base_damage as f32 * 2.4) as i32;
                enemy_stats.current_health -= damage as f32;
                
                // Add AoE hit effect
                commands.entity(entity).insert(HitEffect {
                    timer: 0.0,
                    duration: 0.6,
                    original_scale: enemy_transform.scale,
                });
                
                // Spawn AoE particles (red explosion)
                particle_events.send(SpawnParticlesEvent {
                    position: enemy_transform.translation,
                    color: Color::rgb(1.0, 0.3, 0.2),
                    count: 16,
                });
                
                hits += 1;
                if enemy_stats.current_health <= 0.0 {
                    commands.entity(entity).despawn();
                    // Play enemy death audio
                    audio_events.send(AudioEvent::EnemyDeath);
                } else {
                    // Play enemy hit audio
                    audio_events.send(AudioEvent::EnemyHit);
                }
            }
        }
        
        if hits > 0 {
            combat.r_timer = combat.r_cd;
            // Play ability R audio
            audio_events.send(AudioEvent::AbilityR);
        }
    }
}

fn projectile_movement_system(
    time: Res<Time>,
    mut commands: Commands,
    mut projectiles: Query<(Entity, &mut Transform, &mut Projectile)>,
) {
    let dt = time.delta_seconds();
    
    for (proj_entity, mut proj_transform, mut projectile) in &mut projectiles {
        // Update TTL
        projectile.ttl -= dt;
        if projectile.ttl <= 0.0 {
            commands.entity(proj_entity).despawn();
            continue;
        }
        
        // Move projectile
        proj_transform.translation += projectile.velocity * dt;
    }
}

fn projectile_collision_system(
    mut commands: Commands,
    projectiles: Query<(Entity, &Transform, &Projectile)>,
    mut enemies: Query<(Entity, &Transform, &mut Stats), (With<Enemy>, Without<Player>)>,
    mut player_query: Query<(Entity, &Transform, &mut Stats, &Dash), With<Player>>,
    mut particle_events: EventWriter<SpawnParticlesEvent>,
    mut audio_events: EventWriter<AudioEvent>,
) {
    for (proj_entity, proj_transform, projectile) in &projectiles {
        if projectile.from_enemy {
            // Enemy projectile - check collision with player
            if let Ok((player_entity, player_transform, mut player_stats, player_dash)) = player_query.get_single_mut() {
                if proj_transform.translation.distance(player_transform.translation) <= 0.8 {
                    // Only damage player if not in i-frames
                    if player_dash.i_timer <= 0.0 {
                        player_stats.current_health -= projectile.damage as f32;
                        player_stats.current_health = player_stats.current_health.max(0.0);
                        
                        // Add hit effect to player
                        commands.entity(player_entity).insert(HitEffect {
                            timer: 0.0,
                            duration: 0.2,
                            original_scale: player_transform.scale,
                        });
                    }
                    
                    // Always destroy projectile on hit
                    commands.entity(proj_entity).despawn();
                    // Play projectile hit audio
                    audio_events.send(AudioEvent::ProjectileHit);
                    break;
                }
            }
        } else {
            // Player projectile - check collision with enemies
            for (enemy_entity, enemy_transform, mut enemy_stats) in &mut enemies {
                if proj_transform.translation.distance(enemy_transform.translation) <= 0.7 {
                    // Hit enemy
                    enemy_stats.current_health -= projectile.damage as f32;
                    
                    // Add hit effect
                    commands.entity(enemy_entity).insert(HitEffect {
                        timer: 0.0,
                        duration: 0.4,
                        original_scale: enemy_transform.scale,
                    });
                    
                    // Spawn projectile impact particles (cyan)
                    particle_events.send(SpawnParticlesEvent {
                        position: enemy_transform.translation,
                        color: Color::rgb(0.3, 0.8, 1.0),
                        count: 6,
                    });
                    
                    // Destroy enemy if dead
                    if enemy_stats.current_health <= 0.0 {
                        commands.entity(enemy_entity).despawn();
                        // Play enemy death audio
                        audio_events.send(AudioEvent::EnemyDeath);
                    } else {
                        // Play enemy hit audio
                        audio_events.send(AudioEvent::EnemyHit);
                    }
                    
                    // Destroy projectile
                    commands.entity(proj_entity).despawn();
                    // Play projectile hit audio
                    audio_events.send(AudioEvent::ProjectileHit);
                    break;
                }
            }
        }
    }
}

fn particle_spawn_system(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut particle_events: EventReader<SpawnParticlesEvent>,
) {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    
    for event in particle_events.read() {
        for _ in 0..event.count {
            let angle = rng.gen::<f32>() * std::f32::consts::TAU;
            let speed = rng.gen_range(2.0..8.0);
            let velocity = Vec3::new(
                angle.cos() * speed,
                rng.gen_range(1.0..4.0),
                angle.sin() * speed,
            );
            
            let size = rng.gen_range(0.05..0.15);
            
            commands.spawn((
                PbrBundle {
                    mesh: meshes.add(Sphere::new(size)),
                    material: materials.add(StandardMaterial {
                        base_color: event.color,
                        emissive: (event.color * 3.0).into(),
                        ..default()
                    }),
                    transform: Transform::from_translation(event.position + Vec3::new(
                        rng.gen_range(-0.3..0.3),
                        rng.gen_range(0.1..0.5),
                        rng.gen_range(-0.3..0.3),
                    )),
                    ..default()
                },
                Particle {
                    velocity,
                    ttl: rng.gen_range(0.5..1.5),
                    fade_speed: rng.gen_range(2.0..4.0),
                    initial_scale: Vec3::splat(size),
                },
            ));
        }
    }
}

fn particle_system(
    mut commands: Commands,
    mut particles: Query<(Entity, &mut Transform, &mut Particle, &Handle<StandardMaterial>)>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    time: Res<Time>,
) {
    let dt = time.delta_seconds();
    
    for (entity, mut transform, mut particle, material_handle) in &mut particles {
        // Update lifetime
        particle.ttl -= dt;
        
        if particle.ttl <= 0.0 {
            commands.entity(entity).despawn();
            continue;
        }
        
        // Update position
        transform.translation += particle.velocity * dt;
        
        // Apply gravity
        particle.velocity.y -= 9.8 * dt;
        
        // Fade and shrink over time
        let life_ratio = particle.ttl / 1.0; // Assuming max lifetime of 1.5
        let scale_factor = life_ratio.max(0.1);
        transform.scale = particle.initial_scale * scale_factor;
        
        // Fade material (optional, can be resource intensive)
        if let Some(material) = materials.get_mut(material_handle) {
            let alpha = life_ratio;
            if let Color::Rgba { red, green, blue, .. } = material.base_color {
                material.base_color = Color::rgba(red, green, blue, alpha);
            }
        }
    }
}

fn setup_rooms(
    commands: &mut Commands,
    meshes: &mut ResMut<Assets<Mesh>>,
    materials: &mut ResMut<Assets<StandardMaterial>>,
    game_assets: Option<&GameAssets>,
) {
    let rooms = [
        (0, Vec2::new(0.0, 0.0), RoomType::Combat),     // Starting combat room
        (1, Vec2::new(25.0, 0.0), RoomType::Combat),    // Combat room 1
        (2, Vec2::new(50.0, 0.0), RoomType::Boss),      // Boss room
    ];

    // Create room boundaries
    for (id, center, room_type) in rooms {
        let room_size = Vec2::new(20.0, 20.0);
        
        // Room floor with RTX-generated 3D environment
        commands.spawn((
            PbrBundle {
                mesh: meshes.add(Plane3d::default().mesh().size(room_size.x, room_size.y)),
                material: if let Some(assets) = game_assets {
                    info!("✅ Applying RTX-generated environment texture for {:?} room", room_type);
                    materials.add(StandardMaterial {
                        base_color_texture: Some(match room_type {
                            RoomType::Start => assets.desert_oasis.clone(),
                            RoomType::Combat => assets.tomb_chamber.clone(),
                            RoomType::Boss => assets.pyramid_interior.clone(),
                            RoomType::Treasure => assets.temple_halls.clone(),
                        }),
                        alpha_mode: AlphaMode::Opaque, // No transparency for floors
                        unlit: false, // Use lighting for atmosphere
                        base_color: Color::WHITE, // Full brightness
                        ..default()
                    })
                } else {
                    materials.add(StandardMaterial {
                        base_color: match room_type {
                            RoomType::Start => Color::rgb(0.6, 0.8, 0.6),
                            RoomType::Combat => Color::rgb(0.8, 0.6, 0.6),
                            RoomType::Boss => Color::rgb(0.8, 0.6, 0.8),
                            RoomType::Treasure => Color::rgb(0.8, 0.8, 0.6),
                        },
                        ..default()
                    })
                },
                transform: Transform::from_translation(Vec3::new(center.x, -0.1, center.y)),
                ..default()
            },
            Room {
                id,
                size: room_size,
                center,
                cleared: id == 0, // Start room is already "cleared"
                room_type,
            },
        ));

        // Add atmospheric 3D environment elements
        add_room_decorations(commands, meshes, materials, game_assets, center, room_type);
        
        // Create room walls (visual boundaries)
        create_room_walls(commands, meshes, materials, center, room_size);
    }

    // Create transitions between rooms
    let transitions = [
        (0, 1, Vec3::new(12.5, 0.5, 0.0)),  // Room 0 -> Room 1
        (1, 2, Vec3::new(37.5, 0.5, 0.0)),  // Room 1 -> Room 2
    ];

    for (from_room, to_room, position) in transitions {
        commands.spawn((
            PbrBundle {
                mesh: meshes.add(Cuboid::new(2.0, 2.0, 1.0)),
                material: materials.add(StandardMaterial {
                    base_color: Color::rgb(0.2, 0.8, 1.0),
                    emissive: Color::rgb(0.1, 0.4, 0.5).into(),
                    ..default()
                }),
                transform: Transform::from_translation(position),
                ..default()
            },
            RoomTransition {
                from_room,
                to_room,
                position,
                size: Vec3::new(2.0, 2.0, 1.0),
                active: from_room == 0, // First transition starts active
            },
        ));
    }
}

fn add_room_decorations(
    commands: &mut Commands,
    meshes: &mut ResMut<Assets<Mesh>>,
    materials: &mut ResMut<Assets<StandardMaterial>>,
    game_assets: Option<&GameAssets>,
    center: Vec2,
    room_type: RoomType,
) {
    if let Some(assets) = game_assets {
        info!("✅ Adding 3D environment decorations for {:?} room", room_type);
        
        // Add torch braziers for atmospheric lighting
        let torch_positions = vec![
            Vec3::new(center.x - 8.0, 1.5, center.y - 8.0),
            Vec3::new(center.x + 8.0, 1.5, center.y - 8.0),
            Vec3::new(center.x - 8.0, 1.5, center.y + 8.0),
            Vec3::new(center.x + 8.0, 1.5, center.y + 8.0),
        ];
        
        for torch_pos in torch_positions {
            commands.spawn((
                PbrBundle {
                    mesh: meshes.add(Plane3d::default().mesh().size(2.0, 2.0)),
                    material: materials.add(StandardMaterial {
                        base_color_texture: Some(assets.torch_brazier.clone()),
                        alpha_mode: AlphaMode::Blend,
                        unlit: true, // Self-illuminated for atmospheric effect
                        double_sided: true,
                        base_color: Color::WHITE,
                        ..default()
                    }),
                    transform: Transform::from_translation(torch_pos)
                        .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_4)),
                    ..default()
                },
            ));
        }
        
        // Add room-specific decorations
        match room_type {
            RoomType::Start => {
                // Add Anubis guardian statue in start room
                commands.spawn((
                    PbrBundle {
                        mesh: meshes.add(Plane3d::default().mesh().size(3.0, 3.0)),
                        material: materials.add(StandardMaterial {
                            base_color_texture: Some(assets.anubis_guardian_statue.clone()),
                            alpha_mode: AlphaMode::Blend,
                            unlit: false,
                            double_sided: true,
                            base_color: Color::WHITE,
                            ..default()
                        }),
                        transform: Transform::from_xyz(center.x, 1.5, center.y - 5.0)
                            .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_4)),
                        ..default()
                    },
                ));
            },
            RoomType::Combat => {
                // Add stone pillars in combat rooms for cover and atmosphere
                let pillar_positions = vec![
                    Vec3::new(center.x - 6.0, 2.0, center.y),
                    Vec3::new(center.x + 6.0, 2.0, center.y),
                ];
                
                for pillar_pos in pillar_positions {
                    commands.spawn((
                        PbrBundle {
                            mesh: meshes.add(Plane3d::default().mesh().size(2.5, 2.5)),
                            material: materials.add(StandardMaterial {
                                base_color_texture: Some(assets.stone_pillar_ornate.clone()),
                                alpha_mode: AlphaMode::Blend,
                                unlit: false,
                                double_sided: true,
                                base_color: Color::WHITE,
                                ..default()
                            }),
                            transform: Transform::from_translation(pillar_pos)
                                .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_4)),
                            ..default()
                        },
                    ));
                }
            },
            RoomType::Boss => {
                // Add Egyptian wall sections in boss room
                commands.spawn((
                    PbrBundle {
                        mesh: meshes.add(Plane3d::default().mesh().size(4.0, 4.0)),
                        material: materials.add(StandardMaterial {
                            base_color_texture: Some(assets.egyptian_wall_section.clone()),
                            alpha_mode: AlphaMode::Blend,
                            unlit: false,
                            double_sided: true,
                            base_color: Color::WHITE,
                            ..default()
                        }),
                        transform: Transform::from_xyz(center.x, 2.0, center.y + 8.0)
                            .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_4)),
                        ..default()
                    },
                ));
            },
            RoomType::Treasure => {
                // Future treasure room decorations
            },
        }
    }
}

fn create_room_walls(
    commands: &mut Commands,
    meshes: &mut ResMut<Assets<Mesh>>,
    materials: &mut ResMut<Assets<StandardMaterial>>,
    center: Vec2,
    size: Vec2,
) {
    let wall_height = 3.0;
    let wall_thickness = 0.5;
    let half_size = size / 2.0;

    let wall_material = materials.add(StandardMaterial {
        base_color: Color::rgb(0.4, 0.3, 0.2),
        ..default()
    });

    // North wall
    commands.spawn(PbrBundle {
        mesh: meshes.add(Cuboid::new(size.x + wall_thickness, wall_height, wall_thickness)),
        material: wall_material.clone(),
        transform: Transform::from_translation(Vec3::new(center.x, wall_height / 2.0, center.y + half_size.y)),
        ..default()
    });

    // South wall
    commands.spawn(PbrBundle {
        mesh: meshes.add(Cuboid::new(size.x + wall_thickness, wall_height, wall_thickness)),
        material: wall_material.clone(),
        transform: Transform::from_translation(Vec3::new(center.x, wall_height / 2.0, center.y - half_size.y)),
        ..default()
    });

    // East wall (with gaps for transitions)
    commands.spawn(PbrBundle {
        mesh: meshes.add(Cuboid::new(wall_thickness, wall_height, size.y - 4.0)), // Gap for transition
        material: wall_material.clone(),
        transform: Transform::from_translation(Vec3::new(center.x + half_size.x, wall_height / 2.0, center.y + 2.0)),
        ..default()
    });
    
    commands.spawn(PbrBundle {
        mesh: meshes.add(Cuboid::new(wall_thickness, wall_height, size.y - 4.0)),
        material: wall_material.clone(),
        transform: Transform::from_translation(Vec3::new(center.x + half_size.x, wall_height / 2.0, center.y - 2.0)),
        ..default()
    });

    // West wall
    commands.spawn(PbrBundle {
        mesh: meshes.add(Cuboid::new(wall_thickness, wall_height, size.y + wall_thickness)),
        material: wall_material,
        transform: Transform::from_translation(Vec3::new(center.x - half_size.x, wall_height / 2.0, center.y)),
        ..default()
    });
}

fn room_transition_system(
    mut game_state: ResMut<GameState>,
    mut player_query: Query<&mut Transform, With<Player>>,
    transitions: Query<&RoomTransition>,
    input: Res<InputState>,
) {
    if let Ok(mut player_transform) = player_query.get_single_mut() {
        for transition in &transitions {
            if !transition.active || transition.from_room != game_state.current_room {
                continue;
            }

            let distance = player_transform.translation.distance(transition.position);
            if distance <= 2.0 && input.interact {
                // Trigger room transition
                game_state.previous_room = game_state.current_room;
                game_state.current_room = transition.to_room;
                
                // Move player to new room center
                let room_centers = [
                    Vec2::new(0.0, 0.0),   // Room 0
                    Vec2::new(25.0, 0.0),  // Room 1
                    Vec2::new(50.0, 0.0),  // Room 2
                ];
                
                if let Some(new_center) = room_centers.get(transition.to_room) {
                    player_transform.translation = Vec3::new(new_center.x - 5.0, 0.5, new_center.y);
                }
                
                break;
            }
        }
    }
}

fn room_clear_system(
    mut game_state: ResMut<GameState>,
    mut rooms: Query<&mut Room>,
    mut transitions: Query<&mut RoomTransition>,
    enemies: Query<&Enemy>,
) {
    // Check if current room should be cleared
    let enemy_count = enemies.iter().count();
    
    if enemy_count == 0 {
        // Clear current room
        for mut room in &mut rooms {
            if room.id == game_state.current_room && !room.cleared {
                room.cleared = true;
                game_state.rooms_cleared += 1;
                
                // Activate next transition
                for mut transition in &mut transitions {
                    if transition.from_room == game_state.current_room {
                        transition.active = true;
                    }
                }
            }
        }
    }
}

fn room_enemy_spawn_system(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut game_state: ResMut<GameState>,
    game_assets: Option<Res<GameAssets>>,
    true_3d_assets: Option<Res<true_3d_system::True3DAssets>>,
    rooms: Query<&Room>,
) {
    // Check if we need to spawn enemies in the current room
    if game_state.current_room < game_state.enemies_spawned.len() && 
       !game_state.enemies_spawned[game_state.current_room] {
        
        // Find current room info
        if let Some(current_room) = rooms.iter().find(|r| r.id == game_state.current_room) {
            let room_center = current_room.center;
            
            let enemy_spawns = match current_room.room_type {
                RoomType::Start => vec![], // No new enemies in start room
                RoomType::Combat => vec![
                    (Vec3::new(room_center.x + 3.0, 0.5, room_center.y + 2.0), EnemyType::Chaser),
                    (Vec3::new(room_center.x - 2.0, 0.5, room_center.y - 3.0), EnemyType::Shooter),
                    (Vec3::new(room_center.x + 1.0, 0.5, room_center.y - 1.0), EnemyType::Tank),
                ],
                RoomType::Boss => vec![
                    (Vec3::new(room_center.x, 0.5, room_center.y + 3.0), EnemyType::Tank),
                    (Vec3::new(room_center.x + 4.0, 0.5, room_center.y), EnemyType::Shooter),
                    (Vec3::new(room_center.x - 4.0, 0.5, room_center.y), EnemyType::Shooter),
                    (Vec3::new(room_center.x + 2.0, 0.5, room_center.y - 2.0), EnemyType::Chaser),
                    (Vec3::new(room_center.x - 2.0, 0.5, room_center.y - 2.0), EnemyType::Chaser),
                ],
                RoomType::Treasure => vec![], // No enemies in treasure rooms
            };
            
            for (pos, enemy_type) in enemy_spawns {
                // Use TRUE 3D models from assets/models/
                let enemy_3d_type = match enemy_type {
                    EnemyType::Chaser => true_3d_system::EnemyType::MummyGuardian,
                    EnemyType::Shooter => true_3d_system::EnemyType::EgyptianWarrior, 
                    EnemyType::Tank => true_3d_system::EnemyType::AnubisBoss,
                };
                
                let ai = match enemy_type {
                    EnemyType::Chaser => AI {
                        target_range: 12.0,
                        chase_speed: 4.0,
                        attack_cooldown: 0.0,
                        attack_timer: 0.0,
                    },
                    EnemyType::Shooter => AI {
                        target_range: 15.0,
                        chase_speed: 1.5,
                        attack_cooldown: 2.0,
                        attack_timer: 0.0,
                    },
                    EnemyType::Tank => AI {
                        target_range: 8.0,
                        chase_speed: 1.0,
                        attack_cooldown: 0.0,
                        attack_timer: 0.0,
                    },
                };
                
                let stats = match enemy_type {
                    EnemyType::Chaser => Stats {
                        max_health: 30.0,
                        current_health: 30.0,
                        max_stamina: 0.0,
                        current_stamina: 0.0,
                        speed: 4.0,
                        stamina_regen_rate: 0.0,
                    },
                    EnemyType::Shooter => Stats {
                        max_health: 40.0,
                        current_health: 40.0,
                        max_stamina: 0.0,
                        current_stamina: 0.0,
                        speed: 1.5,
                        stamina_regen_rate: 0.0,
                    },
                    EnemyType::Tank => Stats {
                        max_health: 120.0,
                        current_health: 120.0,
                        max_stamina: 0.0,
                        current_stamina: 0.0,
                        speed: 1.0,
                        stamina_regen_rate: 0.0,
                    },
                };
                
                // Spawn TRUE 3D enemy using glTF models
                if let Some(assets_3d) = &true_3d_assets {
                    true_3d_system::spawn_3d_enemy(
                        &mut commands,
                        assets_3d,
                        enemy_3d_type,
                        pos,
                        ai,
                        stats,
                    );
                    continue;
                }
                
                // Fallback to 2D sprite system
                let (mesh, material, ai, stats) = match enemy_type {
                    EnemyType::Chaser => (
                        meshes.add(Plane3d::default().mesh().size(2.5, 2.5)),
                        if let Some(assets) = &game_assets {
                            materials.add(StandardMaterial {
                                base_color_texture: Some(assets.anubis_judge.clone()),
                                alpha_mode: AlphaMode::Blend,
                                unlit: true,
                                double_sided: true,
                                ..default()
                            })
                        } else {
                            materials.add(StandardMaterial {
                                base_color: Color::rgb(0.8, 0.2, 0.2),
                                emissive: Color::rgb(0.4, 0.1, 0.1).into(),
                                ..default()
                            })
                        },
                        AI {
                            target_range: 12.0,
                            chase_speed: 4.0,
                            attack_cooldown: 0.0,
                            attack_timer: 0.0,
                        },
                        Stats {
                            max_health: 30.0,
                            current_health: 30.0,
                            max_stamina: 0.0,
                            current_stamina: 0.0,
                            speed: 4.0,
                            stamina_regen_rate: 0.0,
                        },
                    ),
                    EnemyType::Shooter => (
                        meshes.add(Plane3d::default().mesh().size(2.0, 2.0)), // Billboard for 3D sprite
                        if let Some(assets) = &game_assets {
                            materials.add(StandardMaterial {
                                base_color_texture: Some(assets.mummy_guardian.clone()),
                                alpha_mode: AlphaMode::Blend,
                                unlit: true,
                                double_sided: true,
                                ..default()
                            })
                        } else {
                            materials.add(StandardMaterial {
                                base_color: Color::rgb(0.2, 0.8, 0.2),
                                emissive: Color::rgb(0.1, 0.4, 0.1).into(),
                                ..default()
                            })
                        },
                        AI {
                            target_range: 15.0,
                            chase_speed: 1.5,
                            attack_cooldown: 2.0,
                            attack_timer: 0.0,
                        },
                        Stats {
                            max_health: 40.0,
                            current_health: 40.0,
                            max_stamina: 0.0,
                            current_stamina: 0.0,
                            speed: 1.5,
                            stamina_regen_rate: 0.0,
                        },
                    ),
                    EnemyType::Tank => (
                        meshes.add(Plane3d::default().mesh().size(2.5, 2.5)), // Larger billboard for tank
                        if let Some(assets) = &game_assets {
                            materials.add(StandardMaterial {
                                base_color_texture: Some(assets.set_chaos.clone()),
                                alpha_mode: AlphaMode::Blend,
                                unlit: true,
                                double_sided: true,
                                ..default()
                            })
                        } else {
                            materials.add(StandardMaterial {
                                base_color: Color::rgb(0.6, 0.6, 0.2),
                                emissive: Color::rgb(0.3, 0.3, 0.1).into(),
                                ..default()
                            })
                        },
                        AI {
                            target_range: 8.0,
                            chase_speed: 1.0,
                            attack_cooldown: 0.0,
                            attack_timer: 0.0,
                        },
                        Stats {
                            max_health: 120.0,
                            current_health: 120.0,
                            max_stamina: 0.0,
                            current_stamina: 0.0,
                            speed: 1.0,
                            stamina_regen_rate: 0.0,
                        },
                    ),
                };

                commands.spawn((
                    PbrBundle {
                        mesh,
                        material,
                        transform: Transform::from_translation(pos)
                            .with_rotation(Quat::from_rotation_y(std::f32::consts::FRAC_PI_4)), // Face camera for 3D effect
                        ..default()
                    },
                    Enemy,
                    enemy_type,
                    ai,
                    stats,
                ));
            }
            
            // Mark this room as having spawned enemies
            let current_room_id = game_state.current_room;
            game_state.enemies_spawned[current_room_id] = true;
        }
    }
}

fn hit_effect_system(
    mut commands: Commands,
    mut query: Query<(Entity, &mut Transform, &mut HitEffect)>,
    time: Res<Time>,
) {
    for (entity, mut transform, mut hit_effect) in &mut query {
        hit_effect.timer += time.delta_seconds();
        
        // Calculate effect progress (0.0 to 1.0)
        let progress = hit_effect.timer / hit_effect.duration;
        
        if progress < 1.0 {
            // Scale effect - pulse larger then back to normal
            let flash_intensity = (progress * 15.0).sin().abs();
            let scale_multiplier = 1.0 + flash_intensity * 0.3;
            transform.scale = hit_effect.original_scale * scale_multiplier;
        } else {
            // Effect finished - restore original state and remove component
            transform.scale = hit_effect.original_scale;
            commands.entity(entity).remove::<HitEffect>();
        }
    }
}

fn audio_system(
    _commands: Commands,
    mut audio_events: EventReader<AudioEvent>,
) {
    for event in audio_events.read() {
        // Since we don't have audio files, we'll create simple procedural audio feedback
        // In a real game, you would play actual audio files using commands.spawn(AudioBundle::from(...))
        
        // For now, we'll just spawn a simple audio bundle with default sounds
        // This creates a brief audio pulse for each event type
        match event {
            AudioEvent::AttackPrimary => {
                // Quick slash sound (high pitch, short)
                // commands.spawn(AudioBundle { /* play slash sound */ });
            },
            AudioEvent::AttackSecondary => {
                // Heavier attack sound (lower pitch, medium)
                // commands.spawn(AudioBundle { /* play heavy attack sound */ });
            },
            AudioEvent::AbilityQ => {
                // Magical cast sound (ethereal, rising pitch)
                // commands.spawn(AudioBundle { /* play magic cast sound */ });
            },
            AudioEvent::AbilityR => {
                // Explosive AoE sound (deep boom)
                // commands.spawn(AudioBundle { /* play explosion sound */ });
            },
            AudioEvent::ProjectileHit => {
                // Impact sound (sharp, brief)
                // commands.spawn(AudioBundle { /* play impact sound */ });
            },
            AudioEvent::EnemyHit => {
                // Enemy damage sound (grunt/hit)
                // commands.spawn(AudioBundle { /* play enemy hit sound */ });
            },
            AudioEvent::Dash => {
                // Whoosh sound (quick, windy)
                // commands.spawn(AudioBundle { /* play dash sound */ });
            },
            AudioEvent::EnemyDeath => {
                // Death sound (fade out, defeat)
                // commands.spawn(AudioBundle { /* play death sound */ });
            },
        }
        
        // For testing purposes, we can at least print audio events to console
        println!("Audio Event: {:?}", event);
    }
}
