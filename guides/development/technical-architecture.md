# Technical Architecture

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM**: 2GB minimum
- **Storage**: 200MB free space
- **Display**: 1920x1080 recommended
- **Python**: 3.12+ (for development)

## Performance Targets
- **Target FPS**: 60 (with graceful degradation)
- **Resolution**: 1920x1080 (scales to display)
- **Memory Usage**: < 500MB
- **Load Times**: < 2 seconds per scene

## Architecture Overview

### Project Structure
```
danger-rose/
├── 📁 assets/           # Game resources
│   ├── 🖼️ images/       # Sprites and backgrounds
│   └── 🔊 audio/        # Music and sound effects
├── 📁 src/              # Source code
│   ├── 🎮 main.py       # Game entry point
│   ├── 🎬 scenes/       # Game scenes
│   └── 🛠️ utils/        # Helper modules
├── 📁 tests/            # Unit tests
├── 📁 docs/             # Documentation
└── 📄 pyproject.toml    # Project config
```

### Core Systems

#### Scene System
Each game mode is a self-contained scene with standard lifecycle:
- `handle_event()` - Process input
- `update()` - Game logic
- `draw()` - Rendering
- `on_enter()` - Scene initialization
- `on_exit()` - Cleanup

#### Entity-Component Architecture
Characters use component-based design:
- Position component
- Sprite component
- Physics component
- Input component

#### Asset Pipeline
- Automatic placeholder generation for missing assets
- Centralized asset loading through `sprite_loader.py`
- Support for sprite sheets and animations

#### Save System
- JSON-based local storage
- Auto-save at checkpoints
- Player progress and high scores

## Building & Distribution

### Standalone Executables
We use PyInstaller to create standalone executables:

```bash
# Build for current platform
poetry run pyinstaller danger-rose-onefile.spec

# Output locations:
# Windows: dist/DangerRose.exe
# macOS: dist/DangerRose
# Linux: dist/DangerRose
```

### Platform-Specific Notes

#### Windows
- Executable is self-contained
- May trigger antivirus warnings (code-sign to avoid)
- Supports Windows 10/11

#### macOS
- Requires code signing for distribution
- Universal binary supports Intel and Apple Silicon
- App bundle creation optional

#### Linux
- AppImage format recommended for distribution
- Works on most modern distributions
- May need to set executable permissions

## Debugging & Profiling

### Debug Mode
```bash
DEBUG=true poetry run python src/main.py
```

Shows:
- FPS counter
- Collision boxes
- Performance metrics
- Debug logging

### Memory Profiling
```bash
MEMORY_DEBUG=true poetry run python src/main.py
```

### Performance Profiling
```bash
PROFILE_SYSTEM=animation poetry run python src/main.py
```

## Testing Strategy

### Test Categories
1. **Unit Tests** (`tests/unit/`)
   - Core game logic
   - Utility functions
   - Data structures

2. **Integration Tests** (`tests/integration/`)
   - Scene transitions
   - Save/load functionality
   - Asset loading

3. **Visual Tests** (`tests/visual/`)
   - Sprite rendering
   - Animation playback
   - UI elements

4. **Performance Tests** (`tests/performance/`)
   - Frame rate stability
   - Memory usage
   - Load times

### Running Tests
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=src --cov-report=html

# Specific category
poetry run pytest tests/unit -v
```

## Dependencies

### Core Dependencies
- **pygame-ce**: Game engine (fork of pygame with better performance)
- **numpy**: Mathematical operations
- **pillow**: Image processing

### Development Dependencies
- **pytest**: Testing framework
- **ruff**: Code formatting and linting
- **pyinstaller**: Executable building
- **pre-commit**: Git hooks

See `pyproject.toml` for complete dependency list.