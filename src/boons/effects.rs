use bevy::prelude::*;

#[derive(Debug, Clone)]
pub enum BoonEffect {
    // Damage Effects
    OnHitChance { chance: f32, effect: Box<BoonEffect> },
    BurnDamage { damage_per_second: f32, duration: f32 },
    ChainLightning { damage: f32, chains: u32, range: f32 },
    ExecuteThreshold { threshold: f32, damage_multiplier: f32 },
    
    // Area Effects
    AuraDamage { radius: f32, damage_per_second: f32 },
    AuraDebuff { radius: f32, speed_multiplier: f32 },
    AreaBurn { radius: f32, damage: f32, duration: f32 },
    RadiantExplosion { damage: f32, heal: f32, radius: f32 },
    
    // Healing and Protection
    HealthRegen { health_per_second: f32 },
    LifeSteal { percentage: f32 },
    Shield { max_shield: f32, regen_rate: f32, regen_delay: f32 },
    EmergencyHeal { threshold: f32, heal_percentage: f32, cooldown: f32 },
    AutoRevive { health_percentage: f32, invincibility_duration: f32 },
    
    // Movement and Utility
    DashEnhancement { shadow_damage: f32, teleport: bool },
    DashTrail { damage: f32, stun_duration: f32, trail_duration: f32 },
    
    // Ability Enhancements
    AbilityEnhancement { ability: String, enhancement: Box<BoonEffect> },
    CooldownReduction { abilities: Vec<String>, reduction_percentage: f32 },
    OnAbilityUse { stamina_restore: f32 },
    SpellEcho { ability: String, echo_chance: f32, echo_damage_multiplier: f32 },
    InfiniteRange { abilities: Vec<String> },
    
    // Trigger Effects
    OnKillTrigger { effect: Box<BoonEffect> },
    OnKillBuff { speed_bonus: f32, attack_speed_bonus: f32, duration: f32, max_stacks: u32 },
    OnHealthThreshold { threshold: f32, effect: Box<BoonEffect> },
    
    // Special Effects
    SummonStorm { duration: f32, lightning_damage: f32, strikes_per_second: f32, tracking: bool },
    ResurrectAllies,
    WallHack,
}

#[derive(Component)]
pub struct ActiveEffect {
    pub effect_type: BoonEffect,
    pub duration: Option<f32>,
    pub timer: f32,
    pub source_boon_id: String,
}

#[derive(Component)]
pub struct BurnEffect {
    pub damage_per_second: f32,
    pub remaining_duration: f32,
}

#[derive(Component)]
pub struct ShieldComponent {
    pub current_shield: f32,
    pub max_shield: f32,
    pub regen_rate: f32,
    pub regen_delay: f32,
    pub last_damage_time: f32,
}

#[derive(Component)]
pub struct StormEntity {
    pub damage: f32,
    pub strikes_per_second: f32,
    pub remaining_duration: f32,
    pub tracking: bool,
    pub strike_timer: f32,
}

#[derive(Component)]
pub struct SpeedBuff {
    pub speed_multiplier: f32,
    pub attack_speed_multiplier: f32,
    pub remaining_duration: f32,
    pub stacks: u32,
}

#[derive(Component)]
pub struct ElectricTrail {
    pub damage: f32,
    pub stun_duration: f32,
    pub remaining_duration: f32,
}

// Effect application systems
pub fn apply_burn_effects(
    time: Res<Time>,
    mut burn_query: Query<(Entity, &mut BurnEffect, &mut Health)>,
    mut commands: Commands,
) {
    for (entity, mut burn, mut health) in burn_query.iter_mut() {
        burn.remaining_duration -= time.delta_seconds();
        
        if burn.remaining_duration <= 0.0 {
            commands.entity(entity).remove::<BurnEffect>();
            continue;
        }
        
        // Apply burn damage
        let damage = burn.damage_per_second * time.delta_seconds();
        health.current -= damage;
        
        if health.current <= 0.0 {
            health.current = 0.0;
        }
    }
}

pub fn update_shield_systems(
    time: Res<Time>,
    mut shield_query: Query<&mut ShieldComponent>,
) {
    for mut shield in shield_query.iter_mut() {
        // Regenerate shield if not damaged recently
        if time.elapsed_seconds() - shield.last_damage_time > shield.regen_delay {
            shield.current_shield += shield.regen_rate * time.delta_seconds();
            shield.current_shield = shield.current_shield.min(shield.max_shield);
        }
    }
}

pub fn update_storm_entities(
    time: Res<Time>,
    mut storm_query: Query<(Entity, &mut StormEntity, &Transform)>,
    enemy_query: Query<(Entity, &Transform), (With<Enemy>, Without<StormEntity>)>,
    mut commands: Commands,
) {
    for (storm_entity, mut storm, storm_transform) in storm_query.iter_mut() {
        storm.remaining_duration -= time.delta_seconds();
        storm.strike_timer -= time.delta_seconds();
        
        if storm.remaining_duration <= 0.0 {
            commands.entity(storm_entity).despawn();
            continue;
        }
        
        // Strike lightning
        if storm.strike_timer <= 0.0 {
            storm.strike_timer = 1.0 / storm.strikes_per_second;
            
            // Find nearest enemy if tracking
            if storm.tracking {
                if let Some((enemy_entity, _)) = enemy_query
                    .iter()
                    .min_by_key(|(_, enemy_transform)| {
                        (storm_transform.translation.distance(enemy_transform.translation) * 100.0) as i32
                    })
                {
                    // Create lightning strike effect
                    commands.spawn((
                        LightningStrike {
                            damage: storm.damage,
                            target: enemy_entity,
                        },
                        Transform::from_translation(storm_transform.translation),
                        GlobalTransform::default(),
                    ));
                }
            }
        }
    }
}

pub fn update_speed_buffs(
    time: Res<Time>,
    mut speed_buff_query: Query<(Entity, &mut SpeedBuff)>,
    mut commands: Commands,
) {
    for (entity, mut speed_buff) in speed_buff_query.iter_mut() {
        speed_buff.remaining_duration -= time.delta_seconds();
        
        if speed_buff.remaining_duration <= 0.0 {
            commands.entity(entity).remove::<SpeedBuff>();
        }
    }
}

pub fn update_electric_trails(
    time: Res<Time>,
    mut trail_query: Query<(Entity, &mut ElectricTrail)>,
    enemy_query: Query<(Entity, &Transform), With<Enemy>>,
    trail_transform_query: Query<&Transform, (With<ElectricTrail>, Without<Enemy>)>,
    mut commands: Commands,
) {
    for (entity, mut trail) in trail_query.iter_mut() {
        trail.remaining_duration -= time.delta_seconds();
        
        if trail.remaining_duration <= 0.0 {
            commands.entity(entity).despawn();
            continue;
        }
        
        // Check for enemies in trail
        if let Ok(trail_transform) = trail_transform_query.get(entity) {
            for (enemy_entity, enemy_transform) in enemy_query.iter() {
                let distance = trail_transform.translation.distance(enemy_transform.translation);
                if distance < 1.5 { // Trail width
                    // Apply damage and stun
                    commands.entity(enemy_entity).insert(StunEffect {
                        remaining_duration: trail.stun_duration,
                    });
                    
                    // Apply electric damage
                    commands.entity(enemy_entity).insert(ElectricDamage {
                        damage: trail.damage,
                    });
                }
            }
        }
    }
}

// Placeholder components for integration
#[derive(Component)]
pub struct Health {
    pub current: f32,
    pub max: f32,
}

#[derive(Component)]
pub struct Enemy;

#[derive(Component)]
pub struct LightningStrike {
    pub damage: f32,
    pub target: Entity,
}

#[derive(Component)]
pub struct StunEffect {
    pub remaining_duration: f32,
}

#[derive(Component)]
pub struct ElectricDamage {
    pub damage: f32,
}

// Effect creation helpers
impl BoonEffect {
    pub fn create_active_effect(&self, source_boon_id: String) -> ActiveEffect {
        ActiveEffect {
            effect_type: self.clone(),
            duration: self.get_duration(),
            timer: 0.0,
            source_boon_id,
        }
    }
    
    fn get_duration(&self) -> Option<f32> {
        match self {
            BoonEffect::BurnDamage { duration, .. } => Some(*duration),
            BoonEffect::EmergencyHeal { cooldown, .. } => Some(*cooldown),
            BoonEffect::AutoRevive { invincibility_duration, .. } => Some(*invincibility_duration),
            BoonEffect::DashTrail { trail_duration, .. } => Some(*trail_duration),
            BoonEffect::OnKillBuff { duration, .. } => Some(*duration),
            BoonEffect::SummonStorm { duration, .. } => Some(*duration),
            _ => None, // Permanent effects
        }
    }
    
    pub fn is_stackable(&self) -> bool {
        match self {
            BoonEffect::OnKillBuff { .. } => true,
            BoonEffect::BurnDamage { .. } => true,
            _ => false,
        }
    }
}