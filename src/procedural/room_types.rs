use bevy::prelude::*;
use rand::{Rng, thread_rng};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum RoomType {
    Combat,      // Standard enemy encounters
    Elite,       // Tougher enemies with better rewards
    Treasure,    // Chests and rewards
    Shop,        // Purchase boons and items with gold
    Event,       // Story events and choices
    Rest,        // Heal and upgrade
    Boss,        // Major boss encounters
    Secret,      // Hidden rooms with special rewards
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum BiomeType {
    Desert,      // Sandy dunes, scorpions, mummies
    Temple,      // Stone corridors, priests, guardians
    Underworld,  // Dark caves, spirits, Anubis realm
}

#[derive(Debug, Clone)]
pub struct RoomTemplate {
    pub room_type: RoomType,
    pub biome: BiomeType,
    pub name: String,
    pub description: String,
    pub min_enemies: u32,
    pub max_enemies: u32,
    pub enemy_types: Vec<String>,
    pub reward_multiplier: f32,
    pub difficulty_modifier: f32,
    pub special_mechanics: Vec<String>,
}

impl RoomType {
    pub fn get_display_name(&self) -> &str {
        match self {
            RoomType::Combat => "Câmara de Combate",
            RoomType::Elite => "Santuário dos Guardiões",
            RoomType::Treasure => "Tesouro Egípcio",
            RoomType::Shop => "Mercador do Deserto",
            RoomType::Event => "Encontro Divino",
            RoomType::Rest => "Oásis Sagrado",
            RoomType::Boss => "Trono dos Deuses",
            RoomType::Secret => "Câmara Secreta",
        }
    }
    
    pub fn get_weight_by_floor(&self, floor: u32) -> f32 {
        match self {
            RoomType::Combat => match floor {
                1..=3 => 0.6,
                4..=7 => 0.5,
                8..=10 => 0.4,
                _ => 0.3,
            },
            RoomType::Elite => match floor {
                1..=2 => 0.0,
                3..=5 => 0.15,
                6..=9 => 0.25,
                _ => 0.3,
            },
            RoomType::Treasure => match floor {
                1..=3 => 0.2,
                4..=7 => 0.15,
                _ => 0.1,
            },
            RoomType::Shop => match floor {
                1..=2 => 0.05,
                3..=6 => 0.1,
                _ => 0.15,
            },
            RoomType::Event => 0.1,
            RoomType::Rest => match floor {
                1..=3 => 0.05,
                4..=6 => 0.1,
                _ => 0.15,
            },
            RoomType::Boss => 0.0, // Bosses are placed manually
            RoomType::Secret => 0.02, // Very rare
        }
    }
}

impl BiomeType {
    pub fn get_display_name(&self) -> &str {
        match self {
            BiomeType::Desert => "Deserto das Areias Eternas",
            BiomeType::Temple => "Templos dos Faraós",
            BiomeType::Underworld => "Reino de Anúbis",
        }
    }
    
    pub fn get_floor_range(&self) -> (u32, u32) {
        match self {
            BiomeType::Desert => (1, 4),
            BiomeType::Temple => (5, 8),
            BiomeType::Underworld => (9, 12),
        }
    }
    
    pub fn get_ambient_color(&self) -> Color {
        match self {
            BiomeType::Desert => Color::rgb(1.0, 0.9, 0.6),
            BiomeType::Temple => Color::rgb(0.8, 0.7, 0.5),
            BiomeType::Underworld => Color::rgb(0.4, 0.3, 0.6),
        }
    }
}

pub struct RoomTemplateGenerator;

impl RoomTemplateGenerator {
    pub fn generate_room_template(room_type: RoomType, biome: BiomeType, floor: u32) -> RoomTemplate {
        let mut rng = thread_rng();
        
        match (room_type, biome) {
            // Desert Combat Rooms
            (RoomType::Combat, BiomeType::Desert) => {
                let templates = vec![
                    ("Dunas Mortais", "Escorpiões gigantes emergem das areias douradas", 
                     vec!["Desert_Scorpion", "Sand_Mummy"], 2, 4),
                    ("Oásis Envenenado", "Águas contaminadas atraem criaturas perigosas",
                     vec!["Poisonous_Snake", "Desert_Bandit"], 3, 5),
                    ("Tempestade de Areia", "Visibilidade limitada, inimigos aparecem das dunas",
                     vec!["Sand_Elemental", "Desert_Warrior"], 2, 3),
                ];
                let (name, desc, enemies, min, max) = templates[rng.gen_range(0..templates.len())].clone();
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: min + floor / 3,
                    max_enemies: max + floor / 2,
                    enemy_types: enemies.iter().map(|s| s.to_string()).collect(),
                    reward_multiplier: 1.0 + floor as f32 * 0.1,
                    difficulty_modifier: 1.0 + floor as f32 * 0.15,
                    special_mechanics: vec!["Sand_Storm_Mechanic".to_string()],
                }
            },
            
            // Temple Combat Rooms
            (RoomType::Combat, BiomeType::Temple) => {
                let templates = vec![
                    ("Salão dos Guardiões", "Estátuas animadas protegem os segredos antigos",
                     vec!["Stone_Guardian", "Temple_Priest"], 2, 4),
                    ("Câmara dos Hieróglifos", "Símbolos nas paredes invocam maldições",
                     vec!["Cursed_Scribe", "Hieroglyph_Specter"], 3, 5),
                    ("Altar dos Sacrifícios", "Sangue antigo ainda mancha o mármore",
                     vec!["Sacrificial_Priest", "Blood_Wraith"], 2, 3),
                ];
                let (name, desc, enemies, min, max) = templates[rng.gen_range(0..templates.len())].clone();
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: min + floor / 3,
                    max_enemies: max + floor / 2,
                    enemy_types: enemies.iter().map(|s| s.to_string()).collect(),
                    reward_multiplier: 1.2 + floor as f32 * 0.1,
                    difficulty_modifier: 1.2 + floor as f32 * 0.15,
                    special_mechanics: vec!["Hieroglyph_Curse".to_string()],
                }
            },
            
            // Underworld Combat Rooms
            (RoomType::Combat, BiomeType::Underworld) => {
                let templates = vec![
                    ("Rio dos Mortos", "Almas perdidas emergem das águas sombrias",
                     vec!["Lost_Soul", "Ferryman_Shadow"], 3, 6),
                    ("Salão do Julgamento", "Anúbis observa enquanto você luta pela vida",
                     vec!["Judgment_Wraith", "Underworld_Guardian"], 2, 4),
                    ("Cavernas do Esquecimento", "Ecos de vidas passadas assombram o ar",
                     vec!["Memory_Phantom", "Bone_Stalker"], 4, 7),
                ];
                let (name, desc, enemies, min, max) = templates[rng.gen_range(0..templates.len())].clone();
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: min + floor / 2,
                    max_enemies: max + floor,
                    enemy_types: enemies.iter().map(|s| s.to_string()).collect(),
                    reward_multiplier: 1.5 + floor as f32 * 0.12,
                    difficulty_modifier: 1.5 + floor as f32 * 0.2,
                    special_mechanics: vec!["Soul_Drain".to_string(), "Shadow_Portal".to_string()],
                }
            },
            
            // Elite Rooms
            (RoomType::Elite, biome) => {
                let (name, desc, enemies) = match biome {
                    BiomeType::Desert => ("Faraó das Areias", "Um antigo governante desperta de seu sono eterno", 
                                         vec!["Sand_Pharaoh", "Royal_Guard"]),
                    BiomeType::Temple => ("Sumo Sacerdote", "O último guardião dos segredos divinos",
                                         vec!["High_Priest", "Temple_Champion"]),
                    BiomeType::Underworld => ("Lorde das Sombras", "Comandante dos exércitos de Anúbis",
                                             vec!["Shadow_Lord", "Death_Knight"]),
                };
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: 1,
                    max_enemies: 2,
                    enemy_types: enemies.iter().map(|s| s.to_string()).collect(),
                    reward_multiplier: 2.0 + floor as f32 * 0.2,
                    difficulty_modifier: 2.0 + floor as f32 * 0.3,
                    special_mechanics: vec!["Elite_Aura".to_string(), "Phase_Transition".to_string()],
                }
            },
            
            // Treasure Rooms
            (RoomType::Treasure, biome) => {
                let (name, desc) = match biome {
                    BiomeType::Desert => ("Tesouro Enterrado", "Riquezas perdidas nas areias do tempo"),
                    BiomeType::Temple => ("Câmara do Tesouro Real", "Ouro e joias dos antigos faraós"),
                    BiomeType::Underworld => ("Cofre das Almas", "Tesouros pagos com vidas"),
                };
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: 0,
                    max_enemies: 0,
                    enemy_types: vec![],
                    reward_multiplier: 1.5 + floor as f32 * 0.1,
                    difficulty_modifier: 0.0,
                    special_mechanics: vec!["Trapped_Chest".to_string()],
                }
            },
            
            // Shop Rooms
            (RoomType::Shop, biome) => {
                let (name, desc) = match biome {
                    BiomeType::Desert => ("Caravana do Deserto", "Mercadores nômades com bens exóticos"),
                    BiomeType::Temple => ("Loja do Escriba", "Conhecimento e artefatos antigos à venda"),
                    BiomeType::Underworld => ("Mercador das Sombras", "Negócios feitos com almas e sangue"),
                };
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: 0,
                    max_enemies: 0,
                    enemy_types: vec![],
                    reward_multiplier: 1.0,
                    difficulty_modifier: 0.0,
                    special_mechanics: vec!["Shop_Keeper".to_string()],
                }
            },
            
            // Event Rooms
            (RoomType::Event, biome) => {
                let events = match biome {
                    BiomeType::Desert => vec![
                        ("Oráculo do Deserto", "Uma vidente oferece visões do futuro"),
                        ("Miragem Divina", "Visões dos deuses testam sua sabedoria"),
                        ("Caravana Perdida", "Sobreviventes precisam de ajuda"),
                    ],
                    BiomeType::Temple => vec![
                        ("Altar de Thoth", "O deus da sabedoria oferece conhecimento"),
                        ("Julgamento de Maät", "A deusa da justiça pesa seu coração"),
                        ("Ritual Interrompido", "Um cerimônia antiga precisa ser completada"),
                    ],
                    BiomeType::Underworld => vec![
                        ("Julgamento de Anúbis", "O deus chacal testa sua dignidade"),
                        ("Rio Styx", "Atravesse as águas dos mortos"),
                        ("Balança do Coração", "Suas ações passadas são pesadas"),
                    ],
                };
                let (name, desc) = events[rng.gen_range(0..events.len())];
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: 0,
                    max_enemies: 0,
                    enemy_types: vec![],
                    reward_multiplier: 1.0,
                    difficulty_modifier: 0.0,
                    special_mechanics: vec!["Event_Choice".to_string(), "God_Interaction".to_string()],
                }
            },
            
            // Rest Rooms
            (RoomType::Rest, biome) => {
                let (name, desc) = match biome {
                    BiomeType::Desert => ("Oásis Sagrado", "Águas cristalinas curam corpo e alma"),
                    BiomeType::Temple => ("Câmara de Meditação", "Paz entre as estátuas silenciosas"),
                    BiomeType::Underworld => ("Refúgio das Almas", "Um raro santuário no reino sombrio"),
                };
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: 0,
                    max_enemies: 0,
                    enemy_types: vec![],
                    reward_multiplier: 0.0,
                    difficulty_modifier: 0.0,
                    special_mechanics: vec!["Healing_Spring".to_string(), "Meditation_Bonus".to_string()],
                }
            },
            
            // Boss Rooms
            (RoomType::Boss, biome) => {
                let (name, desc, boss) = match biome {
                    BiomeType::Desert => ("Trono das Areias Eternas", "O Faraó Supremo desperta", vec!["Pharaoh_Boss"]),
                    BiomeType::Temple => ("Sanctum Sanctorum", "Set, o Deus do Caos, aguarda", vec!["Set_Boss"]),
                    BiomeType::Underworld => ("Salão do Julgamento Final", "Anúbis em pessoa te julga", vec!["Anubis_Boss"]),
                };
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: 1,
                    max_enemies: 1,
                    enemy_types: boss.iter().map(|s| s.to_string()).collect(),
                    reward_multiplier: 5.0,
                    difficulty_modifier: 5.0 + floor as f32 * 0.5,
                    special_mechanics: vec![
                        "Boss_Phases".to_string(), 
                        "Arena_Hazards".to_string(),
                        "Divine_Powers".to_string()
                    ],
                }
            },
            
            // Secret Rooms
            (RoomType::Secret, biome) => {
                let (name, desc) = match biome {
                    BiomeType::Desert => ("Tumba Esquecida", "Segredos enterrados nas profundezas"),
                    BiomeType::Temple => ("Arquivo Proibido", "Conhecimento que deveria permanecer oculto"),
                    BiomeType::Underworld => ("Vault das Almas Perdidas", "Tesouros de vidas esquecidas"),
                };
                
                RoomTemplate {
                    room_type,
                    biome,
                    name: name.to_string(),
                    description: desc.to_string(),
                    min_enemies: rng.gen_range(0..=2),
                    max_enemies: rng.gen_range(2..=4),
                    enemy_types: vec!["Secret_Guardian".to_string()],
                    reward_multiplier: 3.0,
                    difficulty_modifier: 1.0,
                    special_mechanics: vec!["Hidden_Entrance".to_string(), "Legendary_Loot".to_string()],
                }
            },
        }
    }
}