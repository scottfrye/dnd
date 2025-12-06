# UI Architecture and Abstraction

## Overview

The Temple of Elemental Evil roguelike implements a flexible UI architecture that abstracts the display and input handling from the core game logic. This design allows for multiple front-end implementations (terminal, GUI, web, etc.) while maintaining a consistent interface.

## Architecture Principles

1. **Separation of Concerns**: Game logic is completely independent of UI implementation
2. **Abstract Interfaces**: Display and input handling are defined through abstract base classes
3. **Pluggable Implementations**: Different UI backends can be swapped without changing game code
4. **Context Manager Support**: Resources are properly managed through Python's context manager protocol

## Core Abstractions

### Display API (`src/ui/display.py`)

The `Display` abstract base class defines the interface for all display implementations:

```python
from src.ui.display import Display

class CustomDisplay(Display):
    """Your custom display implementation"""
    
    def initialize(self) -> None:
        """Initialize display resources"""
        
    def cleanup(self) -> None:
        """Clean up and release resources"""
        
    def clear(self) -> None:
        """Clear the entire display"""
        
    def render_map(self, map_data: list[list[str]], player_x: int, player_y: int) -> None:
        """Render the game map with player position"""
        
    def render_status(self, status_data: dict[str, Any]) -> None:
        """Render character status information"""
        
    def render_messages(self, messages: list[str]) -> None:
        """Render message log"""
        
    def refresh(self) -> None:
        """Commit all render operations to screen"""
        
    def get_dimensions(self) -> tuple[int, int]:
        """Return display dimensions (width, height)"""
```

#### Key Methods

- **initialize()**: Set up display system, enter appropriate modes, allocate resources
- **cleanup()**: Restore display state, release resources (called automatically on context exit)
- **clear()**: Erase all display content
- **render_map()**: Display the game world with player position marked
- **render_status()**: Show character statistics (HP, AC, level, etc.)
- **render_messages()**: Display game messages and event log
- **refresh()**: Flush rendering to screen (double-buffer support)
- **get_dimensions()**: Query available display space

#### Usage Pattern

```python
display = TerminalDisplay()

with display:  # Automatically calls initialize() and cleanup()
    display.clear()
    display.render_map(map_data, player_x, player_y)
    display.render_status({"hp": 10, "max_hp": 15, "level": 1})
    display.render_messages(["Welcome!", "Press ? for help"])
    display.refresh()
```

### InputHandler API (`src/ui/input.py`)

The `InputHandler` abstract base class defines the interface for input handling:

```python
from src.ui.input import InputHandler, InputAction

class CustomInputHandler(InputHandler):
    """Your custom input handler implementation"""
    
    def initialize(self) -> None:
        """Initialize input handling"""
        
    def cleanup(self) -> None:
        """Clean up input resources"""
        
    def get_input(self, timeout: float | None = None) -> InputAction | None:
        """Get next input action (high-level game command)"""
        
    def get_key(self, timeout: float | None = None) -> str | None:
        """Get raw key press (for prompts and dialogs)"""
```

#### InputAction Enumeration

The `InputAction` enum provides a standardized set of game actions:

**Movement Actions:**
- `MOVE_NORTH`, `MOVE_SOUTH`, `MOVE_EAST`, `MOVE_WEST`
- `MOVE_NORTHEAST`, `MOVE_NORTHWEST`, `MOVE_SOUTHEAST`, `MOVE_SOUTHWEST`

**Game Actions:**
- `WAIT`: Rest/pass turn
- `PICKUP`: Pick up items
- `INVENTORY`: View inventory
- `USE`: Use an item
- `DROP`: Drop an item
- `CAST_SPELL`: Cast a spell
- `LOOK`: Examine surroundings

**UI Actions:**
- `HELP`: Display help information
- `QUIT`: Exit the game
- `SAVE`: Save game state

**Special:**
- `UNKNOWN`: Unmapped/unrecognized input

#### Key Methods

- **initialize()**: Set up input handling system
- **cleanup()**: Restore input state (called automatically on context exit)
- **get_input()**: Returns `InputAction` for game commands
  - `timeout=None`: Blocks until input received
  - `timeout=0`: Non-blocking, returns immediately
  - `timeout=N`: Waits up to N seconds
- **get_key()**: Returns raw key string for dialogs and prompts

#### Usage Pattern

```python
input_handler = TerminalInputHandler()

with input_handler:  # Automatically calls initialize() and cleanup()
    while running:
        action = input_handler.get_input(timeout=0.1)
        
        if action == InputAction.QUIT:
            running = False
        elif action == InputAction.MOVE_NORTH:
            move_player(0, -1)
        elif action is not None:
            process_action(action)
```

## Terminal Implementation

The terminal implementation uses the `blessed` library for cross-platform terminal control.

### TerminalDisplay (`src/ui/terminal_display.py`)

Features:
- ASCII-based map rendering with configurable area sizes
- Color support using blessed's terminal attributes
- Player position highlighted in bold green
- Separate areas for map, status, and messages
- Automatic terminal size detection

Configuration:
```python
display = TerminalDisplay()
display.map_area_height = 20      # Height in character rows
display.map_area_width = 60       # Width in character columns
display.status_area_width = 30    # Status area width
display.message_area_height = 5   # Message log height
```

Map Rendering:
- Walls: `#`
- Floors: `.`
- Player: `@` (bold green)
- Other entities: Various ASCII characters

### TerminalInputHandler (`src/ui/input_handler.py`)

Supports multiple input schemes:

**Vi-keys (Classic Roguelike):**
- `h`/`j`/`k`/`l`: West/South/North/East
- `y`/`u`/`b`/`n`: Diagonals (NW/NE/SW/SE)

**Arrow Keys:**
- Standard directional arrows

**Numpad:**
- `8`/`2`/`4`/`6`: Cardinal directions
- `7`/`9`/`1`/`3`: Diagonals
- `5` or `.`: Wait

**Game Commands:**
- `,` or `g`: Pickup
- `i`: Inventory
- `a`: Use item
- `d`: Drop item
- `c`: Cast spell
- `;`: Look

**UI Commands:**
- `?`: Help
- `q`/`Q`: Quit
- `S`: Save

#### Key Mapping Customization

```python
handler = TerminalInputHandler()

# Add custom key mapping
handler.add_key_mapping("x", InputAction.EXAMINE)

# Remove existing mapping
handler.remove_key_mapping(".")

# Query mapping
action = handler.get_key_mapping("k")  # Returns InputAction.MOVE_NORTH
```

## Integration with Game Engine

The UI system integrates with the game engine through a simple interface:

```python
from src.ui.terminal_display import TerminalDisplay
from src.ui.input_handler import TerminalInputHandler
from src.game.game_engine import GameEngine, GameMode
from src.world.world_state import WorldState

# Initialize components
world = WorldState()
engine = GameEngine(world=world, mode=GameMode.PLAYER)
display = TerminalDisplay()
input_handler = TerminalInputHandler()

# Main game loop
with display, input_handler:
    running = True
    while running:
        # Render current state
        display.clear()
        display.render_map(get_map_data(world), player.x, player.y)
        display.render_status(get_player_status(player))
        display.render_messages(get_recent_messages())
        display.refresh()
        
        # Get and process input
        action = input_handler.get_input(timeout=0.1)
        if action:
            engine.step(action=action)
            running = (action != InputAction.QUIT)
```

## Testing

### Unit Tests

Each component has comprehensive unit tests:

- `tests/test_display.py`: Display abstract base class tests
- `tests/test_input.py`: InputHandler abstract base class and InputAction tests
- `tests/test_terminal_display.py`: TerminalDisplay implementation tests
- `tests/test_input_handler.py`: TerminalInputHandler implementation tests

Run tests:
```bash
pytest tests/test_display.py tests/test_input.py
pytest tests/test_terminal_display.py tests/test_input_handler.py
```

### Integration Testing

Integration tests verify the complete UI workflow:

- `tests/test_ui_integration.py`: Full UI rendering and input cycle tests

### Manual Testing

A demo script provides manual testing:

```bash
python scripts/terminal_ui_demo.py
```

This launches an interactive demo where you can:
- Move a character around an ASCII map
- See status updates
- View message log updates
- Test all input schemes

## Implementing New UI Backends

To implement a new UI backend (e.g., GUI, web interface):

### 1. Create Display Implementation

```python
from src.ui.display import Display

class GUIDisplay(Display):
    def __init__(self):
        # Initialize GUI framework
        pass
    
    def initialize(self) -> None:
        # Set up window, canvas, etc.
        pass
    
    def cleanup(self) -> None:
        # Close window, release resources
        pass
    
    def clear(self) -> None:
        # Clear canvas/screen
        pass
    
    def render_map(self, map_data, player_x, player_y) -> None:
        # Draw map with sprites/tiles
        pass
    
    def render_status(self, status_data) -> None:
        # Update status widgets
        pass
    
    def render_messages(self, messages) -> None:
        # Update message text area
        pass
    
    def refresh(self) -> None:
        # Update GUI display
        pass
    
    def get_dimensions(self) -> tuple[int, int]:
        # Return window/canvas size
        return (800, 600)
```

### 2. Create InputHandler Implementation

```python
from src.ui.input import InputHandler, InputAction

class GUIInputHandler(InputHandler):
    def __init__(self):
        # Initialize event handlers
        pass
    
    def initialize(self) -> None:
        # Set up keyboard/mouse listeners
        pass
    
    def cleanup(self) -> None:
        # Remove listeners
        pass
    
    def get_input(self, timeout=None) -> InputAction | None:
        # Poll event queue, map to InputAction
        pass
    
    def get_key(self, timeout=None) -> str | None:
        # Get raw key event
        pass
```

### 3. Write Tests

Follow the existing test patterns:
- Test abstract interface compliance
- Test context manager behavior
- Test specific rendering/input functionality
- Mock external dependencies (GUI framework, etc.)

### 4. Update Game Engine

The game engine should accept display and input handler as parameters:

```python
engine = GameEngine(
    world=world,
    display=GUIDisplay(),
    input_handler=GUIInputHandler()
)
```

## Best Practices

1. **Use Context Managers**: Always use `with` statements to ensure proper resource cleanup
2. **Handle Timeouts**: Use appropriate timeout values in `get_input()` for responsive UI
3. **Mock for Tests**: Use mocking to test without actual terminal/GUI interaction
4. **Separate Concerns**: Keep game logic independent of UI implementation details
5. **Document Keybindings**: Clearly document all supported input schemes
6. **Test Coverage**: Maintain high test coverage for UI components
7. **Error Handling**: Gracefully handle terminal resize, focus loss, etc.

## Future Enhancements

Potential improvements to the UI system:

1. **Mouse Support**: Add mouse input handling to InputHandler
2. **Color Themes**: Configurable color schemes for terminal display
3. **Tile Graphics**: Support for graphical tiles in GUI implementations
4. **Sound**: Audio feedback system abstraction
5. **Accessibility**: Screen reader support, high contrast modes
6. **Network**: Remote/multiplayer input handling
7. **Replay**: Input recording and playback for debugging
8. **Macros**: Command macros and key rebinding

## References

- [blessed Documentation](https://blessed.readthedocs.io/)
- [Python ABC Module](https://docs.python.org/3/library/abc.html)
- [Context Managers](https://docs.python.org/3/library/contextlib.html)
- Traditional roguelike UI patterns (NetHack, DCSS, etc.)
