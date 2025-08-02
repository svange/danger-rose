# Game Mechanics Guide

## Overview

Danger Rose features three distinct minigames, each with unique mechanics and scoring systems. This guide details the implementation and design of each game mode.

## Hub World

The apartment serves as the central hub connecting all minigames.

### Features
- **Navigation**: Free movement with collision detection
- **Doors**: Interactive portals to minigames
- **Save Points**: Automatic progress saving
- **Trophy Display**: Visual representation of achievements
- **Character State**: Maintains selected character across scenes

### Implementation Notes
- Uses tile-based collision for walls
- Door interactions trigger scene transitions
- Background music loops continuously

## 🎿 Ski Minigame

### Core Mechanics
- **Objective**: Survive 60 seconds while collecting snowflakes
- **Movement**: Left/right steering with momentum
- **Speed**: Constant downward velocity with acceleration
- **Dad AI**: Follows player with rubber-band AI

### Obstacles
- **Trees**: Static obstacles (-1 life on hit)
- **Rocks**: Slows player temporarily
- **Ice Patches**: Reduces steering control

### Scoring
- Snowflake: +10 points
- Survival bonus: +100 points per 10 seconds
- Near-miss bonus: +5 points (passing close to obstacles)

### Technical Details
- Procedural generation for infinite slopes
- Parallax scrolling for depth
- Particle effects for snow spray

## 🏊 Pool Minigame

### Core Mechanics
- **Objective**: Hit targets with water balloons
- **Aiming**: Mouse-controlled crosshair
- **Physics**: Projectile arc with gravity
- **Time Limit**: 60 seconds

### Target Types
1. **Rubber Ducks** (10 pts)
   - Slow moving, easy targets
   - Float in predictable patterns

2. **Beach Balls** (25 pts)
   - Bounce when hit
   - Chain reactions possible

3. **Donut Floats** (50 pts)
   - Fast moving
   - Smaller hitbox

### Power-ups
- **Triple Shot**: Fire 3 balloons at once (10 sec)
- **Rapid Fire**: Reduced cooldown (15 sec)
- **Homing Balloons**: Slight target tracking (5 sec)

### Combo System
- 2x multiplier: 3 hits in 2 seconds
- 3x multiplier: 5 hits in 3 seconds
- 5x multiplier: 10 hits in 5 seconds

## 🎰 Vegas Minigame

### Core Mechanics
- **Genre**: Side-scrolling beat 'em up
- **Combat**: Melee and ranged attacks
- **Health**: 3 hearts, regenerate between rooms
- **Progression**: Linear level with boss fight

### Enemy Types
1. **Casino Chips**
   - Basic melee enemy
   - 1 hit to defeat
   - Drop coins (5 pts)

2. **Dice**
   - Ranged projectiles
   - 2 hits to defeat
   - Drop health occasionally

3. **Playing Cards**
   - Fast, swooping attacks
   - 1 hit to defeat
   - Appear in groups

### Boss Battle: Vegas Sphere

**Phase 1** (100-66% health)
- Laser sweep attacks
- Spawns chip minions
- Predictable patterns

**Phase 2** (66-33% health)
- Adds homing projectiles
- Increased attack speed
- Floor hazards activate

**Phase 3** (33-0% health)
- Screen-filling attacks
- Desperation mode
- All previous attacks combined

### Weapons
- **Sword**: Close range, high damage
- **Rainbow Beam**: Long range, piercing

## Scoring & Progression

### High Score System
- Persistent across sessions
- Per-minigame leaderboards
- Top 10 scores displayed

### Unlockables
- **Dad Character**: Unlock after beating all minigames
- **Hard Mode**: Unlock after achieving target scores
- **Secret Room**: Find all hidden collectibles

## Audio Design

### Music
- Hub World: Cozy, ambient loop
- Ski Game: Upbeat, energetic
- Pool Game: Summer, cheerful
- Vegas Game: Electronic, intense

### Sound Effects
- UI: Button clicks, menu navigation
- Actions: Jump, attack, collect
- Feedback: Hit, miss, victory
- Ambient: Environmental sounds per scene

## Balancing

### Difficulty Progression
- **Easy**: For young kids (more health, slower enemies)
- **Normal**: Default balanced experience
- **Hard**: For experienced players (less health, faster enemies)

### Adaptive Difficulty
- Track player performance
- Adjust spawn rates subtly
- Never punish struggling players
- Reward skilled play with bonus challenges
