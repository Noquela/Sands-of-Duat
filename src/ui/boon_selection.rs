use bevy::prelude::*;
use super::menu_system::AppState;
use super::hud_system::BoonData;
use crate::boons::{
    BoonRegistry, BoonSelectedEvent, 
    EgyptianGod, BoonRarity, Boon
};
use crate::hades_assets::HadesEgyptianAssets;

#[derive(Component)]
pub struct BoonSelectionUI;

#[derive(Component)]
pub struct BoonOption {
    pub option_index: usize,
}

#[derive(Resource)]
pub struct BoonSelectionAssets {
    pub font: Handle<Font>,
    pub selection_bg: Handle<Image>,
    pub god_portrait_ra: Handle<Image>,
    pub god_portrait_anubis: Handle<Image>,
    pub god_portrait_isis: Handle<Image>,
    pub god_portrait_set: Handle<Image>,
    pub god_portrait_thoth: Handle<Image>,
    pub boon_bg_common: Handle<Image>,
    pub boon_bg_rare: Handle<Image>,
    pub boon_bg_epic: Handle<Image>,
    pub boon_bg_legendary: Handle<Image>,
}

#[derive(Resource)]
pub struct CurrentBoonOffer {
    pub boons: Vec<Boon>,
    pub selected: bool,
}

pub struct BoonSelectionPlugin;

impl Plugin for BoonSelectionPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<CurrentBoonOffer>()
            .add_systems(Startup, load_boon_selection_assets)
            .add_systems(OnEnter(AppState::BoonSelection), setup_boon_selection)
            .add_systems(OnExit(AppState::BoonSelection), cleanup_boon_selection)
            .add_systems(Update, (
                handle_boon_selection,
                animate_boon_options,
                handle_boon_hover_effects,
                generate_boon_offer_on_enter,
            ).run_if(in_state(AppState::BoonSelection)));
    }
}

impl Default for CurrentBoonOffer {
    fn default() -> Self {
        Self {
            boons: Vec::new(),
            selected: false,
        }
    }
}

fn load_boon_selection_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading boon selection assets...");
    
    let boon_assets = BoonSelectionAssets {
        font: asset_server.load("fonts/egyptian_hieroglyphs.ttf"),
        selection_bg: asset_server.load("backgrounds/boon_selection_temple.png"),
        god_portrait_ra: asset_server.load("portraits/ra_sun_god_portrait.png"),
        god_portrait_anubis: asset_server.load("portraits/anubis_judge_portrait.png"),
        god_portrait_isis: asset_server.load("portraits/isis_mother_portrait.png"),
        god_portrait_set: asset_server.load("portraits/set_chaos_portrait.png"),
        god_portrait_thoth: asset_server.load("portraits/thoth_wisdom_portrait.png"),
        boon_bg_common: asset_server.load("ui/boon_card_common.png"),
        boon_bg_rare: asset_server.load("ui/boon_card_rare.png"),
        boon_bg_epic: asset_server.load("ui/boon_card_epic.png"),
        boon_bg_legendary: asset_server.load("ui/boon_card_legendary.png"),
    };
    
    commands.insert_resource(boon_assets);
    info!("✅ Boon selection assets loaded");
}

fn generate_boon_offer_on_enter(
    boon_registry: Option<Res<BoonRegistry>>,
    mut current_offer: ResMut<CurrentBoonOffer>,
    _commands: Commands,
) {
    if current_offer.boons.is_empty() && !current_offer.selected {
        if let Some(registry) = boon_registry {
            info!("🎯 Generating new boon offer...");
            let offer = registry.generate_offer(None, 3);
            current_offer.boons = offer.boons;
            info!("✨ Generated {} boon options", current_offer.boons.len());
        } else {
            warn!("BoonRegistry not available yet, skipping boon generation");
        }
    }
}

fn setup_boon_selection(
    mut commands: Commands,
    boon_assets: Res<BoonSelectionAssets>,
    hades_assets: Option<Res<HadesEgyptianAssets>>,
    current_offer: Res<CurrentBoonOffer>,
) {
    info!("Setting up boon selection screen...");
    
    if current_offer.boons.is_empty() {
        warn!("No boons available for selection!");
        return;
    }
    
    // Main boon selection container
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                flex_direction: FlexDirection::Column,
                ..default()
            },
            background_color: Color::rgba(0.05, 0.05, 0.1, 0.95).into(),
            ..default()
        },
        BoonSelectionUI,
    )).with_children(|parent| {
        // Background temple image
        parent.spawn(ImageBundle {
            style: Style {
                position_type: PositionType::Absolute,
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                ..default()
            },
            image: UiImage::new(boon_assets.selection_bg.clone()),
            background_color: Color::rgba(1.0, 1.0, 1.0, 0.3).into(),
            ..default()
        });
        
        // Title
        parent.spawn(TextBundle::from_section(
            "Escolha uma Bênção dos Deuses",
            TextStyle {
                font: boon_assets.font.clone(),
                font_size: 42.0,
                color: Color::rgb(0.9, 0.8, 0.4),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(50.0)),
            ..default()
        }));
        
        // Boon options container (3 options side by side)
        parent.spawn(NodeBundle {
            style: Style {
                flex_direction: FlexDirection::Row,
                column_gap: Val::Px(40.0),
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // Create 3 boon option cards
            for (index, boon) in current_offer.boons.iter().take(3).enumerate() {
                create_boon_option_card(parent, index, boon, &boon_assets, hades_assets.as_ref().map(|v| &**v));
            }
        });
        
        // Instructions
        parent.spawn(TextBundle::from_section(
            "Clique em uma bênção para selecioná-la",
            TextStyle {
                font: boon_assets.font.clone(),
                font_size: 24.0,
                color: Color::rgb(0.6, 0.5, 0.3),
            },
        ).with_style(Style {
            margin: UiRect::top(Val::Px(40.0)),
            ..default()
        }));
    });
}

fn create_boon_option_card(
    parent: &mut ChildBuilder,
    option_index: usize,
    boon: &Boon,
    boon_assets: &BoonSelectionAssets,
    hades_assets: Option<&HadesEgyptianAssets>,
) {
    // Use Hades-style assets if available, fallback to originals
    let card_bg = if let Some(hades) = hades_assets {
        hades.get_boon_frame(&boon.rarity)
    } else {
        match boon.rarity {
            BoonRarity::Common => boon_assets.boon_bg_common.clone(),
            BoonRarity::Rare => boon_assets.boon_bg_rare.clone(),
            BoonRarity::Epic => boon_assets.boon_bg_epic.clone(),
            BoonRarity::Legendary => boon_assets.boon_bg_legendary.clone(),
        }
    };
    
    // Use Hades-style god portraits if available
    let god_portrait = if let Some(hades) = hades_assets {
        hades.get_god_portrait(&boon.god)
    } else {
        match boon.god {
            EgyptianGod::Ra => boon_assets.god_portrait_ra.clone(),
            EgyptianGod::Anubis => boon_assets.god_portrait_anubis.clone(),
            EgyptianGod::Isis => boon_assets.god_portrait_isis.clone(),
            EgyptianGod::Set => boon_assets.god_portrait_set.clone(),
            EgyptianGod::Thoth => boon_assets.god_portrait_thoth.clone(),
        }
    };
    
    parent.spawn((
        ButtonBundle {
            style: Style {
                width: Val::Px(350.0),
                height: Val::Px(500.0),
                flex_direction: FlexDirection::Column,
                justify_content: JustifyContent::FlexStart,
                align_items: AlignItems::Center,
                padding: UiRect::all(Val::Px(20.0)),
                border: UiRect::all(Val::Px(4.0)),
                ..default()
            },
            border_color: boon.rarity.get_color().into(),
            background_color: Color::rgba(0.1, 0.08, 0.05, 0.9).into(),
            image: UiImage::new(card_bg),
            ..default()
        },
        BoonOption { option_index },
    )).with_children(|parent| {
        // God name
        parent.spawn(TextBundle::from_section(
            boon.god.get_display_name(),
            TextStyle {
                font: boon_assets.font.clone(),
                font_size: 28.0,
                color: boon.god.get_theme_color(),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(10.0)),
            ..default()
        }));
        
        // God portrait
        parent.spawn(NodeBundle {
            style: Style {
                width: Val::Px(120.0),
                height: Val::Px(120.0),
                margin: UiRect::bottom(Val::Px(15.0)),
                border: UiRect::all(Val::Px(3.0)),
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                ..default()
            },
            border_color: boon.god.get_theme_color().into(),
            background_color: Color::rgba(0.1, 0.08, 0.05, 0.8).into(),
            ..default()
        }).with_children(|parent| {
            parent.spawn(ImageBundle {
                style: Style {
                    width: Val::Px(110.0),
                    height: Val::Px(110.0),
                    ..default()
                },
                image: UiImage::new(god_portrait),
                ..default()
            });
        });
        
        // Boon name
        parent.spawn(TextBundle::from_section(
            &boon.name,
            TextStyle {
                font: boon_assets.font.clone(),
                font_size: 32.0,
                color: Color::rgb(0.9, 0.8, 0.4),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(10.0)),
            ..default()
        }));
        
        // Rarity indicator
        parent.spawn(TextBundle::from_section(
            boon.rarity.get_display_name(),
            TextStyle {
                font: boon_assets.font.clone(),
                font_size: 20.0,
                color: boon.rarity.get_color(),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(15.0)),
            ..default()
        }));
        
        // Description
        parent.spawn(TextBundle::from_section(
            &boon.description,
            TextStyle {
                font: boon_assets.font.clone(),
                font_size: 18.0,
                color: Color::rgb(0.8, 0.7, 0.5),
            },
        ).with_style(Style {
            max_width: Val::Px(300.0),
            ..default()
        }));
    });
}

fn handle_boon_selection(
    mut interaction_query: Query<
        (&Interaction, &BoonOption, &mut BorderColor),
        (Changed<Interaction>, With<Button>),
    >,
    mut current_offer: ResMut<CurrentBoonOffer>,
    mut boon_selection_events: EventWriter<BoonSelectedEvent>,
    mut boon_data: ResMut<BoonData>,
    mut app_state: ResMut<NextState<AppState>>,
) {
    for (interaction, boon_option, mut border_color) in &mut interaction_query {
        match *interaction {
            Interaction::Pressed => {
                if let Some(chosen_boon) = current_offer.boons.get(boon_option.option_index).cloned() {
                    info!("🌟 Selected boon: {} from {}", chosen_boon.name, chosen_boon.god.get_display_name());
                    
                    // Send boon selection event
                    boon_selection_events.send(BoonSelectedEvent {
                        boon: chosen_boon.clone(),
                    });
                    
                    // Award coins based on rarity
                    let coin_reward = match chosen_boon.rarity {
                        BoonRarity::Common => 10,
                        BoonRarity::Rare => 15,
                        BoonRarity::Epic => 25,
                        BoonRarity::Legendary => 50,
                    };
                    boon_data.coins += coin_reward;
                    
                    // Mark offer as selected and clear for next time
                    current_offer.selected = true;
                    current_offer.boons.clear();
                    
                    info!("💰 Awarded {} coins for {} boon", coin_reward, chosen_boon.rarity.get_display_name());
                    
                    // Continue to next room
                    app_state.set(AppState::InGame);
                }
            }
            Interaction::Hovered => {
                *border_color = Color::rgb(1.0, 0.9, 0.5).into();
            }
            Interaction::None => {
                if let Some(chosen_boon) = current_offer.boons.get(boon_option.option_index) {
                    *border_color = chosen_boon.rarity.get_color().into();
                }
            }
        }
    }
}

fn animate_boon_options(
    time: Res<Time>,
    mut query: Query<&mut Transform, With<BoonOption>>,
) {
    // Gentle floating animation for boon cards
    let offset = (time.elapsed_seconds() * 1.5).sin() * 5.0;
    
    for (i, mut transform) in query.iter_mut().enumerate() {
        let phase_offset = i as f32 * 0.5;
        transform.translation.y = offset + (time.elapsed_seconds() + phase_offset).sin() * 3.0;
    }
}

fn handle_boon_hover_effects(
    mut query: Query<(&Interaction, &mut BackgroundColor), (With<BoonOption>, Changed<Interaction>)>,
) {
    for (interaction, mut bg_color) in &mut query {
        match *interaction {
            Interaction::Hovered => {
                *bg_color = Color::rgba(0.15, 0.12, 0.08, 0.95).into();
            }
            Interaction::None => {
                *bg_color = Color::rgba(0.1, 0.08, 0.05, 0.9).into();
            }
            _ => {}
        }
    }
}

fn cleanup_boon_selection(
    mut commands: Commands,
    query: Query<Entity, With<BoonSelectionUI>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}