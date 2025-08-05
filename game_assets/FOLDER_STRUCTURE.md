# Sands of Duat - Asset Organization Structure

## Professional Asset Pipeline Architecture

This document defines the standardized folder structure and naming conventions for maintaining a professional, Hades-style Egyptian art pipeline.

## Directory Structure

```
game_assets/
├── ASSET_MANIFEST.json          # Master asset catalog
├── FOLDER_STRUCTURE.md          # This documentation
├── cards/                       # Card artwork
│   ├── hades_quality/          # Professional Hades-style cards
│   │   ├── sand_strike_hades.png
│   │   ├── anubis_judgment_hades.png
│   │   ├── ra_solar_flare_hades.png
│   │   └── isis_grace_hades.png
│   ├── standard_quality/       # Original/placeholder cards
│   │   ├── tomb_strike.png
│   │   ├── scarab_swarm.png
│   │   ├── ankh_blessing.png
│   │   ├── pyramid_power.png
│   │   ├── papyrus_scroll.png
│   │   ├── desert_whisper.png
│   │   ├── thoths_wisdom.png
│   │   ├── pharaohs_resurrection.png
│   │   ├── mummys_wrath.png
│   │   └── sand_grain.png
│   └── concepts/               # Concept art and sketches
├── characters/
│   ├── hades_quality/          # Professional character art
│   ├── standard_quality/       # Current character sprites
│   │   └── sprites/
│   │       ├── player_character_idle.png
│   │       ├── player_character_attack.png
│   │       ├── player_character_walk.png
│   │       ├── anubis_guardian_idle.png
│   │       ├── anubis_guardian_attack.png
│   │       ├── anubis_guardian_walk.png
│   │       ├── desert_scorpion_idle.png
│   │       ├── desert_scorpion_attack.png
│   │       ├── desert_scorpion_walk.png
│   │       ├── pharaoh_lich_idle.png
│   │       ├── pharaoh_lich_attack.png
│   │       ├── pharaoh_lich_walk.png
│   │       ├── temple_guardian_idle.png
│   │       ├── temple_guardian_attack.png
│   │       └── temple_guardian_walk.png
│   ├── concepts/               # Character concept art
│   │   ├── anubis_guardian.png
│   │   ├── desert_scorpion.png
│   │   ├── pharaoh_lich.png
│   │   ├── player_character.png
│   │   └── temple_guardian.png
│   └── animations/             # Animation frame sequences
├── environments/
│   ├── hades_quality/          # Professional backgrounds
│   ├── standard_quality/       # Current backgrounds
│   │   ├── menu_background.png
│   │   └── combat_background.png
│   └── concepts/               # Environment concepts
├── ui_elements/
│   ├── hades_quality/          # Professional UI elements
│   ├── buttons/                # Button designs
│   ├── frames/                 # Card frames and borders
│   ├── indicators/             # Health, mana, status indicators
│   └── decorations/            # Ornamental elements
├── effects/
│   ├── particles/              # Particle effect sequences
│   ├── magic/                  # Spell effect animations
│   └── transitions/            # Screen transition effects
└── audio/                      # Sound assets
    ├── music/                  # Background music
    ├── sfx/                    # Sound effects
    └── voice/                  # Voice samples
```

## Naming Conventions

### File Naming Standards

1. **Snake Case**: All filenames use lowercase with underscores
   - ✅ `sand_strike_hades.png`
   - ❌ `SandStrike-Hades.png`

2. **Quality Suffix**: Indicate quality level in filename
   - `_hades` - Professional Hades-style quality
   - `_standard` - Original/placeholder quality
   - `_concept` - Concept art or sketches

3. **Animation States**: For character sprites
   - `_idle` - Static standing pose
   - `_attack` - Attack animation frame
   - `_walk` - Walking animation frame
   - `_death` - Death animation frame

4. **Asset Type Prefix**: For specialized elements
   - `ui_` - User interface elements
   - `fx_` - Visual effects
   - `bg_` - Background elements

### Directory Organization Rules

1. **Quality Separation**: Assets organized by quality level
   - Professional assets in `hades_quality/` folders
   - Original assets in `standard_quality/` folders
   - Concept work in `concepts/` folders

2. **Type Categorization**: Clear separation by asset function
   - Cards, characters, environments, UI, effects
   - Consistent subfolder structure across categories

3. **Version Control**: Track asset evolution
   - Keep previous versions in archive folders
   - Document changes in manifest

## Asset Quality Standards

### Hades-Style Quality Requirements

1. **Visual Style**
   - Cel-shaded illustration technique
   - Dramatic lighting with strong shadows
   - Rich, saturated Egyptian color palette
   - Intricate detail and professional lineart

2. **Technical Specifications**
   - Cards: 512x768 PNG, optimized compression
   - Characters: 512x768 PNG for portraits, spritesheet for animations
   - Environments: 1920x1080 PNG for backgrounds
   - UI Elements: Variable resolution, consistent style

3. **Thematic Consistency**
   - Egyptian mythology accuracy
   - Underworld/Duat atmosphere
   - Consistent lighting and color treatment
   - Professional game art quality

## Asset Pipeline Workflow

### 1. Planning Phase
- Review ASSET_MANIFEST.json for priorities
- Identify missing or low-quality assets
- Plan generation schedule

### 2. Generation Phase
- Use `tools/hades_style_art_generator.py`
- Generate assets according to prompts in manifest
- Apply consistent post-processing

### 3. Quality Assurance
- Verify technical specifications
- Check thematic consistency
- Validate naming conventions
- Update manifest with new assets

### 4. Integration
- Place assets in appropriate quality folders
- Update asset manager configurations
- Test loading and display in game
- Document any integration requirements

## Maintenance Guidelines

### Regular Audits
1. Review asset quality vs. game standards
2. Identify inconsistencies or outdated assets
3. Update manifest with current status
4. Plan upgrade cycles for older assets

### Performance Monitoring
1. Track asset loading times
2. Monitor memory usage patterns
3. Optimize file sizes without quality loss
4. Implement efficient caching strategies

### Documentation Updates
1. Keep manifest current with actual assets
2. Document any new asset requirements
3. Update naming conventions as needed
4. Track asset generation statistics

## Tools and Scripts

### Primary Tools
- **Art Generator**: `tools/hades_style_art_generator.py`
- **Asset Manager**: `sands_duat/graphics/asset_manager.py`
- **Loader System**: `sands_duat/assets/manager.py`

### Utility Scripts
- **Asset Validator**: Verify naming and quality standards
- **Batch Processor**: Bulk asset operations
- **Performance Analyzer**: Asset loading optimization

## Quality Metrics

### Current Status (as of 2025-08-04)
- **Total Assets**: 26 identified
- **Hades Quality**: 4 complete (15.4%)
- **Standard Quality**: 13 assets (50.0%)
- **Missing**: 9 assets (34.6%)

### Target Goals
- **90% Hades Quality** by project completion
- **Consistent visual style** across all asset types
- **Optimized performance** with professional quality
- **Complete asset coverage** for all game features

## Asset Generation Priority

### Phase 1 (High Priority)
1. Complete missing card art upgrades
2. Generate deck builder and progression backgrounds
3. Create essential UI elements

### Phase 2 (Medium Priority)
1. Upgrade character sprites to Hades quality
2. Create particle effects and animations
3. Generate additional UI decorations

### Phase 3 (Enhancement)
1. Create alternative asset variations
2. Add seasonal or contextual variants
3. Optimize and refine existing assets

This structure ensures maintainable, professional asset management that supports the game's visual excellence goals while providing clear guidelines for contributors and automated systems.