# Problem Statement
Determine the next development steps for the Temple of Elemental Evil AD&D 1E roguelike based on end goals in README.md, original requirements in prompt001.txt, and existing completed work. The project requires implementing the complete Temple of Elemental Evil adventure module with autonomous world simulation, full AD&D 1E rules, and professional code quality.
# Current State Overview
## What's Been Completed
### Foundation Systems (Phase 1 - Mostly Complete)
**Project Infrastructure**
* Python 3.12+ with pyproject.toml package management
* Pre-commit hooks (black, ruff) for code quality
* Comprehensive test suite (453 tests across 22 test files)
* Logging framework configured
* Configuration system (YAML-based)
* CI pipeline for Windows, macOS, Linux
* Documentation structure established
**Core Rules Engine (Partial - Phase 1)**
* ✅ abilities.py: Complete (92% coverage) - Ability scores with STR/DEX/CON modifiers
* ✅ combat_system.py: Complete (95% coverage) - THAC0-based combat, 4 class groups, attack resolution
* ✅ dice.py: Complete - Dice rolling utilities with DiceRoller
* ❌ character_classes.py: Not implemented - No class system (Fighter, Cleric, etc.)
* ❌ races.py: Not implemented - No race system
* ❌ saving_throws.py: Not implemented
* ❌ experience.py: Not implemented
* ❌ spells.py: Not implemented
* ❌ magic_items.py: Not implemented
* ❌ morale.py: Not implemented
**Entity System (Phase 1 - Basic)**
* ✅ entity.py: Base Entity and Position classes with serialization
* ❌ character.py: Not implemented - No full character representation
* ❌ monster.py: Not implemented
* ❌ item.py: Not implemented
* ❌ faction.py: Not implemented
**World Simulation (Phase 2 - Partial)**
* ✅ world_state.py: Complete - Entity registry, time tracking, serialization
* ✅ time_system.py: Complete - Time management (ticks/rounds/turns/hours/days)
* ✅ event_system.py: Complete - Event scheduling and dispatch
* ❌ location_manager.py: Not implemented
* ❌ faction_manager.py: Not implemented (critical gap)
**Game Engine (Phase 3 - Basic)**
* ✅ game_engine.py: Basic implementation - Player/headless modes, tick advancement
* ✅ action_handler.py: Basic move/attack/idle actions
* ❌ dungeon_crawl.py: Not implemented - No exploration mechanics
* ❌ encounter_manager.py: Not implemented
* ❌ dialogue_system.py: Not implemented
**Terminal UI (Phase 4 - Complete)**
* ✅ display.py: Abstract display interface
* ✅ terminal_display.py: ASCII display implementation with blessed
* ✅ input.py: Abstract input interface
* ✅ input_handler.py: Keyboard input (vi-keys, arrows, numpad)
* ✅ Manual test demo script (terminal_ui_demo.py)
* ✅ Comprehensive UI integration tests
**Persistence (Phase 5 - Partial)**
* ✅ save_manager.py: YAML/JSON serialization for WorldState
* ❌ state_exporter.py: Not implemented - No human-readable reports
* ❌ log_writer.py: Not implemented - No detailed game logging
* ❌ Admin command expansion needed
**NPC/World AI (Phase 2 - Minimal)**
* ✅ npc_ai.py: Basic behaviors (idle, patrol, attack on sight)
* ❌ faction_ai.py: Not implemented (critical gap)
* ❌ recruitment_system.py: Not implemented
* ❌ conflict_resolution.py: Not implemented
* ❌ world_evolution.py: Not implemented
**Content Population (Phase 7 - Not Started)**
* ❌ No Temple of Elemental Evil locations implemented
* ❌ No NPCs from the module
* ❌ No monsters populated
* ❌ No adventure-specific content
## Key Gaps Identified
1. **No Character System**: Cannot create playable characters with classes/races
2. **No Faction System**: Core requirement for world simulation missing
3. **No Content**: Zero Temple of Elemental Evil locations or NPCs
4. **No Exploration**: No dungeon crawling mechanics
5. **No Complete Creatures**: No monster or NPC implementations
6. **Rules Incomplete**: Missing 7 of 9 planned rules modules
7. **No Autonomous Simulation**: Faction AI not implemented
## Testing Status
* Total Tests: 453 across 22 test files
* Rules Coverage: abilities (92%), combat (95%)
* Good coverage for: world state, time system, event system, UI, persistence
* Missing coverage for: unimplemented modules
# Proposed Solution
## Development Priority Assessment
Based on the original requirements and current state, prioritize:
1. **Character Classes & Races** (High) - Required for playable game
2. **Faction Manager** (High) - Required for world simulation
3. **Location System** (High) - Required for Temple content
4. **Monster/NPC Entities** (High) - Required for encounters
5. **Faction AI** (High) - Required for autonomous simulation
6. **Temple Content Population** (Medium) - Can be incremental
7. **Remaining Rules Modules** (Medium) - Can be implemented as needed
8. **Advanced Features** (Low) - Polish after core functionality
## Phase Breakdown
### Phase A: Character System Foundation (3-4 weeks)
**Goal**: Enable character creation with AD&D 1E classes and races
**Modules to Implement**:
1. **src/rules/character_classes.py**
    * Base Character class framework
    * Fighter, Cleric, Magic-User, Thief (core four)
    * Level progression tables
    * THAC0 integration
    * Hit dice tables
    * Class restrictions (armor/weapons)
    * Multi-class and dual-class support structure
    * Tests: 90%+ coverage target
2. **src/rules/races.py**
    * Human, Elf, Dwarf, Halfling (core four)
    * Sub-race support (High Elf, Hill Dwarf, etc.)
    * Ability score adjustments
    * Level limits per class
    * Special abilities (infravision, detect slopes)
    * Language lists
    * Tests: 90%+ coverage target
3. **src/rules/saving_throws.py**
    * Five saving throw categories per AD&D 1E
    * Tables for all classes
    * Racial bonuses
    * Resolution function
    * Tests: 90%+ coverage target
4. **src/entities/character.py**
    * Complete Character entity
    * Integrate AbilityScores, class, race
    * Inventory system
    * HP/AC/THAC0 calculation
    * Serialization support
    * Tests: 90%+ coverage target
**Deliverables**:
* Character creation system
* Full character sheet representation
* Character serialization for saves
* Character stat calculations
* Updated documentation
**Success Criteria**:
* Can create characters with any class/race combination
* Character stats calculate correctly per AD&D 1E
* Characters persist through save/load
* 90%+ test coverage on all new modules
### Phase B: Faction & Location Systems (3-4 weeks)
**Goal**: Implement faction management and location system for world simulation
**Modules to Implement**:
1. **src/world/faction_manager.py**
    * Faction registry
    * Relationship tracking (-100 to +100)
    * Power level calculations
    * Territory control
    * Member management
    * Conflict resolution mechanics
    * Tests: 90%+ coverage target
2. **src/world/location_manager.py**
    * Location registry
    * Room/area definitions
    * Connection/movement graph
    * Entity-location tracking
    * Visibility/fog of war support
    * Tests: 90%+ coverage target
3. **src/entities/faction.py**
    * Faction dataclass
    * Goals and objectives
    * Resource tracking
    * Alliance/hostility states
    * Tests: 90%+ coverage target
4. **src/simulation/faction_ai.py**
    * Recruitment strategy
    * Territorial expansion AI
    * Diplomatic decision-making
    * Resource allocation
    * Conflict initiation logic
    * Tests: 85%+ coverage target
**Temple of Elemental Evil Factions**:
* Fire Temple (Cult of the Salamander)
* Water Temple (Cult of the Crayfish)
* Air Temple (Cult of the Air)
* Earth Temple (Cult of the Black Earth)
* Greater Temple (Zuggtmoy's forces)
* Hommlet Defenders
* Nulb Raiders
**Deliverables**:
* Faction system with 7 ToEE factions
* Location data structure
* Faction AI for autonomous behavior
* Territory control tracking
* Integration with event system
**Success Criteria**:
* Factions track relationships and power
* Faction AI makes strategic decisions
* Locations can contain entities
* Integration with existing world simulation
* 85%+ test coverage on all modules
### Phase C: Creatures & Encounters (2-3 weeks)
**Goal**: Implement monster and NPC entities for encounters
**Modules to Implement**:
1. **src/entities/monster.py**
    * Monster entity class
    * Hit dice calculation
    * Special abilities structure
    * Treasure generation
    * AI behavior mapping
    * Tests: 90%+ coverage target
2. **src/entities/npc.py** (or extend character.py)
    * NPC specialization
    * AI state tracking
    * Loyalty/morale
    * Faction membership
    * Dialogue data references
    * Tests: 90%+ coverage target
3. **src/entities/item.py**
    * Item base class
    * Weapons, armor, equipment
    * Treasure items
    * Weight and encumbrance
    * Tests: 90%+ coverage target
4. **src/game/encounter_manager.py**
    * Random encounter tables
    * Wandering monsters
    * Encounter scheduling
    * Distance and detection
    * Tests: 85%+ coverage target
5. **Enhanced NPC AI** (extend npc_ai.py)
    * Guard behavior (patrol, investigate, reinforce)
    * Priest behavior (ceremonies, healing, buffs)
    * Leader behavior (command, recruit)
    * Merchant behavior (shop schedule, prices)
    * Commoner behavior (daily routine, flee)
    * Monster behaviors by type
**Deliverables**:
* Monster entity implementation
* NPC entity implementation
* Item system
* Encounter generation
* Expanded NPC AI behaviors
**Success Criteria**:
* Can spawn monsters with proper stats
* NPCs have faction membership
* Encounters generate appropriately
* AI behaviors drive NPC actions
* 85%+ test coverage
### Phase D: Dungeon Crawling & Exploration (2-3 weeks)
**Goal**: Enable player exploration and dungeon mechanics
**Modules to Implement**:
1. **src/game/dungeon_crawl.py**
    * Movement mechanics
    * Line of sight calculations
    * Trap detection and resolution
    * Secret door mechanics
    * Door states (locked, stuck, open)
    * Tests: 85%+ coverage target
2. **src/world/map_manager.py**
    * Map data structures (tiles, walls, features)
    * Map generation/loading
    * Pathfinding algorithms
    * Visibility calculations
    * Tests: 85%+ coverage target
3. **Enhanced Action Handler** (extend action_handler.py)
    * Search action
    * Use item action
    * Open/close door
    * Pick lock
    * Disarm trap
    * Climb, swim, etc.
4. **src/game/dialogue_system.py** (basic)
    * Dialogue tree structure
    * NPC conversation state
    * Information gathering
    * Quest tracking hooks
    * Tests: 80%+ coverage target
**Deliverables**:
* Full movement system
* Trap and secret door mechanics
* Map system
* Basic dialogue system
* Enhanced player actions
**Success Criteria**:
* Player can explore dungeon maps
* Line of sight works correctly
* Traps and secrets function
* Basic NPC dialogue works
* 80%+ test coverage
### Phase E: Temple Content Population (4-6 weeks, incremental)
**Goal**: Populate Temple of Elemental Evil locations and NPCs
**Content to Create** (data files in data/ directory):
1. **Hommlet Village** (20+ locations)
    * Inn of the Welcome Wench
    * Trading Post
    * Church of St. Cuthbert
    * Tower of Burne and Rufus
    * Village buildings
    * Named NPCs with stats
2. **Nulb Village** (10+ locations)
    * Waterside Hostel
    * Boatmen
    * Bandits and brigands
3. **Moathouse Ruins**
    * Surface level
    * Dungeon level
    * Lareth the Beautiful encounter
4. **The Temple Exterior**
    * Ground level
    * Main gates
    * Guard posts
5. **Temple Dungeon Levels** (incremental)
    * Level 1: Fire Temple
    * Level 2: Earth Temple
    * Level 3: Air Temple
    * Level 4: Water Temple
    * Greater Temple levels
6. **Monster Data**
    * All monsters from adventure module
    * Monster Manual I entries used in module
    * Special abilities defined
7. **Treasure Data**
    * Placed treasure per module
    * Random treasure tables
    * Magic items
**Approach**:
* Start with Hommlet (player starting area)
* Add Moathouse (first dungeon)
* Incrementally add temple levels
* Use JSON/YAML data files
* Data validation schemas
* Content loading system
**Deliverables**:
* Complete location data for major areas
* All named NPCs with full stats
* Monster spawns and encounters
* Treasure placement
* Content documentation
**Success Criteria**:
* Hommlet fully functional
* At least one dungeon (Moathouse) playable
* Named NPCs present with correct stats
* Data validates against schemas
* Content matches adventure module
### Phase F: Remaining Rules & Polish (3-4 weeks)
**Goal**: Complete remaining AD&D 1E rules and polish features
**Modules to Implement**:
1. **src/rules/experience.py**
    * XP calculation (monsters, treasure)
    * Level advancement
    * Training requirements
    * Prime requisite bonuses
    * Tests: 90%+ coverage
2. **src/rules/spells.py** (subset initially)
    * Spell base class
    * Spell effect system
    * Memorization mechanics
    * Casting mechanics
    * Cleric spells (levels 1-3)
    * Magic-User spells (levels 1-3)
    * Tests: 85%+ coverage
3. **src/rules/morale.py**
    * Morale scores
    * Morale check triggers
    * Resolution (2d6)
    * Modifiers and results
    * Tests: 90%+ coverage
4. **src/rules/magic_items.py** (basic)
    * Magic weapon/armor
    * Potion effects
    * Scroll handling
    * Tests: 85%+ coverage
**Polish Features**:
* Enhanced admin commands
* Human-readable state exports
* Combat log writer
* Performance optimization
* Documentation completion
* Tutorial/help system
**Deliverables**:
* Complete core rules modules
* Basic spell system
* Magic item handling
* Polished admin tools
* Complete documentation
**Success Criteria**:
* Characters can gain XP and level up
* Basic spellcasting works
* Morale system functions
* Magic items have effects
* 85%+ test coverage on all modules
* Documentation complete and accurate
## Implementation Best Practices
### Code Quality Standards
* **Type Hints**: Full type annotations (Python 3.12+ style)
* **Docstrings**: Comprehensive docstrings for all public APIs
* **Testing**: Minimum 85% coverage per module, 90% for core rules
* **Linting**: Pass black and ruff checks (enforced by pre-commit)
* **Documentation**: Update docs for each module
* **AD&D Accuracy**: Reference rulebooks (PDFs in resources/)
### Testing Strategy
* **Unit Tests**: Test each function/class in isolation
* **Integration Tests**: Test system interactions
* **Simulation Tests**: Long-running headless mode validation
* **Manual Tests**: Playtest with terminal UI
* **Balance Tests**: Ensure faction systems remain balanced
### Development Workflow
1. Create feature branch from development
2. Implement module with tests
3. Ensure 85%+ coverage
4. Run pre-commit hooks
5. Manual testing as needed
6. Update documentation
7. Create PR to development branch
8. Review and merge
### Documentation Requirements
For each new module:
* Module docstring with overview
* Function/class docstrings with examples
* Update relevant documentation files
* Add usage examples where appropriate
* Reference AD&D 1E rulebooks for mechanics
## Success Metrics
### Phase A Success
* Character creation wizard functional
* All 4 core classes implemented
* All 4 core races implemented
* Characters persist through save/load
* 90%+ test coverage
### Phase B Success
* 7 ToEE factions defined and functional
* Faction AI makes autonomous decisions
* Recruitment system works
* Territory tracking active
* 85%+ test coverage
### Phase C Success
* Monster entities spawn with correct stats
* NPC AI drives behaviors
* Encounters generate appropriately
* Items exist and can be equipped
* 85%+ test coverage
### Phase D Success
* Player can explore maps
* Line of sight and visibility work
* Traps and secrets function
* Basic dialogue operational
* 80%+ test coverage
### Phase E Success
* Hommlet village fully populated
* Moathouse dungeon playable
* Named NPCs present with correct stats
* Content validates
### Phase F Success
* All core rules modules complete
* Basic spellcasting works
* XP and leveling functional
* Documentation complete
* 85%+ overall test coverage
## Overall Timeline Estimate
* **Phase A**: 3-4 weeks (Character System)
* **Phase B**: 3-4 weeks (Factions & Locations)
* **Phase C**: 2-3 weeks (Creatures & Encounters)
* **Phase D**: 2-3 weeks (Dungeon Crawling)
* **Phase E**: 4-6 weeks (Content Population, can be parallel)
* **Phase F**: 3-4 weeks (Remaining Rules & Polish)
**Total**: 17-24 weeks (4-6 months) for complete core implementation
**Note**: Phases E can be done incrementally alongside other phases. Focus on getting a playable slice (Hommlet + Moathouse) before completing all temple levels.
## Risk Mitigation
### Technical Risks
1. **Complexity of Spell System** - Start with subset of spells
2. **Performance with Many Entities** - Profile early, optimize as needed
3. **AI Balance Issues** - Extensive simulation testing
4. **Save File Compatibility** - Version migration system already planned
### Schedule Risks
1. **Underestimated Content** - Phase E is flexible and incremental
2. **Rules Complexity** - AD&D 1E PDFs available for reference
3. **Testing Overhead** - Maintain test coverage throughout
### Mitigation Strategies
* Implement in priority order (character system first)
* Create playable slice early (Hommlet + Moathouse)
* Incremental testing and integration
* Regular playtesting to validate mechanics
* Use issue tracking for scope management
