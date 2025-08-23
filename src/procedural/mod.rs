use bevy::prelude::*;

pub mod room_system;
pub mod biome_system;
pub mod dungeon_generator;
pub mod room_types;

pub use room_system::*;
pub use biome_system::*;
pub use dungeon_generator::*;
pub use room_types::*;

pub struct ProceduralPlugin;

impl Plugin for ProceduralPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins((
            RoomSystemPlugin,
            BiomeSystemPlugin,
            DungeonGeneratorPlugin,
        ));
    }
}