# 🎮 Danger Rose

<div align="center">
  <img src="docs/images/logo-placeholder.png" alt="Danger Rose Logo" width="400">

  **A cozy family game with endless minigame adventures**

  [![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
  [![Pygame](https://img.shields.io/badge/Pygame--CE-2.4%2B-green.svg)](https://pyga.me/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 🏠 About

**Danger Rose** is a cozy family game built with Python and Pygame. Players control Danger, Rose, or Dad as they explore an apartment hub world and play various minigames.

Each minigame offers a different adventure - from skiing down mountains to water balloon battles at the pool to side-scrolling action in Vegas. The game continues to grow with new minigames being added regularly.

<div align="center">
  <h3>
    <a href="https://github.com/svange/danger-rose/releases/latest">
      🎮 Download Game
    </a>
  </h3>
  <p>
    <strong>Windows, macOS, and Linux</strong>
  </p>
</div>

## 🎯 Quick Play

1. **[Download the game](https://github.com/svange/danger-rose/releases)** for your system
2. **Run it** - no installation needed!
3. **Pick a character** with arrow keys
4. **Press SPACE** to start exploring

### Controls
- **Move**: Arrow keys or WASD
- **Jump/Interact**: Space
- **Pause**: Escape

## 🎮 Current Minigames

Start in the apartment hub and walk through doors to discover:

### Available Now
- **🎿 Ski Game** - Race down the mountain while Dad chases on his snowboard
- **🏊 Pool Game** - Water balloon target practice 
- **🎰 Vegas Game** - Side-scrolling adventure through the city

### Coming Soon
More minigames are in development! The hub world is designed to expand with new doors and adventures.

## 👨‍💻 Development

Here's how to run the game from source:

```bash
# Get the code
git clone https://github.com/svange/danger-rose.git
cd danger-rose

# Install Poetry (if needed)
curl -sSL https://install.python-poetry.org | python3 -

# Install game dependencies
poetry install

# Run the game
make run
```

### Useful Commands

```bash
make run          # Play the game
make test         # Run tests
make lint         # Check code style
make format       # Auto-format code
make claude       # Start Claude Code for AI pair programming
```

See our [development guides](./guides/) for more details.

## 🤝 Contributing

Contributions are welcome from developers of all experience levels!

Check out [CONTRIBUTING.md](guides/setup/contributing.md) to get started.

## 📚 Documentation

- **[LINKS.md](./LINKS.md)** - Quick navigation to all docs
- **[Setup Guides](./guides/setup/)** - Getting started
- **[Development Guides](./guides/development/)** - How we build the game
- **[AI Guides](./guides/ai/)** - Using Claude Code effectively

## 👥 Credits

**Made by**: Samuel, Yasha, and Ellie Vange

**Special Thanks**:
- Character sprites from [Kenney.nl](https://kenney.nl)
- Sound effects from [Freesound.org](https://freesound.org)
- Music made with BeepBox

---

<div align="center">
  Made with ❤️ thanks to the <a href="https://pyga.me/">pygame-ce</a> community
</div>