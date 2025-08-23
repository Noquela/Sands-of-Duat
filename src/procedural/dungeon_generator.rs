use bevy::prelude::*;
use super::room_types::*;
// Removed unused import
use std::collections::{HashMap, HashSet, VecDeque};
use rand::{Rng, seq::SliceRandom, SeedableRng};

#[derive(Debug, Clone)]
pub struct DungeonLayout {
    pub rooms: HashMap<RoomId, DungeonRoom>,
    pub connections: HashMap<RoomId, Vec<RoomConnection>>,
    pub start_room: RoomId,
    pub boss_rooms: Vec<RoomId>,
    pub total_rooms: u32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct RoomId(pub u32);

#[derive(Debug, Clone)]
pub struct DungeonRoom {
    pub id: RoomId,
    pub template: RoomTemplate,
    pub position: Vec2,
    pub depth: u32,
    pub is_critical_path: bool,
    pub connections: Vec<RoomConnection>,
}

#[derive(Debug, Clone)]
pub struct RoomConnection {
    pub from_room: RoomId,
    pub to_room: RoomId,
    pub direction: ConnectionDirection,
    pub is_locked: bool,
    pub unlock_condition: Option<String>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ConnectionDirection {
    North,
    South,
    East,
    West,
}

#[derive(Resource)]
pub struct GeneratedDungeon {
    pub layout: DungeonLayout,
    pub current_room: RoomId,
    pub unlocked_rooms: HashSet<RoomId>,
    pub generation_seed: u64,
}

#[derive(Resource)]
pub struct DungeonGenerationConfig {
    pub total_rooms: u32,
    pub max_branches_per_room: u32,
    pub boss_room_frequency: u32, // Every N floors
    pub secret_room_chance: f32,
    pub backtrack_connections: bool,
    pub ensure_all_rooms_reachable: bool,
}

impl Default for DungeonGenerationConfig {
    fn default() -> Self {
        Self {
            total_rooms: 12,
            max_branches_per_room: 3,
            boss_room_frequency: 4, // Bosses at floors 4, 8, 12
            secret_room_chance: 0.15,
            backtrack_connections: true,
            ensure_all_rooms_reachable: true,
        }
    }
}

pub struct DungeonGeneratorPlugin;

impl Plugin for DungeonGeneratorPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<DungeonGenerationConfig>()
            .add_systems(Startup, generate_initial_dungeon)
            .add_systems(Update, (
                handle_room_unlock_events,
                validate_dungeon_integrity,
                update_room_accessibility,
            ));
    }
}

fn generate_initial_dungeon(
    mut commands: Commands,
    config: Res<DungeonGenerationConfig>,
) {
    info!("🎲 Generating procedural dungeon...");
    
    let seed = 42u64; // In practice, this would be random or from settings
    let layout = DungeonGenerator::generate_dungeon(&config, seed);
    
    info!("✅ Generated dungeon with {} rooms", layout.rooms.len());
    info!("🏁 Start room: {:?}", layout.start_room);
    info!("👑 Boss rooms: {:?}", layout.boss_rooms);
    
    let mut unlocked_rooms = HashSet::new();
    unlocked_rooms.insert(layout.start_room);
    
    commands.insert_resource(GeneratedDungeon {
        current_room: layout.start_room,
        unlocked_rooms,
        generation_seed: seed,
        layout,
    });
}

fn handle_room_unlock_events(
    // This would be connected to game events
    // For now, it's a placeholder
) {
    // Handle events that unlock new rooms
    // e.g., defeating bosses, finding keys, completing puzzles
}

fn validate_dungeon_integrity(
    dungeon: Res<GeneratedDungeon>,
) {
    // Periodic validation that the dungeon is still in a valid state
    // Useful for debugging and ensuring generation quality
    if dungeon.is_changed() {
        if !DungeonValidator::validate_connectivity(&dungeon.layout) {
            error!("⚠️ Dungeon connectivity validation failed!");
        }
        
        if !DungeonValidator::validate_critical_path(&dungeon.layout) {
            error!("⚠️ Dungeon critical path validation failed!");
        }
    }
}

fn update_room_accessibility(
    _dungeon: ResMut<GeneratedDungeon>,
    // Add game state dependencies here
) {
    // Update which rooms are accessible based on current game state
    // This would integrate with key/unlock systems, boss defeats, etc.
}

pub struct DungeonGenerator;

impl DungeonGenerator {
    pub fn generate_dungeon(config: &DungeonGenerationConfig, seed: u64) -> DungeonLayout {
        let mut rng = rand_chacha::ChaCha8Rng::seed_from_u64(seed);
        
        // Step 1: Generate critical path (start -> boss rooms -> end)
        let critical_path = Self::generate_critical_path(config, &mut rng);
        
        // Step 2: Add branching rooms off the critical path
        let all_rooms = Self::add_branching_rooms(config, critical_path, &mut rng);
        
        // Step 3: Generate connections between rooms
        let connections = Self::generate_connections(&all_rooms, config, &mut rng);
        
        // Step 4: Add secret rooms with special connections
        let (final_rooms, final_connections) = Self::add_secret_rooms(
            all_rooms, 
            connections, 
            config, 
            &mut rng
        );
        
        // Step 5: Validate and fix connectivity issues
        let validated_layout = Self::validate_and_fix_layout(
            final_rooms, 
            final_connections, 
            config
        );
        
        validated_layout
    }
    
    fn generate_critical_path(
        config: &DungeonGenerationConfig,
        rng: &mut impl Rng,
    ) -> Vec<DungeonRoom> {
        let mut critical_rooms = Vec::new();
        let mut room_id_counter = 0u32;
        
        // Start room
        let start_room = DungeonRoom {
            id: RoomId(room_id_counter),
            template: RoomTemplateGenerator::generate_room_template(
                RoomType::Combat, 
                BiomeType::Desert, 
                1
            ),
            position: Vec2::ZERO,
            depth: 0,
            is_critical_path: true,
            connections: Vec::new(),
        };
        critical_rooms.push(start_room);
        room_id_counter += 1;
        
        // Generate boss rooms at fixed intervals
        let boss_floors = (0..config.total_rooms)
            .step_by(config.boss_room_frequency as usize)
            .skip(1) // Skip floor 0 (start room)
            .collect::<Vec<_>>();
        
        for &floor in &boss_floors {
            let biome = determine_biome_for_floor(floor);
            let boss_room = DungeonRoom {
                id: RoomId(room_id_counter),
                template: RoomTemplateGenerator::generate_room_template(
                    RoomType::Boss,
                    biome,
                    floor,
                ),
                position: Vec2::new(0.0, floor as f32 * 100.0),
                depth: floor,
                is_critical_path: true,
                connections: Vec::new(),
            };
            critical_rooms.push(boss_room);
            room_id_counter += 1;
        }
        
        // Fill in combat rooms between boss rooms
        let mut depth = 1u32;
        let mut insertion_index = 1;
        
        while depth < config.total_rooms && insertion_index < critical_rooms.len() {
            if critical_rooms[insertion_index].depth > depth {
                let biome = determine_biome_for_floor(depth);
                let room_type = if rng.gen_bool(0.8) { 
                    RoomType::Combat 
                } else { 
                    RoomType::Elite 
                };
                
                let room = DungeonRoom {
                    id: RoomId(room_id_counter),
                    template: RoomTemplateGenerator::generate_room_template(room_type, biome, depth),
                    position: Vec2::new(0.0, depth as f32 * 100.0),
                    depth,
                    is_critical_path: true,
                    connections: Vec::new(),
                };
                
                critical_rooms.insert(insertion_index, room);
                room_id_counter += 1;
            }
            insertion_index += 1;
            depth += 1;
        }
        
        info!("🛤️ Generated critical path with {} rooms", critical_rooms.len());
        critical_rooms
    }
    
    fn add_branching_rooms(
        config: &DungeonGenerationConfig,
        critical_rooms: Vec<DungeonRoom>,
        rng: &mut impl Rng,
    ) -> Vec<DungeonRoom> {
        let mut all_rooms = critical_rooms.clone();
        let mut room_id_counter = critical_rooms.len() as u32;
        
        // Add branches from each critical path room
        for critical_room in &critical_rooms {
            let num_branches = rng.gen_range(0..=config.max_branches_per_room);
            
            for branch_idx in 0..num_branches {
                let branch_room_type = Self::select_branch_room_type(critical_room, rng);
                let biome = determine_biome_for_floor(critical_room.depth);
                
                // Position branches around the critical room
                let angle = (branch_idx as f32 / num_branches as f32) * std::f32::consts::TAU;
                let offset = Vec2::new(angle.cos(), angle.sin()) * 150.0;
                let branch_position = critical_room.position + offset;
                
                let branch_room = DungeonRoom {
                    id: RoomId(room_id_counter),
                    template: RoomTemplateGenerator::generate_room_template(
                        branch_room_type,
                        biome,
                        critical_room.depth,
                    ),
                    position: branch_position,
                    depth: critical_room.depth,
                    is_critical_path: false,
                    connections: Vec::new(),
                };
                
                all_rooms.push(branch_room);
                room_id_counter += 1;
            }
        }
        
        info!("🌿 Added {} branch rooms", all_rooms.len() - critical_rooms.len());
        all_rooms
    }
    
    fn select_branch_room_type(parent_room: &DungeonRoom, rng: &mut impl Rng) -> RoomType {
        let weights = match parent_room.template.room_type {
            RoomType::Combat => vec![
                (RoomType::Treasure, 0.3),
                (RoomType::Shop, 0.15),
                (RoomType::Event, 0.2),
                (RoomType::Rest, 0.1),
                (RoomType::Elite, 0.25),
            ],
            RoomType::Boss => vec![
                (RoomType::Treasure, 0.6),
                (RoomType::Shop, 0.3),
                (RoomType::Rest, 0.1),
            ],
            RoomType::Elite => vec![
                (RoomType::Treasure, 0.5),
                (RoomType::Rest, 0.3),
                (RoomType::Shop, 0.2),
            ],
            _ => vec![
                (RoomType::Combat, 0.5),
                (RoomType::Treasure, 0.3),
                (RoomType::Event, 0.2),
            ],
        };
        
        let total_weight: f32 = weights.iter().map(|(_, w)| w).sum();
        let mut random_value = rng.gen::<f32>() * total_weight;
        
        for (room_type, weight) in weights {
            random_value -= weight;
            if random_value <= 0.0 {
                return room_type;
            }
        }
        
        RoomType::Combat // Fallback
    }
    
    fn generate_connections(
        rooms: &[DungeonRoom],
        config: &DungeonGenerationConfig,
        rng: &mut impl Rng,
    ) -> HashMap<RoomId, Vec<RoomConnection>> {
        let mut connections: HashMap<RoomId, Vec<RoomConnection>> = HashMap::new();
        
        // Connect critical path rooms sequentially
        let critical_rooms: Vec<_> = rooms.iter()
            .filter(|r| r.is_critical_path)
            .collect();
        
        for window in critical_rooms.windows(2) {
            let from_room = window[0];
            let to_room = window[1];
            
            let connection = RoomConnection {
                from_room: from_room.id,
                to_room: to_room.id,
                direction: Self::calculate_connection_direction(
                    from_room.position, 
                    to_room.position
                ),
                is_locked: false,
                unlock_condition: None,
            };
            
            connections.entry(from_room.id)
                .or_insert_with(Vec::new)
                .push(connection.clone());
                
            // Add reverse connection if backtracking is enabled
            if config.backtrack_connections {
                let reverse_connection = RoomConnection {
                    from_room: to_room.id,
                    to_room: from_room.id,
                    direction: Self::opposite_direction(connection.direction),
                    is_locked: false,
                    unlock_condition: None,
                };
                
                connections.entry(to_room.id)
                    .or_insert_with(Vec::new)
                    .push(reverse_connection);
            }
        }
        
        // Connect branch rooms to their nearest critical path room
        let branch_rooms: Vec<_> = rooms.iter()
            .filter(|r| !r.is_critical_path)
            .collect();
            
        for branch_room in branch_rooms {
            if let Some(nearest_critical) = Self::find_nearest_critical_room(
                branch_room, 
                &critical_rooms
            ) {
                let connection = RoomConnection {
                    from_room: nearest_critical.id,
                    to_room: branch_room.id,
                    direction: Self::calculate_connection_direction(
                        nearest_critical.position,
                        branch_room.position,
                    ),
                    is_locked: Self::should_lock_branch_connection(branch_room, rng),
                    unlock_condition: if Self::should_lock_branch_connection(branch_room, rng) {
                        Some("defeat_room_enemies".to_string())
                    } else {
                        None
                    },
                };
                
                connections.entry(nearest_critical.id)
                    .or_insert_with(Vec::new)
                    .push(connection.clone());
                    
                // Add reverse connection
                let reverse_connection = RoomConnection {
                    from_room: branch_room.id,
                    to_room: nearest_critical.id,
                    direction: Self::opposite_direction(connection.direction),
                    is_locked: false,
                    unlock_condition: None,
                };
                
                connections.entry(branch_room.id)
                    .or_insert_with(Vec::new)
                    .push(reverse_connection);
            }
        }
        
        info!("🔗 Generated {} room connections", 
              connections.values().map(|v| v.len()).sum::<usize>());
        
        connections
    }
    
    fn add_secret_rooms(
        mut rooms: Vec<DungeonRoom>,
        mut connections: HashMap<RoomId, Vec<RoomConnection>>,
        config: &DungeonGenerationConfig,
        rng: &mut impl Rng,
    ) -> (Vec<DungeonRoom>, HashMap<RoomId, Vec<RoomConnection>>) {
        let mut room_id_counter = rooms.len() as u32;
        let secret_rooms_count = ((rooms.len() as f32) * config.secret_room_chance) as u32;
        
        for _ in 0..secret_rooms_count {
            if let Some(parent_room) = rooms.choose(rng) {
                let biome = determine_biome_for_floor(parent_room.depth);
                
                // Secret rooms are positioned away from the main paths
                let secret_position = parent_room.position + 
                    Vec2::new(rng.gen_range(-200.0..200.0), rng.gen_range(-200.0..200.0));
                
                let secret_room = DungeonRoom {
                    id: RoomId(room_id_counter),
                    template: RoomTemplateGenerator::generate_room_template(
                        RoomType::Secret,
                        biome,
                        parent_room.depth,
                    ),
                    position: secret_position,
                    depth: parent_room.depth,
                    is_critical_path: false,
                    connections: Vec::new(),
                };
                
                // Secret rooms have special unlock conditions
                let secret_connection = RoomConnection {
                    from_room: parent_room.id,
                    to_room: secret_room.id,
                    direction: Self::calculate_connection_direction(
                        parent_room.position,
                        secret_position,
                    ),
                    is_locked: true,
                    unlock_condition: Some("find_secret_switch".to_string()),
                };
                
                connections.entry(parent_room.id)
                    .or_insert_with(Vec::new)
                    .push(secret_connection);
                
                rooms.push(secret_room);
                room_id_counter += 1;
            }
        }
        
        if secret_rooms_count > 0 {
            info!("🔐 Added {} secret rooms", secret_rooms_count);
        }
        
        (rooms, connections)
    }
    
    fn validate_and_fix_layout(
        rooms: Vec<DungeonRoom>,
        connections: HashMap<RoomId, Vec<RoomConnection>>,
        config: &DungeonGenerationConfig,
    ) -> DungeonLayout {
        let start_room = rooms.iter()
            .find(|r| r.depth == 0)
            .map(|r| r.id)
            .unwrap_or(RoomId(0));
            
        let boss_rooms = rooms.iter()
            .filter(|r| r.template.room_type == RoomType::Boss)
            .map(|r| r.id)
            .collect();
        
        let room_map = rooms.into_iter()
            .map(|room| (room.id, room))
            .collect();
        
        let layout = DungeonLayout {
            rooms: room_map,
            connections,
            start_room,
            boss_rooms,
            total_rooms: config.total_rooms,
        };
        
        // Validate connectivity
        if !DungeonValidator::validate_connectivity(&layout) {
            warn!("⚠️ Dungeon connectivity issues detected, but proceeding anyway");
        }
        
        layout
    }
    
    // Helper methods
    fn calculate_connection_direction(from: Vec2, to: Vec2) -> ConnectionDirection {
        let delta = to - from;
        if delta.y.abs() > delta.x.abs() {
            if delta.y > 0.0 { ConnectionDirection::North } else { ConnectionDirection::South }
        } else {
            if delta.x > 0.0 { ConnectionDirection::East } else { ConnectionDirection::West }
        }
    }
    
    fn opposite_direction(dir: ConnectionDirection) -> ConnectionDirection {
        match dir {
            ConnectionDirection::North => ConnectionDirection::South,
            ConnectionDirection::South => ConnectionDirection::North,
            ConnectionDirection::East => ConnectionDirection::West,
            ConnectionDirection::West => ConnectionDirection::East,
        }
    }
    
    fn find_nearest_critical_room<'a>(
        branch_room: &DungeonRoom,
        critical_rooms: &[&'a DungeonRoom],
    ) -> Option<&'a DungeonRoom> {
        critical_rooms.iter()
            .filter(|r| r.depth == branch_room.depth)
            .min_by(|a, b| {
                let dist_a = branch_room.position.distance(a.position);
                let dist_b = branch_room.position.distance(b.position);
                dist_a.partial_cmp(&dist_b).unwrap()
            })
            .copied()
    }
    
    fn should_lock_branch_connection(room: &DungeonRoom, rng: &mut impl Rng) -> bool {
        match room.template.room_type {
            RoomType::Treasure => rng.gen_bool(0.3),
            RoomType::Elite => rng.gen_bool(0.1),
            RoomType::Shop => false,
            RoomType::Rest => false,
            _ => rng.gen_bool(0.1),
        }
    }
}

pub struct DungeonValidator;

impl DungeonValidator {
    pub fn validate_connectivity(layout: &DungeonLayout) -> bool {
        // Use BFS to check if all rooms are reachable from start room
        let mut visited = HashSet::new();
        let mut queue = VecDeque::new();
        
        queue.push_back(layout.start_room);
        visited.insert(layout.start_room);
        
        while let Some(room_id) = queue.pop_front() {
            if let Some(connections) = layout.connections.get(&room_id) {
                for connection in connections {
                    if !connection.is_locked && !visited.contains(&connection.to_room) {
                        visited.insert(connection.to_room);
                        queue.push_back(connection.to_room);
                    }
                }
            }
        }
        
        // Count rooms that should be immediately accessible (not locked/secret)
        let immediately_accessible = layout.rooms.values()
            .filter(|room| {
                // Check if this room is connected via unlocked connections
                layout.connections.values()
                    .flat_map(|connections| connections.iter())
                    .any(|conn| conn.to_room == room.id && !conn.is_locked)
                    || room.id == layout.start_room
            })
            .count();
        
        let reachable_count = visited.len();
        
        info!("🔍 Connectivity check: {}/{} immediately accessible rooms reachable", 
              reachable_count, immediately_accessible);
        
        // All immediately accessible rooms should be reachable
        reachable_count >= immediately_accessible
    }
    
    pub fn validate_critical_path(layout: &DungeonLayout) -> bool {
        // Check that there's a valid path from start to all boss rooms
        for &boss_room in &layout.boss_rooms {
            if !Self::has_path_between(layout, layout.start_room, boss_room) {
                warn!("⚠️ No path from start to boss room {:?}", boss_room);
                return false;
            }
        }
        
        true
    }
    
    fn has_path_between(layout: &DungeonLayout, start: RoomId, end: RoomId) -> bool {
        let mut visited = HashSet::new();
        let mut queue = VecDeque::new();
        
        queue.push_back(start);
        visited.insert(start);
        
        while let Some(room_id) = queue.pop_front() {
            if room_id == end {
                return true;
            }
            
            if let Some(connections) = layout.connections.get(&room_id) {
                for connection in connections {
                    if !visited.contains(&connection.to_room) {
                        visited.insert(connection.to_room);
                        queue.push_back(connection.to_room);
                    }
                }
            }
        }
        
        false
    }
}

fn determine_biome_for_floor(floor: u32) -> BiomeType {
    match floor {
        1..=4 => BiomeType::Desert,
        5..=8 => BiomeType::Temple,
        9..=12 => BiomeType::Underworld,
        _ => BiomeType::Underworld,
    }
}