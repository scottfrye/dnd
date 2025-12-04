# Temple of Elemental Evil - AD&D 1E Roguelike

[![CI](https://github.com/scottfrye/dnd/actions/workflows/ci.yml/badge.svg)](https://github.com/scottfrye/dnd/actions/workflows/ci.yml)

## Purpose

A game similar to Nethack that uses the Advanced Dungeon and Dragons (1st Edition) rules. The dungeon will be from the adventure module The Temple of Elemental Evil. The rule books and adventure modules are included in PDF form and should be referenced when creating the game.

The game includes all the areas in the adventure module including the dungeons, the towns of Hommlett and Nulb, the Keep and the Temple of Elemental Evil itself and all of its dungeons. The details of play will be kept in log files. The dungeon and the towns will change over time as described in the adventure module.

The different leaders, while alive will continue recruiting new followers and occasionally there will be battles between the different areas as the leaders of the areas try to gain over their rivals. The game will have the capability to run without player characters and the non player characters and dungeons will evolve. The game will provide a way to simulate these changes for long periods of time with or without player characters.

The state of the dungeon will be available through admin commands and human readable state files. The game will be entirely terminal based but the gameplay will be abstracted enough to consider a different GUI front end in the future. The code will be professional level quality and incorporate best practices for software development at all levels, including documentation and testing.

## Repository Layout

```
dnd/
├── Documentation/      # Design documents and implementation plans
├── prompts/           # AI prompt templates and configurations
├── resources/         # Game resources (PDFs, reference materials)
├── src/               # Main source code
│   ├── entities/      # Game entities (characters, monsters, items)
│   ├── game/          # Core game logic and state management
│   ├── persistence/   # Save/load and data persistence
│   ├── rules/         # AD&D 1E rule implementations
│   ├── simulation/    # World simulation and time progression
│   ├── ui/            # Terminal user interface
│   └── world/         # World, maps, and location management
├── tests/             # Unit and integration tests
├── pyproject.toml     # Python project configuration
└── README.md          # This file
```

## Development

### Requirements

- Python 3.12+

### Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```