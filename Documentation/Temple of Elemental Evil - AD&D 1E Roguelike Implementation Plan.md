# Problem Statement
Create a terminal-based roguelike game based on the Temple of Elemental Evil adventure module using AD&D 1st Edition rules. The game must support both player-driven gameplay and autonomous simulation of a living, evolving world where NPCs, factions, and dungeons change over time. The system needs to be modular enough to support future GUI implementations.
# Current State
The project is in early stages with basic scaffolding:
* **Language**: Python 3
* **Structure**: Basic src/, data/, tests/ directories
* **Existing Code**: Minimal implementations of dice rolling, abilities, combat mechanics (surprise/initiative), and basic character/monster classes
* **Data Files**: JSON data for NPCs, monsters, items, treasure, and locations (currently only 2 locations in Hommlet)
* **Issues**: 
    * Limited test coverage (only dice and combat stubs)
    * No game loop, state management, or terminal UI
    * No world simulation engine
    * Incomplete combat system
    * No persistence layer
    * pioneer_test.py appears unrelated to the project
* **Reference Materials**: PDF rulebooks and Temple of Elemental Evil module available locally (not in source control)
# Proposed Solution
## Architecture Overview
Implement a layered architecture separating concerns:
* **Core Engine Layer**: AD&D 1E rules implementation (combat, spells, abilities, leveling)
* **World State Layer**: Game world management, entity tracking, time progression
* **Simulation Layer**: Autonomous NPC behavior, faction dynamics, recruitment, inter-faction conflicts
* **Game Logic Layer**: Player actions, turn management, dungeon exploration
* **Persistence Layer**: Save/load game state, logging, human-readable state exports
* **Interface Layer**: Terminal UI (abstracted for future GUI support)
## Phase 1: Foundation & Core Systems
### 1.1 Project Structure & Dependencies
* Add requirements.txt with dependencies: pytest, pytest-cov, pyyaml (for config), blessed/curses (terminal UI)
* Add pyproject.toml or setup.py for proper package management
* Create proper package structure with **init**.py files
* Set up logging framework (python logging module)
* Add .gitignore for Python projects
* Create config.yaml for game configuration
### 1.2 AD&D 1E Rules Engine
Implement core mechanics modules in src/rules/:
* **abilities.py**: Complete ability score implementation with modifiers (strength hit/damage bonuses, dex AC/initiative, con HP, etc.)
* **character_classes.py**: Fighter, Cleric, Magic-User, Thief, Ranger, Paladin, Druid, etc. with level progression, THAC0, saving throws, class abilities
* **races.py**: Human, Elf, Dwarf, Halfling, etc. with racial abilities and level limits
* **combat_system.py**: Complete combat with THAC0 tables, attack resolution, damage, armor class calculations, special attacks (grapple, charge, etc.)
* **spells.py**: Spell definitions for clerics and magic-users with effects
* **magic_items.py**: Magic item definitions and effects
* **experience.py**: XP calculation and leveling
* **saving_throws.py**: All saving throw categories by class and level
* **morale.py**: Morale checks for NPCs and monsters
### 1.3 Entity System
Create src/entities/ for game objects:
* **entity.py**: Base Entity class with position, state, properties
* **character.py**: Player and NPC characters with full AD&D stats, inventory, spells
* **monster.py**: Monster entities with special abilities
* **item.py**: Items, weapons, armor, treasures
* **faction.py**: Faction membership, relationships, goals
### 1.4 Data Layer Enhancement
Expand data/ directory:
* Complete monster definitions from AD&D Monster Manual
* All NPCs from Temple of Elemental Evil module with stats, AI behaviors, faction allegiances
* All locations: Hommlet (complete), Nulb, the Keep, Temple exterior, all dungeon levels
* Faction data: elemental cults, neutral areas, power dynamics
* Treasure tables and specific treasure placements
* Wandering monster tables
* Add data validation schemas
## Phase 2: World Simulation Engine
### 2.1 World State Management
Create src/world/:
* **world_state.py**: Central world state manager tracking all entities, time, events
* **time_system.py**: Game time tracking (turns, rounds, days), time-based events
* **event_system.py**: Event queue for scheduling future events (recruitment, battles, etc.)
* **location_manager.py**: Manages all locations, rooms, connections, visibility
* **faction_manager.py**: Tracks faction relationships, power levels, territory
### 2.2 Autonomous Simulation
Create src/simulation/:
* **npc_ai.py**: AI behaviors for NPCs (patrol, guard, recruit, attack, flee)
* **faction_ai.py**: High-level faction strategies (recruitment rates, territory expansion, inter-faction conflict triggers)
* **recruitment_system.py**: Leader recruitment mechanics per Temple of Elemental Evil module
* **conflict_resolution.py**: Battle resolution between factions without player involvement
* **world_evolution.py**: Orchestrates long-term world changes
* **simulation_runner.py**: Headless simulation mode with configurable time acceleration
### 2.3 Dynamic World Features
* NPCs gain levels, die, and are replaced
* Leaders recruit followers based on their power and resources
* Faction strength ebbs and flows based on leadership and conflicts
* Cleared areas can be repopulated
* Time-sensitive events from the module (e.g., temple ceremonies)
## Phase 3: Game Loop & Player Interaction
### 3.1 Core Game Loop
Create src/game/:
* **game_engine.py**: Main game loop, turn processing, mode switching (player/simulation)
* **action_handler.py**: Process player actions (move, attack, cast spell, use item, etc.)
* **dungeon_crawl.py**: Exploration mechanics, visibility, traps, secret doors
* **encounter_manager.py**: Random encounters, wandering monsters
* **dialogue_system.py**: NPC interaction, information gathering
### 3.2 Player Character Management
* Character creation wizard (roll stats, choose class/race)
* Inventory management
* Spell memorization and casting
* Leveling and XP tracking
* Character death and permadeath handling
### 3.3 Combat System Integration
* Turn-based combat with full AD&D rules
* Initiative, surprise, multiple combatants
* Status effects (poison, paralysis, etc.)
* Tactical options (fighting withdrawal, charge, etc.)
* Morale checks for NPCs
## Phase 4: Terminal Interface
### 4.1 Display System
Create src/ui/:
* **terminal_display.py**: Blessed/curses-based display manager
* **map_renderer.py**: ASCII map rendering with @ for player, letters for monsters, symbols for terrain
* **status_display.py**: Character stats, HP, spells, current effects
* **message_log.py**: Scrolling message history
* **menu_system.py**: Inventory, spell selection, character sheet menus
### 4.2 Input System
* **input_handler.py**: Keyboard input processing (vi-keys, numpad, or arrow keys for movement)
* Command parser for admin commands
* Confirmation prompts for dangerous actions
### 4.3 UI Abstraction
* Create abstract base classes for display and input
* Implement terminal version as concrete implementation
* Design allows future GUI implementations to plug in
## Phase 5: Persistence & Administration
### 5.1 Save/Load System
Create src/persistence/:
* **save_manager.py**: Full game state serialization (JSON or YAML)
* **state_exporter.py**: Human-readable state exports for inspection
* **log_writer.py**: Detailed game logs (combat, events, NPC actions)
### 5.2 Admin Commands
* Teleport to locations
* Reveal map
* Show faction status
* Show NPC/monster locations and states
* Time advancement
* Spawn entities
* Export world state snapshots
### 5.3 Human-Readable State Files
* Current faction power levels and relationships
* NPC roster with locations and stats
* Recent significant events
* Dungeon clearance status
* Player journal/achievements
## Phase 6: Testing & Documentation
### 6.1 Comprehensive Testing
* Unit tests for all rules modules (combat, spells, abilities, etc.)
* Integration tests for world simulation
* End-to-end tests for common gameplay scenarios
* Performance tests for simulation speed
* Aim for >80% code coverage
### 6.2 Documentation
* README with installation, running instructions
* Architecture documentation (this plan + detailed design docs)
* API documentation (docstrings for all public functions/classes)
* Player manual explaining commands and gameplay
* Developer guide for extending the game
* Code comments explaining complex AD&D rule implementations
### 6.3 Code Quality
* Type hints throughout (Python 3.9+ style)
* Linting with pylint or flake8
* Code formatting with black
* Pre-commit hooks for quality checks
## Phase 7: Content Population
### 7.1 Complete Temple of Elemental Evil Content
* All Hommlet locations and NPCs (complete the 20+ locations)
* Nulb village (10+ locations)
* The Keep (multiple levels)
* Temple exterior and ground level
* Temple dungeon level 1 (elemental fire)
* Temple dungeon level 2 (elemental earth)
* Temple dungeon level 3 (elemental air)
* Temple dungeon level 4 (elemental water)
* Greater Temple below
* Hidden nodes of elemental evil
### 7.2 NPC and Monster Population
* All named NPCs with personalities and goals
* All unique monsters and encounters
* Proper treasure placement
* Special encounters and scripted events
## Implementation Order
1. Phase 1 (Foundation) - Critical path
2. Phase 2.1 (World State) - Required for everything
3. Phase 3.1 + 3.2 (Basic gameplay without simulation)
4. Phase 4 (Terminal UI for playable prototype)
5. Phase 5.1 (Save/Load)
6. Phase 2.2 + 2.3 (Full simulation)
7. Phase 5.2 + 5.3 (Admin tools)
8. Phase 6 (Testing/Docs - ongoing throughout)
9. Phase 7 (Content - ongoing throughout)
## Technical Decisions
* **Language**: Python 3.9+ (already established, good for rapid development)
* **Terminal Library**: blessed (cleaner API than curses, cross-platform)
* **Data Format**: JSON for game data (already in use), YAML for saves (more human-readable)
* **Testing**: pytest with pytest-cov
* **Logging**: Python logging module with configurable levels and file output
* **No external PDFs needed**: Implement from AD&D knowledge and Temple of Elemental Evil module familiarity (PDFs mentioned but not present)
## Success Criteria
* Playable game with basic dungeon exploration
* Full AD&D 1E combat system
* Autonomous world simulation runs without player
* All major Temple of Elemental Evil areas implemented
* Save/load functionality
* Admin commands for world inspection
* Comprehensive test coverage
* Professional code quality and documentation
