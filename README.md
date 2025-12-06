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
├── CHANGELOG.md       # Version history and release notes
├── CONTRIBUTING.md    # Contributing guidelines
└── README.md          # This file
```

## Quick Start

### Installation

Install the core dependencies:

```bash
pip install -r requirements.txt
```

### Running Tests

Run the test suite with pytest:

```bash
pytest
```

### Headless Simulation

Run the game in autonomous simulation mode without player input:

```bash
python -c "from src.game.game_engine import GameEngine, GameMode; engine = GameEngine(mode=GameMode.HEADLESS); engine.run_headless(100)"
```

This will simulate 100 game ticks, allowing NPCs, factions, and the world to evolve autonomously.

### Documentation

For detailed implementation plans and design documentation, see:
- [Temple of Elemental Evil - AD&D 1E Roguelike Implementation Plan](Documentation/Temple%20of%20Elemental%20Evil%20-%20AD%26D%201E%20Roguelike%20Implementation%20Plan.md)

## Development

### Requirements

- Python 3.12, 3.13, 3.14 or above
- Supported on Windows, macOS, and Linux
- Compatible with Anaconda/Miniconda environments

### Setup

#### Using pip

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

#### Using Anaconda

```bash
# Create a new conda environment
conda create -n dnd python=3.12
conda activate dnd

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Code Quality

This project uses pre-commit hooks to maintain code quality. The hooks include:
- **Black**: Automatic code formatting
- **Ruff**: Fast Python linter (replaces flake8, isort, and more)
- **Standard checks**: Trailing whitespace, YAML validation, etc.

After installing development dependencies, set up pre-commit hooks:

```bash
pre-commit install
```

The hooks will run automatically on `git commit`. You can also run them manually:

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run ruff --all-files
```

### Terminal UI Demo

To test the terminal UI implementation, run the smoke test demo:

```bash
python scripts/terminal_ui_demo.py
```

This will launch a simple interactive terminal display showing:
- An ASCII map with walls (`#`) and floors (`.`)
- Your character represented by `@` that you can move around
- A status area showing character information
- A message log displaying game events

**Controls:**
- `hjkl` - Vi-keys for movement (h=west, j=south, k=north, l=east)
- `yubn` - Diagonal movement (y=NW, u=NE, b=SW, n=SE)
- Arrow keys - Alternative movement controls
- Numpad (2468) - Another movement option
- `.` or `5` - Wait/rest
- `?` - Help
- `q` - Quit

The demo showcases the abstracted Display and InputHandler interfaces that allow
for different UI backends to be implemented in the future (GUI, web, etc.).

For detailed manual testing instructions, see: [Documentation/ui-manual-tests.md](Documentation/ui-manual-tests.md)

## UI Architecture

The game features a fully abstracted UI system that separates display and input handling from core game logic. This architecture enables:

- **Terminal Interface**: ASCII-based display using the `blessed` library (currently implemented)
- **Future GUI Support**: Pluggable architecture allows for graphical front-ends
- **Consistent Interface**: All UI implementations follow the same abstract base classes

### Abstract APIs

The UI system is built on two core abstractions:

1. **Display API** (`src/ui/display.py`): Handles rendering of game state
   - `render_map()`: Display game world and player position
   - `render_status()`: Show character statistics
   - `render_messages()`: Display event log
   - `refresh()`: Update screen with rendered content

2. **InputHandler API** (`src/ui/input.py`): Manages user input
   - `get_input()`: Returns high-level game actions (`InputAction` enum)
   - `get_key()`: Returns raw key presses for prompts
   - Supports multiple input schemes (vi-keys, arrow keys, numpad)

### Terminal Implementation

The current terminal implementation (`src/ui/terminal_display.py` and `src/ui/input_handler.py`) provides:

- ASCII map rendering with color support
- Flexible layout (configurable map, status, and message areas)
- Multiple key binding schemes
- Cross-platform terminal support via `blessed`

### Documentation

For detailed information about the UI architecture, including:
- API specifications and usage examples
- How to implement new UI backends
- Integration with the game engine
- Testing strategies

See: [Documentation/ui-architecture.md](Documentation/ui-architecture.md)

### Testing

The UI system has comprehensive test coverage:

- **Unit Tests**: `tests/test_display.py`, `tests/test_input.py`, `tests/test_terminal_display.py`, `tests/test_input_handler.py`
- **Integration Tests**: `tests/test_ui_integration.py` - Tests complete render/input cycles
- **Manual Testing**: `scripts/terminal_ui_demo.py` - Interactive demonstration

Run UI tests:
```bash
# Run all UI tests
pytest tests/test_*display*.py tests/test_*input*.py tests/test_ui_integration.py

# Run just integration tests
pytest tests/test_ui_integration.py -v
```

### Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.
