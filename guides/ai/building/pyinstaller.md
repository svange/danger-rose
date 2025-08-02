# PyInstaller Build Guide

## Quick Commands

```bash
make build              # Build folder version (recommended)
make build-onefile      # Build single executable file
make build-all          # Build for all platforms
```

## Build Types

### Folder Version (Recommended)
```bash
poetry run pyinstaller danger-rose.spec --noconfirm
```
- Faster startup time
- Smaller individual file size
- Located in `dist/DangerRose/`
- Includes DangerRose.exe + assets folder

### One-File Version
```bash
poetry run pyinstaller danger-rose-onefile.spec --noconfirm
```
- Single executable file
- Slower startup (extracts to temp)
- Larger file size (~100MB+)
- Self-contained distribution

## Asset Bundling

The spec files automatically include:
```python
datas=[
    ('assets', 'assets'),        # All game assets
    ('src/config', 'src/config') # Configuration files
]
```

## Hidden Imports

Required for Pygame to work properly:
```python
hiddenimports=[
    'pygame',
    'pygame_ce',
    'pygame.locals'
]
```

## Optimization Settings

```python
excludes=[
    'pytest', 'black', 'ruff',  # Development tools
    'pre_commit', 'augint_github'
]
optimize=2  # Bytecode optimization (onefile only)
upx=True    # UPX compression
```

## Cross-Platform Notes

- Windows: Generates .exe files
- macOS: Creates app bundle
- Linux: Creates executable binary
- Icon: Uses `assets/images/icon.ico` if available

## Troubleshooting

If build fails:
1. Check all assets exist: `make assets-check`
2. Verify dependencies: `poetry install`
3. Clean build cache: `make clean-build`
4. Test game runs locally: `make run`
