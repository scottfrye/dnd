---
name: Phase D - Dungeon Crawling & Exploration
about: Enable player exploration and dungeon mechanics
title: 'Phase D: Dungeon Crawling & Exploration'
labels: ['enhancement', 'phase-d', 'exploration', 'dungeon-crawling']
assignees: ''
---

## Phase Description

Implement dungeon crawling and exploration mechanics to enable player movement through the Temple of Elemental Evil. This includes movement, line of sight, traps, secret doors, maps, and basic dialogue system for NPC interaction.

## Objectives

- [ ] Implement dungeon crawling mechanics
- [ ] Create map management system
- [ ] Add exploration actions (search, open doors, etc.)
- [ ] Implement basic dialogue system
- [ ] Enable line of sight and visibility calculations
- [ ] Achieve 80%+ test coverage on all new modules

## Modules to Implement

### 1. src/game/dungeon_crawl.py
- [ ] Movement mechanics with collision detection
- [ ] Line of sight calculations
- [ ] Trap detection and resolution
- [ ] Secret door mechanics
- [ ] Door states (locked, stuck, open, closed)
- [ ] Stair/level transition handling
- [ ] Tests with 85%+ coverage

### 2. src/world/map_manager.py
- [ ] Map data structures (tiles, walls, features)
- [ ] Map generation/loading from data files
- [ ] Pathfinding algorithms (A* or similar)
- [ ] Visibility calculations
- [ ] Fog of war support
- [ ] Tests with 85%+ coverage

### 3. Enhanced Action Handler (extend action_handler.py)
- [ ] Search action (find traps, secret doors)
- [ ] Use item action
- [ ] Open/close door action
- [ ] Pick lock action
- [ ] Disarm trap action
- [ ] Climb, swim actions (if applicable)
- [ ] Rest/camp action

### 4. src/game/dialogue_system.py (basic)
- [ ] Dialogue tree structure
- [ ] NPC conversation state tracking
- [ ] Information gathering mechanics
- [ ] Quest tracking hooks (placeholder)
- [ ] Dialogue branching logic
- [ ] Tests with 80%+ coverage

## Deliverables

- [ ] Full movement system with collision detection
- [ ] Trap and secret door mechanics
- [ ] Map system with pathfinding
- [ ] Line of sight and visibility system
- [ ] Basic dialogue system for NPC interaction
- [ ] Enhanced player action set
- [ ] Updated documentation
- [ ] All tests passing with 80%+ coverage

## Success Criteria

- [ ] Player can explore dungeon maps smoothly
- [ ] Line of sight works correctly (can't see through walls)
- [ ] Traps can be detected and disarmed
- [ ] Secret doors can be found
- [ ] Doors can be opened, closed, locked, and unlocked
- [ ] Basic NPC dialogue functions
- [ ] Maps load from data files
- [ ] Pathfinding works for NPC movement
- [ ] 80%+ test coverage on all new modules
- [ ] All pre-commit hooks pass (black, ruff)
- [ ] Documentation is complete and accurate

## Documentation

Related documentation:
- [Next Development Phase Plan](../../Documentation/Temple%20of%20Elemental%20Evil%20-%20Next%20Development%20Phase.md) - Phase D section
- [UI Architecture](../../Documentation/ui-architecture.md) - For display integration
- AD&D 1E Dungeon Master's Guide (resources/) - For trap and exploration rules

Documentation to create/update:
- [ ] Dungeon crawling mechanics guide
- [ ] Map system architecture
- [ ] Action system documentation (updated)
- [ ] Dialogue system design
- [ ] Module docstrings for all new files

## Implementation Notes

### Technical Considerations
- Map format: Use grid-based tiles (consider JSON/YAML for data)
- Line of sight: Raycasting or shadow casting algorithm
- Pathfinding: A* for NPC movement
- Performance: Optimize visibility calculations for large maps
- Integration with existing terminal_display.py

### Movement System
- Grid-based movement (standard roguelike)
- Movement cost per tile type
- Collision detection with walls and doors
- Diagonal movement rules (AD&D 1E)

### Trap System
- Trap types: pit, arrow, poison, magic
- Detection based on character abilities (Thief skill)
- Disarm mechanics (Thief skill)
- Trap triggers and effects

### Secret Doors
- Hidden until detected
- Detection based on search action
- Elves have bonus to detect secret doors (AD&D 1E)
- Once found, function like normal doors

### Door System
- States: open, closed, locked, stuck
- Actions: open, close, force, pick lock
- STR checks to force stuck/locked doors
- Thief skill to pick locks

### Line of Sight
- Determine what player/NPCs can see
- Blocks vision through walls
- Affects combat (can't attack what you can't see)
- Affects NPC AI (guards investigate what they see)

### Dialogue System (Basic)
- Simple branching dialogue trees
- NPC state affects available dialogue
- Information gathering (rumors, quests)
- Extensible for future quest system

## Timeline

Estimated: 2-3 weeks

Breakdown:
- Week 1: dungeon_crawl.py and map_manager.py core implementation
- Week 2: Enhanced action handler and dialogue_system.py
- Week 3: Integration testing, polish, documentation

## Related Issues

This is part of Phase D of the Temple of Elemental Evil implementation plan.

Dependencies:
- Depends on Phase B: Faction & Location Systems (location infrastructure)
- Depends on Phase C: Creatures & Encounters (NPCs for dialogue)
- Builds on existing action_handler.py
- Integrates with existing terminal_display.py

Enables:
- Phase E: Temple Content Population (exploration needed to experience content)

## Additional Context

This phase transforms the game from a simulation into an explorable world. Players can now navigate dungeons, interact with the environment, and converse with NPCs. This is essential for the roguelike dungeon-crawling experience.

Key AD&D 1E Mechanics:
- Movement rates based on encumbrance
- Elven racial ability to detect secret doors
- Thief skills for finding/disarming traps and picking locks
- Surprise and detection ranges
- Light sources and vision ranges

Example Exploration Scenarios:
- Search a room for traps before entering
- Find a secret door to a hidden treasure room
- Pick a locked door to bypass guards
- Talk to an NPC to learn about the temple layout
- Navigate through a trapped corridor

Integration with Terminal UI:
- Display map with line of sight
- Show available actions in context
- Render dialogue conversations
- Indicate doors, traps, and secret passages

Priority: **MEDIUM** - Required for player exploration but not blocking.
