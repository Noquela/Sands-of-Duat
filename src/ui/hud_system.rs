use bevy::prelude::*;
use crate::{Player, Stats, Dash, Combat};

#[derive(Component)]
pub struct HudUI;

#[derive(Component)]
pub struct HealthBar;

#[derive(Component)]
pub struct EnergyBar;

#[derive(Component)]
pub struct AbilityIcon {
    pub ability_type: AbilityType,
}

#[derive(Clone, Copy)]
pub enum AbilityType {
    Dash,      // Space
    Primary,   // Q
    Secondary, // R
}

#[derive(Component)]
pub struct BoonSlot {
    pub slot_index: usize,
}

#[derive(Component)]
pub struct MiniMap;

#[derive(Component)]
pub struct CoinCounter;

#[derive(Resource)]
pub struct HudAssets {
    pub font: Handle<Font>,
    pub health_bar_bg: Handle<Image>,
    pub health_bar_fill: Handle<Image>,
    pub energy_bar_bg: Handle<Image>,
    pub energy_bar_fill: Handle<Image>,
    pub ability_frame: Handle<Image>,
    pub boon_frame_common: Handle<Image>,
    pub boon_frame_rare: Handle<Image>,
    pub boon_frame_epic: Handle<Image>,
    pub boon_frame_legendary: Handle<Image>,
    pub coin_icon: Handle<Image>,
    pub minimap_bg: Handle<Image>,
}

#[derive(Resource)]
pub struct BoonData {
    pub active_boons: Vec<ActiveBoon>,
    pub coins: u32,
}

impl Default for BoonData {
    fn default() -> Self {
        Self {
            active_boons: Vec::new(),
            coins: 0,
        }
    }
}

#[derive(Clone)]
pub struct ActiveBoon {
    pub name: String,
    pub god: EgyptianGod,
    pub rarity: BoonRarity,
    pub description: String,
    pub icon: Handle<Image>,
}

#[derive(Clone)]
pub enum EgyptianGod {
    Ra,     // Solar/Fire
    Anubis, // Death/Execute
    Isis,   // Healing/Protection
    Set,    // Chaos/Lightning
    Thoth,  // Magic/Knowledge
}

#[derive(Clone)]
pub enum BoonRarity {
    Common,
    Rare,
    Epic,
    Legendary,
}

pub struct HudSystemPlugin;

impl Plugin for HudSystemPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<BoonData>()
            .add_systems(Startup, load_hud_assets)
            .add_systems(PostStartup, setup_hud)
            .add_systems(Update, (
                update_health_bar,
                update_energy_bar,
                update_ability_cooldowns,
                update_boon_display,
                update_coin_counter,
                animate_hud_elements,
            ));
    }
}

fn load_hud_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading HUD assets for 21:9 ultrawide...");
    
    let hud_assets = HudAssets {
        font: asset_server.load("fonts/egyptian_hieroglyphs.ttf"),
        health_bar_bg: asset_server.load("ui/health_bar_bg.png"),
        health_bar_fill: asset_server.load("ui/health_bar_fill_ankh.png"),
        energy_bar_bg: asset_server.load("ui/energy_bar_bg.png"),
        energy_bar_fill: asset_server.load("ui/energy_bar_fill_scarab.png"),
        ability_frame: asset_server.load("ui/ability_frame_circular.png"),
        boon_frame_common: asset_server.load("ui/boon_frame_common.png"),
        boon_frame_rare: asset_server.load("ui/boon_frame_rare.png"),
        boon_frame_epic: asset_server.load("ui/boon_frame_epic.png"),
        boon_frame_legendary: asset_server.load("ui/boon_frame_legendary.png"),
        coin_icon: asset_server.load("ui/coin_scarab_gold.png"),
        minimap_bg: asset_server.load("ui/minimap_papyrus_frame.png"),
    };
    
    commands.insert_resource(hud_assets);
    info!("✅ HUD assets loaded");
}

fn setup_hud(
    mut commands: Commands,
    hud_assets: Res<HudAssets>,
) {
    info!("Setting up Hades-style HUD for 21:9 ultrawide...");
    
    // Main HUD container with safe margins for ultrawide
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                position_type: PositionType::Absolute,
                padding: UiRect {
                    left: Val::Px(50.0),   // Safe margin for 21:9
                    right: Val::Px(50.0),
                    top: Val::Px(30.0),
                    bottom: Val::Px(30.0),
                },
                ..default()
            },
            ..default()
        },
        HudUI,
    )).with_children(|parent| {
        // Top-left: Health and Energy bars
        parent.spawn(NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                left: Val::Px(0.0),
                top: Val::Px(0.0),
                flex_direction: FlexDirection::Column,
                row_gap: Val::Px(10.0),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // Health bar
            create_resource_bar(
                parent,
                "Vida",
                &hud_assets.health_bar_bg,
                &hud_assets.health_bar_fill,
                Color::rgb(0.8, 0.2, 0.2),
                HealthBar,
                &hud_assets,
            );
            
            // Energy bar
            create_resource_bar(
                parent,
                "Energia",
                &hud_assets.energy_bar_bg,
                &hud_assets.energy_bar_fill,
                Color::rgb(0.2, 0.4, 0.9),
                EnergyBar,
                &hud_assets,
            );
        });
        
        // Top-right: Active boons
        parent.spawn(NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                right: Val::Px(0.0),
                top: Val::Px(0.0),
                flex_direction: FlexDirection::Row,
                column_gap: Val::Px(8.0),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // Create 6 boon slots
            for i in 0..6 {
                create_boon_slot(parent, i, &hud_assets);
            }
        });
        
        // Bottom-left: Ability icons
        parent.spawn(NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                left: Val::Px(0.0),
                bottom: Val::Px(0.0),
                flex_direction: FlexDirection::Row,
                column_gap: Val::Px(15.0),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // Dash ability (Space)
            create_ability_icon(
                parent,
                AbilityType::Dash,
                "ESPAÇO",
                &hud_assets,
            );
            
            // Primary ability (Q)
            create_ability_icon(
                parent,
                AbilityType::Primary,
                "Q",
                &hud_assets,
            );
            
            // Secondary ability (R)
            create_ability_icon(
                parent,
                AbilityType::Secondary,
                "R",
                &hud_assets,
            );
        });
        
        // Bottom-right: Coin counter and minimap
        parent.spawn(NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                right: Val::Px(0.0),
                bottom: Val::Px(0.0),
                flex_direction: FlexDirection::Column,
                align_items: AlignItems::End,
                row_gap: Val::Px(10.0),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // Coin counter
            parent.spawn(NodeBundle {
                style: Style {
                    flex_direction: FlexDirection::Row,
                    align_items: AlignItems::Center,
                    column_gap: Val::Px(8.0),
                    padding: UiRect::all(Val::Px(10.0)),
                    border: UiRect::all(Val::Px(2.0)),
                    ..default()
                },
                border_color: Color::rgb(0.8, 0.6, 0.2).into(),
                background_color: Color::rgba(0.1, 0.08, 0.05, 0.8).into(),
                ..default()
            }).with_children(|parent| {
                parent.spawn(ImageBundle {
                    style: Style {
                        width: Val::Px(24.0),
                        height: Val::Px(24.0),
                        ..default()
                    },
                    image: UiImage::new(hud_assets.coin_icon.clone()),
                    ..default()
                });
                
                parent.spawn((
                    TextBundle::from_section(
                        "0",
                        TextStyle {
                            font: hud_assets.font.clone(),
                            font_size: 24.0,
                            color: Color::rgb(0.9, 0.8, 0.4),
                        },
                    ),
                    CoinCounter,
                ));
            });
            
            // Minimap
            parent.spawn((
                NodeBundle {
                    style: Style {
                        width: Val::Px(200.0),
                        height: Val::Px(150.0),
                        border: UiRect::all(Val::Px(3.0)),
                        justify_content: JustifyContent::Center,
                        align_items: AlignItems::Center,
                        ..default()
                    },
                    border_color: Color::rgb(0.8, 0.6, 0.2).into(),
                    background_color: Color::rgba(0.1, 0.08, 0.05, 0.8).into(),
                    ..default()
                },
                MiniMap,
            )).with_children(|parent| {
                parent.spawn(ImageBundle {
                    style: Style {
                        width: Val::Px(194.0),
                        height: Val::Px(144.0),
                        ..default()
                    },
                    image: UiImage::new(hud_assets.minimap_bg.clone()),
                    ..default()
                });
            });
        });
        
        // Center-top: Room progress indicator
        parent.spawn(NodeBundle {
            style: Style {
                position_type: PositionType::Absolute,
                left: Val::Percent(50.0),
                top: Val::Px(0.0),
                width: Val::Px(300.0),
                margin: UiRect::left(Val::Px(-150.0)), // Center it
                padding: UiRect::all(Val::Px(15.0)),
                border: UiRect::all(Val::Px(2.0)),
                ..default()
            },
            border_color: Color::rgb(0.8, 0.6, 0.2).into(),
            background_color: Color::rgba(0.1, 0.08, 0.05, 0.8).into(),
            ..default()
        }).with_children(|parent| {
            parent.spawn(TextBundle::from_section(
                "Câmara do Tesouro - Sala 5/12",
                TextStyle {
                    font: hud_assets.font.clone(),
                    font_size: 20.0,
                    color: Color::rgb(0.9, 0.8, 0.4),
                },
            ));
        });
    });
}

fn create_resource_bar<T: Component>(
    parent: &mut ChildBuilder,
    label: &str,
    bg_image: &Handle<Image>,
    fill_image: &Handle<Image>,
    fill_color: Color,
    marker: T,
    hud_assets: &HudAssets,
) {
    parent.spawn(NodeBundle {
        style: Style {
            flex_direction: FlexDirection::Column,
            row_gap: Val::Px(5.0),
            ..default()
        },
        ..default()
    }).with_children(|parent| {
        // Label
        parent.spawn(TextBundle::from_section(
            label,
            TextStyle {
                font: hud_assets.font.clone(),
                font_size: 18.0,
                color: Color::rgb(0.9, 0.8, 0.4),
            },
        ));
        
        // Bar container
        parent.spawn(ImageBundle {
            style: Style {
                width: Val::Px(250.0),
                height: Val::Px(30.0),
                ..default()
            },
            image: UiImage::new(bg_image.clone()),
            ..default()
        }).with_children(|parent| {
            // Fill bar
            parent.spawn((
                ImageBundle {
                    style: Style {
                        width: Val::Percent(100.0), // Will be updated
                        height: Val::Percent(100.0),
                        ..default()
                    },
                    image: UiImage::new(fill_image.clone()),
                    background_color: fill_color.into(),
                    ..default()
                },
                marker,
            ));
        });
    });
}

fn create_boon_slot(
    parent: &mut ChildBuilder,
    slot_index: usize,
    hud_assets: &HudAssets,
) {
    parent.spawn((
        NodeBundle {
            style: Style {
                width: Val::Px(50.0),
                height: Val::Px(50.0),
                border: UiRect::all(Val::Px(2.0)),
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                ..default()
            },
            border_color: Color::rgb(0.6, 0.5, 0.3).into(),
            background_color: Color::rgba(0.2, 0.15, 0.1, 0.7).into(),
            ..default()
        },
        BoonSlot { slot_index },
    )).with_children(|parent| {
        parent.spawn(ImageBundle {
            style: Style {
                width: Val::Px(46.0),
                height: Val::Px(46.0),
                ..default()
            },
            image: UiImage::new(hud_assets.boon_frame_common.clone()),
            ..default()
        });
    });
}

fn create_ability_icon(
    parent: &mut ChildBuilder,
    ability_type: AbilityType,
    key_text: &str,
    hud_assets: &HudAssets,
) {
    parent.spawn(NodeBundle {
        style: Style {
            flex_direction: FlexDirection::Column,
            align_items: AlignItems::Center,
            row_gap: Val::Px(5.0),
            ..default()
        },
        ..default()
    }).with_children(|parent| {
        // Ability icon
        parent.spawn((
            NodeBundle {
                style: Style {
                    width: Val::Px(60.0),
                    height: Val::Px(60.0),
                    border: UiRect::all(Val::Px(3.0)),
                    justify_content: JustifyContent::Center,
                    align_items: AlignItems::Center,
                    ..default()
                },
                border_color: Color::rgb(0.8, 0.6, 0.2).into(),
                background_color: Color::rgba(0.1, 0.08, 0.05, 0.9).into(),
                ..default()
            },
            AbilityIcon { ability_type },
        )).with_children(|parent| {
            parent.spawn(ImageBundle {
                style: Style {
                    width: Val::Px(54.0),
                    height: Val::Px(54.0),
                    ..default()
                },
                image: UiImage::new(hud_assets.ability_frame.clone()),
                ..default()
            });
        });
        
        // Key binding
        parent.spawn(TextBundle::from_section(
            key_text,
            TextStyle {
                font: hud_assets.font.clone(),
                font_size: 14.0,
                color: Color::rgb(0.8, 0.7, 0.5),
            },
        ));
    });
}

fn update_health_bar(
    player_query: Query<&Stats, With<Player>>,
    mut health_bar_query: Query<&mut Style, With<HealthBar>>,
) {
    if let Ok(stats) = player_query.get_single() {
        if let Ok(mut style) = health_bar_query.get_single_mut() {
            let health_percent = (stats.current_health as f32 / stats.max_health as f32) * 100.0;
            style.width = Val::Percent(health_percent);
        }
    }
}

fn update_energy_bar(
    player_query: Query<&Stats, With<Player>>,
    mut energy_bar_query: Query<&mut Style, With<EnergyBar>>,
) {
    if let Ok(stats) = player_query.get_single() {
        if let Ok(mut style) = energy_bar_query.get_single_mut() {
            // Using stamina as energy for now
            let energy_percent = (stats.current_stamina as f32 / stats.max_stamina as f32) * 100.0;
            style.width = Val::Percent(energy_percent.min(100.0));
        }
    }
}

fn update_ability_cooldowns(
    player_query: Query<(&Dash, &Combat), With<Player>>,
    mut ability_query: Query<(&mut BackgroundColor, &AbilityIcon)>,
) {
    if let Ok((dash, combat)) = player_query.get_single() {
        for (mut bg_color, ability_icon) in ability_query.iter_mut() {
            match ability_icon.ability_type {
                AbilityType::Dash => {
                    if dash.cooldown_timer > 0.0 {
                        *bg_color = Color::rgba(0.5, 0.3, 0.3, 0.8).into();
                    } else {
                        *bg_color = Color::rgba(0.1, 0.08, 0.05, 0.9).into();
                    }
                }
                AbilityType::Primary => {
                    if combat.atk_timer > 0.0 {
                        *bg_color = Color::rgba(0.5, 0.3, 0.3, 0.8).into();
                    } else {
                        *bg_color = Color::rgba(0.1, 0.08, 0.05, 0.9).into();
                    }
                }
                AbilityType::Secondary => {
                    if combat.special_cd > 0.0 {
                        *bg_color = Color::rgba(0.5, 0.3, 0.3, 0.8).into();
                    } else {
                        *bg_color = Color::rgba(0.1, 0.08, 0.05, 0.9).into();
                    }
                }
            }
        }
    }
}

fn update_boon_display(
    boon_data: Res<BoonData>,
    mut boon_slot_query: Query<(&mut UiImage, &mut BorderColor, &BoonSlot)>,
    hud_assets: Res<HudAssets>,
) {
    for (mut image, mut border_color, boon_slot) in boon_slot_query.iter_mut() {
        if let Some(boon) = boon_data.active_boons.get(boon_slot.slot_index) {
            // Update boon icon
            *image = UiImage::new(boon.icon.clone());
            
            // Update border color based on rarity
            *border_color = match boon.rarity {
                BoonRarity::Common => Color::rgb(0.6, 0.6, 0.6),
                BoonRarity::Rare => Color::rgb(0.2, 0.6, 1.0),
                BoonRarity::Epic => Color::rgb(0.8, 0.3, 1.0),
                BoonRarity::Legendary => Color::rgb(1.0, 0.8, 0.2),
            }.into();
        } else {
            // Empty slot
            *image = UiImage::new(hud_assets.boon_frame_common.clone());
            *border_color = Color::rgb(0.3, 0.25, 0.2).into();
        }
    }
}

fn update_coin_counter(
    boon_data: Res<BoonData>,
    mut coin_text_query: Query<&mut Text, With<CoinCounter>>,
) {
    if let Ok(mut text) = coin_text_query.get_single_mut() {
        text.sections[0].value = boon_data.coins.to_string();
    }
}

fn animate_hud_elements(
    time: Res<Time>,
    mut query: Query<&mut BackgroundColor, With<HealthBar>>,
) {
    // Subtle pulse animation for low health
    let pulse = 0.8 + (time.elapsed_seconds() * 4.0).sin() * 0.2;
    
    // This would be enhanced to check actual health percentage
    for mut bg_color in query.iter_mut() {
        // Apply pulsing effect when health is low
        // if health_percent < 25.0 {
        //     *bg_color = Color::rgb(0.8 * pulse, 0.2, 0.2).into();
        // }
    }
}

impl BoonRarity {
    pub fn get_color(&self) -> Color {
        match self {
            BoonRarity::Common => Color::rgb(0.6, 0.6, 0.6),
            BoonRarity::Rare => Color::rgb(0.2, 0.6, 1.0),
            BoonRarity::Epic => Color::rgb(0.8, 0.3, 1.0),
            BoonRarity::Legendary => Color::rgb(1.0, 0.8, 0.2),
        }
    }
    
    pub fn get_name(&self) -> &str {
        match self {
            BoonRarity::Common => "Comum",
            BoonRarity::Rare => "Raro",
            BoonRarity::Epic => "Épico",
            BoonRarity::Legendary => "Lendário",
        }
    }
}

impl EgyptianGod {
    pub fn get_color(&self) -> Color {
        match self {
            EgyptianGod::Ra => Color::rgb(1.0, 0.8, 0.2),      // Golden
            EgyptianGod::Anubis => Color::rgb(0.2, 0.2, 0.2),  // Dark
            EgyptianGod::Isis => Color::rgb(0.2, 0.8, 0.6),    // Teal
            EgyptianGod::Set => Color::rgb(0.8, 0.2, 0.2),     // Red
            EgyptianGod::Thoth => Color::rgb(0.4, 0.2, 0.8),   // Purple
        }
    }
    
    pub fn get_name(&self) -> &str {
        match self {
            EgyptianGod::Ra => "Rá",
            EgyptianGod::Anubis => "Anúbis",
            EgyptianGod::Isis => "Ísis",
            EgyptianGod::Set => "Set",
            EgyptianGod::Thoth => "Thoth",
        }
    }
}