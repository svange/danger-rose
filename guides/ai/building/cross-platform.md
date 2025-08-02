# Cross-Platform Building

## Platform Support

Danger Rose builds on Windows, macOS, and Linux using the same codebase and build commands.

## Build Process

### Same Commands Everywhere
```bash
make build              # Works on all platforms
make build-onefile      # Creates single executable
poetry run python src/main.py  # Test before building
```

### Platform-Specific Outputs

**Windows:**
- `dist/DangerRose/DangerRose.exe` (folder build)
- `dist/DangerRose.exe` (onefile build)
- Includes all DLLs automatically

**macOS:**
- `dist/DangerRose/DangerRose` (Unix executable)
- May create `.app` bundle in future versions
- Handles macOS-specific Pygame dependencies

**Linux:**
- `dist/DangerRose/DangerRose` (ELF executable)
- Includes required shared libraries
- Works on most distributions

## Asset Compatibility

All assets work cross-platform:
- PNG images with transparency
- OGG audio files (better than WAV)
- Icon files automatically detected

## Testing Strategy

```bash
# Test on each platform
make run                # Verify game works
make test              # Run unit tests
make assets-check      # Validate assets
make build             # Create executable
```

## Distribution

### Windows
- Zip the `dist/DangerRose/` folder
- Include README with system requirements
- Test on clean Windows system

### macOS
- Use tar.gz for Unix permissions
- May need code signing for distribution
- Test on different macOS versions

### Linux
- Create tar.gz archive
- Document required system packages
- Test on Ubuntu/Debian and other distros

## Docker Alternative

For consistent builds across platforms:
```bash
make docker-build      # Build in container
make claude           # Develop in container
```
