use bevy::prelude::*;

/// Hades-Style Egyptian Asset Loading System
/// Manages high-quality Egyptian assets in Hades visual style
#[derive(Resource)]
pub struct HadesEgyptianAssets {
    // Character sprites in Hades style
    pub pharaoh_warrior: Handle<Image>,
    pub anubis_judge: Handle<Image>,
    pub isis_mother: Handle<Image>, 
    pub ra_sun_god: Handle<Image>,
    pub set_chaos: Handle<Image>,
    pub thoth_wisdom: Handle<Image>,
    
    // God portraits for boon selection
    pub pharaoh_portrait: Handle<Image>,
    pub anubis_portrait: Handle<Image>,
    pub isis_portrait: Handle<Image>,
    pub ra_portrait: Handle<Image>, 
    pub set_portrait: Handle<Image>,
    pub thoth_portrait: Handle<Image>,
    
    // Hades-style environments (4K backgrounds)
    pub combat_background: Handle<Image>,
    pub hall_of_gods_background: Handle<Image>,
    pub deck_builder_background: Handle<Image>,
    pub main_menu_background: Handle<Image>,
    
    // Egyptian UI elements with Hades design
    pub boon_frame_common: Handle<Image>,
    pub boon_frame_rare: Handle<Image>,
    pub boon_frame_epic: Handle<Image>,
    pub boon_frame_legendary: Handle<Image>,
    
    // Additional Hades-style elements
    pub loading_screen_art: Handle<Image>,
    pub death_screen_art: Handle<Image>,
    pub victory_screen_art: Handle<Image>,
}

pub struct HadesAssetsPlugin;

impl Plugin for HadesAssetsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, load_hades_egyptian_assets)
            .add_systems(Update, check_asset_loading_progress);
    }
}

fn load_hades_egyptian_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    info!("🏺 Loading Hades-style Egyptian assets...");
    
    let hades_assets = HadesEgyptianAssets {
        // Character sprites
        pharaoh_warrior: asset_server.load("characters/pharaoh_warrior.png"),
        anubis_judge: asset_server.load("characters/anubis_judge.png"),
        isis_mother: asset_server.load("characters/isis_mother.png"),
        ra_sun_god: asset_server.load("characters/ra_sun_god.png"), 
        set_chaos: asset_server.load("characters/set_chaos.png"),
        thoth_wisdom: asset_server.load("characters/thoth_wisdom.png"),
        
        // God portraits for boon system
        pharaoh_portrait: asset_server.load("portraits/pharaoh_warrior_portrait.png"),
        anubis_portrait: asset_server.load("portraits/anubis_judge_portrait.png"),
        isis_portrait: asset_server.load("portraits/isis_mother_portrait.png"),
        ra_portrait: asset_server.load("portraits/ra_sun_god_portrait.png"),
        set_portrait: asset_server.load("portraits/set_chaos_portrait.png"),
        thoth_portrait: asset_server.load("portraits/thoth_wisdom_portrait.png"),
        
        // High-quality 4K environments
        combat_background: asset_server.load("backgrounds/bg_combat_4k.png"),
        hall_of_gods_background: asset_server.load("backgrounds/bg_hall_of_gods_4k.png"),
        deck_builder_background: asset_server.load("backgrounds/bg_deck_builder_4k.png"),
        main_menu_background: asset_server.load("backgrounds/bg_main_menu_4k.png"),
        
        // Ornate UI frames in Egyptian style
        boon_frame_common: asset_server.load("ui/boon_card_common.png"),
        boon_frame_rare: asset_server.load("ui/boon_card_rare.png"),
        boon_frame_epic: asset_server.load("ui/boon_card_epic.png"),
        boon_frame_legendary: asset_server.load("ui/boon_card_legendary.png"),
        
        // Additional screens
        loading_screen_art: asset_server.load("backgrounds/loading_screen_hades.png"),
        death_screen_art: asset_server.load("backgrounds/death_screen_hades.png"),
        victory_screen_art: asset_server.load("backgrounds/victory_screen_hades.png"),
    };
    
    commands.insert_resource(hades_assets);
    info!("✅ Hades Egyptian asset loading initiated");
}

fn check_asset_loading_progress(
    asset_server: Res<AssetServer>,
    hades_assets: Option<Res<HadesEgyptianAssets>>,
    mut loaded_assets: Local<usize>,
) {
    if let Some(assets) = hades_assets {
        let total_assets = 22; // Total number of assets we're loading
        let mut loaded_count = 0;
        
        // Check each asset's loading status
        let asset_handles = vec![
            &assets.pharaoh_warrior,
            &assets.anubis_judge,
            &assets.isis_mother,
            &assets.ra_sun_god,
            &assets.set_chaos,
            &assets.thoth_wisdom,
            &assets.pharaoh_portrait,
            &assets.anubis_portrait,
            &assets.isis_portrait,
            &assets.ra_portrait,
            &assets.set_portrait,
            &assets.thoth_portrait,
            &assets.combat_background,
            &assets.hall_of_gods_background,
            &assets.deck_builder_background,
            &assets.main_menu_background,
            &assets.boon_frame_common,
            &assets.boon_frame_rare,
            &assets.boon_frame_epic,
            &assets.boon_frame_legendary,
            &assets.loading_screen_art,
            &assets.death_screen_art,
        ];
        
        for handle in asset_handles {
            match asset_server.load_state(handle) {
                bevy::asset::LoadState::Loaded => loaded_count += 1,
                bevy::asset::LoadState::Failed => {
                    warn!("❌ Failed to load asset: {:?}", handle);
                }
                _ => {} // Still loading or not started
            }
        }
        
        // Update progress if changed
        if loaded_count != *loaded_assets {
            *loaded_assets = loaded_count;
            let progress = (loaded_count as f32 / total_assets as f32) * 100.0;
            info!("🎨 Hades Egyptian assets loading: {:.1}% ({}/{})", 
                  progress, loaded_count, total_assets);
            
            if loaded_count == total_assets {
                info!("🎉 All Hades Egyptian assets loaded successfully!");
                info!("🎮 Game ready with beautiful Egyptian art in Hades style");
            }
        }
    }
}

/// Helper functions to get god portraits for the boon system
impl HadesEgyptianAssets {
    pub fn get_god_portrait(&self, god: &crate::boons::EgyptianGod) -> Handle<Image> {
        match god {
            crate::boons::EgyptianGod::Ra => self.ra_portrait.clone(),
            crate::boons::EgyptianGod::Anubis => self.anubis_portrait.clone(),
            crate::boons::EgyptianGod::Isis => self.isis_portrait.clone(),
            crate::boons::EgyptianGod::Set => self.set_portrait.clone(),
            crate::boons::EgyptianGod::Thoth => self.thoth_portrait.clone(),
        }
    }
    
    pub fn get_boon_frame(&self, rarity: &crate::boons::BoonRarity) -> Handle<Image> {
        match rarity {
            crate::boons::BoonRarity::Common => self.boon_frame_common.clone(),
            crate::boons::BoonRarity::Rare => self.boon_frame_rare.clone(),
            crate::boons::BoonRarity::Epic => self.boon_frame_epic.clone(), 
            crate::boons::BoonRarity::Legendary => self.boon_frame_legendary.clone(),
        }
    }
    
    pub fn get_character_sprite(&self, character_name: &str) -> Option<Handle<Image>> {
        match character_name {
            "pharaoh_warrior" => Some(self.pharaoh_warrior.clone()),
            "anubis_judge" => Some(self.anubis_judge.clone()),
            "isis_mother" => Some(self.isis_mother.clone()),
            "ra_sun_god" => Some(self.ra_sun_god.clone()),
            "set_chaos" => Some(self.set_chaos.clone()),
            "thoth_wisdom" => Some(self.thoth_wisdom.clone()),
            _ => None,
        }
    }
}