use bevy::prelude::*;

#[derive(Debug, Clone, Copy, Default, Eq, PartialEq, Hash, States)]
pub enum AppState {
    #[default]
    MainMenu,
    Settings,
    Loading,
    InGame,
    Paused,
    RoomTransition,
    BoonSelection,
    Death,
    MetaProgression,
}

#[derive(Component)]
pub struct MainMenuUI;

#[derive(Component)]
pub struct SettingsMenuUI;

#[derive(Component)]
pub struct LoadingScreenUI;

#[derive(Component)]
pub struct PauseMenuUI;

#[derive(Component)]
pub struct DeathScreenUI;

#[derive(Component)]
pub struct MetaProgressionUI;

#[derive(Resource)]
pub struct MenuAssets {
    pub font: Handle<Font>,
    pub button_normal: Handle<Image>,
    pub button_hovered: Handle<Image>,
    pub button_pressed: Handle<Image>,
    pub background_main: Handle<Image>,
    pub background_settings: Handle<Image>,
    pub logo: Handle<Image>,
}

// Button interaction system
#[derive(Component)]
pub struct MenuButton {
    pub action: ButtonAction,
}

#[derive(Clone, Copy, Debug)]
pub enum ButtonAction {
    NewGame,
    Settings,
    Quit,
    Back,
    Resume,
    MainMenu,
    ToggleFullscreen,
    VolumeUp,
    VolumeDown,
    ResetProgress,
}

pub struct MenuSystemPlugin;

impl Plugin for MenuSystemPlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<AppState>()
            .add_systems(Startup, load_menu_assets)
            .add_systems(OnEnter(AppState::MainMenu), setup_main_menu)
            .add_systems(OnExit(AppState::MainMenu), cleanup_main_menu)
            .add_systems(OnEnter(AppState::Settings), setup_settings_menu)
            .add_systems(OnExit(AppState::Settings), cleanup_settings_menu)
            .add_systems(OnEnter(AppState::Loading), setup_loading_screen)
            .add_systems(OnExit(AppState::Loading), cleanup_loading_screen)
            .add_systems(OnEnter(AppState::Death), setup_death_screen)
            .add_systems(OnExit(AppState::Death), cleanup_death_screen)
            .add_systems(Update, (
                button_interaction_system,
                animate_menu_elements,
                handle_menu_input,
            ).run_if(not(in_state(AppState::InGame))))
            .add_systems(Update, auto_complete_loading.run_if(in_state(AppState::Loading)));
    }
}

fn load_menu_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading menu assets...");
    
    let menu_assets = MenuAssets {
        font: asset_server.load("fonts/egyptian_hieroglyphs.ttf"),
        button_normal: asset_server.load("ui/button_papyrus_normal.png"),
        button_hovered: asset_server.load("ui/button_papyrus_hovered.png"),
        button_pressed: asset_server.load("ui/button_papyrus_pressed.png"),
        background_main: asset_server.load("backgrounds/menu_background_4k.png"),
        background_settings: asset_server.load("backgrounds/settings_background_4k.png"),
        logo: asset_server.load("ui/sands_of_duat_logo.png"),
    };
    
    commands.insert_resource(menu_assets);
    info!("✅ Menu assets loaded");
}

fn setup_main_menu(
    mut commands: Commands,
    menu_assets: Res<MenuAssets>,
) {
    info!("Setting up main menu...");
    
    // Root container for 21:9 ultrawide
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                ..default()
            },
            background_color: Color::rgb(0.05, 0.05, 0.1).into(),
            ..default()
        },
        MainMenuUI,
    )).with_children(|parent| {
        // Background image
        parent.spawn(ImageBundle {
            style: Style {
                position_type: PositionType::Absolute,
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                ..default()
            },
            image: UiImage::new(menu_assets.background_main.clone()),
            ..default()
        });
        
        // Title/Logo
        parent.spawn(ImageBundle {
            style: Style {
                width: Val::Px(800.0),
                height: Val::Px(200.0),
                margin: UiRect::all(Val::Px(50.0)),
                ..default()
            },
            image: UiImage::new(menu_assets.logo.clone()),
            ..default()
        });
        
        // Menu buttons container
        parent.spawn(NodeBundle {
            style: Style {
                flex_direction: FlexDirection::Column,
                align_items: AlignItems::Center,
                row_gap: Val::Px(20.0),
                margin: UiRect::top(Val::Px(100.0)),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // New Game button
            create_menu_button(
                parent,
                "Novo Jogo",
                ButtonAction::NewGame,
                &menu_assets,
            );
            
            // Settings button
            create_menu_button(
                parent,
                "Configurações",
                ButtonAction::Settings,
                &menu_assets,
            );
            
            // Quit button
            create_menu_button(
                parent,
                "Sair",
                ButtonAction::Quit,
                &menu_assets,
            );
        });
        
        // Version info (bottom corner)
        parent.spawn(TextBundle::from_section(
            "Sands of Duat v0.5.0 - Hades-like Egyptian Roguelike",
            TextStyle {
                font: menu_assets.font.clone(),
                font_size: 24.0,
                color: Color::rgb(0.7, 0.7, 0.7),
            },
        ).with_style(Style {
            position_type: PositionType::Absolute,
            bottom: Val::Px(20.0),
            left: Val::Px(20.0),
            ..default()
        }));
    });
}

fn create_menu_button(
    parent: &mut ChildBuilder,
    text: &str,
    action: ButtonAction,
    menu_assets: &MenuAssets,
) {
    parent.spawn((
        ButtonBundle {
            style: Style {
                width: Val::Px(400.0),
                height: Val::Px(80.0),
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                margin: UiRect::all(Val::Px(5.0)),
                border: UiRect::all(Val::Px(3.0)),
                ..default()
            },
            border_color: Color::rgb(0.8, 0.6, 0.2).into(),
            background_color: Color::rgb(0.2, 0.15, 0.1).into(),
            image: UiImage::new(menu_assets.button_normal.clone()),
            ..default()
        },
        MenuButton { action },
    )).with_children(|parent| {
        parent.spawn(TextBundle::from_section(
            text,
            TextStyle {
                font: menu_assets.font.clone(),
                font_size: 32.0,
                color: Color::rgb(0.9, 0.8, 0.4),
            },
        ));
    });
}

fn setup_settings_menu(
    mut commands: Commands,
    menu_assets: Res<MenuAssets>,
) {
    info!("Setting up settings menu...");
    
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                ..default()
            },
            background_color: Color::rgb(0.05, 0.05, 0.1).into(),
            ..default()
        },
        SettingsMenuUI,
    )).with_children(|parent| {
        // Background
        parent.spawn(ImageBundle {
            style: Style {
                position_type: PositionType::Absolute,
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                ..default()
            },
            image: UiImage::new(menu_assets.background_settings.clone()),
            ..default()
        });
        
        // Title
        parent.spawn(TextBundle::from_section(
            "Configurações",
            TextStyle {
                font: menu_assets.font.clone(),
                font_size: 48.0,
                color: Color::rgb(0.9, 0.8, 0.4),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(50.0)),
            ..default()
        }));
        
        // Settings options
        parent.spawn(NodeBundle {
            style: Style {
                flex_direction: FlexDirection::Column,
                align_items: AlignItems::Center,
                row_gap: Val::Px(20.0),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            // Volume controls
            parent.spawn(NodeBundle {
                style: Style {
                    flex_direction: FlexDirection::Row,
                    align_items: AlignItems::Center,
                    column_gap: Val::Px(20.0),
                    ..default()
                },
                ..default()
            }).with_children(|parent| {
                parent.spawn(TextBundle::from_section(
                    "Volume:",
                    TextStyle {
                        font: menu_assets.font.clone(),
                        font_size: 28.0,
                        color: Color::rgb(0.8, 0.7, 0.5),
                    },
                ));
                
                // Volume down
                create_menu_button(
                    parent,
                    "-",
                    ButtonAction::VolumeDown,
                    &menu_assets,
                );
                
                // Volume indicator (placeholder)
                parent.spawn(TextBundle::from_section(
                    "70%",
                    TextStyle {
                        font: menu_assets.font.clone(),
                        font_size: 28.0,
                        color: Color::rgb(0.9, 0.8, 0.4),
                    },
                ));
                
                // Volume up
                create_menu_button(
                    parent,
                    "+",
                    ButtonAction::VolumeUp,
                    &menu_assets,
                );
            });
            
            // Fullscreen toggle
            create_menu_button(
                parent,
                "Alternar Tela Cheia",
                ButtonAction::ToggleFullscreen,
                &menu_assets,
            );
            
            // Resolution info
            parent.spawn(TextBundle::from_section(
                "Resolução: 3440x1440 (21:9 Ultrawide)",
                TextStyle {
                    font: menu_assets.font.clone(),
                    font_size: 24.0,
                    color: Color::rgb(0.7, 0.6, 0.4),
                },
            ));
            
            // Back button
            create_menu_button(
                parent,
                "Voltar",
                ButtonAction::Back,
                &menu_assets,
            );
        });
    });
}

fn setup_loading_screen(
    mut commands: Commands,
    menu_assets: Res<MenuAssets>,
) {
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
            background_color: Color::rgb(0.05, 0.05, 0.1).into(),
            ..default()
        },
        LoadingScreenUI,
    )).with_children(|parent| {
        // Loading text
        parent.spawn(TextBundle::from_section(
            "Carregando...",
            TextStyle {
                font: menu_assets.font.clone(),
                font_size: 36.0,
                color: Color::rgb(0.9, 0.8, 0.4),
            },
        ));
        
        // Loading bar (placeholder)
        parent.spawn(NodeBundle {
            style: Style {
                width: Val::Px(600.0),
                height: Val::Px(20.0),
                margin: UiRect::top(Val::Px(20.0)),
                border: UiRect::all(Val::Px(2.0)),
                ..default()
            },
            border_color: Color::rgb(0.8, 0.6, 0.2).into(),
            background_color: Color::rgb(0.2, 0.15, 0.1).into(),
            ..default()
        });
    });
}

fn setup_death_screen(
    mut commands: Commands,
    menu_assets: Res<MenuAssets>,
) {
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
            background_color: Color::rgba(0.1, 0.05, 0.05, 0.9).into(),
            ..default()
        },
        DeathScreenUI,
    )).with_children(|parent| {
        // Death message
        parent.spawn(TextBundle::from_section(
            "Você foi derrotado pelos Guardiões do Duat",
            TextStyle {
                font: menu_assets.font.clone(),
                font_size: 42.0,
                color: Color::rgb(0.9, 0.3, 0.3),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(30.0)),
            ..default()
        }));
        
        // Run stats
        parent.spawn(TextBundle::from_section(
            "Salas Completadas: 5\nInimigos Derrotados: 23\nBoons Coletados: 7",
            TextStyle {
                font: menu_assets.font.clone(),
                font_size: 24.0,
                color: Color::rgb(0.8, 0.7, 0.5),
            },
        ).with_style(Style {
            margin: UiRect::bottom(Val::Px(40.0)),
            ..default()
        }));
        
        // Buttons
        parent.spawn(NodeBundle {
            style: Style {
                flex_direction: FlexDirection::Row,
                column_gap: Val::Px(30.0),
                ..default()
            },
            ..default()
        }).with_children(|parent| {
            create_menu_button(
                parent,
                "Tentar Novamente",
                ButtonAction::NewGame,
                &menu_assets,
            );
            
            create_menu_button(
                parent,
                "Menu Principal",
                ButtonAction::MainMenu,
                &menu_assets,
            );
        });
    });
}

fn button_interaction_system(
    mut interaction_query: Query<
        (&Interaction, &mut BackgroundColor, &MenuButton, &mut BorderColor),
        (Changed<Interaction>, With<Button>),
    >,
    mut app_state: ResMut<NextState<AppState>>,
    mut exit: EventWriter<bevy::app::AppExit>,
) {
    for (interaction, mut color, menu_button, mut border_color) in &mut interaction_query {
        match *interaction {
            Interaction::Pressed => {
                *color = Color::rgb(0.4, 0.3, 0.2).into();
                *border_color = Color::rgb(1.0, 0.8, 0.3).into();
                
                match menu_button.action {
                    ButtonAction::NewGame => {
                        info!("Starting new game...");
                        app_state.set(AppState::Loading);
                    },
                    ButtonAction::Settings => {
                        info!("Opening settings...");
                        app_state.set(AppState::Settings);
                    },
                    ButtonAction::Quit => {
                        info!("Quitting game...");
                        exit.send(bevy::app::AppExit);
                    },
                    ButtonAction::Back => {
                        info!("Going back...");
                        app_state.set(AppState::MainMenu);
                    },
                    ButtonAction::MainMenu => {
                        info!("Returning to main menu...");
                        app_state.set(AppState::MainMenu);
                    },
                    _ => {
                        info!("Button action not implemented: {:?}", menu_button.action);
                    }
                }
            }
            Interaction::Hovered => {
                *color = Color::rgb(0.3, 0.2, 0.15).into();
                *border_color = Color::rgb(1.0, 0.8, 0.4).into();
            }
            Interaction::None => {
                *color = Color::rgb(0.2, 0.15, 0.1).into();
                *border_color = Color::rgb(0.8, 0.6, 0.2).into();
            }
        }
    }
}

fn animate_menu_elements(
    time: Res<Time>,
    mut query: Query<&mut Style, With<MainMenuUI>>,
) {
    // Subtle breathing animation for menu elements
    let scale = 1.0 + (time.elapsed_seconds() * 2.0).sin() * 0.02;
    
    for mut style in query.iter_mut() {
        // Apply subtle scale animation
        // This would need Transform component for actual scaling
    }
}

fn handle_menu_input(
    keys: Res<ButtonInput<KeyCode>>,
    mut app_state: ResMut<NextState<AppState>>,
    current_state: Res<State<AppState>>,
) {
    if keys.just_pressed(KeyCode::Escape) {
        match current_state.get() {
            AppState::Settings => app_state.set(AppState::MainMenu),
            AppState::InGame => app_state.set(AppState::Paused),
            AppState::Paused => app_state.set(AppState::InGame),
            _ => {}
        }
    }
}

// Cleanup functions
fn cleanup_main_menu(
    mut commands: Commands,
    query: Query<Entity, With<MainMenuUI>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}

fn cleanup_settings_menu(
    mut commands: Commands,
    query: Query<Entity, With<SettingsMenuUI>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}

fn cleanup_loading_screen(
    mut commands: Commands,
    query: Query<Entity, With<LoadingScreenUI>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}

fn auto_complete_loading(
    time: Res<Time>,
    mut app_state: ResMut<NextState<AppState>>,
    mut timer: Local<f32>,
) {
    *timer += time.delta_seconds();
    
    // Transition to game after 2 seconds of loading
    if *timer >= 2.0 {
        info!("Loading complete, transitioning to game...");
        app_state.set(AppState::InGame);
    }
}

fn cleanup_death_screen(
    mut commands: Commands,
    query: Query<Entity, With<DeathScreenUI>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn_recursive();
    }
}