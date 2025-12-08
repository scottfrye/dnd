---
name: Phase A - Character System Foundation
about: Implement AD&D 1E character creation with classes and races
title: 'Phase A: Character System Foundation'
labels: ['enhancement', 'phase-a', 'character-system', 'rules']
assignees: ''
---

## Phase Description

Implement character creation system with AD&D 1E classes and races. This is the foundation for playable characters and includes ability scores, character classes, races, saving throws, and complete character entity representation.

## Objectives

- [ ] Implement character classes (Fighter, Cleric, Magic-User, Thief)
- [ ] Implement races (Human, Elf, Dwarf, Halfling)
- [ ] Implement saving throws system
- [ ] Create complete Character entity
- [ ] Integrate with existing ability scores and combat systems
- [ ] Achieve 90%+ test coverage on all new modules

## Modules to Implement

### 1. src/rules/character_classes.py
- [ ] Base Character class framework
- [ ] Fighter class with THAC0 and hit dice
- [ ] Cleric class with THAC0 and hit dice
- [ ] Magic-User class with THAC0 and hit dice
- [ ] Thief class with THAC0 and hit dice
- [ ] Level progression tables
- [ ] Class restrictions (armor/weapons)
- [ ] Multi-class and dual-class support structure
- [ ] Tests with 90%+ coverage

### 2. src/rules/races.py
- [ ] Human race implementation
- [ ] Elf race with sub-race support (High Elf, etc.)
- [ ] Dwarf race with sub-race support (Hill Dwarf, etc.)
- [ ] Halfling race implementation
- [ ] Ability score adjustments per race
- [ ] Level limits per class
- [ ] Special abilities (infravision, detect slopes)
- [ ] Language lists
- [ ] Tests with 90%+ coverage

### 3. src/rules/saving_throws.py
- [ ] Five saving throw categories per AD&D 1E
- [ ] Saving throw tables for all classes
- [ ] Racial bonuses integration
- [ ] Saving throw resolution function
- [ ] Tests with 90%+ coverage

### 4. src/entities/character.py
- [ ] Complete Character entity class
- [ ] Integration with AbilityScores
- [ ] Integration with class and race systems
- [ ] Inventory system structure
- [ ] HP/AC/THAC0 calculation methods
- [ ] Character serialization support
- [ ] Tests with 90%+ coverage

## Deliverables

- [ ] Character creation system functional
- [ ] Full character sheet representation
- [ ] Character serialization for save/load
- [ ] Character stat calculations per AD&D 1E rules
- [ ] Updated documentation for new modules
- [ ] All tests passing with 90%+ coverage

## Success Criteria

- [ ] Can create characters with any class/race combination
- [ ] Character stats calculate correctly per AD&D 1E rules
- [ ] Characters persist through save/load cycles
- [ ] Integration with existing combat system works
- [ ] 90%+ test coverage on all new modules
- [ ] All pre-commit hooks pass (black, ruff)
- [ ] Documentation is complete and accurate

## Documentation

Related documentation:
- [Next Development Phase Plan](../../Documentation/Temple%20of%20Elemental%20Evil%20-%20Next%20Development%20Phase.md) - Phase A section
- AD&D 1E rulebooks in resources/ directory

Documentation to create/update:
- [ ] Module docstrings for all new files
- [ ] API documentation for character creation
- [ ] Character system architecture document
- [ ] Examples for creating characters

## Implementation Notes

### Technical Considerations
- Use dataclasses for character data structures
- Full type hints (Python 3.12+ style)
- Follow existing code patterns from abilities.py and combat_system.py
- Ensure serialization compatibility with existing save_manager.py

### AD&D 1E Reference
- Reference Player's Handbook for class/race mechanics
- Use Dungeon Master's Guide for tables and rules
- Ensure accuracy to AD&D 1E (not later editions)

### Dependencies
- Builds on existing abilities.py module
- Integrates with combat_system.py for THAC0
- Uses dice.py for random generation
- Extends entity.py base classes

## Timeline

Estimated: 3-4 weeks

Breakdown:
- Week 1: character_classes.py implementation and tests
- Week 2: races.py and saving_throws.py implementation and tests
- Week 3: character.py entity implementation and tests
- Week 4: Integration, documentation, and polish

## Related Issues

This is part of Phase A of the Temple of Elemental Evil implementation plan.

Dependencies:
- Depends on existing abilities.py (already complete)
- Depends on existing combat_system.py (already complete)

Enables:
- Phase B: Faction & Location Systems (will need character entities)
- Phase C: Creatures & Encounters (NPC characters)

## Additional Context

This is the first major phase of the Temple of Elemental Evil development plan. It establishes the foundation for creating playable characters and NPCs. Without this system, the game cannot have meaningful player representation or complex NPC interactions.

Priority: **HIGH** - This is a blocking requirement for meaningful gameplay.
