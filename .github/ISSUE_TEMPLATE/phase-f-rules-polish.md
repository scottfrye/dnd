---
name: Phase F - Remaining Rules & Polish
about: Complete remaining AD&D 1E rules and polish features
title: 'Phase F: Remaining Rules & Polish'
labels: ['enhancement', 'phase-f', 'rules', 'polish', 'spells', 'magic-items']
assignees: ''
---

## Phase Description

Complete the remaining AD&D 1E rules modules and polish the game features. This includes experience and leveling, spell system, morale, magic items, enhanced admin commands, and overall game polish.

## Objectives

- [ ] Implement experience and leveling system
- [ ] Create spell system with memorization and casting
- [ ] Implement morale system
- [ ] Add basic magic item system
- [ ] Enhance admin commands
- [ ] Polish and optimize all features
- [ ] Achieve 85%+ test coverage on all new modules

## Modules to Implement

### 1. src/rules/experience.py
- [ ] XP calculation for monster defeats
- [ ] XP calculation for treasure
- [ ] Level advancement mechanics
- [ ] Training requirements
- [ ] Prime requisite XP bonuses
- [ ] XP distribution for party
- [ ] Tests with 90%+ coverage

### 2. src/rules/spells.py (Initial Subset)
- [ ] Spell base class and structure
- [ ] Spell effect system
- [ ] Memorization mechanics
- [ ] Casting mechanics and components
- [ ] Spell save throws
- [ ] Cleric spells (levels 1-3)
- [ ] Magic-User spells (levels 1-3)
- [ ] Tests with 85%+ coverage

### 3. src/rules/morale.py
- [ ] Morale score system
- [ ] Morale check triggers
- [ ] 2d6 resolution with modifiers
- [ ] Morale check results (flee, surrender, fight)
- [ ] Leadership bonuses
- [ ] Tests with 90%+ coverage

### 4. src/rules/magic_items.py (Basic)
- [ ] Magic item base class
- [ ] Magic weapons (+1, +2, etc.)
- [ ] Magic armor
- [ ] Potion effects system
- [ ] Scroll handling
- [ ] Item identification mechanics
- [ ] Tests with 85%+ coverage

## Polish Features

### Enhanced Admin Commands
- [ ] Extend admin command system
- [ ] Inspect entity details command
- [ ] Modify entity stats command
- [ ] Spawn entity command
- [ ] Teleport command
- [ ] Time manipulation commands
- [ ] Faction relationship commands
- [ ] Save state inspection

### State Export Enhancements
- [ ] Implement state_exporter.py
- [ ] Human-readable world state reports
- [ ] Faction relationship reports
- [ ] Entity roster reports
- [ ] Combat statistics reports

### Combat Log Writer
- [ ] Implement log_writer.py
- [ ] Detailed combat logging
- [ ] Turn-by-turn action logs
- [ ] Damage and effect tracking
- [ ] Log file management

### Performance Optimization
- [ ] Profile performance bottlenecks
- [ ] Optimize entity updates
- [ ] Optimize pathfinding
- [ ] Optimize visibility calculations
- [ ] Memory usage optimization

### Documentation Completion
- [ ] Complete all module docstrings
- [ ] User manual/gameplay guide
- [ ] Developer documentation
- [ ] API reference documentation
- [ ] Tutorial system or help screens

### UI/UX Polish
- [ ] Improve terminal display clarity
- [ ] Add color coding for clarity
- [ ] Better error messages
- [ ] Loading indicators
- [ ] Progress feedback

## Deliverables

- [ ] Complete core rules modules (XP, spells, morale, magic items)
- [ ] Basic spellcasting system functional
- [ ] Magic item effects working
- [ ] Polished admin tools
- [ ] Human-readable state exports
- [ ] Combat log system
- [ ] Complete documentation
- [ ] Performance optimizations
- [ ] All tests passing with 85%+ coverage

## Success Criteria

- [ ] Characters can gain XP and level up correctly
- [ ] Basic spellcasting works (memorize, cast, effects)
- [ ] Morale system functions and affects combat
- [ ] Magic items have proper effects on characters
- [ ] Admin commands provide useful debugging tools
- [ ] State exports are readable and informative
- [ ] Combat logs capture all relevant details
- [ ] Performance is acceptable with many entities
- [ ] 85%+ test coverage on all modules
- [ ] All pre-commit hooks pass (black, ruff)
- [ ] Documentation is complete and accurate
- [ ] Tutorial or help system available

## Documentation

Related documentation:
- [Next Development Phase Plan](../../Documentation/Temple%20of%20Elemental%20Evil%20-%20Next%20Development%20Phase.md) - Phase F section
- [Admin Commands Reference](../../Documentation/admin-commands.md)
- [Save/Load Format](../../Documentation/save-load-format.md)
- AD&D 1E rulebooks (resources/)

Documentation to create/update:
- [ ] Experience and leveling guide
- [ ] Spell system documentation
- [ ] Magic item reference
- [ ] Admin commands reference (update)
- [ ] Gameplay guide/manual
- [ ] Developer guide
- [ ] Module docstrings for all new files

## Implementation Notes

### Technical Considerations
- Spell effects need flexible system (many different effects)
- XP calculation must handle edge cases (level limits, etc.)
- Magic items interact with many systems
- Performance optimization requires profiling first
- Admin commands need security considerations

### Experience System
- XP from monsters based on HD and special abilities
- XP from treasure (1 GP = 1 XP typically)
- Prime requisite bonuses (e.g., +10% for high INT on Magic-User)
- Level advancement triggers
- Training time and cost requirements

### Spell System (Initial Subset)
Focus on essential spells:
- **Cleric 1st**: Cure Light Wounds, Protection from Evil, Detect Magic
- **Cleric 2nd**: Hold Person, Silence 15' Radius, Spiritual Hammer
- **Cleric 3rd**: Cure Disease, Dispel Magic, Prayer
- **Magic-User 1st**: Magic Missile, Sleep, Shield, Charm Person
- **Magic-User 2nd**: Web, Mirror Image, Invisibility
- **Magic-User 3rd**: Fireball, Lightning Bolt, Haste

More spells can be added incrementally.

### Morale System
- Morale scores (2-12 typical)
- Check triggers: first casualty, 50% losses, leader killed
- 2d6 roll vs morale score
- Results: pass (keep fighting), fail (flee or surrender)
- Modifiers: leadership, situation, creature type

### Magic Items (Basic Set)
- +1 to +3 weapons and armor
- Potions: healing, strength, etc.
- Scrolls with spells
- Identification required for unknown items

### Admin Commands Examples
```
/inspect <entity_id>
/modify <entity_id> <stat> <value>
/spawn <entity_type> <location>
/teleport <entity_id> <location>
/time advance <amount>
/faction <faction1> <faction2> <relationship>
/save_state <filename>
```

## Timeline

Estimated: 3-4 weeks

Breakdown:
- Week 1: experience.py and morale.py implementation
- Week 2: spells.py (subset) and magic_items.py implementation
- Week 3: Admin commands, state export, combat log
- Week 4: Performance optimization, documentation, polish

## Related Issues

This is part of Phase F (final phase) of the Temple of Elemental Evil implementation plan.

Dependencies:
- Depends on Phase A: Character System (for leveling)
- Depends on Phase C: Creatures & Encounters (for morale, XP)
- Depends on Phase D: Dungeon Crawling (for complete gameplay)
- Builds on all previous phases

This phase completes:
- All core AD&D 1E rules needed for gameplay
- Administrative and debugging tools
- Documentation and polish
- Performance optimization

## Additional Context

This is the final phase that completes the core implementation. After this phase, the game should be fully playable with all essential AD&D 1E mechanics. Additional content, spells, and features can be added incrementally beyond this phase.

### Spell System Scope
Starting with a subset of ~20 spells across 6 spell levels (3 each for Cleric and Magic-User). This covers the most commonly used and mechanically important spells. Additional spells can be added as time permits.

### Magic Item Scope
Focus on basic +1/+2/+3 weapons and armor, healing potions, and spell scrolls. More exotic items (rings, wands, etc.) can be added later.

### Polish vs New Features
This phase prioritizes:
1. Completing essential rules (XP, morale)
2. Basic spellcasting functionality
3. Tools for debugging and demonstration
4. Documentation for users and developers
5. Performance for smooth gameplay

New features beyond the plan should be deferred to post-launch.

### Performance Targets
- Support 100+ active entities without lag
- Map rendering < 50ms
- Turn processing < 100ms
- Save/load < 2 seconds for typical game

Priority: **MEDIUM** - Important for complete experience but can be done after earlier phases establish core gameplay.

## Success Metrics

### Quantitative
- 85%+ test coverage overall
- All linters passing
- < 100ms average turn time
- 0 critical bugs

### Qualitative
- Feels like AD&D 1E
- Intuitive admin commands
- Readable state exports
- Clear documentation
- Smooth gameplay experience
