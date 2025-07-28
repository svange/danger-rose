# 🎮 Danger Rose

<div align="center">
  <img src="docs/images/logo-placeholder.png" alt="Danger Rose Logo" width="400">

  **A family-friendly couch co-op adventure starring Dad, Danger (Yasha), and Rose (Ellie)**

  [![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
  [![Pygame](https://img.shields.io/badge/Pygame--CE-2.4%2B-green.svg)](https://pyga.me/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  [![Issues](https://img.shields.io/github/issues/svange/danger-rose)](https://github.com/svange/danger-rose/issues)
</div>

## 🌟 Overview

**Danger Rose** is an educational game development project designed to teach kids programming through collaborative coding with AI assistance. Players control family members through a cozy apartment hub world and three exciting minigames, each offering unique gameplay experiences.

### 🎯 Key Features
- **Family Characters**: Play as Danger (10), Rose (8), or unlock Dad
- **3 Unique Minigames**: Ski, Pool, and Vegas themed adventures
- **Couch Co-op**: Up to 3 players local multiplayer
- **Educational**: Learn programming concepts through game development
- **AI-Assisted**: Built with Claude Code for collaborative learning

## 📸 Screenshots

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="docs/images/title-screen.png" alt="Title Screen" width="300"><br>
        <b>Character Selection</b>
      </td>
      <td align="center">
        <img src="docs/images/hub-world.png" alt="Hub World" width="300"><br>
        <b>Cozy Apartment Hub</b>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="docs/images/ski-game.png" alt="Ski Minigame" width="300"><br>
        <b>Ski Downhill</b>
      </td>
      <td align="center">
        <img src="docs/images/pool-game.png" alt="Pool Minigame" width="300"><br>
        <b>Pool Splash</b>
      </td>
    </tr>
  </table>
</div>

## 🚀 Quick Start for Kids

### 1️⃣ Install the Game
```bash
# Ask a parent to help you open a terminal!
# Then type these magic commands:

# Download the game
git clone https://github.com/svange/danger-rose.git
cd danger-rose

# Install what the game needs
poetry install

# Start playing!
poetry run python src/main.py
```

### 2️⃣ Choose Your Character
- Press **←** and **→** arrows to pick Danger or Rose
- Press **SPACE** to start your adventure!

### 3️⃣ Explore and Play
- Walk around the apartment with arrow keys
- Stand by a door and press **SPACE** to play a minigame
- Try to beat your high scores!

## 📋 Table of Contents

1. [Installation](#-installation)
2. [How to Play](#-how-to-play)
3. [Game Modes](#-game-modes)
4. [Technical Details](#-technical-details)
5. [Development](#-development)
6. [Contributing](#-contributing)
7. [Credits](#-credits)
8. [License](#-license)

## 💻 Installation

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.12 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB free space
- **Display**: 1920x1080 recommended

### Detailed Installation

#### Windows
```bash
# 1. Install Python 3.12+ from python.org
# 2. Install Poetry (Python package manager)
curl -sSL https://install.python-poetry.org | python -

# 3. Clone and setup
git clone https://github.com/svange/danger-rose.git
cd danger-rose
poetry install

# 4. Run the game
poetry run python src/main.py
```

#### macOS/Linux
```bash
# Install dependencies
git clone https://github.com/svange/danger-rose.git
cd danger-rose
poetry install

# Run the game
poetry run python src/main.py
```

### 🎮 Pre-built Releases
Download ready-to-play versions from [Releases](https://github.com/svange/danger-rose/releases) (coming soon!)

## 🎮 How to Play

### Hub World
The apartment is your home base! Walk around and interact with:
- **🎿 Blue Door**: Enter the Ski minigame
- **🏊 Green Door**: Enter the Pool minigame
- **🎰 Red Door**: Enter the Vegas minigame
- **🏆 Trophy Shelf**: View your high scores
- **💾 Save Point**: Auto-saves your progress

### Controls
| Action | Keyboard | Gamepad |
|--------|----------|---------|
| Move | Arrow Keys / WASD | D-Pad / Left Stick |
| Jump | Space | A / X |
| Interact | Space / Enter | A / X |
| Attack | Z | B / Circle |
| Pause | Escape | Start |
| Aim (Pool) | Mouse | Right Stick |

## 🎯 Game Modes

### 🎿 Ski Downhill
Race down the mountain with Dad on his snowboard!
- **Goal**: Dodge obstacles and collect snowflakes
- **Duration**: 60-second runs
- **Scoring**:
  - Snowflakes: +10 points
  - Finish bonus: +500 points
  - Perfect run: +1000 points
- **Tips**: Dad uses rubber-band AI to stay near you!

### 🏊 Pool Splash
A relaxing water balloon target practice!
- **Goal**: Hit floating targets and collect rings
- **Duration**: 60-second rounds
- **Power-ups**:
  - 🎯 Triple Shot: Fire 3 balloons at once
  - ⚡ Speed Boost: Move faster for 10 seconds
- **Scoring**:
  - Targets: +50 points
  - Rings: +25 points
  - Combo multiplier: x2, x3, x4...

### 🎰 Vegas Dash
Adventure through the neon streets of mini Las Vegas!
- **Goal**: Collect chips and defeat the Vegas Sphere boss
- **Boss Fight**: 3 phases with different emoji faces
- **Weapons**:
  - ⚔️ Sword slash (close range)
  - 🌈 Rainbow beam (long range)
- **Scoring**:
  - Chips: +100 points
  - Enemies: +200 points
  - Boss victory: +5000 points

## 🔧 Technical Details

### Architecture
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

### Performance
- **Target FPS**: 60 (with graceful degradation)
- **Resolution**: 1920x1080 (scales to display)
- **Memory Usage**: < 500MB
- **Load Times**: < 2 seconds per scene

## 🛠️ Development

### Setting Up Development Environment
```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run with debug mode
DEBUG=true poetry run python src/main.py

# Build executable
poetry run pyinstaller danger-rose.spec
```

### Code Structure
- **Scene System**: Each game mode is a separate scene
- **Entity-Component**: Characters use component-based design
- **Asset Pipeline**: Automatic fallback for missing assets
- **Save System**: JSON-based local storage

### Running Tests
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=src --cov-report=html

# Visual tests
poetry run pytest tests/ -k visual
```

## 🤝 Contributing

We love contributions from our young developers! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report bugs 🐛
- How to suggest features 💡
- Coding guidelines 📝
- How to submit changes 🚀

### For Kids
1. **Find a Bug?** Tell us what happened!
2. **Have an Idea?** Draw it or describe it!
3. **Want to Code?** Start with "good first issue" tags!

## 👥 Credits

### Development Team
- **Game Design**: The whole family!
- **Programming**: Parents & Kids with Claude Code
- **Art Direction**: Kids' creative vision
- **Testing**: Daily family game nights

### Assets
- Character sprites from [Kenney.nl](https://kenney.nl)
- Sound effects from [Freesound.org](https://freesound.org)
- Music composed using BeepBox
- Additional art from [OpenGameArt.org](https://opengameart.org)

### Special Thanks
- Claude Code for AI-assisted development
- The Pygame community for inspiration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ by a coding family

  [🐛 Report Bug](https://github.com/svange/danger-rose/issues) • [💡 Request Feature](https://github.com/svange/danger-rose/issues) • [📖 Documentation](docs/)
</div>
