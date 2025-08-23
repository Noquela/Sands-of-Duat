use bevy::prelude::*;
use bevy::window::{WindowResolution, PresentMode};

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
        .init_resource::<InputState>()
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

fn setup(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
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

    // Player (Hades-style capsule)
    commands.spawn((
        PbrBundle {
            mesh: meshes.add(Capsule3d::new(0.4, 1.0)),
            material: materials.add(StandardMaterial {
                base_color: Color::rgb(0.85, 0.9, 1.0),
                emissive: Color::rgb(0.1, 0.2, 0.3).into(),
                ..default()
            }),
            transform: Transform::from_xyz(0.0, 0.5, 0.0),
            ..default()
        },
        Player,
        Stats::default(),
        Dash::default(),
        Combat::default(),
    ));

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
            "WASD: Move | SPACE: Dash | LMB: Attack | RMB: Special | Q: Cast | R: AoE",
            TextStyle {
                font_size: 24.0,
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

    // Spawn different types of enemies
    let enemy_spawns = [
        (Vec3::new(5.0, 0.5, 3.0), EnemyType::Chaser),
        (Vec3::new(-4.0, 0.5, -2.0), EnemyType::Shooter),
        (Vec3::new(2.0, 0.5, -5.0), EnemyType::Tank),
        (Vec3::new(-6.0, 0.5, 4.0), EnemyType::Chaser),
        (Vec3::new(7.0, 0.5, -3.0), EnemyType::Shooter),
    ];

    for (pos, enemy_type) in enemy_spawns {
        let (mesh, material, ai, stats) = match enemy_type {
            EnemyType::Chaser => {
                // Fast, weak chaser
                (
                    meshes.add(Cuboid::new(0.8, 0.8, 0.8)),
                    materials.add(StandardMaterial {
                        base_color: Color::rgb(0.8, 0.2, 0.2),
                        emissive: Color::rgb(0.4, 0.1, 0.1).into(),
                        ..default()
                    }),
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
                // Ranged shooter
                (
                    meshes.add(Cuboid::new(0.7, 1.2, 0.7)),
                    materials.add(StandardMaterial {
                        base_color: Color::rgb(0.2, 0.8, 0.2),
                        emissive: Color::rgb(0.1, 0.4, 0.1).into(),
                        ..default()
                    }),
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
                // Slow, heavy tank
                (
                    meshes.add(Cuboid::new(1.2, 1.2, 1.2)),
                    materials.add(StandardMaterial {
                        base_color: Color::rgb(0.6, 0.6, 0.2),
                        emissive: Color::rgb(0.3, 0.3, 0.1).into(),
                        ..default()
                    }),
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
                transform: Transform::from_translation(pos),
                ..default()
            },
            Enemy,
            enemy_type,
            ai,
            stats,
        ));
    }
}

fn read_input(
    kb: Res<ButtonInput<KeyCode>>,
    mouse: Res<ButtonInput<MouseButton>>,
    mut input_state: ResMut<InputState>,
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
                
                hits += 1;
                if enemy_stats.current_health <= 0.0 {
                    commands.entity(entity).despawn();
                }
            }
        }
        
        if hits > 0 {
            combat.chain_step = (combat.chain_step + 1) % 3;
            combat.atk_timer = combat.atk_cd;
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
                
                hits += 1;
                if enemy_stats.current_health <= 0.0 {
                    commands.entity(entity).despawn();
                }
            }
        }
        
        if hits > 0 {
            combat.special_timer = combat.special_cd;
        }
    }

    // Q ABILITY - Cast projectile
    if input.ability_q && combat.q_timer <= 0.0 {
        let direction = Vec3::new(0.0, 0.0, -1.0); // Forward direction (MVP)
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
                
                hits += 1;
                if enemy_stats.current_health <= 0.0 {
                    commands.entity(entity).despawn();
                }
            }
        }
        
        if hits > 0 {
            combat.r_timer = combat.r_cd;
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
                    
                    // Destroy enemy if dead
                    if enemy_stats.current_health <= 0.0 {
                        commands.entity(enemy_entity).despawn();
                    }
                    
                    // Destroy projectile
                    commands.entity(proj_entity).despawn();
                    break;
                }
            }
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
