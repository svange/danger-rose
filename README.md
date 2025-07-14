# Danger Rose

## Overview

*Danger-Rose* is a cozy, family‑friendly Pygame project where you and your kids star as the main characters. Players navigate a warm, apartment‑style hub world and choose from three themed minigames:

* **Ski Downhill**: Top‑down skiing down a snowy mountain, dodging trees and collecting snowflakes.
* **Pool Splash**: A cute "shoot‑em‑up" laid‑back pool game—splash targets and collect rings.
* **Vegas Dash**: A colorful side‑scrolling adventure through a miniature Las Vegas, collecting tokens and avoiding slot‑machine obstacles, while slashing and dashing through the streets.

Each minigame is framed as an activity with Dad, reinforcing family bonds and cooperative fun.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Gameplay Description](#gameplay-description)

   * [Hub World](#hub-world)
   * [Ski Minigame](#ski-minigame)
   * [Pool Minigame](#pool-minigame)
   * [Vegas Minigame](#vegas-minigame)
4. [Controls](#controls)
5. [Assets & Art](#assets--art)
6. [Development Roadmap](#development-roadmap)
7. [Contributing](#contributing)
8. [License](#license)

## Getting Started

### Prerequisites

* **Python 3.12+**

## Project Structure

```
danger-rose/
├── assets/
│   ├── images/
│   │   ├── characters/      # Dad and kids sprites (idle, run, jump, etc.)
│   │   ├── tilesets/        # Hub world (apartment) art, ski lift, poolside, Vegas buildings
│   │   └── icons/           # UI icons (coins, rings, menus)
│   └── audio/
│       ├── music/           # Background loops for hub and minigames
│       └── sfx/             # Sound effects (swoosh, splash, collect)
├── docs/                    # Design docs, this README
├── src/
│   ├── constants.py         # Global settings (screen size, colors)
│   ├── main.py              # Entry point, game loop management
│   ├── scenes/
│   │   ├── hub.py           # HubWorld scene class
│   │   ├── ski.py           # SkiGame scene class
│   │   ├── pool.py          # PoolGame scene class
│   │   └── vegas.py         # VegasGame scene class
│   └── utils/
│       ├── sprite_loader.py # Helper for loading sprite sheets
│       └── ui.py            # Button & menu classes
└── README.md
```

## Gameplay Description

### Hub World

* **Style**: Cozy apartment living room with a big window showing a pool on a sunny day with kids splashing outside.
* **Interaction**: Use arrow keys to move Dad and kids through the room. Stand near a door and press **Enter** (or **Space**) to enter a minigame.
* **Goal**: Explore, select activities, and return after each minigame to see cumulative scores.

### Ski Minigame

* **Perspective**: Top‑down view of a snowy mountain.
* **Objective**: Ski downhill, avoid trees and rocks, and collect falling snowflakes. Try to keep up with dad on his snowboard! Rubberbanding is used to keep the player close to Dad.
* **Mechanics**:

  * Arrow keys to steer left/right, **Space** to jump.
  * Score points by collecting snowflakes; lose a life if colliding with obstacles.
  * Three lives per run; finish line triggers return to hub with bonus points.

### Pool Minigame

* **Style**: Colorful poolside shoot‑em‑up ("cute‑em‑up").
* **Objective**: Shoot water balloons at floating targets and collect rings.
* **Mechanics**:

  * Move with arrow keys; aim with the mouse cursor.
  * **Left Click** to fire a water balloon.
  * Targets drift across the pool; hit as many as possible within the timer.
  * Collect power‑ups (multi‑shot, speed boost) for extra fun.

### Vegas Minigame

* **Perspective**: 2D side‑scroller along a stylized Las Vegas strip.
* **Objective**: Dash through neon‑lit streets, collect casino chips, while slashing swords or shooting rainbows at incoming slot machines and hazards.
* **Mechanics**:

  * **W/A/S/D** or arrow keys to move/jump.
  * Collect chips to rack up points; touch hazards to lose health.
  * Health pickups (nachos, soda pops) restore lives.
  * Reach the end marquee to unlock a jackpot bonus and return to hub.

## Controls

| Action     | Keys              |
|------------| ----------------- |
| Move       | W/A/S/D or arrows        |
| Move       | W/A/S/D or arrows |
| Shoot      | Mouse left click  |
| Jump       | Spacebar          |
| Enter room | Enter / Space     |
| Pause/Quit | Esc               |

## Assets & Art

* All character sprites and art should be placed in `assets/images/characters` and `assets/images/tilesets`.
* Music and sfx in `assets/audio/music` and `assets/audio/sfx`.
* Naming convention: `<game>_<asset>_<action>.png` (e.g., `ski_dad_idle.png`).

## Development Roadmap

1. **Core Framework**: Implement scene manager and main loop.
2. **Hub World**: Basic movement, interactions, and door transitions.
3. **Minigame Skeletons**: Empty scenes for Ski, Pool, Vegas.
4. **Ski Mechanics**: Terrain generation, collision detection, scoring.
5. **Pool Mechanics**: Target spawning, projectile physics.
6. **Vegas Mechanics**: Side‑scroll physics, hazard & pickup logic.
7. **UI & Menus**: Main menu, pause screen, score display.
8. **Audio Integration**: Background music loops and sound effects.
9. **Polish & Testing**: Tweaks, bug fixes, and playtesting with the kids.
