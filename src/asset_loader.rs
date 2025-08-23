use bevy::prelude::*;

#[derive(Resource)]
pub struct GameAssets {
    // Character Sprite Atlases - SDXL Generated with transparency
    pub pharaoh_warrior_atlas: Handle<Image>,
    pub pharaoh_warrior_layout: Handle<TextureAtlasLayout>,
    pub anubis_judge_atlas: Handle<Image>,
    pub anubis_judge_layout: Handle<TextureAtlasLayout>,
    pub isis_mother_atlas: Handle<Image>,
    pub isis_mother_layout: Handle<TextureAtlasLayout>,
    
    // Single sprite fallbacks - all SDXL generated characters
    pub pharaoh_warrior: Handle<Image>,
    pub anubis_judge: Handle<Image>,
    pub isis_mother: Handle<Image>,
    pub ra_sun_god: Handle<Image>,
    pub set_chaos: Handle<Image>,
    pub egyptian_warrior: Handle<Image>,
    pub mummy_guardian: Handle<Image>,
    pub sphinx_guardian: Handle<Image>,
    
    // Environment Backgrounds - 3D Isometric
    pub pyramid_interior: Handle<Image>,
    pub tomb_chamber: Handle<Image>,
    pub temple_halls: Handle<Image>,
    pub desert_oasis: Handle<Image>,
    
    // UI Elements - 3D Styled
    pub ankh_health: Handle<Image>,
    pub scarab_energy: Handle<Image>,
    pub eye_of_horus: Handle<Image>,
    
    // Items and Weapons - 3D Isometric
    pub khopesh_sword: Handle<Image>,
    pub ankh_artifact: Handle<Image>,
    pub canopic_jar: Handle<Image>,
    
    // 3D Environment Elements - RTX Generated Isometric
    pub egyptian_wall_section: Handle<Image>,
    pub stone_pillar_ornate: Handle<Image>,
    pub torch_brazier: Handle<Image>,
    pub anubis_guardian_statue: Handle<Image>,
}

pub struct AssetLoaderPlugin;

impl Plugin for AssetLoaderPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PreStartup, load_game_assets);
    }
}

fn load_game_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    info!("Loading RTX-generated 3D isometric game assets...");
    
    // Create texture atlas layouts for sprite animations
    let pharaoh_layout = TextureAtlasLayout::from_grid(Vec2::new(1152.0, 1152.0), 2, 2, None, None);
    let anubis_layout = TextureAtlasLayout::from_grid(Vec2::new(1152.0, 1152.0), 2, 2, None, None);
    let isis_layout = TextureAtlasLayout::from_grid(Vec2::new(1152.0, 1152.0), 2, 2, None, None);
    
    let game_assets = GameAssets {
        // SDXL-generated sprite atlases with transparency
        pharaoh_warrior_atlas: asset_server.load("sprites/pharaoh_warrior.png"),
        pharaoh_warrior_layout: texture_atlas_layouts.add(pharaoh_layout),
        anubis_judge_atlas: asset_server.load("sprites/anubis_judge.png"),
        anubis_judge_layout: texture_atlas_layouts.add(anubis_layout),
        isis_mother_atlas: asset_server.load("sprites/isis_mother.png"),
        isis_mother_layout: texture_atlas_layouts.add(isis_layout),
        
        // Single sprite fallbacks - using new 3D isometric versions
        pharaoh_warrior: asset_server.load("characters_isometric/pharaoh_warrior_iso_alpha.png"),
        anubis_judge: asset_server.load("characters_isometric/anubis_judge_iso_alpha.png"), 
        isis_mother: asset_server.load("characters/isis_mother_rtx_alpha.png"), // Keep old until new is generated
        ra_sun_god: asset_server.load("characters/ra_sun_god_rtx_alpha.png"), // Keep old until new is generated
        set_chaos: asset_server.load("characters/set_chaos_rtx_alpha.png"), // Keep old until new is generated
        egyptian_warrior: asset_server.load("characters/egyptian_warrior_rtx_alpha.png"), // Keep old until new is generated
        mummy_guardian: asset_server.load("characters/mummy_guardian_rtx_alpha.png"), // Keep old until new is generated
        sphinx_guardian: asset_server.load("characters/sphinx_guardian_rtx_alpha.png"), // Keep old until new is generated
        
        // Environments - AI generated 3D isometric backgrounds
        pyramid_interior: asset_server.load("environments/pyramid_interior_rtx.png"),
        tomb_chamber: asset_server.load("environments/tomb_chamber_rtx.png"),
        temple_halls: asset_server.load("environments/temple_halls_rtx.png"),
        desert_oasis: asset_server.load("environments/desert_oasis_rtx.png"),
        
        // UI Elements - AI generated 3D styled icons
        ankh_health: asset_server.load("ui_elements/ankh_health_rtx.png"),
        scarab_energy: asset_server.load("ui_elements/scarab_energy_rtx.png"),
        eye_of_horus: asset_server.load("ui_elements/eye_of_horus_rtx.png"),
        
        // Items - AI generated 3D isometric items
        khopesh_sword: asset_server.load("items/khopesh_sword_rtx.png"),
        ankh_artifact: asset_server.load("items/ankh_artifact_rtx.png"),
        canopic_jar: asset_server.load("items/canopic_jar_rtx.png"),
        
        // 3D Environment Elements - RTX Generated Isometric
        egyptian_wall_section: asset_server.load("environment_3d/egyptian_wall_section_alpha.png"),
        stone_pillar_ornate: asset_server.load("environment_3d/stone_pillar_ornate_alpha.png"),
        torch_brazier: asset_server.load("environment_3d/torch_brazier_alpha.png"),
        anubis_guardian_statue: asset_server.load("environment_3d/anubis_guardian_statue_alpha.png"),
    };
    
    commands.insert_resource(game_assets);
    info!("✅ All RTX 5070 generated 3D assets loaded successfully!");
}