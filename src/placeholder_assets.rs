use bevy::prelude::*;

pub struct PlaceholderAssetsPlugin;

impl Plugin for PlaceholderAssetsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, create_placeholder_assets);
    }
}

fn create_placeholder_assets(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut images: ResMut<Assets<Image>>,
) {
    info!("🎨 Creating placeholder assets for missing files...");
    
    // Create placeholder texture (1x1 white pixel)
    let placeholder_image = Image::new_fill(
        bevy::render::render_resource::Extent3d {
            width: 1,
            height: 1,
            depth_or_array_layers: 1,
        },
        bevy::render::render_resource::TextureDimension::D2,
        &[255, 255, 255, 255],
        bevy::render::render_resource::TextureFormat::Rgba8UnormSrgb,
        bevy::render::render_asset::RenderAssetUsages::RENDER_WORLD,
    );
    
    let placeholder_handle = images.add(placeholder_image);
    
    // Store placeholder handles for systems that might need them
    commands.insert_resource(PlaceholderAssets {
        white_pixel: placeholder_handle,
    });
    
    info!("✅ Placeholder assets created");
}

#[derive(Resource)]
pub struct PlaceholderAssets {
    pub white_pixel: Handle<Image>,
}