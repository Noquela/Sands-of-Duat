use bevy::prelude::*;

#[derive(Component)]
pub struct Player;

#[derive(Component)]
pub struct Stats {
    pub max_health: f32,
    pub current_health: f32,
    pub max_stamina: f32,
    pub current_stamina: f32,
    pub speed: f32,
    pub stamina_regen_rate: f32,
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
pub struct Dash {
    pub cooldown: f32,
    pub cooldown_timer: f32,
    pub distance: f32,
    pub i_frames: f32,
    pub i_timer: f32,
    pub is_dashing: bool,
    pub dash_timer: f32,
    pub dash_direction: Vec3,
    pub stamina_cost: f32,
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
pub struct Combat {
    pub base_damage: i32,
    // primário (mouse esq) – chain de 3
    pub atk_cd: f32,
    pub atk_timer: f32,
    pub chain_step: u8,
    // secundário (mouse dir) – especial leve
    pub special_cd: f32,
    pub special_timer: f32,
    // Q – cast/projétil
    pub q_cd: f32,
    pub q_timer: f32,
    // R – habilidade principal (AoE)
    pub r_cd: f32,
    pub r_timer: f32,
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