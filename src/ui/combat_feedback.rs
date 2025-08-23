use bevy::prelude::*;
use crate::{Player, Combat, Stats};

#[derive(Component)]
pub struct CombatFeedbackUI;

#[derive(Component)]
pub struct DamageNumber {
    pub lifetime: Timer,
    pub velocity: Vec3,
    pub damage_type: DamageType,
}

#[derive(Component)]
pub struct HitEffect {
    pub lifetime: Timer,
    pub scale_curve: f32,
}

#[derive(Component)]
pub struct ScreenShake {
    pub intensity: f32,
    pub duration: Timer,
}

#[derive(Clone, Copy, PartialEq)]
pub enum DamageType {
    Player,
    Enemy,
    Critical,
    Heal,
}

#[derive(Resource)]
pub struct CombatFeedbackAssets {
    pub font: Handle<Font>,
    pub hit_particle: Handle<Image>,
    pub critical_effect: Handle<Image>,
    pub blood_splatter: Handle<Image>,
    pub heal_sparkle: Handle<Image>,
}

#[derive(Event)]
pub struct DamageEvent {
    pub position: Vec3,
    pub damage: i32,
    pub damage_type: DamageType,
    pub is_critical: bool,
}

#[derive(Event)]
pub struct HitStopEvent {
    pub duration: f32,
}

#[derive(Event)]
pub struct ScreenShakeEvent {
    pub intensity: f32,
    pub duration: f32,
}

pub struct CombatFeedbackPlugin;

impl Plugin for CombatFeedbackPlugin {
    fn build(&self, app: &mut App) {
        app.add_event::<DamageEvent>()
            .add_event::<HitStopEvent>()
            .add_event::<ScreenShakeEvent>()
            .add_systems(Startup, load_combat_feedback_assets)
            .add_systems(PostStartup, setup_combat_feedback_ui)
            .add_systems(Update, (
                handle_damage_events,
                update_damage_numbers,
                handle_hit_effects,
                apply_screen_shake,
                handle_hit_stop,
                cleanup_expired_effects,
                create_hit_particles,
            ));
    }
}

fn load_combat_feedback_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("Loading combat feedback assets...");
    
    let feedback_assets = CombatFeedbackAssets {
        font: asset_server.load("fonts/egyptian_hieroglyphs.ttf"),
        hit_particle: asset_server.load("effects/hit_spark_particle.png"),
        critical_effect: asset_server.load("effects/critical_hit_burst.png"),
        blood_splatter: asset_server.load("effects/blood_splatter_egyptian.png"),
        heal_sparkle: asset_server.load("effects/heal_sparkle_ankh.png"),
    };
    
    commands.insert_resource(feedback_assets);
    info!("✅ Combat feedback assets loaded");
}

fn setup_combat_feedback_ui(
    mut commands: Commands,
) {
    // Spawn UI container for damage numbers and effects
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                position_type: PositionType::Absolute,
                ..default()
            },
            ..default()
        },
        CombatFeedbackUI,
    ));
}

fn handle_damage_events(
    mut commands: Commands,
    mut damage_events: EventReader<DamageEvent>,
    mut screen_shake_events: EventWriter<ScreenShakeEvent>,
    mut hit_stop_events: EventWriter<HitStopEvent>,
    feedback_assets: Res<CombatFeedbackAssets>,
) {
    for event in damage_events.read() {
        // Create floating damage number
        spawn_damage_number(&mut commands, event, &feedback_assets);
        
        // Screen shake based on damage type
        let shake_intensity = match event.damage_type {
            DamageType::Player => 0.2,
            DamageType::Enemy => 0.1,
            DamageType::Critical => 0.4,
            DamageType::Heal => 0.0,
        };
        
        if shake_intensity > 0.0 {
            screen_shake_events.send(ScreenShakeEvent {
                intensity: shake_intensity,
                duration: 0.15,
            });
        }
        
        // Hit stop for impactful hits
        if event.is_critical || event.damage > 20 {
            hit_stop_events.send(HitStopEvent {
                duration: 0.08,
            });
        }
        
        // Create hit effect
        spawn_hit_effect(&mut commands, event, &feedback_assets);
    }
}

fn spawn_damage_number(
    commands: &mut Commands,
    event: &DamageEvent,
    feedback_assets: &CombatFeedbackAssets,
) {
    let (color, font_size) = match event.damage_type {
        DamageType::Player => (Color::rgb(1.0, 0.3, 0.3), 32.0),
        DamageType::Enemy => (Color::rgb(1.0, 1.0, 0.4), 28.0),
        DamageType::Critical => (Color::rgb(1.0, 0.8, 0.2), 42.0),
        DamageType::Heal => (Color::rgb(0.3, 1.0, 0.3), 30.0),
    };
    
    let damage_text = if event.damage_type == DamageType::Heal {
        format!("+{}", event.damage)
    } else {
        event.damage.to_string()
    };
    
    // Convert world position to screen position (simplified)
    let screen_pos = world_to_screen(event.position);
    
    commands.spawn((
        TextBundle::from_section(
            damage_text,
            TextStyle {
                font: feedback_assets.font.clone(),
                font_size,
                color,
            },
        ).with_style(Style {
            position_type: PositionType::Absolute,
            left: Val::Px(screen_pos.x),
            top: Val::Px(screen_pos.y),
            ..default()
        }),
        DamageNumber {
            lifetime: Timer::from_seconds(2.0, TimerMode::Once),
            velocity: Vec3::new(0.0, -50.0, 0.0), // Float upward
            damage_type: event.damage_type,
        },
    ));
}

fn spawn_hit_effect(
    commands: &mut Commands,
    event: &DamageEvent,
    feedback_assets: &CombatFeedbackAssets,
) {
    let effect_image = match event.damage_type {
        DamageType::Critical => feedback_assets.critical_effect.clone(),
        DamageType::Heal => feedback_assets.heal_sparkle.clone(),
        _ => feedback_assets.hit_particle.clone(),
    };
    
    let screen_pos = world_to_screen(event.position);
    
    commands.spawn((
        ImageBundle {
            style: Style {
                position_type: PositionType::Absolute,
                left: Val::Px(screen_pos.x - 25.0),
                top: Val::Px(screen_pos.y - 25.0),
                width: Val::Px(50.0),
                height: Val::Px(50.0),
                ..default()
            },
            image: UiImage::new(effect_image),
            ..default()
        },
        HitEffect {
            lifetime: Timer::from_seconds(0.5, TimerMode::Once),
            scale_curve: 0.0,
        },
    ));
}

fn update_damage_numbers(
    mut commands: Commands,
    time: Res<Time>,
    mut query: Query<(Entity, &mut DamageNumber, &mut Style, &mut Text)>,
) {
    for (entity, mut damage_num, mut style, mut text) in query.iter_mut() {
        damage_num.lifetime.tick(time.delta());
        
        if damage_num.lifetime.finished() {
            commands.entity(entity).despawn();
            continue;
        }
        
        // Update position (float upward and fade)
        let progress = damage_num.lifetime.elapsed_secs() / damage_num.lifetime.duration().as_secs_f32();
        let new_y = match style.top {
            Val::Px(y) => y + damage_num.velocity.y * time.delta_seconds(),
            _ => 0.0,
        };
        style.top = Val::Px(new_y);
        
        // Fade out
        let alpha = 1.0 - progress;
        if let Some(section) = text.sections.first_mut() {
            section.style.color = section.style.color.with_a(alpha);
        }
        
        // Scale effect for critical hits
        if matches!(damage_num.damage_type, DamageType::Critical) {
            let scale = 1.0 + (progress * 2.0).sin() * 0.2;
            // Note: Would need Transform component for actual scaling
        }
    }
}

fn handle_hit_effects(
    mut commands: Commands,
    time: Res<Time>,
    mut query: Query<(Entity, &mut HitEffect, &mut Style)>,
) {
    for (entity, mut hit_effect, mut style) in query.iter_mut() {
        hit_effect.lifetime.tick(time.delta());
        
        if hit_effect.lifetime.finished() {
            commands.entity(entity).despawn();
            continue;
        }
        
        // Animate scale (burst effect)
        let progress = hit_effect.lifetime.elapsed_secs() / hit_effect.lifetime.duration().as_secs_f32();
        let scale = if progress < 0.3 {
            // Quick scale up
            progress * 3.33
        } else {
            // Scale down and fade
            1.0 - (progress - 0.3) / 0.7
        };
        
        hit_effect.scale_curve = scale;
        
        // Apply scale to style (simplified - would be better with Transform)
        let size = 50.0 * scale;
        style.width = Val::Px(size);
        style.height = Val::Px(size);
    }
}

fn apply_screen_shake(
    mut screen_shake_events: EventReader<ScreenShakeEvent>,
    mut commands: Commands,
    mut camera_query: Query<&mut Transform, With<Camera>>,
    time: Res<Time>,
    mut shake_query: Query<(Entity, &mut ScreenShake)>,
) {
    // Add new screen shake
    for event in screen_shake_events.read() {
        commands.spawn(ScreenShake {
            intensity: event.intensity,
            duration: Timer::from_seconds(event.duration, TimerMode::Once),
        });
    }
    
    // Apply active screen shake
    let mut total_shake = Vec3::ZERO;
    
    for (entity, mut shake) in shake_query.iter_mut() {
        shake.duration.tick(time.delta());
        
        if shake.duration.finished() {
            commands.entity(entity).despawn();
            continue;
        }
        
        // Calculate shake offset
        let progress = shake.duration.elapsed_secs() / shake.duration.duration().as_secs_f32();
        let intensity = shake.intensity * (1.0 - progress); // Fade out
        
        let shake_x = (time.elapsed_seconds() * 50.0).sin() * intensity * 10.0;
        let shake_y = (time.elapsed_seconds() * 60.0).cos() * intensity * 10.0;
        
        total_shake += Vec3::new(shake_x, shake_y, 0.0);
    }
    
    // Apply to camera
    for mut camera_transform in camera_query.iter_mut() {
        // Store original position and apply shake offset
        // This is simplified - in practice you'd store the base position
        camera_transform.translation += total_shake * 0.01; // Scale down the effect
    }
}

fn handle_hit_stop(
    mut hit_stop_events: EventReader<HitStopEvent>,
    mut time: ResMut<Time<Virtual>>,
) {
    for event in hit_stop_events.read() {
        // Pause virtual time for hit stop effect
        // This is a simplified implementation
        // In practice, you'd use a more sophisticated time scaling system
        time.pause();
        
        // You would typically use a timer system to unpause after the duration
        // For now, we'll just create a very short pause effect
        info!("Hit stop for {:.2}s", event.duration);
    }
}

fn cleanup_expired_effects(
    mut commands: Commands,
    damage_query: Query<(Entity, &DamageNumber)>,
    hit_query: Query<(Entity, &HitEffect)>,
) {
    // Clean up expired damage numbers
    for (entity, damage_num) in damage_query.iter() {
        if damage_num.lifetime.finished() {
            commands.entity(entity).despawn();
        }
    }
    
    // Clean up expired hit effects
    for (entity, hit_effect) in hit_query.iter() {
        if hit_effect.lifetime.finished() {
            commands.entity(entity).despawn();
        }
    }
}

fn create_hit_particles(
    mut commands: Commands,
    mut damage_events: EventReader<DamageEvent>,
    feedback_assets: Res<CombatFeedbackAssets>,
) {
    for event in damage_events.read() {
        // Create particle burst at hit location
        for i in 0..5 {
            let angle = (i as f32 / 5.0) * std::f32::consts::TAU;
            let velocity = Vec3::new(angle.cos(), angle.sin(), 0.0) * 100.0;
            
            let screen_pos = world_to_screen(event.position);
            
            commands.spawn((
                ImageBundle {
                    style: Style {
                        position_type: PositionType::Absolute,
                        left: Val::Px(screen_pos.x),
                        top: Val::Px(screen_pos.y),
                        width: Val::Px(8.0),
                        height: Val::Px(8.0),
                        ..default()
                    },
                    image: UiImage::new(feedback_assets.hit_particle.clone()),
                    background_color: Color::rgb(1.0, 0.8, 0.2).into(),
                    ..default()
                },
                DamageNumber {
                    lifetime: Timer::from_seconds(0.3, TimerMode::Once),
                    velocity,
                    damage_type: event.damage_type,
                },
            ));
        }
    }
}

// Helper function to convert world position to screen position
fn world_to_screen(world_pos: Vec3) -> Vec2 {
    // This is a simplified conversion
    // In practice, you'd use the camera's view-projection matrix
    Vec2::new(
        400.0 + world_pos.x * 10.0, // Rough conversion
        300.0 - world_pos.z * 10.0, // Flip Y for screen coords
    )
}

impl DamageType {
    pub fn get_color(&self) -> Color {
        match self {
            DamageType::Player => Color::rgb(1.0, 0.3, 0.3),
            DamageType::Enemy => Color::rgb(1.0, 1.0, 0.4),
            DamageType::Critical => Color::rgb(1.0, 0.8, 0.2),
            DamageType::Heal => Color::rgb(0.3, 1.0, 0.3),
        }
    }
}