---
name: Phase C - Creatures & Encounters
about: Implement monster and NPC entities for encounters
title: 'Phase C: Creatures & Encounters'
labels: ['enhancement', 'phase-c', 'monsters', 'npcs', 'encounters']
assignees: ''
---

## Phase Description

Implement monster and NPC entities to populate the world with creatures. This includes monster stats, NPC specializations, item system, encounter generation, and enhanced AI behaviors for different creature types.

## Objectives

- [ ] Implement monster entity system
- [ ] Implement NPC entity system
- [ ] Create item system (weapons, armor, equipment)
- [ ] Implement encounter manager for random encounters
- [ ] Enhance NPC AI with specialized behaviors
- [ ] Achieve 85%+ test coverage on all new modules

## Modules to Implement

### 1. src/entities/monster.py
- [ ] Monster entity class
- [ ] Hit dice calculation
- [ ] Special abilities structure
- [ ] Treasure generation
- [ ] AI behavior mapping
- [ ] Monster serialization
- [ ] Tests with 90%+ coverage

### 2. src/entities/npc.py (or extend character.py)
- [ ] NPC specialization from Character
- [ ] AI state tracking
- [ ] Loyalty/morale tracking
- [ ] Faction membership integration
- [ ] Dialogue data references
- [ ] NPC serialization
- [ ] Tests with 90%+ coverage

### 3. src/entities/item.py
- [ ] Item base class
- [ ] Weapon items (damage, type)
- [ ] Armor items (AC, type)
- [ ] Equipment items
- [ ] Treasure items
- [ ] Weight and encumbrance calculations
- [ ] Item serialization
- [ ] Tests with 90%+ coverage

### 4. src/game/encounter_manager.py
- [ ] Random encounter tables
- [ ] Wandering monster generation
- [ ] Encounter scheduling system
- [ ] Distance and detection calculations
- [ ] Integration with event system
- [ ] Tests with 85%+ coverage

### 5. Enhanced NPC AI (extend npc_ai.py)
- [ ] Guard behavior (patrol, investigate, reinforce)
- [ ] Priest behavior (ceremonies, healing, buffs)
- [ ] Leader behavior (command, recruit)
- [ ] Merchant behavior (shop schedule, prices)
- [ ] Commoner behavior (daily routine, flee)
- [ ] Monster-specific behaviors by type

## Deliverables

- [ ] Monster entity implementation with proper AD&D 1E stats
- [ ] NPC entity implementation with faction support
- [ ] Complete item system (weapons, armor, equipment)
- [ ] Encounter generation system
- [ ] Expanded NPC AI behaviors
- [ ] Updated documentation
- [ ] All tests passing with 85%+ coverage

## Success Criteria

- [ ] Can spawn monsters with correct AD&D 1E stats
- [ ] NPCs have faction membership and loyalty
- [ ] Encounters generate appropriately for locations
- [ ] AI behaviors drive realistic NPC actions
- [ ] Items can be equipped and provide correct bonuses
- [ ] Integration with Phase A (character system) and Phase B (factions)
- [ ] 85%+ test coverage on all new modules
- [ ] All pre-commit hooks pass (black, ruff)
- [ ] Documentation is complete and accurate

## Documentation

Related documentation:
- [Next Development Phase Plan](../../Documentation/Temple%20of%20Elemental%20Evil%20-%20Next%20Development%20Phase.md) - Phase C section
- AD&D 1E Monster Manual (resources/)
- Existing npc_ai.py for base AI patterns

Documentation to create/update:
- [ ] Monster system architecture
- [ ] NPC AI behavior guide
- [ ] Item system documentation
- [ ] Encounter generation guide
- [ ] Module docstrings for all new files

## Implementation Notes

### Technical Considerations
- Monsters vs NPCs: Monsters use simpler stat blocks, NPCs use full character system
- Item system should integrate with inventory in character.py
- Encounter tables should be data-driven (JSON/YAML)
- AI behaviors should be composable and reusable
- Performance considerations for many active entities

### Monster Implementation
- Use AD&D 1E stat blocks (HD, AC, attacks, damage)
- Special abilities as extensible system
- Treasure generation based on monster type
- Integration with combat_system.py

### NPC Specialization
- NPCs are characters with AI and faction membership
- Different occupations (guard, priest, merchant, etc.)
- Loyalty affects behavior (may flee, betray, etc.)
- Dialogue hooks for future dialogue system

### Item System
- Basic item types: weapons, armor, equipment, treasure
- Weight for encumbrance calculations
- Equipped vs carried state
- Magical item support (placeholder for Phase F)

### Encounter Generation
- Random encounter tables per location type
- Time-based wandering monster checks
- Distance and detection rules
- Integration with time_system.py

## Timeline

Estimated: 2-3 weeks

Breakdown:
- Week 1: monster.py, npc.py, and item.py implementation
- Week 2: encounter_manager.py and enhanced AI behaviors
- Week 3: Integration testing, documentation, and polish

## Related Issues

This is part of Phase C of the Temple of Elemental Evil implementation plan.

Dependencies:
- Depends on Phase A: Character System (for NPC implementation)
- Depends on Phase B: Faction & Location Systems (for faction membership)
- Builds on existing npc_ai.py

Enables:
- Phase D: Dungeon Crawling (needs monsters for encounters)
- Phase E: Temple Content Population (needs creatures to populate)

## Additional Context

This phase populates the world with living creatures. Monsters provide challenges for players, NPCs provide interaction and world depth, and items provide equipment and rewards. The encounter system ensures dynamic gameplay with wandering monsters.

Key AD&D 1E Considerations:
- Monster stats follow AD&D 1E format (not later editions)
- Hit Dice determine hit points and experience value
- Special abilities are crucial for unique monsters
- Treasure types affect reward distribution
- Morale system affects NPC/monster behavior in combat

Example Monsters for Temple of Elemental Evil:
- Gnolls (basic humanoid monsters)
- Zombies (undead)
- Bugbears (tough humanoid monsters)
- Ogres (large monsters)
- Temple guards (NPC warriors)
- Cultist priests (NPC clerics)

Priority: **HIGH** - Required for combat encounters and world population.
