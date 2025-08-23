use bevy::prelude::*;
use super::room_types::*;
use std::collections::HashMap;
use rand::Rng;

#[derive(Resource)]
pub struct CurrentRoom {
    pub template: RoomTemplate,
    pub is_completed: bool,
    pub enemies_remaining: u32,
    pub loot_spawned: bool,
}

#[derive(Resource)]
pub struct DungeonState {
    pub current_floor: u32,
    pub rooms_completed: u32,
    pub total_rooms: u32,
    pub current_biome: BiomeType,
    pub room_history: Vec<RoomType>,
}

impl Default for DungeonState {
    fn default() -> Self {
        Self {
            current_floor: 1,
            rooms_completed: 0,
            total_rooms: 12,
            current_biome: BiomeType::Desert,
            room_history: Vec::new(),
        }
    }
}

#[derive(Component)]
pub struct RoomEntity;

#[derive(Component)]
pub struct RoomExit {
    pub direction: ExitDirection,
    pub leads_to: Option<Entity>,
}

#[derive(Debug, Clone, Copy)]
pub enum ExitDirection {
    North,
    South,
    East,
    West,
}

#[derive(Event)]
pub struct RoomCompletedEvent {
    pub room_type: RoomType,
    pub floor: u32,
    pub enemies_defeated: u32,
    pub time_taken: f32,
}

#[derive(Event)]
pub struct GenerateNextRoomEvent {
    pub preferred_type: Option<RoomType>,
}

#[derive(Event)]
pub struct TransitionToRoomEvent {
    pub new_room: RoomTemplate,
}

pub struct RoomSystemPlugin;

impl Plugin for RoomSystemPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<DungeonState>()
            .add_event::<RoomCompletedEvent>()
            .add_event::<GenerateNextRoomEvent>()
            .add_event::<TransitionToRoomEvent>()
            .add_systems(Startup, initialize_room_system)
            .add_systems(Update, (
                monitor_room_completion,
                handle_room_generation_requests,
                handle_room_transitions,
                update_biome_transitions,
                track_room_progress,
            ));
    }
}

fn initialize_room_system(
    mut commands: Commands,
    mut dungeon_state: ResMut<DungeonState>,
) {
    info!("🏛️ Initializing room system...");
    
    // Start with a Desert Combat room
    let initial_room = RoomTemplateGenerator::generate_room_template(
        RoomType::Combat,
        BiomeType::Desert,
        1
    );
    
    info!("🏜️ Starting room: {}", initial_room.name);
    
    commands.insert_resource(CurrentRoom {
        template: initial_room.clone(),
        is_completed: false,
        enemies_remaining: initial_room.max_enemies,
        loot_spawned: false,
    });
    
    dungeon_state.room_history.push(RoomType::Combat);
    
    info!("✅ Room system initialized");
}

fn monitor_room_completion(
    mut current_room: ResMut<CurrentRoom>,
    mut room_completed_events: EventWriter<RoomCompletedEvent>,
    mut dungeon_state: ResMut<DungeonState>,
    // We'll add enemy tracking later
    time: Res<Time>,
) {
    if !current_room.is_completed && current_room.enemies_remaining == 0 {
        info!("🎉 Room '{}' completed!", current_room.template.name);
        
        current_room.is_completed = true;
        dungeon_state.rooms_completed += 1;
        
        room_completed_events.send(RoomCompletedEvent {
            room_type: current_room.template.room_type,
            floor: dungeon_state.current_floor,
            enemies_defeated: current_room.template.max_enemies,
            time_taken: time.elapsed_seconds(), // Simplified
        });
        
        // Auto-trigger next room generation after combat rooms
        if matches!(current_room.template.room_type, RoomType::Combat | RoomType::Elite) {
            // This would typically be handled by the transition system
        }
    }
}

fn handle_room_generation_requests(
    mut generation_events: EventReader<GenerateNextRoomEvent>,
    mut transition_events: EventWriter<TransitionToRoomEvent>,
    dungeon_state: Res<DungeonState>,
) {
    for event in generation_events.read() {
        let new_room = generate_next_room(&dungeon_state, event.preferred_type);
        
        info!("🎲 Generated new room: {} ({})", 
              new_room.name, 
              new_room.room_type.get_display_name());
        
        transition_events.send(TransitionToRoomEvent { new_room });
    }
}

fn handle_room_transitions(
    mut commands: Commands,
    mut transition_events: EventReader<TransitionToRoomEvent>,
    mut dungeon_state: ResMut<DungeonState>,
    current_room_query: Query<Entity, With<RoomEntity>>,
) {
    for event in transition_events.read() {
        // Clean up current room entities
        for entity in current_room_query.iter() {
            commands.entity(entity).despawn_recursive();
        }
        
        // Set up new room
        let new_room = &event.new_room;
        
        commands.insert_resource(CurrentRoom {
            template: new_room.clone(),
            is_completed: matches!(new_room.room_type, 
                                 RoomType::Treasure | RoomType::Shop | RoomType::Rest),
            enemies_remaining: new_room.max_enemies,
            loot_spawned: false,
        });
        
        // Update dungeon state
        dungeon_state.current_floor += 1;
        dungeon_state.room_history.push(new_room.room_type);
        
        // Spawn room environment
        spawn_room_environment(&mut commands, new_room);
        
        info!("🚪 Transitioned to room: {} (Floor {})", 
              new_room.name, dungeon_state.current_floor);
    }
}

fn update_biome_transitions(
    mut dungeon_state: ResMut<DungeonState>,
) {
    let floor = dungeon_state.current_floor;
    let new_biome = determine_biome_for_floor(floor);
    
    if new_biome != dungeon_state.current_biome {
        info!("🌍 Entering new biome: {} (Floor {})", 
              new_biome.get_display_name(), floor);
        dungeon_state.current_biome = new_biome;
    }
}

fn track_room_progress(
    dungeon_state: Res<DungeonState>,
    current_room: Res<CurrentRoom>,
) {
    // This system can be used for analytics and progression tracking
    if dungeon_state.is_changed() {
        let progress = (dungeon_state.rooms_completed as f32 / dungeon_state.total_rooms as f32) * 100.0;
        
        info!("📊 Dungeon Progress: {:.1}% ({}/{}) - Current: {}", 
              progress, 
              dungeon_state.rooms_completed,
              dungeon_state.total_rooms,
              current_room.template.name);
    }
}

fn generate_next_room(dungeon_state: &DungeonState, preferred_type: Option<RoomType>) -> RoomTemplate {
    use rand::{thread_rng, Rng};
    let mut rng = thread_rng();
    
    let floor = dungeon_state.current_floor + 1;
    let biome = determine_biome_for_floor(floor);
    
    // Handle preferred room type (from events, story, etc.)
    if let Some(room_type) = preferred_type {
        return RoomTemplateGenerator::generate_room_template(room_type, biome, floor);
    }
    
    // Handle special floor rules
    match floor {
        4 | 8 | 12 => {
            // Boss floors
            return RoomTemplateGenerator::generate_room_template(RoomType::Boss, biome, floor);
        },
        _ => {}
    }
    
    // Weighted room type selection
    let mut room_weights = HashMap::new();
    room_weights.insert(RoomType::Combat, RoomType::Combat.get_weight_by_floor(floor));
    room_weights.insert(RoomType::Elite, RoomType::Elite.get_weight_by_floor(floor));
    room_weights.insert(RoomType::Treasure, RoomType::Treasure.get_weight_by_floor(floor));
    room_weights.insert(RoomType::Shop, RoomType::Shop.get_weight_by_floor(floor));
    room_weights.insert(RoomType::Event, RoomType::Event.get_weight_by_floor(floor));
    room_weights.insert(RoomType::Rest, RoomType::Rest.get_weight_by_floor(floor));
    room_weights.insert(RoomType::Secret, RoomType::Secret.get_weight_by_floor(floor));
    
    // Apply history-based adjustments
    apply_history_adjustments(&mut room_weights, &dungeon_state.room_history);
    
    // Select room type based on weights
    let selected_room_type = select_weighted_room_type(&room_weights, &mut rng);
    
    RoomTemplateGenerator::generate_room_template(selected_room_type, biome, floor)
}

fn determine_biome_for_floor(floor: u32) -> BiomeType {
    match floor {
        1..=4 => BiomeType::Desert,
        5..=8 => BiomeType::Temple,
        9..=12 => BiomeType::Underworld,
        _ => BiomeType::Underworld, // Beyond normal progression
    }
}

fn apply_history_adjustments(weights: &mut HashMap<RoomType, f32>, history: &[RoomType]) {
    if history.len() >= 2 {
        let last_two = &history[history.len()-2..];
        
        // Reduce weight for repeated room types
        for room_type in last_two {
            if let Some(weight) = weights.get_mut(room_type) {
                *weight *= 0.5;
            }
        }
        
        // Encourage variety
        match last_two {
            [RoomType::Combat, RoomType::Combat] => {
                weights.entry(RoomType::Treasure).and_modify(|w| *w *= 1.5);
                weights.entry(RoomType::Event).and_modify(|w| *w *= 1.3);
            },
            [RoomType::Elite, _] => {
                weights.entry(RoomType::Rest).and_modify(|w| *w *= 2.0);
            },
            _ => {}
        }
    }
}

fn select_weighted_room_type(weights: &HashMap<RoomType, f32>, rng: &mut impl Rng) -> RoomType {
    let total_weight: f32 = weights.values().sum();
    let mut random_value = rng.gen::<f32>() * total_weight;
    
    for (room_type, weight) in weights {
        random_value -= weight;
        if random_value <= 0.0 {
            return *room_type;
        }
    }
    
    // Fallback
    RoomType::Combat
}

fn spawn_room_environment(commands: &mut Commands, room_template: &RoomTemplate) {
    // Create basic room entity
    let room_entity = commands.spawn((
        RoomEntity,
        Transform::from_translation(Vec3::ZERO),
        GlobalTransform::default(),
        Name::new(format!("Room: {}", room_template.name)),
    )).id();
    
    // Add room exits (simplified - would be more complex in full implementation)
    commands.entity(room_entity).with_children(|parent| {
        // North exit
        parent.spawn((
            RoomExit {
                direction: ExitDirection::North,
                leads_to: None,
            },
            Transform::from_translation(Vec3::new(0.0, 0.0, 10.0)),
            GlobalTransform::default(),
            Name::new("North Exit"),
        ));
        
        // Add more exits as needed based on room layout
    });
    
    info!("🏗️ Spawned room environment: {} ({})", 
          room_template.name, room_template.biome.get_display_name());
}

// Helper functions for external use
impl CurrentRoom {
    pub fn decrease_enemies(&mut self, count: u32) {
        self.enemies_remaining = self.enemies_remaining.saturating_sub(count);
    }
    
    pub fn is_cleared(&self) -> bool {
        self.enemies_remaining == 0
    }
    
    pub fn get_reward_multiplier(&self) -> f32 {
        self.template.reward_multiplier
    }
}

impl DungeonState {
    pub fn get_progress_percentage(&self) -> f32 {
        (self.rooms_completed as f32 / self.total_rooms as f32) * 100.0
    }
    
    pub fn is_boss_floor(&self) -> bool {
        matches!(self.current_floor, 4 | 8 | 12)
    }
    
    pub fn get_next_boss_floor(&self) -> u32 {
        if self.current_floor < 4 { 4 }
        else if self.current_floor < 8 { 8 }
        else { 12 }
    }
}