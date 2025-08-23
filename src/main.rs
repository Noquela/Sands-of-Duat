use bevy::prelude::*;
use bevy::window::{WindowResolution, PresentMode};

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
        .add_systems(Startup, setup)
        .add_systems(Update, (fps_counter_system, dash_ui_system, attack_ui_system, input_system, ai_system, combat_system, movement_system))
        .run();
}

#[derive(Component)]
struct Player;

#[derive(Component)]
struct Enemy;

#[derive(Component)]
struct AI {
    target_range: f32,
    chase_speed: f32,
}

#[derive(Component)]
struct FpsText;

#[derive(Component)]
struct DashText;

#[derive(Component)]
struct AttackText;

#[derive(Component)]
struct DashAbility {
    cooldown_timer: f32,
    cooldown_duration: f32,
    dash_distance: f32,
    dash_duration: f32,
    is_dashing: bool,
    dash_timer: f32,
    dash_direction: Vec3,
}

impl Default for DashAbility {
    fn default() -> Self {
        Self {
            cooldown_timer: 0.0,
            cooldown_duration: 1.0, // 1 second cooldown
            dash_distance: 8.0,
            dash_duration: 0.2, // 0.2 seconds dash
            is_dashing: false,
            dash_timer: 0.0,
            dash_direction: Vec3::ZERO,
        }
    }
}

#[derive(Component)]
struct Stats {
    max_health: f32,
    current_health: f32,
    speed: f32,
}

impl Default for Stats {
    fn default() -> Self {
        Self {
            max_health: 100.0,
            current_health: 100.0,
            speed: 5.0,
        }
    }
}

#[derive(Component)]
struct AttackAbility {
    cooldown_timer: f32,
    cooldown_duration: f32,
    attack_range: f32,
    damage: f32,
}

impl Default for AttackAbility {
    fn default() -> Self {
        Self {
            cooldown_timer: 0.0,
            cooldown_duration: 0.5, // 0.5 second cooldown
            attack_range: 3.0,
            damage: 25.0,
        }
    }
}

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

    // Player cube (bright green for visibility)
    commands.spawn((
        PbrBundle {
            mesh: meshes.add(Cuboid::new(1.0, 1.0, 1.0)),
            material: materials.add(StandardMaterial {
                base_color: Color::rgb(0.2, 0.8, 0.2),
                emissive: Color::rgb(0.1, 0.4, 0.1).into(),
                ..default()
            }),
            transform: Transform::from_xyz(0.0, 0.5, 0.0),
            ..default()
        },
        Player,
        DashAbility::default(),
        Stats::default(),
        AttackAbility::default(),
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

    // Attack status UI
    commands.spawn((
        TextBundle::from_sections([
            TextSection::new(
                "ATTACK: ",
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
        AttackText,
    ));

    // Controls help
    commands.spawn(
        TextBundle::from_section(
            "WASD: Move | SPACE: Dash | J: Attack",
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

    // Spawn enemies
    let enemy_positions = [
        Vec3::new(5.0, 0.5, 3.0),
        Vec3::new(-4.0, 0.5, -2.0),
        Vec3::new(2.0, 0.5, -5.0),
    ];

    for pos in enemy_positions {
        commands.spawn((
            PbrBundle {
                mesh: meshes.add(Cuboid::new(0.8, 0.8, 0.8)),
                material: materials.add(StandardMaterial {
                    base_color: Color::rgb(0.8, 0.2, 0.2),
                    emissive: Color::rgb(0.4, 0.1, 0.1).into(),
                    ..default()
                }),
                transform: Transform::from_translation(pos),
                ..default()
            },
            Enemy,
            AI {
                target_range: 10.0,
                chase_speed: 3.0,
            },
            Stats {
                max_health: 50.0,
                current_health: 50.0,
                speed: 3.0,
            },
        ));
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
    player_query: Query<&DashAbility, With<Player>>,
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

fn attack_ui_system(
    player_query: Query<&AttackAbility, With<Player>>,
    mut attack_text_query: Query<&mut Text, With<AttackText>>,
) {
    if let Ok(attack) = player_query.get_single() {
        for mut text in &mut attack_text_query {
            if attack.cooldown_timer > 0.0 {
                text.sections[1].value = format!("{:.1}s", attack.cooldown_timer);
                text.sections[1].style.color = Color::RED;
            } else {
                text.sections[1].value = "READY".to_string();
                text.sections[1].style.color = Color::GREEN;
            }
        }
    }
}

fn input_system(
    keys: Res<ButtonInput<KeyCode>>,
    mut player_query: Query<(&mut Transform, &mut DashAbility, &mut AttackAbility, &Stats), With<Player>>,
    time: Res<Time>,
) {
    for (mut transform, mut dash, mut attack, stats) in &mut player_query {
        let mut movement = Vec3::ZERO;
        
        // Movement input
        if keys.pressed(KeyCode::KeyW) {
            movement.z -= 1.0;
        }
        if keys.pressed(KeyCode::KeyS) {
            movement.z += 1.0;
        }
        if keys.pressed(KeyCode::KeyA) {
            movement.x -= 1.0;
        }
        if keys.pressed(KeyCode::KeyD) {
            movement.x += 1.0;
        }
        
        // Normalize movement vector
        movement = movement.normalize_or_zero();
        
        // Handle dash input
        if keys.just_pressed(KeyCode::Space) && !dash.is_dashing && dash.cooldown_timer <= 0.0 {
            if movement != Vec3::ZERO {
                // Start dash in movement direction
                dash.is_dashing = true;
                dash.dash_timer = dash.dash_duration;
                dash.dash_direction = movement;
                dash.cooldown_timer = dash.cooldown_duration;
            }
        }
        
        // Update dash cooldown
        if dash.cooldown_timer > 0.0 {
            dash.cooldown_timer -= time.delta_seconds();
        }
        
        // Update attack cooldown
        if attack.cooldown_timer > 0.0 {
            attack.cooldown_timer -= time.delta_seconds();
        }
        
        // Handle attack input
        if keys.just_pressed(KeyCode::KeyJ) && attack.cooldown_timer <= 0.0 {
            // Trigger attack (will be handled by combat_system)
            attack.cooldown_timer = attack.cooldown_duration;
        }
        
        // Handle dash movement
        if dash.is_dashing {
            dash.dash_timer -= time.delta_seconds();
            if dash.dash_timer > 0.0 {
                // Dash movement (faster)
                let dash_speed = dash.dash_distance / dash.dash_duration;
                transform.translation += dash.dash_direction * dash_speed * time.delta_seconds();
            } else {
                // End dash
                dash.is_dashing = false;
                dash.dash_direction = Vec3::ZERO;
            }
        } else if movement != Vec3::ZERO {
            // Normal movement
            transform.translation += movement * stats.speed * time.delta_seconds();
        }
        
        // Keep player above ground
        transform.translation.y = 0.5;
    }
}

fn ai_system(
    player_query: Query<&Transform, (With<Player>, Without<Enemy>)>,
    mut enemy_query: Query<(&mut Transform, &AI, &Stats), (With<Enemy>, Without<Player>)>,
    time: Res<Time>,
) {
    if let Ok(player_transform) = player_query.get_single() {
        for (mut enemy_transform, ai, stats) in &mut enemy_query {
            let distance = player_transform.translation.distance(enemy_transform.translation);
            
            if distance < ai.target_range && distance > 1.0 {
                // Move towards player
                let direction = (player_transform.translation - enemy_transform.translation).normalize();
                enemy_transform.translation += direction * stats.speed * time.delta_seconds();
                
                // Keep enemy above ground
                enemy_transform.translation.y = 0.5;
            }
        }
    }
}

fn combat_system(
    mut commands: Commands,
    keys: Res<ButtonInput<KeyCode>>,
    player_query: Query<(&Transform, &AttackAbility), With<Player>>,
    mut enemy_query: Query<(Entity, &mut Transform, &mut Stats), (With<Enemy>, Without<Player>)>,
) {
    if let Ok((player_transform, attack)) = player_query.get_single() {
        // Check if attack was just pressed and is off cooldown
        if keys.just_pressed(KeyCode::KeyJ) && attack.cooldown_timer <= 0.0 {
            // Find enemies within attack range
            for (entity, mut enemy_transform, mut enemy_stats) in &mut enemy_query {
                let distance = player_transform.translation.distance(enemy_transform.translation);
                
                if distance <= attack.attack_range {
                    // Apply damage
                    enemy_stats.current_health -= attack.damage;
                    
                    // Visual feedback: make enemy flash red briefly
                    enemy_transform.scale = Vec3::splat(1.2);
                    
                    // Destroy enemy if health <= 0
                    if enemy_stats.current_health <= 0.0 {
                        commands.entity(entity).despawn();
                    }
                }
            }
        }
    }
}

fn movement_system() {
    // Placeholder for more complex movement logic
}
