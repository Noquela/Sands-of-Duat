use bevy::prelude::*;
use super::menu_system::AppState;

#[derive(Component)]
pub struct RoomTransitionUI;

#[derive(Component)]
pub struct TransitionEffect;

#[derive(Resource)]
pub struct TransitionAssets {
    pub font: Handle<Font>,
    pub transition_bg: Handle<Image>,
    pub completion_seal: Handle<Image>,
}

#[derive(Resource)]
pub struct TransitionData {
    pub rooms_completed: u32,
    pub total_rooms: u32,
    pub enemies_defeated: u32,
    pub room_type: String,
    pub next_room_type: String,
}

impl Default for TransitionData {
    fn default() -> Self {
        Self {
            rooms_completed: 1,
            total_rooms: 12,
            enemies_defeated: 5,
            room_type: "Câmara de Combate".to_string(),
            next_room_type: "Tesouro Egípcio".to_string(),
        }
    }
}

pub struct TransitionSystemPlugin;

impl Plugin for TransitionSystemPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<TransitionData>()
            .add_systems(Startup, load_transition_assets)
            .add_systems(OnEnter(AppState::RoomTransition), setup_room_transition)
            .add_systems(OnExit(AppState::RoomTransition), cleanup_room_transition)
            .add_systems(Update, (
                animate_transition_effects,
                handle_transition_input,
                auto_advance_transition,
            ).run_if(in_state(AppState::RoomTransition)));
    }
}

fn load_transition_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading transition assets...");
    
    let transition_assets = TransitionAssets {
        font: asset_server.load("fonts/egyptian_hieroglyphs.ttf"),
        transition_bg: asset_server.load("backgrounds/papyrus_transition.png"),
        completion_seal: asset_server.load("ui/room_complete_ankh_seal.png"),
    };
    
    commands.insert_resource(transition_assets);
    info!("✅ Transition assets loaded");
}

fn setup_room_transition(
    mut commands: Commands,
    transition_assets: Res<TransitionAssets>,
    transition_data: Res<TransitionData>,
) {
    info!("Setting up room transition screen...");
    
    // Main transition container
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
        RoomTransitionUI,
    )).with_children(|parent| {
        // Background papyrus effect
        parent.spawn((
            ImageBundle {
                style: Style {
                    position_type: PositionType::Absolute,
                    width: Val::Percent(100.0),
                    height: Val::Percent(100.0),
                    ..default()
                },
                image: UiImage::new(transition_assets.transition_bg.clone()),
                background_color: Color::rgba(1.0, 1.0, 1.0, 0.1).into(),
                ..default()
            },
            TransitionEffect,
        ));
        
        // Room completed seal
        parent.spawn((
            ImageBundle {
                style: Style {
                    width: Val::Px(150.0),
                    height: Val::Px(150.0),
                    margin: UiRect::bottom(Val::Px(30.0)),
                    ..default()
                },
                image: UiImage::new(transition_assets.completion_seal.clone()),
                ..default()
            },
            TransitionEffect,
        ));
        
        // "Room Cleared" text
        parent.spawn((
            TextBundle::from_section(
                format!("{} Limpa!", transition_data.room_type),
                TextStyle {
                    font: transition_assets.font.clone(),
                    font_size: 48.0,
                    color: Color::rgb(0.9, 0.8, 0.4),
                },
            ).with_style(Style {
                margin: UiRect::bottom(Val::Px(20.0)),
                ..default()
            }),
            TransitionEffect,
        ));
        
        // Progress indicator
        parent.spawn(TextBundle::from_section(
            format!("Sala {} de {} • {} Inimigos Derrotados", 
                   transition_data.rooms_completed, 
                   transition_data.total_rooms,
                   transition_data.enemies_defeated),
            TextStyle {
                font: transition_assets.font.clone(),
                font_size: 24.0,
                color: Color::rgb(0.7, 0.6, 0.4),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(40.0)),
            ..default()
        }));
        
        // Next room preview
        parent.spawn(NodeBundle {
            style: Style {
                padding: UiRect::all(Val::Px(20.0)),
                border: UiRect::all(Val::Px(2.0)),
                margin: UiRect::bottom(Val::Px(30.0)),
                ..default()
            },
            border_color: Color::rgb(0.8, 0.6, 0.2).into(),
            background_color: Color::rgba(0.1, 0.08, 0.05, 0.8).into(),
            ..default()
        }).with_children(|parent| {
            parent.spawn(TextBundle::from_section(
                format!("Próxima Sala: {}", transition_data.next_room_type),
                TextStyle {
                    font: transition_assets.font.clone(),
                    font_size: 28.0,
                    color: Color::rgb(0.9, 0.8, 0.4),
                },
            ));
        });
        
        // Continue prompt
        parent.spawn((
            TextBundle::from_section(
                "Pressione ESPAÇO para continuar...",
                TextStyle {
                    font: transition_assets.font.clone(),
                    font_size: 20.0,
                    color: Color::rgb(0.6, 0.5, 0.3),
                },
            ),
            TransitionEffect,
        ));
    });
}

fn animate_transition_effects(
    time: Res<Time>,
    mut query: Query<&mut Transform, With<TransitionEffect>>,
) {
    let scale_factor = 1.0 + (time.elapsed_seconds() * 2.0).sin() * 0.05;
    
    for mut transform in query.iter_mut() {
        // Subtle breathing animation for transition elements
        transform.scale = Vec3::splat(scale_factor);
    }
}

fn handle_transition_input(
    keys: Res<ButtonInput<KeyCode>>,
    mouse: Res<ButtonInput<MouseButton>>,
    mut app_state: ResMut<NextState<AppState>>,
) {
    if keys.just_pressed(KeyCode::Space) || 
       keys.just_pressed(KeyCode::Enter) ||
       mouse.just_pressed(MouseButton::Left) {
        info!("Advancing from room transition...");
        app_state.set(AppState::InGame);
    }
}

fn auto_advance_transition(
    time: Res<Time>,
    mut app_state: ResMut<NextState<AppState>>,
    mut timer: Local<Option<Timer>>,
) {
    // Auto-advance after 5 seconds if player doesn't interact
    if timer.is_none() {
        *timer = Some(Timer::from_seconds(5.0, TimerMode::Once));
    }
    
    if let Some(ref mut timer) = timer.as_mut() {
        timer.tick(time.delta());
        if timer.finished() {
            info!("Auto-advancing from room transition...");
            app_state.set(AppState::InGame);
        }
    }
}

fn cleanup_room_transition(
    mut commands: Commands,
    query: Query<Entity, With<RoomTransitionUI>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}