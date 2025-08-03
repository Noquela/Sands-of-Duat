# Sands of Duat - Master Development Plan v2.0

## Project Overview
**Sands of Duat** is an innovative roguelike deck-builder set in the ancient Egyptian underworld during the 12 hours of the night. The game features a unique **Hour-Glass Initiative** combat system where timing and resource management create tactical depth beyond traditional turn-based mechanics.

**Target Resolution**: 3440x1440 ultrawide primary support with adaptive scaling
**Development Philosophy**: Local-first AI pipeline, precision timing mechanics, automated DevOps

## Core Innovation: Hour-Glass Initiative System

### Concept
- Each combatant possesses an "Hour-Glass" containing 0-6 grains of sand (expandable to 8+ with buffs)
- Playing cards costs sand (0-6 cost range)
- Sand regenerates in real-time at 1 grain per second using `time.perf_counter()` for sub-millisecond precision
- Creates strategic tension between quick cheap plays vs powerful expensive cards with downtime
- Enemy sand gauges are visible, enabling tactical timing predictions

### Strategic Implications
- **Stutter-stepping**: Chain cheap (0-1 cost) cards for rapid pressure
- **Power spikes**: Save sand for expensive (4-6 cost) game-changing moves
- **Tempo reading**: Watch enemy sand to predict their next major play
- **Animation timing**: Sand regen pauses during animations to maintain sync
- **Overflow Protection**: Max sand buffs properly handled without drift

### Technical Implementation
- High-resolution timing with `time.perf_counter()` for precision
- Delta time clamping (0.05s max) to prevent lag-induced acceleration
- Debug `time_scale` parameter for testing different speeds
- Frame-rate independence with fixed timestep updates

## Technical Architecture

### Core Engine Stack
```
Python 3.11+ 
├── Pygame 2.6 (rendering & input with ultrawide support)
├── Pydantic (data validation & models with JSON Schema export)
├── Watchdog (hot-reload with Windows debouncing)
├── asyncio (real-time sand regeneration)
├── PyYAML (content pipeline with versioning)
├── esper-lite (optimized ECS for performance)
├── pygame.freetype (advanced text rendering for sand countdown)
└── freezegun (testing timing mechanics)
```

### Enhanced Directory Structure
```
sands_duat/
├── core/                    # Engine systems
│   ├── hourglass.py        # Precision sand timing with perf_counter
│   ├── combat.py           # Combat engine & queue
│   ├── ecs.py              # Entity component system (esper-lite)
│   ├── cards.py            # Card system & effects
│   └── engine.py           # Main game loop
├── services/                # External integrations
│   ├── save_load.py        # Persistence layer
│   ├── logging.py          # Centralized logging
│   ├── telemetry.py        # Performance metrics
│   └── config.py           # Configuration management
├── content/                # YAML definitions with JSON Schema
│   ├── cards/              # Card definitions (versioned)
│   ├── enemies/            # Enemy data
│   ├── events/             # Map events
│   ├── decks/              # Starting decks
│   └── schemas/            # JSON Schema files for validation
├── assets/                 # Generated art & audio
│   ├── art_raw/            # AI-generated base images
│   ├── art_clean/          # Upscaled & processed (with fit_and_pad)
│   ├── audio/              # Sound effects & music
│   └── fonts/              # Egyptian-themed fonts
├── tools/                  # Development utilities
│   ├── gen_art.py          # ComfyUI with fixed model versions
│   ├── upscale.py          # Real-ESRGAN wrapper
│   ├── lora_train.py       # Style consistency training
│   ├── content_validator.py # YAML + Schema validation
│   └── model_downloader.py # HF API automated model fetching
├── ui/                     # Game interface with theme system
│   ├── theme.py            # Centralized colors, fonts, styling
│   ├── combat_screen.py    # Main battle UI (ultrawide optimized)
│   ├── map_screen.py       # Node progression
│   ├── deck_builder.py     # Card collection management
│   └── components/         # Reusable UI widgets
├── tests/                  # Comprehensive testing
│   ├── unit/               # Unit tests with timing mocks
│   ├── integration/        # Full system tests
│   ├── performance/        # Load tests (500x AI vs AI)
│   └── content/            # YAML validation tests
├── scripts/                # Automation scripts
│   ├── manage.py           # CLI for common tasks
│   ├── ci_setup.py         # GitHub Actions automation
│   └── dev_environment.py  # Development setup
└── config/                 # Configuration files
    ├── config.ini          # Paths and model settings
    ├── requirements.txt     # Runtime dependencies
    └── requirements-dev.txt # Development dependencies
```

## Enhanced Development Strategy

### DevOps & Automation Pipeline

#### GitHub Actions CI/CD
```yaml
# .github/workflows/python-ci.yml
- Lint (black, flake8)
- Type checking (mypy) 
- Unit tests (pytest with coverage)
- Content validation (YAML + JSON Schema)
- Performance regression tests
- Automated model downloads for CI
- Build artifacts with version tagging
```

#### Development Scripts
```bash
# scripts/manage.py commands
python manage.py test          # Run full test suite
python manage.py lint          # Format and lint code
python manage.py typecheck     # MyPy validation
python manage.py generate_art  # Batch art generation
python manage.py validate     # Content validation
python manage.py dev_setup     # First-time environment setup
```

#### Configuration Management
```ini
# config/config.ini
[paths]
models_dir = models/
content_dir = content/
assets_dir = assets/

[models]
playground_v25_hash = sha256:abc123...
stable_cascade_hash = sha256:def456...
realesrgan_version = v0.6.0
```

### Specialized Development Agents
1. **Combat System Agent**: Precision Hour-Glass mechanics, overflow handling
2. **Content Pipeline Agent**: YAML + JSON Schema validation, hot-reload with debouncing
3. **Asset Generation Agent**: Fixed model versions, automated downloads, batch processing
4. **UI/UX Agent**: Ultrawide support, theme system, freetype text rendering
5. **Testing Agent**: Timing mocks, performance benchmarks, regression detection

### MCP Tool Integration
- **GitHub Integration**: Automated releases, issue tracking, CI status
- **Local File Management**: Enhanced operations with conflict resolution
- **Performance Monitoring**: FPS tracking, memory profiling, timing accuracy
- **Content Management**: Schema generation, cross-reference validation

## Asset Generation Pipeline

### Local AI Model Stack (RTX 5070 Optimized) - Fixed Versions

#### Primary Models with Exact Versions
1. **Playground v2.5** (12GB VRAM)
   - Checkpoint: `playgroundai/playground-v2.5-1024px-aesthetic`
   - HF Commit: `f42ad2a86c6f19aa2c11b2a6e62b93f8c77b21e8`
   - Purpose: High-aesthetic concept art generation

2. **Stable Cascade** (14GB VRAM) 
   - Checkpoint: `stabilityai/stable-cascade`
   - HF Commit: `71c4925c1c4723ced0b6ad0abc85b5d76176a3c2`
   - Purpose: High-resolution decode and inpainting

3. **Kandinsky 3.0** (Apache-2.0)
   - Checkpoint: `kandinsky-community/kandinsky-3`
   - HF Commit: `4f4bdeb0bb89e4d9e8f1c3ebbde0e84dcbf0d857`
   - Purpose: Style variety and backup generation

4. **Real-ESRGAN v0.6.0**
   - Model: `RealESRGAN_x4plus.pth`
   - SHA256: `4fa0d38905067d17d4ec86a088b0c480a80fd45b5e77b8ca6f8a9ac5e7d3df8e`
   - Purpose: 4x upscaling with edge enhancement

#### Enhanced Workflow Automation
```bash
# Download and verify model checksums
python tools/model_downloader.py --verify-checksums

# Generate card art with VRAM optimization
python tools/gen_art.py --content content/cards/ --output assets/art_raw/ \
  --batch-size 2 --offload-to-cpu

# Upscale with padding for card frames
python tools/upscale.py assets/art_raw assets/art_clean \
  --model real-esrgan --fit-and-pad 400x650

# Apply Egyptian papyrus overlay
python tools/add_papyrus_overlay.py assets/art_clean --opacity 0.6

# Train style consistency LoRA (after 30+ images)
python tools/lora_train.py --model playground-v2.5 \
  --images assets/art_clean --output loras/duat_style \
  --verify-style-consistency
```

#### VRAM Management Strategy
- **Two-Stage Pipeline**: Load Playground → Generate → Offload to CPU → Load Cascade
- **Memory Monitoring**: `torch.cuda.memory_summary()` between model swaps
- **Batch Processing**: Process 2-4 images per batch to prevent OOM
- **Graceful Degradation**: Fall back to CPU processing if VRAM insufficient

## Content Design Philosophy

### Card Categories by Sand Cost
- **0-1 Sand**: Cantrips, weak attacks, utility (rapid fire potential)
- **2-3 Sand**: Standard attacks, moderate effects (balanced tempo)
- **4-5 Sand**: Powerful spells, game-changing effects (setup required)
- **6 Sand**: Ultimate abilities, fight-ending moves (maximum commitment)

### Sample Card Progression
```yaml
# Early game tempo card
id: desert_strike
cost: 1
effects: [damage: 6, draw: 1]

# Mid-game value card  
id: solar_flare
cost: 3
effects: [damage: 12, ignite: 2]

# Late game finisher
id: judgment_of_anubis
cost: 6
effects: [damage: 25, execute_if_below: 15]
```

## Display & UI Architecture

### Ultrawide Support (3440x1440 Primary Target)

#### Resolution Strategy
- **Primary**: 3440x1440 (21:9 ultrawide) - Native UI layout
- **Secondary**: 2560x1440 (16:9) - Scaled with side padding
- **Fallback**: 1920x1080 (16:9) - Proportional scaling
- **Minimum**: 1024x768 - Compact UI mode

#### UI Layout System
```python
# ui/theme.py - Responsive layout calculations
class DisplayManager:
    def __init__(self, target_width=3440, target_height=1440):
        self.base_width = target_width
        self.base_height = target_height
        self.aspect_ratio = target_width / target_height
    
    def get_scaled_dimensions(self, current_resolution):
        # Calculate optimal scaling and padding
        # Return: (scale_factor, x_offset, y_offset, ui_width, ui_height)
```

#### Layout Zones for 3440x1440
```
┌─────────────────────────────────────────────────────────────────────┐
│ [Menu Bar 3440x60]                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ [Sand Gauge Left] [Combat Arena 2400x1000] [Enemy Sand Right]       │
│     400x1000                                        400x1000         │
├─────────────────────────────────────────────────────────────────────┤
│ [Hand Display 3440x380]                                              │
└─────────────────────────────────────────────────────────────────────┘
```

#### Pygame Display Configuration
```python
# Enhanced display initialization
def initialize_ultrawide_display(width=3440, height=1440, windowed=False):
    if not windowed:
        # Fullscreen with proper aspect ratio handling
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    else:
        # Borderless windowed for ultrawide
        flags = pygame.NOFRAME
    
    screen = pygame.display.set_mode((width, height), flags)
    
    # Center window on ultrawide monitors
    if windowed and width > 2560:
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'
    
    return screen
```

#### Text Rendering Optimization
```python
# Using pygame.freetype for crisp text at high DPI
import pygame.freetype

class TextRenderer:
    def __init__(self):
        # High-quality font rendering for ultrawide
        self.fonts = {
            'title': pygame.freetype.Font('assets/fonts/egyptian_title.ttf', 48),
            'ui': pygame.freetype.Font('assets/fonts/egyptian_ui.ttf', 24),
            'sand_counter': pygame.freetype.Font('assets/fonts/digital.ttf', 72)
        }
    
    def render_sand_countdown(self, time_remaining):
        # Large, visible countdown for sand regeneration
        # Optimized for ultrawide viewing distances
```

## Quality Assurance Strategy

### Enhanced Testing Strategy

#### Automated Testing with Timing Precision
```python
# tests/unit/test_hourglass_timing.py
from freezegun import freeze_time
import pytest

@freeze_time("2025-01-01 12:00:00")
def test_sand_regeneration_precision():
    hourglass = HourGlass()
    hourglass.set_sand(0)
    
    # Mock time advance
    with freeze_time("2025-01-01 12:00:01.000"):
        hourglass.update_sand()
        assert hourglass.current_sand == 1
    
    # Test sub-second precision
    with freeze_time("2025-01-01 12:00:01.500"):
        hourglass.update_sand()
        assert hourglass.time_to_next_sand == 0.5
```

#### Performance & Load Testing
```python
# tests/performance/test_ai_vs_ai.py
def test_500_ai_battles():
    """Run 500 AI vs AI battles to detect memory leaks and performance regression."""
    initial_memory = get_memory_usage()
    fps_samples = []
    
    for i in range(500):
        battle = create_ai_battle()
        start_time = time.perf_counter()
        result = battle.run_to_completion()
        end_time = time.perf_counter()
        
        fps_samples.append(1.0 / (end_time - start_time))
        
        # Memory leak detection
        if i % 50 == 0:
            current_memory = get_memory_usage()
            assert current_memory < initial_memory * 1.2  # Max 20% growth
    
    # Performance regression detection
    assert np.mean(fps_samples) > 55  # Target 60 FPS average
    assert np.percentile(fps_samples, 95) > 45  # p95 threshold
```

#### Content Validation with JSON Schema
```python
# tests/content/test_yaml_schemas.py
def test_card_definitions_against_schema():
    """Validate all card YAML files against generated JSON Schema."""
    schema = load_json_schema('content/schemas/card_schema.json')
    
    for card_file in glob('content/cards/*.yaml'):
        with open(card_file) as f:
            card_data = yaml.safe_load(f)
        
        # Validate structure
        jsonschema.validate(card_data, schema)
        
        # Validate version compatibility
        assert card_data.get('version', 0) >= MINIMUM_CONTENT_VERSION
```

#### Performance Metrics Logging
```python
# services/telemetry.py - CSV logging for CI regression detection
class PerformanceLogger:
    def __init__(self):
        self.metrics_file = 'performance_metrics.csv'
    
    def log_frame_metrics(self, fps, frame_time, sand_timing_error):
        """Log metrics for trend analysis in CI."""
        with open(self.metrics_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                fps,
                frame_time,
                sand_timing_error
            ])
```

### Balance Testing & Automation
- **Sand Economy**: Automated simulations with different regeneration rates
- **Card Power Curves**: Statistical analysis of damage-per-sand across all cards
- **Combat Duration**: Target 3-5 minute fights validated via AI vs AI testing
- **Difficulty Scaling**: Progressive enemy sand complexity with win-rate metrics
- **Regression Detection**: CSV-logged performance data with CI trend analysis

## Development Phases

### Phase 1: Core Systems (Week 1-2)
- Hour-Glass Initiative implementation
- Basic card system and effects
- Combat engine with timing queue
- Simple text-based combat demo

### Phase 2: Content Pipeline (Week 2-3)
- YAML loading and validation
- Hot-reload system implementation
- Sample card set (15-20 cards)
- Basic enemy roster (5-8 types)

### Phase 3: Visual Systems (Week 3-4)
- Pygame UI implementation
- Sand gauge visualization
- Card art integration
- Combat animations

### Phase 4: Asset Generation (Week 4-5)
- ComfyUI workflow setup
- AI model integration
- Batch art generation
- Style consistency training

### Phase 5: Polish & Testing (Week 5-6)
- Performance optimization
- Balance testing and iteration
- Audio integration
- Launcher scripts and packaging

## Success Metrics

### Technical Goals
- Sand regeneration accuracy within 50ms of target timing
- Hot-reload system responds within 200ms of file changes
- Combat engine handles 60fps with smooth animations
- Asset generation produces consistent Egyptian aesthetic

### Gameplay Goals
- Combat decisions every 2-3 seconds maintain engagement
- Sand cost distribution creates meaningful timing choices
- Enemy AI demonstrates varied sand usage patterns
- Player progression feels rewarding and strategic

## Risk Mitigation & Technical Challenges

### Critical Technical Risks

| ⚠️ Risk | Impact | Mitigation Strategy |
|---------|--------|---------------------|
| **Timing Drift** | Sand regeneration becomes inaccurate when PC lags | • Use `pygame.time.Clock.get_time()` with delta clamping (0.05s max)<br>• Add debug `time_scale` parameter for lag simulation<br>• Frame-rate independence with fixed timestep |
| **VRAM Overflow** | ComfyUI crashes switching between models | • Two-GPU virtual allocation with xformers + accelerate<br>• Pipeline `.to("cpu")` offloading between batches<br>• Memory monitoring with `torch.cuda.memory_summary()` |
| **PNG Overflow** | 512×768 images don't fit card frames | • `fit_and_pad(img, 400, 650)` function before compositing<br>• Automated aspect ratio validation in art pipeline |
| **Hot-reload Duplication** | Windows Watchdog fires multiple events | • Filter by `event.is_directory == False`<br>• 100ms debouncing with event deduplication |
| **Ultrawide Centering** | SDL2 doesn't center windowed mode on 3440×1440 | • Use `pygame.NOFRAME` with manual positioning<br>• `os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'` |

### Asset Generation Stability
```python
# tools/vram_manager.py - Graceful VRAM handling
class VRAMManager:
    def __init__(self):
        self.available_vram = torch.cuda.get_device_properties(0).total_memory
        self.models_loaded = {}
    
    def load_with_fallback(self, model_name):
        try:
            if self.get_free_vram() < self.get_model_vram_requirement(model_name):
                self.offload_least_recently_used()
            return self.load_model(model_name)
        except torch.cuda.OutOfMemoryError:
            logging.warning(f"VRAM exhausted, falling back to CPU for {model_name}")
            return self.load_model_cpu(model_name)
```

### Hot-Reload Stability 
```python
# content/hot_reload.py - Windows-optimized file watching
class DebounceWatcher:
    def __init__(self, path, callback, debounce_ms=100):
        self.debounce_ms = debounce_ms
        self.pending_events = {}
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Debounce duplicate events on Windows
        event_key = (event.src_path, event.event_type)
        self.pending_events[event_key] = time.time()
        
        # Schedule callback after debounce period
        threading.Timer(self.debounce_ms / 1000, 
                       self._process_event, [event_key]).start()
```

### Performance Monitoring
```python
# services/performance_monitor.py - Real-time performance tracking
class PerformanceMonitor:
    def __init__(self):
        self.frame_times = collections.deque(maxlen=60)  # 1 second at 60fps
        self.sand_timing_errors = collections.deque(maxlen=100)
    
    def log_frame(self, delta_time):
        self.frame_times.append(delta_time)
        
        # Alert on performance regression
        if len(self.frame_times) == 60:
            avg_fps = 1.0 / (sum(self.frame_times) / 60)
            if avg_fps < 45:  # Below threshold
                logging.warning(f"Performance regression: {avg_fps:.1f} FPS")
    
    def log_sand_timing_error(self, expected_time, actual_time):
        error_ms = abs(expected_time - actual_time) * 1000
        self.sand_timing_errors.append(error_ms)
        
        if error_ms > 50:  # 50ms threshold
            logging.warning(f"Sand timing drift: {error_ms:.1f}ms")
```

### Design Risk Mitigation
- **Hour-Glass Balance**: A/B testing with configurable regeneration rates (0.5s to 2.0s per sand)
- **Complexity Overwhelm**: Progressive tutorial introducing one mechanic at a time
- **Art Consistency**: LoRA training with style validation and automated rejection of outliers
- **Scope Creep**: Feature freeze after core mechanics, strict milestone reviews

## Future Expansion Opportunities

### Advanced Systems
- **Multi-class Hour-Glasses**: Different sand types (time, space, life, death)
- **Temporal Mechanics**: Cards that manipulate sand regeneration rates
- **Ritual Magic**: Multi-turn card combinations with sand investment
- **Dynamic Difficulty**: AI opponents that learn player timing patterns

### Content Expansion
- **Full Campaign**: 12 hours of night with unique challenges per hour
- **Deck Archetypes**: Focused strategies around different sand cost curves
- **Boss Mechanics**: Unique Hour-Glass variants for major encounters
- **Multiplayer**: Competitive and cooperative Hour-Glass duels

This plan provides a comprehensive roadmap for creating an innovative roguelike that pushes the boundaries of deck-builder design through its unique timing mechanics while maintaining technical excellence and Egyptian thematic authenticity.