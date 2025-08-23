use bevy::prelude::*;

/// Temporary 3D placeholder models for immediate gameplay
/// These are simple geometric shapes until we have proper glTF models

#[derive(Resource)]
pub struct Placeholder3DAssets {
    pub hero_mesh: Handle<Mesh>,
    pub enemy_mesh: Handle<Mesh>,
    pub weapon_mesh: Handle<Mesh>,
    pub pillar_mesh: Handle<Mesh>,
    
    pub hero_material: Handle<StandardMaterial>,
    pub enemy_material: Handle<StandardMaterial>,
    pub weapon_material: Handle<StandardMaterial>,
    pub environment_material: Handle<StandardMaterial>,
}

pub struct Placeholder3DPlugin;

impl Plugin for Placeholder3DPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PreStartup, create_placeholder_assets)
            .add_systems(PostStartup, spawn_placeholder_hero);
    }
}

fn create_placeholder_assets(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    info!("Creating placeholder 3D models for immediate gameplay...");
    
    // Create simple geometric meshes
    let hero_mesh = meshes.add(Capsule3d::new(0.5, 2.0));
    let enemy_mesh = meshes.add(Cuboid::new(1.0, 1.5, 1.0));
    let weapon_mesh = meshes.add(Cuboid::new(0.1, 1.5, 0.1));
    let pillar_mesh = meshes.add(Cylinder::new(0.3, 3.0));
    
    // Create materials with Egyptian-inspired colors
    let hero_material = materials.add(StandardMaterial {
        base_color: Color::rgb(0.8, 0.6, 0.2), // Golden pharaoh
        metallic: 0.3,
        perceptual_roughness: 0.5,
        ..default()
    });
    
    let enemy_material = materials.add(StandardMaterial {
        base_color: Color::rgb(0.3, 0.2, 0.1), // Dark mummy
        metallic: 0.1,
        perceptual_roughness: 0.8,
        ..default()
    });
    
    let weapon_material = materials.add(StandardMaterial {
        base_color: Color::rgb(0.7, 0.5, 0.1), // Bronze weapon
        metallic: 0.8,
        perceptual_roughness: 0.2,
        ..default()
    });
    
    let environment_material = materials.add(StandardMaterial {
        base_color: Color::rgb(0.6, 0.5, 0.3), // Sandstone
        metallic: 0.0,
        perceptual_roughness: 0.9,
        ..default()
    });
    
    commands.insert_resource(Placeholder3DAssets {
        hero_mesh,
        enemy_mesh,
        weapon_mesh,
        pillar_mesh,
        hero_material,
        enemy_material,
        weapon_material,
        environment_material,
    });
    
    info!("✅ Placeholder 3D assets created!");
}

fn spawn_placeholder_hero(
    mut commands: Commands,
    placeholder_assets: Res<Placeholder3DAssets>,
    mut spawned: Local<bool>,
) {
    if *spawned {
        return;
    }
    *spawned = true;
    
    info!("Spawning placeholder 3D hero...");
    
    // Spawn hero as capsule
    let hero_entity = commands.spawn((
        PbrBundle {
            mesh: placeholder_assets.hero_mesh.clone(),
            material: placeholder_assets.hero_material.clone(),
            transform: Transform::from_xyz(0.0, 1.0, 0.0),
            ..default()
        },
        crate::true_3d_system::Hero3D,
        crate::Player,
        crate::Stats::default(),
        crate::Dash::default(),
        crate::Combat::default(),
        Name::new("Placeholder_Hero"),
    )).id();
    
    // Spawn weapon in hero's hand (offset)
    let weapon_entity = commands.spawn((
        PbrBundle {
            mesh: placeholder_assets.weapon_mesh.clone(),
            material: placeholder_assets.weapon_material.clone(),
            transform: Transform::from_xyz(0.8, 0.5, 0.0),
            ..default()
        },
        crate::true_3d_system::Weapon3D {
            weapon_type: crate::true_3d_system::WeaponType::Khopesh,
            equipped: true,
        },
        Name::new("Placeholder_Weapon"),
    )).id();
    
    // Parent weapon to hero
    commands.entity(hero_entity).add_child(weapon_entity);
    
    info!("✅ Placeholder hero and weapon spawned!");
}

pub fn spawn_placeholder_enemy(
    commands: &mut Commands,
    placeholder_assets: &Placeholder3DAssets,
    position: Vec3,
    enemy_type: crate::true_3d_system::EnemyType,
    ai: crate::AI,
    stats: crate::Stats,
) -> Entity {
    commands.spawn((
        PbrBundle {
            mesh: placeholder_assets.enemy_mesh.clone(),
            material: placeholder_assets.enemy_material.clone(),
            transform: Transform::from_translation(position),
            ..default()
        },
        crate::true_3d_system::Enemy3D { enemy_type },
        crate::Enemy,
        ai,
        stats,
        Name::new("Placeholder_Enemy"),
    )).id()
}

pub fn spawn_placeholder_pillar(
    commands: &mut Commands,
    placeholder_assets: &Placeholder3DAssets,
    position: Vec3,
) -> Entity {
    commands.spawn((
        PbrBundle {
            mesh: placeholder_assets.pillar_mesh.clone(),
            material: placeholder_assets.environment_material.clone(),
            transform: Transform::from_translation(position),
            ..default()
        },
        Name::new("Placeholder_Pillar"),
    )).id()
}