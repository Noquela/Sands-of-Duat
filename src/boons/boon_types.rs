use bevy::prelude::*;
use super::{Boon, EgyptianGod, BoonRarity, BoonEffect};

pub fn create_ra_boons() -> Vec<Boon> {
    vec![
        // RA - Solar/Fire Boons
        Boon {
            id: "ra_solar_strike".to_string(),
            god: EgyptianGod::Ra,
            rarity: BoonRarity::Common,
            name: "Golpe Solar".to_string(),
            description: "Seus ataques têm 15% de chance de queimar inimigos, causando dano ao longo do tempo".to_string(),
            effects: vec![BoonEffect::OnHitChance { 
                chance: 0.15, 
                effect: Box::new(BoonEffect::BurnDamage { damage_per_second: 5.0, duration: 3.0 })
            }],
            synergy_tags: vec!["fire".to_string(), "burn".to_string()],
            level: 1,
            max_level: 3,
        },
        
        Boon {
            id: "ra_radiant_aura".to_string(),
            god: EgyptianGod::Ra,
            rarity: BoonRarity::Rare,
            name: "Aura Radiante".to_string(),
            description: "Inimigos próximos recebem 2 de dano solar por segundo e têm velocidade reduzida".to_string(),
            effects: vec![
                BoonEffect::AuraDamage { radius: 5.0, damage_per_second: 2.0 },
                BoonEffect::AuraDebuff { radius: 5.0, speed_multiplier: 0.8 },
            ],
            synergy_tags: vec!["fire".to_string(), "aura".to_string()],
            level: 1,
            max_level: 2,
        },
        
        Boon {
            id: "ra_solar_flare".to_string(),
            god: EgyptianGod::Ra,
            rarity: BoonRarity::Epic,
            name: "Erupção Solar".to_string(),
            description: "Sua habilidade R cria uma explosão solar que queima todos os inimigos na área".to_string(),
            effects: vec![BoonEffect::AbilityEnhancement { 
                ability: "R".to_string(),
                enhancement: Box::new(BoonEffect::AreaBurn { radius: 8.0, damage: 25.0, duration: 5.0 })
            }],
            synergy_tags: vec!["fire".to_string(), "area".to_string(), "r_ability".to_string()],
            level: 1,
            max_level: 1,
        },
        
        Boon {
            id: "ra_eternal_sun".to_string(),
            god: EgyptianGod::Ra,
            rarity: BoonRarity::Legendary,
            name: "Sol Eterno".to_string(),
            description: "Quando sua vida fica abaixo de 25%, você irradia luz intensa, causando dano massivo e curando-se".to_string(),
            effects: vec![BoonEffect::OnHealthThreshold {
                threshold: 0.25,
                effect: Box::new(BoonEffect::RadiantExplosion { damage: 100.0, heal: 50.0, radius: 12.0 })
            }],
            synergy_tags: vec!["fire".to_string(), "legendary".to_string(), "heal".to_string()],
            level: 1,
            max_level: 1,
        },
    ]
}

pub fn create_anubis_boons() -> Vec<Boon> {
    vec![
        // ANUBIS - Death/Execute Boons
        Boon {
            id: "anubis_death_mark".to_string(),
            god: EgyptianGod::Anubis,
            rarity: BoonRarity::Common,
            name: "Marca da Morte".to_string(),
            description: "Inimigos abaixo de 30% de vida recebem 50% mais dano de todos os ataques".to_string(),
            effects: vec![BoonEffect::ExecuteThreshold { threshold: 0.3, damage_multiplier: 1.5 }],
            synergy_tags: vec!["death".to_string(), "execute".to_string()],
            level: 1,
            max_level: 3,
        },
        
        Boon {
            id: "anubis_life_steal".to_string(),
            god: EgyptianGod::Anubis,
            rarity: BoonRarity::Rare,
            name: "Roubo de Alma".to_string(),
            description: "Seus ataques curam você por 15% do dano causado".to_string(),
            effects: vec![BoonEffect::LifeSteal { percentage: 0.15 }],
            synergy_tags: vec!["death".to_string(), "heal".to_string()],
            level: 1,
            max_level: 2,
        },
        
        Boon {
            id: "anubis_shadow_step".to_string(),
            god: EgyptianGod::Anubis,
            rarity: BoonRarity::Epic,
            name: "Passo Sombrio".to_string(),
            description: "Seu dash teleporta você através das sombras, causando dano aos inimigos no destino".to_string(),
            effects: vec![BoonEffect::DashEnhancement {
                shadow_damage: 20.0,
                teleport: true,
            }],
            synergy_tags: vec!["death".to_string(), "mobility".to_string(), "dash".to_string()],
            level: 1,
            max_level: 1,
        },
        
        Boon {
            id: "anubis_judgment".to_string(),
            god: EgyptianGod::Anubis,
            rarity: BoonRarity::Legendary,
            name: "Julgamento Final".to_string(),
            description: "Eliminar um inimigo ressuscita todos os aliados mortos na sala".to_string(),
            effects: vec![BoonEffect::OnKillTrigger {
                effect: Box::new(BoonEffect::ResurrectAllies)
            }],
            synergy_tags: vec!["death".to_string(), "legendary".to_string(), "resurrection".to_string()],
            level: 1,
            max_level: 1,
        },
    ]
}

pub fn create_isis_boons() -> Vec<Boon> {
    vec![
        // ISIS - Healing/Protection Boons
        Boon {
            id: "isis_healing_aura".to_string(),
            god: EgyptianGod::Isis,
            rarity: BoonRarity::Common,
            name: "Aura Curativa".to_string(),
            description: "Regenera 2 pontos de vida por segundo constantemente".to_string(),
            effects: vec![BoonEffect::HealthRegen { health_per_second: 2.0 }],
            synergy_tags: vec!["heal".to_string(), "regeneration".to_string()],
            level: 1,
            max_level: 3,
        },
        
        Boon {
            id: "isis_divine_shield".to_string(),
            god: EgyptianGod::Isis,
            rarity: BoonRarity::Rare,
            name: "Escudo Divino".to_string(),
            description: "Absorve até 25 pontos de dano antes de afetar sua vida. Regenera com o tempo".to_string(),
            effects: vec![BoonEffect::Shield { 
                max_shield: 25.0, 
                regen_rate: 2.0, 
                regen_delay: 3.0 
            }],
            synergy_tags: vec!["protection".to_string(), "shield".to_string()],
            level: 1,
            max_level: 2,
        },
        
        Boon {
            id: "isis_blessing_of_life".to_string(),
            god: EgyptianGod::Isis,
            rarity: BoonRarity::Epic,
            name: "Bênção da Vida".to_string(),
            description: "Quando sua vida fica baixa, cura instantaneamente 40% da vida máxima (uma vez por sala)".to_string(),
            effects: vec![BoonEffect::EmergencyHeal {
                threshold: 0.2,
                heal_percentage: 0.4,
                cooldown: 60.0, // Room duration
            }],
            synergy_tags: vec!["heal".to_string(), "protection".to_string(), "emergency".to_string()],
            level: 1,
            max_level: 1,
        },
        
        Boon {
            id: "isis_resurrection".to_string(),
            god: EgyptianGod::Isis,
            rarity: BoonRarity::Legendary,
            name: "Ressurreição Divina".to_string(),
            description: "Ao morrer, ressuscita automaticamente com 50% de vida e 5 segundos de invencibilidade".to_string(),
            effects: vec![BoonEffect::AutoRevive {
                health_percentage: 0.5,
                invincibility_duration: 5.0,
            }],
            synergy_tags: vec!["heal".to_string(), "legendary".to_string(), "resurrection".to_string()],
            level: 1,
            max_level: 1,
        },
    ]
}

pub fn create_set_boons() -> Vec<Boon> {
    vec![
        // SET - Chaos/Lightning Boons  
        Boon {
            id: "set_lightning_strike".to_string(),
            god: EgyptianGod::Set,
            rarity: BoonRarity::Common,
            name: "Golpe Elétrico".to_string(),
            description: "Seus ataques têm 20% de chance de causar dano elétrico que se espalha para inimigos próximos".to_string(),
            effects: vec![BoonEffect::OnHitChance {
                chance: 0.2,
                effect: Box::new(BoonEffect::ChainLightning { damage: 8.0, chains: 3, range: 4.0 })
            }],
            synergy_tags: vec!["lightning".to_string(), "chain".to_string()],
            level: 1,
            max_level: 3,
        },
        
        Boon {
            id: "set_storm_speed".to_string(),
            god: EgyptianGod::Set,
            rarity: BoonRarity::Rare,
            name: "Velocidade da Tempestade".to_string(),
            description: "Cada inimigo eliminado aumenta sua velocidade de movimento e ataque por 5 segundos".to_string(),
            effects: vec![BoonEffect::OnKillBuff {
                speed_bonus: 0.2,
                attack_speed_bonus: 0.15,
                duration: 5.0,
                max_stacks: 5,
            }],
            synergy_tags: vec!["speed".to_string(), "stacking".to_string()],
            level: 1,
            max_level: 2,
        },
        
        Boon {
            id: "set_chaos_dash".to_string(),
            god: EgyptianGod::Set,
            rarity: BoonRarity::Epic,
            name: "Dash do Caos".to_string(),
            description: "Seu dash deixa um rastro elétrico que causa dano e atordoa inimigos por 2 segundos".to_string(),
            effects: vec![BoonEffect::DashTrail {
                damage: 15.0,
                stun_duration: 2.0,
                trail_duration: 3.0,
            }],
            synergy_tags: vec!["lightning".to_string(), "dash".to_string(), "stun".to_string()],
            level: 1,
            max_level: 1,
        },
        
        Boon {
            id: "set_storm_lord".to_string(),
            god: EgyptianGod::Set,
            rarity: BoonRarity::Legendary,
            name: "Senhor das Tempestades".to_string(),
            description: "Sua habilidade R invoca uma tempestade que persegue inimigos por 10 segundos".to_string(),
            effects: vec![BoonEffect::SummonStorm {
                duration: 10.0,
                lightning_damage: 30.0,
                strikes_per_second: 2.0,
                tracking: true,
            }],
            synergy_tags: vec!["lightning".to_string(), "legendary".to_string(), "r_ability".to_string()],
            level: 1,
            max_level: 1,
        },
    ]
}

pub fn create_thoth_boons() -> Vec<Boon> {
    vec![
        // THOTH - Magic/Knowledge Boons
        Boon {
            id: "thoth_arcane_knowledge".to_string(),
            god: EgyptianGod::Thoth,
            rarity: BoonRarity::Common,
            name: "Conhecimento Arcano".to_string(),
            description: "Suas habilidades Q e R têm 20% de redução no tempo de recarga".to_string(),
            effects: vec![BoonEffect::CooldownReduction {
                abilities: vec!["Q".to_string(), "R".to_string()],
                reduction_percentage: 0.2,
            }],
            synergy_tags: vec!["magic".to_string(), "cooldown".to_string()],
            level: 1,
            max_level: 3,
        },
        
        Boon {
            id: "thoth_mana_overflow".to_string(),
            god: EgyptianGod::Thoth,
            rarity: BoonRarity::Rare,
            name: "Transbordamento de Mana".to_string(),
            description: "Usar uma habilidade regenera 15 pontos de stamina instantaneamente".to_string(),
            effects: vec![BoonEffect::OnAbilityUse {
                stamina_restore: 15.0,
            }],
            synergy_tags: vec!["magic".to_string(), "stamina".to_string()],
            level: 1,
            max_level: 2,
        },
        
        Boon {
            id: "thoth_spell_echo".to_string(),
            god: EgyptianGod::Thoth,
            rarity: BoonRarity::Epic,
            name: "Eco Mágico".to_string(),
            description: "Suas habilidades Q têm 40% de chance de serem lançadas novamente automaticamente".to_string(),
            effects: vec![BoonEffect::SpellEcho {
                ability: "Q".to_string(),
                echo_chance: 0.4,
                echo_damage_multiplier: 0.8,
            }],
            synergy_tags: vec!["magic".to_string(), "q_ability".to_string(), "echo".to_string()],
            level: 1,
            max_level: 1,
        },
        
        Boon {
            id: "thoth_omniscience".to_string(),
            god: EgyptianGod::Thoth,
            rarity: BoonRarity::Legendary,
            name: "Onisciência".to_string(),
            description: "Vê todos os inimigos através das paredes e suas habilidades têm alcance infinito".to_string(),
            effects: vec![
                BoonEffect::WallHack,
                BoonEffect::InfiniteRange { abilities: vec!["Q".to_string(), "R".to_string()] },
            ],
            synergy_tags: vec!["magic".to_string(), "legendary".to_string(), "vision".to_string()],
            level: 1,
            max_level: 1,
        },
    ]
}