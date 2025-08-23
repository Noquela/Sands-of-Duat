use bevy::prelude::*;
use rand::{Rng, thread_rng, seq::SliceRandom};
use std::collections::HashMap;

pub mod boon_types;
pub mod synergy_system;
pub mod effects;

pub use boon_types::*;
pub use synergy_system::*;
pub use effects::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum EgyptianGod {
    Ra,     // Solar/Fire - Damage over time, radiance, burning
    Anubis, // Death/Execute - Executions, life steal, darkness
    Isis,   // Healing/Protection - Shields, healing, buffs
    Set,    // Chaos/Lightning - Critical strikes, speed, storms
    Thoth,  // Magic/Knowledge - Mana, cooldowns, enchantments
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum BoonRarity {
    Common,    // White - Base effects
    Rare,      // Blue - Enhanced effects
    Epic,      // Purple - Powerful effects
    Legendary, // Gold - Game-changing effects
}

#[derive(Debug, Clone, Component)]
pub struct Boon {
    pub id: String,
    pub god: EgyptianGod,
    pub rarity: BoonRarity,
    pub name: String,
    pub description: String,
    pub effects: Vec<BoonEffect>,
    pub synergy_tags: Vec<String>,
    pub level: u32,
    pub max_level: u32,
}

#[derive(Debug, Clone)]
pub struct BoonOffer {
    pub boons: Vec<Boon>,
    pub source: String, // "God Encounter", "Treasure", "Shop", etc.
}

#[derive(Resource)]
pub struct BoonRegistry {
    pub available_boons: HashMap<EgyptianGod, Vec<Boon>>,
    pub god_favor: HashMap<EgyptianGod, f32>, // 0.0 to 1.0
}

#[derive(Resource)]
pub struct ActiveBoons {
    pub player_boons: Vec<Boon>,
    pub synergy_bonuses: Vec<SynergyBonus>,
}

#[derive(Event)]
pub struct BoonSelectedEvent {
    pub boon: Boon,
}

#[derive(Event)]
pub struct BoonOfferEvent {
    pub offers: Vec<Boon>,
    pub selection_count: u32, // Usually 3 for choice
}

pub struct BoonSystemPlugin;

impl Plugin for BoonSystemPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<BoonRegistry>()
            .init_resource::<ActiveBoons>()
            .add_event::<BoonSelectedEvent>()
            .add_event::<BoonOfferEvent>()
            .add_systems(Startup, initialize_boon_registry)
            .add_systems(Update, (
                handle_boon_selection,
                update_synergies,
                apply_boon_effects,
            ));
    }
}

impl EgyptianGod {
    pub fn get_display_name(&self) -> &str {
        match self {
            EgyptianGod::Ra => "Rá, Deus do Sol",
            EgyptianGod::Anubis => "Anúbis, Juiz dos Mortos", 
            EgyptianGod::Isis => "Ísis, Mãe Divina",
            EgyptianGod::Set => "Set, Senhor do Caos",
            EgyptianGod::Thoth => "Thoth, Escriba dos Deuses",
        }
    }

    pub fn get_theme_color(&self) -> Color {
        match self {
            EgyptianGod::Ra => Color::rgb(1.0, 0.7, 0.0),      // Golden sun
            EgyptianGod::Anubis => Color::rgb(0.2, 0.1, 0.3),  // Dark purple
            EgyptianGod::Isis => Color::rgb(0.0, 0.8, 0.6),    // Healing cyan
            EgyptianGod::Set => Color::rgb(0.8, 0.2, 0.8),     // Electric purple
            EgyptianGod::Thoth => Color::rgb(0.3, 0.5, 1.0),   // Mystic blue
        }
    }

    pub fn get_domain(&self) -> &str {
        match self {
            EgyptianGod::Ra => "Sol e Fogo",
            EgyptianGod::Anubis => "Morte e Julgamento",
            EgyptianGod::Isis => "Cura e Proteção", 
            EgyptianGod::Set => "Caos e Tempestades",
            EgyptianGod::Thoth => "Magia e Conhecimento",
        }
    }

    pub fn get_all() -> Vec<EgyptianGod> {
        vec![
            EgyptianGod::Ra,
            EgyptianGod::Anubis,
            EgyptianGod::Isis,
            EgyptianGod::Set,
            EgyptianGod::Thoth,
        ]
    }
}

impl BoonRarity {
    pub fn get_color(&self) -> Color {
        match self {
            BoonRarity::Common => Color::rgb(0.9, 0.9, 0.9),    // White
            BoonRarity::Rare => Color::rgb(0.2, 0.6, 1.0),      // Blue
            BoonRarity::Epic => Color::rgb(0.6, 0.2, 1.0),      // Purple
            BoonRarity::Legendary => Color::rgb(1.0, 0.8, 0.0), // Gold
        }
    }

    pub fn get_spawn_weight(&self) -> f32 {
        match self {
            BoonRarity::Common => 0.6,
            BoonRarity::Rare => 0.25,
            BoonRarity::Epic => 0.12,
            BoonRarity::Legendary => 0.03,
        }
    }

    pub fn get_display_name(&self) -> &str {
        match self {
            BoonRarity::Common => "Comum",
            BoonRarity::Rare => "Raro", 
            BoonRarity::Epic => "Épico",
            BoonRarity::Legendary => "Lendário",
        }
    }
}

impl Default for BoonRegistry {
    fn default() -> Self {
        Self {
            available_boons: HashMap::new(),
            god_favor: EgyptianGod::get_all().iter().map(|g| (*g, 0.0)).collect(),
        }
    }
}

impl Default for ActiveBoons {
    fn default() -> Self {
        Self {
            player_boons: Vec::new(),
            synergy_bonuses: Vec::new(),
        }
    }
}

fn initialize_boon_registry(mut commands: Commands) {
    info!("🌟 Initializing Egyptian Boon Registry...");
    
    let mut registry = BoonRegistry::default();
    
    // Populate boons for each god
    for god in EgyptianGod::get_all() {
        registry.available_boons.insert(god, create_god_boons(god));
    }
    
    commands.insert_resource(registry);
    commands.insert_resource(ActiveBoons::default());
    
    info!("✅ Boon registry initialized with {} gods", EgyptianGod::get_all().len());
}

fn create_god_boons(god: EgyptianGod) -> Vec<Boon> {
    match god {
        EgyptianGod::Ra => create_ra_boons(),
        EgyptianGod::Anubis => create_anubis_boons(),
        EgyptianGod::Isis => create_isis_boons(),
        EgyptianGod::Set => create_set_boons(),
        EgyptianGod::Thoth => create_thoth_boons(),
    }
}

fn handle_boon_selection(
    mut selection_events: EventReader<BoonSelectedEvent>,
    mut active_boons: ResMut<ActiveBoons>,
    mut registry: ResMut<BoonRegistry>,
) {
    for event in selection_events.read() {
        info!("🎯 Player selected boon: {}", event.boon.name);
        
        // Check if player already has this boon (for upgrades)
        if let Some(existing_boon) = active_boons.player_boons
            .iter_mut()
            .find(|b| b.id == event.boon.id) 
        {
            if existing_boon.level < existing_boon.max_level {
                existing_boon.level += 1;
                info!("📈 Upgraded {} to level {}", existing_boon.name, existing_boon.level);
            }
        } else {
            // Add new boon
            active_boons.player_boons.push(event.boon.clone());
            info!("✨ Added new boon: {}", event.boon.name);
        }
        
        // Increase god favor
        *registry.god_favor.get_mut(&event.boon.god).unwrap() += 0.1;
        
        // Trigger synergy recalculation
        recalculate_synergies(&mut active_boons);
    }
}

fn update_synergies(
    mut active_boons: ResMut<ActiveBoons>,
) {
    if active_boons.is_changed() {
        recalculate_synergies(&mut active_boons);
    }
}

fn apply_boon_effects(
    active_boons: Res<ActiveBoons>,
    // Add queries for entities that need boon effects applied
    // This would integrate with combat system, stats, etc.
) {
    // This system would apply active boon effects to relevant entities
    // For now, it's a placeholder for the actual implementation
    if !active_boons.player_boons.is_empty() {
        // Apply effects would go here
    }
}

// Public API for generating boon offers
impl BoonRegistry {
    pub fn generate_offer(&self, god_preferences: Option<Vec<EgyptianGod>>, count: u32) -> BoonOffer {
        let mut rng = thread_rng();
        let mut offers = Vec::new();
        
        let gods_to_offer = god_preferences.unwrap_or_else(|| {
            // Weighted selection based on god favor
            let mut weighted_gods = Vec::new();
            for (god, favor) in &self.god_favor {
                let weight = (1.0 + favor) * 10.0;
                for _ in 0..(weight as u32) {
                    weighted_gods.push(*god);
                }
            }
            weighted_gods.shuffle(&mut rng);
            weighted_gods.into_iter().take(count as usize).collect()
        });
        
        for god in gods_to_offer.iter().take(count as usize) {
            if let Some(god_boons) = self.available_boons.get(god) {
                if let Some(boon) = god_boons.choose(&mut rng) {
                    offers.push(boon.clone());
                }
            }
        }
        
        // Ensure we have the requested count
        while offers.len() < count as usize {
            let all_gods = EgyptianGod::get_all();
            let random_god = all_gods.choose(&mut rng).unwrap();
            if let Some(god_boons) = self.available_boons.get(random_god) {
                if let Some(boon) = god_boons.choose(&mut rng) {
                    offers.push(boon.clone());
                }
            }
        }
        
        BoonOffer {
            boons: offers,
            source: "God Encounter".to_string(),
        }
    }
    
    pub fn get_god_favor(&self, god: EgyptianGod) -> f32 {
        *self.god_favor.get(&god).unwrap_or(&0.0)
    }
    
    pub fn increase_god_favor(&mut self, god: EgyptianGod, amount: f32) {
        *self.god_favor.get_mut(&god).unwrap() += amount;
    }
}

pub fn recalculate_synergies(active_boons: &mut ActiveBoons) {
    active_boons.synergy_bonuses.clear();
    
    // Check for synergies between active boons
    let synergy_calculator = SynergyCalculator::new();
    active_boons.synergy_bonuses = synergy_calculator.calculate_synergies(&active_boons.player_boons);
    
    if !active_boons.synergy_bonuses.is_empty() {
        info!("⚡ Active synergies: {}", active_boons.synergy_bonuses.len());
    }
}