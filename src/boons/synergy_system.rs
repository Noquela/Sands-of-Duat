use bevy::prelude::*;
use std::collections::HashMap;
use super::{Boon, EgyptianGod, BoonEffect};

#[derive(Debug, Clone)]
pub struct SynergyBonus {
    pub id: String,
    pub name: String,
    pub description: String,
    pub gods_involved: Vec<EgyptianGod>,
    pub required_tags: Vec<String>,
    pub bonus_effects: Vec<BoonEffect>,
    pub active: bool,
}

pub struct SynergyCalculator {
    pub synergy_definitions: Vec<SynergyDefinition>,
}

#[derive(Debug, Clone)]
struct SynergyDefinition {
    pub id: String,
    pub name: String,
    pub description: String,
    pub gods_required: Vec<EgyptianGod>,
    pub tags_required: Vec<String>,
    pub min_boons: usize,
    pub bonus_effects: Vec<BoonEffect>,
}

impl SynergyCalculator {
    pub fn new() -> Self {
        Self {
            synergy_definitions: create_synergy_definitions(),
        }
    }
    
    pub fn calculate_synergies(&self, player_boons: &[Boon]) -> Vec<SynergyBonus> {
        let mut active_synergies = Vec::new();
        
        for synergy_def in &self.synergy_definitions {
            if self.check_synergy_requirements(synergy_def, player_boons) {
                active_synergies.push(SynergyBonus {
                    id: synergy_def.id.clone(),
                    name: synergy_def.name.clone(),
                    description: synergy_def.description.clone(),
                    gods_involved: synergy_def.gods_required.clone(),
                    required_tags: synergy_def.tags_required.clone(),
                    bonus_effects: synergy_def.bonus_effects.clone(),
                    active: true,
                });
            }
        }
        
        if !active_synergies.is_empty() {
            info!("⚡ {} synergies activated!", active_synergies.len());
            for synergy in &active_synergies {
                info!("  🔥 {}: {}", synergy.name, synergy.description);
            }
        }
        
        active_synergies
    }
    
    fn check_synergy_requirements(&self, synergy: &SynergyDefinition, player_boons: &[Boon]) -> bool {
        // Count boons by god
        let mut god_boon_count: HashMap<EgyptianGod, usize> = HashMap::new();
        let mut all_tags: Vec<String> = Vec::new();
        
        for boon in player_boons {
            *god_boon_count.entry(boon.god).or_insert(0) += 1;
            all_tags.extend(boon.synergy_tags.clone());
        }
        
        // Check god requirements
        for required_god in &synergy.gods_required {
            if god_boon_count.get(required_god).unwrap_or(&0) == &0 {
                return false;
            }
        }
        
        // Check minimum boons
        if player_boons.len() < synergy.min_boons {
            return false;
        }
        
        // Check tag requirements
        for required_tag in &synergy.tags_required {
            if !all_tags.contains(required_tag) {
                return false;
            }
        }
        
        true
    }
}

fn create_synergy_definitions() -> Vec<SynergyDefinition> {
    vec![
        // Ra + Anubis: Solar Death
        SynergyDefinition {
            id: "solar_death".to_string(),
            name: "Morte Solar".to_string(),
            description: "Inimigos queimados explodem ao morrer, causando dano solar em área".to_string(),
            gods_required: vec![EgyptianGod::Ra, EgyptianGod::Anubis],
            tags_required: vec!["fire".to_string(), "death".to_string()],
            min_boons: 2,
            bonus_effects: vec![BoonEffect::OnKillTrigger {
                effect: Box::new(BoonEffect::RadiantExplosion {
                    damage: 30.0,
                    heal: 0.0,
                    radius: 6.0,
                })
            }],
        },
        
        // Isis + Anubis: Life and Death Balance
        SynergyDefinition {
            id: "life_death_balance".to_string(),
            name: "Equilíbrio Vida-Morte".to_string(),
            description: "Curar-se também causa dano aos inimigos próximos. Causar dano também cura você".to_string(),
            gods_required: vec![EgyptianGod::Isis, EgyptianGod::Anubis],
            tags_required: vec!["heal".to_string(), "death".to_string()],
            min_boons: 2,
            bonus_effects: vec![
                BoonEffect::AuraDamage { radius: 4.0, damage_per_second: 3.0 },
                BoonEffect::LifeSteal { percentage: 0.1 },
            ],
        },
        
        // Set + Ra: Storm and Sun
        SynergyDefinition {
            id: "storm_sun".to_string(),
            name: "Tempestade Solar".to_string(),
            description: "Seus ataques elétricos têm chance de incendiar inimigos. Inimigos queimados atraem raios".to_string(),
            gods_required: vec![EgyptianGod::Set, EgyptianGod::Ra],
            tags_required: vec!["lightning".to_string(), "fire".to_string()],
            min_boons: 2,
            bonus_effects: vec![
                BoonEffect::OnHitChance {
                    chance: 0.3,
                    effect: Box::new(BoonEffect::BurnDamage { damage_per_second: 8.0, duration: 4.0 })
                },
                BoonEffect::ChainLightning { damage: 15.0, chains: 5, range: 6.0 },
            ],
        },
        
        // Thoth + Set: Chaotic Magic
        SynergyDefinition {
            id: "chaotic_magic".to_string(),
            name: "Magia Caótica".to_string(),
            description: "Suas habilidades têm 25% de chance de serem lançadas duas vezes sem consumir recursos".to_string(),
            gods_required: vec![EgyptianGod::Thoth, EgyptianGod::Set],
            tags_required: vec!["magic".to_string(), "lightning".to_string()],
            min_boons: 2,
            bonus_effects: vec![
                BoonEffect::SpellEcho {
                    ability: "Q".to_string(),
                    echo_chance: 0.25,
                    echo_damage_multiplier: 1.0,
                },
                BoonEffect::SpellEcho {
                    ability: "R".to_string(),
                    echo_chance: 0.25,
                    echo_damage_multiplier: 1.0,
                },
            ],
        },
        
        // Isis + Ra: Divine Radiance
        SynergyDefinition {
            id: "divine_radiance".to_string(),
            name: "Radiância Divina".to_string(),
            description: "Sua aura curativa também causa dano aos inimigos e reduz o dano que você recebe".to_string(),
            gods_required: vec![EgyptianGod::Isis, EgyptianGod::Ra],
            tags_required: vec!["heal".to_string(), "fire".to_string()],
            min_boons: 2,
            bonus_effects: vec![
                BoonEffect::AuraDamage { radius: 5.0, damage_per_second: 4.0 },
                BoonEffect::Shield { max_shield: 20.0, regen_rate: 3.0, regen_delay: 2.0 },
            ],
        },
        
        // Thoth + Isis: Wisdom and Healing
        SynergyDefinition {
            id: "wisdom_healing".to_string(),
            name: "Sabedoria Curativa".to_string(),
            description: "Usar habilidades cura você. Curar-se reduz o tempo de recarga das habilidades".to_string(),
            gods_required: vec![EgyptianGod::Thoth, EgyptianGod::Isis],
            tags_required: vec!["magic".to_string(), "heal".to_string()],
            min_boons: 2,
            bonus_effects: vec![
                BoonEffect::OnAbilityUse { stamina_restore: 10.0 },
                BoonEffect::CooldownReduction {
                    abilities: vec!["Q".to_string(), "R".to_string()],
                    reduction_percentage: 0.15,
                },
            ],
        },
        
        // Anubis + Set: Death and Chaos
        SynergyDefinition {
            id: "death_chaos".to_string(),
            name: "Caos Mortal".to_string(),
            description: "Eliminar inimigos cria raios que saltam entre inimigos restantes".to_string(),
            gods_required: vec![EgyptianGod::Anubis, EgyptianGod::Set],
            tags_required: vec!["death".to_string(), "lightning".to_string()],
            min_boons: 2,
            bonus_effects: vec![BoonEffect::OnKillTrigger {
                effect: Box::new(BoonEffect::ChainLightning {
                    damage: 25.0,
                    chains: 10,
                    range: 8.0,
                })
            }],
        },
        
        // Thoth + Anubis: Forbidden Knowledge
        SynergyDefinition {
            id: "forbidden_knowledge".to_string(),
            name: "Conhecimento Proibido".to_string(),
            description: "Suas habilidades têm chance de marcar inimigos para execução instantânea abaixo de 40% de vida".to_string(),
            gods_required: vec![EgyptianGod::Thoth, EgyptianGod::Anubis],
            tags_required: vec!["magic".to_string(), "death".to_string()],
            min_boons: 2,
            bonus_effects: vec![
                BoonEffect::ExecuteThreshold { threshold: 0.4, damage_multiplier: 999.0 },
                BoonEffect::OnAbilityUse { stamina_restore: 20.0 },
            ],
        },
        
        // Triple God Synergies (Legendary)
        SynergyDefinition {
            id: "trinity_of_power".to_string(),
            name: "Trindade do Poder".to_string(),
            description: "LENDÁRIO: Ra + Set + Thoth - Suas habilidades invocam meteoros elétricos que explodem em chamas".to_string(),
            gods_required: vec![EgyptianGod::Ra, EgyptianGod::Set, EgyptianGod::Thoth],
            tags_required: vec!["fire".to_string(), "lightning".to_string(), "magic".to_string()],
            min_boons: 5,
            bonus_effects: vec![BoonEffect::SummonStorm {
                duration: 15.0,
                lightning_damage: 50.0,
                strikes_per_second: 3.0,
                tracking: true,
            }],
        },
        
        SynergyDefinition {
            id: "eternal_cycle".to_string(),
            name: "Ciclo Eterno".to_string(),
            description: "LENDÁRIO: Isis + Anubis + Thoth - Morte e renascimento concedem conhecimento: cada morte te torna mais forte permanentemente".to_string(),
            gods_required: vec![EgyptianGod::Isis, EgyptianGod::Anubis, EgyptianGod::Thoth],
            tags_required: vec!["heal".to_string(), "death".to_string(), "magic".to_string()],
            min_boons: 5,
            bonus_effects: vec![
                BoonEffect::AutoRevive { health_percentage: 0.75, invincibility_duration: 8.0 },
                BoonEffect::OnKillBuff { 
                    speed_bonus: 0.05, 
                    attack_speed_bonus: 0.05, 
                    duration: 999.0, // Permanent
                    max_stacks: 20 
                },
            ],
        },
        
        // Pentarchy Synergy (All Five Gods)
        SynergyDefinition {
            id: "pantheon_blessing".to_string(),
            name: "Bênção do Panteão".to_string(),
            description: "MÍTICO: Todos os 5 deuses - Você se torna um semideus, ganhando todos os poderes divinos simultaneamente".to_string(),
            gods_required: vec![
                EgyptianGod::Ra, 
                EgyptianGod::Anubis, 
                EgyptianGod::Isis, 
                EgyptianGod::Set, 
                EgyptianGod::Thoth
            ],
            tags_required: vec![
                "fire".to_string(), 
                "death".to_string(), 
                "heal".to_string(), 
                "lightning".to_string(), 
                "magic".to_string()
            ],
            min_boons: 8,
            bonus_effects: vec![
                BoonEffect::AuraDamage { radius: 10.0, damage_per_second: 10.0 },
                BoonEffect::HealthRegen { health_per_second: 5.0 },
                BoonEffect::CooldownReduction { 
                    abilities: vec!["Q".to_string(), "R".to_string()], 
                    reduction_percentage: 0.5 
                },
                BoonEffect::ExecuteThreshold { threshold: 0.5, damage_multiplier: 2.0 },
                BoonEffect::AutoRevive { health_percentage: 1.0, invincibility_duration: 10.0 },
            ],
        },
    ]
}

// Helper functions for synergy management
impl SynergyBonus {
    pub fn get_tier(&self) -> SynergyTier {
        match self.gods_involved.len() {
            2 => SynergyTier::Dual,
            3 => SynergyTier::Trinity,
            5 => SynergyTier::Pantheon,
            _ => SynergyTier::Dual,
        }
    }
    
    pub fn get_tier_color(&self) -> Color {
        match self.get_tier() {
            SynergyTier::Dual => Color::rgb(0.8, 0.4, 1.0),     // Purple
            SynergyTier::Trinity => Color::rgb(1.0, 0.6, 0.0),  // Orange
            SynergyTier::Pantheon => Color::rgb(1.0, 0.0, 1.0), // Magenta
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum SynergyTier {
    Dual,     // 2 gods
    Trinity,  // 3 gods
    Pantheon, // All 5 gods
}

// Events for synergy activation/deactivation
#[derive(Event)]
pub struct SynergyActivatedEvent {
    pub synergy: SynergyBonus,
}

#[derive(Event)]
pub struct SynergyDeactivatedEvent {
    pub synergy_id: String,
}