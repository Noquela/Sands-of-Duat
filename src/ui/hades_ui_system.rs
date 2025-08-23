use bevy::prelude::*;
use crate::ui::AppState;
use crate::components::*;

/// Hades-Quality UI System for Egyptian Theme
/// Following the Egyptian Art Bible design standards
pub struct HadesUIPlugin;

impl Plugin for HadesUIPlugin {
    fn build(&self, app: &mut App) {
        app
            .add_systems(Update, (
                hades_main_menu_system.run_if(in_state(AppState::MainMenu)),
                hades_gameplay_hud_system.run_if(in_state(AppState::InGame)),
                hades_boon_selection_system.run_if(in_state(AppState::BoonSelection)),
                hades_pause_menu_system.run_if(in_state(AppState::Paused)),
                animate_ui_elements,
                update_health_bar_animation,
                update_divine_energy_animation,
            ))
            .add_systems(OnEnter(AppState::MainMenu), setup_hades_main_menu)
            .add_systems(OnExit(AppState::MainMenu), cleanup_main_menu)
            .add_systems(OnEnter(AppState::InGame), setup_hades_gameplay_hud)
            .add_systems(OnExit(AppState::InGame), cleanup_gameplay_hud)
            .init_resource::<HadesUIResources>();
    }
}

/// Egyptian Art Bible Color Palette
pub struct EgyptianColors;

impl EgyptianColors {
    // Primary Palette - Royal Egyptian
    pub const DIVINE_GOLD: Color = Color::rgb(0.831, 0.686, 0.216);
    pub const DEEP_BLUE: Color = Color::rgb(0.098, 0.098, 0.439);
    pub const ROYAL_CRIMSON: Color = Color::rgb(0.863, 0.078, 0.235);
    
    // Secondary Palette - Desert & Death  
    pub const SAND_TONE: Color = Color::rgb(0.957, 0.643, 0.376);
    pub const MYSTICAL_EMERALD: Color = Color::rgb(0.314, 0.784, 0.471);
    pub const OBSIDIAN_BLACK: Color = Color::rgb(0.184, 0.184, 0.184);
    
    // UI Specific Colors
    pub const UI_BACKGROUND: Color = Color::rgba(0.05, 0.05, 0.1, 0.9);
    pub const UI_BORDER: Color = Color::rgb(0.831, 0.686, 0.216);
    pub const TEXT_PRIMARY: Color = Color::rgb(1.0, 0.95, 0.8);
    pub const TEXT_SECONDARY: Color = Color::rgb(0.8, 0.7, 0.5);
}

/// Hades-style UI animation components
#[derive(Component)]
pub struct HadesUIAnimation {
    pub pulse_speed: f32,
    pub glow_intensity: f32,
    pub original_scale: Vec3,
}

#[derive(Component)]
pub struct DivineHealthBar {
    pub current_health: f32,
    pub max_health: f32,
    pub animation_speed: f32,
}

#[derive(Component)]
pub struct DivineEnergyBar {
    pub current_energy: f32,
    pub max_energy: f32,
    pub recharge_rate: f32,
}

/// UI Resources for managing Hades-style interface
#[derive(Resource)]
pub struct HadesUIResources {
    pub font_hieroglyphs: Handle<Font>,
    pub font_papyrus: Handle<Font>,
    pub ui_background_texture: Handle<Image>,
    pub health_bar_texture: Handle<Image>,
    pub energy_bar_texture: Handle<Image>,
    pub boon_card_texture: Handle<Image>,
}

impl Default for HadesUIResources {
    fn default() -> Self {
        Self {
            font_hieroglyphs: Handle::default(),
            font_papyrus: Handle::default(),
            ui_background_texture: Handle::default(),
            health_bar_texture: Handle::default(),
            energy_bar_texture: Handle::default(),
            boon_card_texture: Handle::default(),
        }
    }
}

/// Setup Hades-style main menu with Egyptian theming
fn setup_hades_main_menu(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut ui_resources: ResMut<HadesUIResources>,
) {
    println!("🏺 Setting up Hades-style Egyptian main menu...");
    
    // Load Egyptian-themed fonts and textures
    ui_resources.font_hieroglyphs = asset_server.load("fonts/hieroglyphs.ttf");
    ui_resources.font_papyrus = asset_server.load("fonts/papyrus.ttf");
    ui_resources.ui_background_texture = asset_server.load("ui/papyrus_background.png");
    
    // Main menu root container
    commands
        .spawn(NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                position_type: PositionType::Absolute,
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                flex_direction: FlexDirection::Column,
                ..default()
            },
            background_color: EgyptianColors::UI_BACKGROUND.into(),
            ..default()
        })
        .with_children(|parent| {
            // Game Title with Egyptian styling
            parent
                .spawn(TextBundle::from_section(
                    "SANDS OF DUAT",
                    TextStyle {
                        font: ui_resources.font_hieroglyphs.clone(),
                        font_size: 120.0,
                        color: EgyptianColors::DIVINE_GOLD,
                    },
                ))
                .insert(HadesUIAnimation {
                    pulse_speed: 1.0,
                    glow_intensity: 1.2,
                    original_scale: Vec3::ONE,
                });
            
            // Subtitle
            parent.spawn(TextBundle::from_section(
                "Hades-like Egyptian Roguelike",
                TextStyle {
                    font: ui_resources.font_papyrus.clone(),
                    font_size: 32.0,
                    color: EgyptianColors::TEXT_SECONDARY,
                },
            ));
            
            // Menu buttons container
            parent
                .spawn(NodeBundle {
                    style: Style {
                        flex_direction: FlexDirection::Column,
                        align_items: AlignItems::Center,
                        row_gap: Val::Px(20.0),
                        margin: UiRect::top(Val::Px(80.0)),
                        ..default()
                    },
                    ..default()
                })
                .with_children(|buttons| {
                    // Start Game Button
                    create_egyptian_button(
                        buttons,
                        "BEGIN JOURNEY",
                        EgyptianColors::DIVINE_GOLD,
                        ui_resources.font_papyrus.clone(),
                    );
                    
                    // Settings Button
                    create_egyptian_button(
                        buttons,
                        "DIVINE SETTINGS",
                        EgyptianColors::MYSTICAL_EMERALD,
                        ui_resources.font_papyrus.clone(),
                    );
                    
                    // Exit Button
                    create_egyptian_button(
                        buttons,
                        "RETURN TO AFTERLIFE",
                        EgyptianColors::ROYAL_CRIMSON,
                        ui_resources.font_papyrus.clone(),
                    );
                });
        });
}

/// Create Egyptian-themed button with Hades-style design
fn create_egyptian_button(
    parent: &mut ChildBuilder,
    text: &str,
    color: Color,
    font: Handle<Font>,
) {
    parent
        .spawn(ButtonBundle {
            style: Style {
                width: Val::Px(400.0),
                height: Val::Px(80.0),
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                padding: UiRect::all(Val::Px(20.0)),
                border: UiRect::all(Val::Px(3.0)),
                ..default()
            },
            border_color: EgyptianColors::UI_BORDER.into(),
            background_color: Color::rgba(0.1, 0.1, 0.2, 0.8).into(),
            ..default()
        })
        .insert(HadesUIAnimation {
            pulse_speed: 2.0,
            glow_intensity: 1.5,
            original_scale: Vec3::ONE,
        })
        .with_children(|button| {
            button.spawn(TextBundle::from_section(
                text,
                TextStyle {
                    font: font.clone(),
                    font_size: 28.0,
                    color,
                },
            ));
        });
}

/// Setup Hades-style gameplay HUD
fn setup_hades_gameplay_hud(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    ui_resources: Res<HadesUIResources>,
) {
    println!("⚔️ Setting up Hades-style gameplay HUD...");
    
    // HUD Root Container
    commands
        .spawn(NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                position_type: PositionType::Absolute,
                ..default()
            },
            ..default()
        })
        .with_children(|parent| {
            // Top HUD Panel
            parent
                .spawn(NodeBundle {
                    style: Style {
                        width: Val::Percent(100.0),
                        height: Val::Px(120.0),
                        position_type: PositionType::Absolute,
                        top: Val::Px(0.0),
                        padding: UiRect::all(Val::Px(20.0)),
                        justify_content: JustifyContent::SpaceBetween,
                        align_items: AlignItems::Center,
                        ..default()
                    },
                    background_color: Color::rgba(0.0, 0.0, 0.0, 0.6).into(),
                    ..default()
                })
                .with_children(|top_panel| {
                    // Health Bar Container
                    create_divine_health_bar(top_panel, &ui_resources);
                    
                    // Divine Energy Bar Container  
                    create_divine_energy_bar(top_panel, &ui_resources);
                });
            
            // Bottom HUD Panel - Abilities
            parent
                .spawn(NodeBundle {
                    style: Style {
                        width: Val::Percent(100.0),
                        height: Val::Px(100.0),
                        position_type: PositionType::Absolute,
                        bottom: Val::Px(0.0),
                        justify_content: JustifyContent::Center,
                        align_items: AlignItems::Center,
                        ..default()
                    },
                    background_color: Color::rgba(0.0, 0.0, 0.0, 0.4).into(),
                    ..default()
                })
                .with_children(|bottom_panel| {
                    // Ability icons with Egyptian styling
                    create_ability_icons(bottom_panel, &ui_resources);
                });
        });
}

/// Create Egyptian-themed health bar with divine styling
fn create_divine_health_bar(parent: &mut ChildBuilder, ui_resources: &HadesUIResources) {
    parent
        .spawn(NodeBundle {
            style: Style {
                width: Val::Px(300.0),
                height: Val::Px(40.0),
                border: UiRect::all(Val::Px(2.0)),
                padding: UiRect::all(Val::Px(4.0)),
                ..default()
            },
            border_color: EgyptianColors::DIVINE_GOLD.into(),
            background_color: Color::rgba(0.0, 0.0, 0.0, 0.7).into(),
            ..default()
        })
        .insert(DivineHealthBar {
            current_health: 100.0,
            max_health: 100.0,
            animation_speed: 5.0,
        })
        .with_children(|health_container| {
            // Health bar fill
            health_container.spawn(NodeBundle {
                style: Style {
                    width: Val::Percent(100.0),
                    height: Val::Percent(100.0),
                    ..default()
                },
                background_color: EgyptianColors::ROYAL_CRIMSON.into(),
                ..default()
            });
            
            // Health text overlay
            health_container.spawn(TextBundle::from_section(
                "DIVINE HEALTH",
                TextStyle {
                    font: ui_resources.font_papyrus.clone(),
                    font_size: 16.0,
                    color: EgyptianColors::TEXT_PRIMARY,
                },
            ));
        });
}

/// Create Egyptian-themed energy bar
fn create_divine_energy_bar(parent: &mut ChildBuilder, ui_resources: &HadesUIResources) {
    parent
        .spawn(NodeBundle {
            style: Style {
                width: Val::Px(200.0),
                height: Val::Px(30.0),
                border: UiRect::all(Val::Px(2.0)),
                padding: UiRect::all(Val::Px(2.0)),
                ..default()
            },
            border_color: EgyptianColors::MYSTICAL_EMERALD.into(),
            background_color: Color::rgba(0.0, 0.0, 0.0, 0.7).into(),
            ..default()
        })
        .insert(DivineEnergyBar {
            current_energy: 50.0,
            max_energy: 100.0,
            recharge_rate: 2.0,
        })
        .with_children(|energy_container| {
            energy_container.spawn(NodeBundle {
                style: Style {
                    width: Val::Percent(50.0), // Will be animated
                    height: Val::Percent(100.0),
                    ..default()
                },
                background_color: EgyptianColors::MYSTICAL_EMERALD.into(),
                ..default()
            });
        });
}

/// Create ability icons with Egyptian theming
fn create_ability_icons(parent: &mut ChildBuilder, ui_resources: &HadesUIResources) {
    let abilities = vec![
        ("Q - Divine Cast", EgyptianColors::MYSTICAL_EMERALD),
        ("R - Pharaoh's Wrath", EgyptianColors::DIVINE_GOLD),
        ("Space - Divine Dash", EgyptianColors::DEEP_BLUE),
    ];
    
    parent
        .spawn(NodeBundle {
            style: Style {
                column_gap: Val::Px(40.0),
                ..default()
            },
            ..default()
        })
        .with_children(|abilities_container| {
            for (ability_name, color) in abilities {
                abilities_container
                    .spawn(NodeBundle {
                        style: Style {
                            width: Val::Px(80.0),
                            height: Val::Px(80.0),
                            border: UiRect::all(Val::Px(2.0)),
                            justify_content: JustifyContent::Center,
                            align_items: AlignItems::Center,
                            ..default()
                        },
                        border_color: color.into(),
                        background_color: Color::rgba(0.1, 0.1, 0.2, 0.8).into(),
                        ..default()
                    })
                    .insert(HadesUIAnimation {
                        pulse_speed: 1.5,
                        glow_intensity: 1.0,
                        original_scale: Vec3::ONE,
                    })
                    .with_children(|icon| {
                        icon.spawn(TextBundle::from_section(
                            &ability_name[0..1], // First character as icon
                            TextStyle {
                                font: ui_resources.font_hieroglyphs.clone(),
                                font_size: 32.0,
                                color,
                            },
                        ));
                    });
            }
        });
}

/// Animate UI elements with Hades-style effects
fn animate_ui_elements(
    time: Res<Time>,
    mut query: Query<(&mut Transform, &HadesUIAnimation)>,
) {
    for (mut transform, animation) in query.iter_mut() {
        // Pulse animation
        let pulse = 1.0 + (time.elapsed_seconds() * animation.pulse_speed).sin() * 0.05;
        transform.scale = animation.original_scale * pulse;
        
        // TODO: Add glow effects when Bevy supports custom shaders
    }
}

/// Update health bar animation
fn update_health_bar_animation(
    time: Res<Time>,
    mut health_bars: Query<(&DivineHealthBar, &mut BackgroundColor)>,
) {
    for (health_bar, mut bg_color) in health_bars.iter_mut() {
        let health_percentage = health_bar.current_health / health_bar.max_health;
        
        // Animate color based on health
        let color = if health_percentage > 0.6 {
            EgyptianColors::MYSTICAL_EMERALD
        } else if health_percentage > 0.3 {
            EgyptianColors::DIVINE_GOLD
        } else {
            EgyptianColors::ROYAL_CRIMSON
        };
        
        // Pulse effect when low health
        if health_percentage < 0.3 {
            let pulse = 0.8 + (time.elapsed_seconds() * 4.0).sin() * 0.2;
            bg_color.0 = Color::rgba(color.r(), color.g(), color.b(), pulse);
        } else {
            bg_color.0 = color;
        }
    }
}

/// Update divine energy animation
fn update_divine_energy_animation(
    time: Res<Time>,
    mut energy_bars: Query<&mut DivineEnergyBar>,
) {
    for mut energy_bar in energy_bars.iter_mut() {
        // Auto-regenerate energy
        if energy_bar.current_energy < energy_bar.max_energy {
            energy_bar.current_energy += energy_bar.recharge_rate * time.delta_seconds();
            energy_bar.current_energy = energy_bar.current_energy.min(energy_bar.max_energy);
        }
    }
}

// Cleanup systems
fn cleanup_main_menu(mut commands: Commands, query: Query<Entity, With<Node>>) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}

fn cleanup_gameplay_hud(mut commands: Commands, query: Query<Entity, With<Node>>) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}

// System stubs for other states
fn hades_main_menu_system() {
    // Main menu interaction logic
}

fn hades_gameplay_hud_system() {
    // Gameplay HUD updates
}

fn hades_boon_selection_system() {
    // Boon selection interface
}

fn hades_pause_menu_system() {
    // Pause menu logic
}