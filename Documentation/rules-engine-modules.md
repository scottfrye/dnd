# Rules Engine Module Development Tracker

This document tracks the planned development of individual modules for the AD&D 1E rules engine. Each module represents a distinct piece of functionality that should be implemented, tested, and documented.

## Module Status Overview

| Module | Status | Priority | Complexity | Target Coverage | Dependencies |
|--------|--------|----------|------------|-----------------|--------------|
| abilities | ✅ Complete | High | Medium | 95% | None |
| combat_system | ✅ Complete | High | High | 95% | abilities, utils.dice |
| character_classes | 📋 Planned | High | High | 90% | abilities, combat_system |
| races | 📋 Planned | High | Medium | 90% | abilities |
| saving_throws | 📋 Planned | High | Medium | 90% | character_classes, races |
| experience | 📋 Planned | Medium | Medium | 90% | character_classes |
| spells | 📋 Planned | Medium | Very High | 85% | abilities, character_classes, saving_throws |
| magic_items | 📋 Planned | Low | High | 85% | abilities, spells |
| morale | 📋 Planned | Low | Low | 90% | None |

Legend:
- ✅ Complete: Module implemented, tested, and documented
- 🚧 In Progress: Currently being developed
- 📋 Planned: Scheduled for future development
- ⏸️ Blocked: Waiting on dependencies or decisions

## Completed Modules

### Module: abilities.py

**Status**: ✅ Complete  
**Completed**: 2025-12-06  
**Current Coverage**: 92%  
**Target Coverage**: 95%

#### Description
Implements the six primary ability scores and their modifiers per AD&D 1E Player's Handbook.

#### Acceptance Criteria
- [x] AbilityScores dataclass implemented
- [x] Strength modifier functions (hit, damage)
- [x] Dexterity modifier functions (AC, initiative)
- [x] Constitution HP modifier function
- [x] Validation for ability score ranges
- [x] Support for exceptional strength (18/xx) - Partial
- [x] Support for scores 1-25
- [x] Comprehensive unit tests
- [x] Module docstring
- [x] Function docstrings with examples
- [x] Exported in __init__.py

#### Known Gaps
- Missing tests for some edge cases (5% coverage gap)
- Exceptional strength for fighters (18/01-18/00) not fully implemented
- Intelligence, Wisdom, and Charisma modifiers not yet implemented (languages, spell bonus, reaction adjustments, etc.)

#### Future Enhancements
- Add Intelligence: languages, max spell level, chance to learn spell
- Add Wisdom: magical attack adjustment, bonus spells for clerics
- Add Charisma: reaction adjustment, max henchmen, loyalty base

---

### Module: combat_system.py

**Status**: ✅ Complete  
**Completed**: 2025-12-06  
**Current Coverage**: 95%  
**Target Coverage**: 95%

#### Description
Implements THAC0-based combat mechanics from AD&D 1E with support for four class groups.

#### Acceptance Criteria
- [x] THAC0 tables for all class groups
- [x] get_thac0() function for class/level lookup
- [x] calculate_target_number() for hit determination
- [x] CombatStats dataclass for attacker/defender
- [x] AttackResult dataclass for results
- [x] resolve_attack() with full mechanics
- [x] resolve_attack_simple() convenience function
- [x] Natural 20 always hits
- [x] Natural 1 always misses
- [x] Support for hit modifiers
- [x] Deterministic testing support (roll parameter)
- [x] DiceRoller integration
- [x] Comprehensive unit tests
- [x] Module docstring
- [x] Function docstrings
- [x] Exported in __init__.py

#### Known Gaps
- No support for special attack types (grappling, charging, etc.)
- No support for weapon vs armor type adjustments
- No support for rear/flank attacks
- No support for multiple attacks per round
- No damage calculation (only hit/miss)

#### Future Enhancements
- Add damage resolution with weapon dice
- Add special attack types (charge, grapple, disarm)
- Add positional modifiers (rear, flank, higher ground)
- Add weapon type vs armor type matrix
- Add multiple attacks for high-level fighters
- Add two-weapon fighting penalties

---

## Planned Modules

### Module: character_classes.py

**Status**: 📋 Planned  
**Priority**: High  
**Estimated Complexity**: High  
**Target Coverage**: 90%  
**Dependencies**: abilities, combat_system

#### Description
Implement all AD&D 1E character classes with their progression tables, abilities, and restrictions.

#### Proposed Classes
- Fighter (base warrior)
- Ranger (wilderness warrior with limited spells)
- Paladin (holy warrior with limited spells)
- Cleric (divine spellcaster)
- Druid (nature divine spellcaster)
- Magic-User (arcane spellcaster)
- Illusionist (illusion specialist)
- Thief (rogue with skills)
- Assassin (evil rogue with poison)
- Monk (unarmed martial artist)

#### Acceptance Criteria
- [ ] Base Character class or interface
- [ ] Fighter class with level progression
- [ ] Cleric class with level progression
- [ ] Magic-User class with level progression
- [ ] Thief class with level progression
- [ ] Ranger class with special abilities
- [ ] Paladin class with special abilities
- [ ] Druid class with special abilities
- [ ] Illusionist class with special abilities
- [ ] Assassin class with special abilities
- [ ] Monk class with special abilities
- [ ] Hit dice tables per class
- [ ] THAC0 integration
- [ ] Saving throw integration (depends on saving_throws.py)
- [ ] Spell progression tables (spellcasters)
- [ ] Class ability restrictions (armor, weapons)
- [ ] Multi-class rules
- [ ] Dual-class rules
- [ ] Level limit enforcement (with races)
- [ ] Unit tests for each class
- [ ] Module docstring
- [ ] Class docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- Use class hierarchy or composition?
- How to represent multi-class characters?
- Integration with race level limits
- Spell progression representation
- Special ability modeling

#### Estimated Effort
- Development: 40-60 hours
- Testing: 20-30 hours
- Documentation: 10-15 hours
- **Total**: 70-105 hours

---

### Module: races.py

**Status**: 📋 Planned  
**Priority**: High  
**Estimated Complexity**: Medium  
**Target Coverage**: 90%  
**Dependencies**: abilities

#### Description
Implement all AD&D 1E player character races with their modifiers, abilities, and restrictions.

#### Proposed Races
- Human
- Elf (including sub-races: High, Grey, Wood, Dark)
- Dwarf (including Hill, Mountain)
- Halfling (including Hairfoot, Tallfellow, Stout)
- Gnome
- Half-Elf
- Half-Orc

#### Acceptance Criteria
- [ ] Base Race class or interface
- [ ] Human race implementation
- [ ] Elf race with sub-races
- [ ] Dwarf race with sub-races
- [ ] Halfling race with sub-races
- [ ] Gnome race implementation
- [ ] Half-Elf race implementation
- [ ] Half-Orc race implementation
- [ ] Ability score adjustments per race
- [ ] Level limits by class per race
- [ ] Special abilities (infravision, resistance, etc.)
- [ ] Language lists
- [ ] Height/weight tables
- [ ] Age categories
- [ ] Class restrictions
- [ ] Multi-class availability
- [ ] Unit tests for each race
- [ ] Module docstring
- [ ] Race docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- How to model sub-races?
- Integration with character_classes for level limits
- Handling racial ability score requirements
- Modeling special senses (infravision, detect slopes)

#### Estimated Effort
- Development: 25-35 hours
- Testing: 15-20 hours
- Documentation: 8-12 hours
- **Total**: 48-67 hours

---

### Module: saving_throws.py

**Status**: 📋 Planned  
**Priority**: High  
**Estimated Complexity**: Medium  
**Target Coverage**: 90%  
**Dependencies**: character_classes, races

#### Description
Implement the five saving throw categories with class/level tables and modifiers.

#### Saving Throw Categories
1. Paralyzation, Poison, Death Magic
2. Petrification, Polymorph
3. Rod, Staff, Wand
4. Breath Weapon
5. Spell

#### Acceptance Criteria
- [ ] Saving throw tables for all classes
- [ ] get_saving_throw() function by category/class/level
- [ ] Racial bonuses (dwarf vs poison/magic, halfling vs wands, etc.)
- [ ] Magic item bonuses
- [ ] Situational modifiers
- [ ] Save resolution function
- [ ] Critical success/failure handling
- [ ] Unit tests for all saving throw types
- [ ] Module docstring
- [ ] Function docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- How to handle class-specific save progressions
- Modeling save bonuses from multiple sources
- Integration with spells and effects

#### Estimated Effort
- Development: 20-30 hours
- Testing: 12-18 hours
- Documentation: 6-10 hours
- **Total**: 38-58 hours

---

### Module: experience.py

**Status**: 📋 Planned  
**Priority**: Medium  
**Estimated Complexity**: Medium  
**Target Coverage**: 90%  
**Dependencies**: character_classes

#### Description
Implement XP awards and level advancement mechanics.

#### Acceptance Criteria
- [ ] Monster XP calculation by HD
- [ ] Treasure XP calculation
- [ ] XP awards for special accomplishments
- [ ] Level advancement tables per class
- [ ] XP requirements per level
- [ ] Multi-class XP division
- [ ] Training time calculation
- [ ] Training cost calculation
- [ ] Level-up HP roll
- [ ] Level-up ability checks
- [ ] Unit tests for XP calculations
- [ ] Module docstring
- [ ] Function docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- How to track XP sources
- Integration with character_classes
- Handling XP penalties (level drain, death)
- Prime requisite bonuses

#### Estimated Effort
- Development: 18-25 hours
- Testing: 10-15 hours
- Documentation: 5-8 hours
- **Total**: 33-48 hours

---

### Module: spells.py

**Status**: 📋 Planned  
**Priority**: Medium  
**Estimated Complexity**: Very High  
**Target Coverage**: 85%  
**Dependencies**: abilities, character_classes, saving_throws

#### Description
Implement spell definitions and mechanics for clerics and magic-users.

#### Spell Classes
- Cleric spells (levels 1-7)
- Magic-User spells (levels 1-9)
- Illusionist spells (levels 1-7)
- Druid spells (levels 1-7)

#### Acceptance Criteria
- [ ] Base Spell class or dataclass
- [ ] Spell effect system
- [ ] Spell memorization mechanics
- [ ] Spell casting mechanics
- [ ] Spell level organization
- [ ] Component tracking (V, S, M)
- [ ] Casting time
- [ ] Range calculation
- [ ] Area of effect
- [ ] Duration tracking
- [ ] Saving throw integration
- [ ] Spell resistance
- [ ] Counter-spelling
- [ ] Cleric spell list (sample)
- [ ] Magic-User spell list (sample)
- [ ] Unit tests for spell mechanics
- [ ] Module docstring
- [ ] Class/function docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- Spell effect representation (damage, buffs, debuffs, etc.)
- How to model spell targets
- Spell area of effect shapes
- Duration tracking system
- Integration with combat system
- Concentration mechanics (if applicable)

#### Estimated Effort
- Development: 60-90 hours
- Testing: 30-45 hours
- Documentation: 15-20 hours
- **Total**: 105-155 hours

---

### Module: magic_items.py

**Status**: 📋 Planned  
**Priority**: Low  
**Estimated Complexity**: High  
**Target Coverage**: 85%  
**Dependencies**: abilities, spells

#### Description
Implement magic item definitions, effects, and identification mechanics.

#### Item Categories
- Magic weapons (+1 to +5, special abilities)
- Magic armor (+1 to +5, special properties)
- Potions
- Scrolls (spell scrolls, protection scrolls)
- Rings
- Wands, Rods, Staves
- Miscellaneous magic items
- Artifacts and Relics

#### Acceptance Criteria
- [ ] Base MagicItem class
- [ ] Magic weapon implementation
- [ ] Magic armor implementation
- [ ] Potion effects
- [ ] Scroll effects
- [ ] Ring effects
- [ ] Wand/Rod/Staff effects
- [ ] Cursed item mechanics
- [ ] Identification system
- [ ] Charges tracking
- [ ] Activation mechanics
- [ ] Sample magic items
- [ ] Unit tests for item mechanics
- [ ] Module docstring
- [ ] Class/function docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- How to represent item powers
- Curse mechanics
- Identification methods
- Charge depletion
- Item creation (for future)

#### Estimated Effort
- Development: 40-55 hours
- Testing: 20-28 hours
- Documentation: 10-14 hours
- **Total**: 70-97 hours

---

### Module: morale.py

**Status**: 📋 Planned  
**Priority**: Low  
**Estimated Complexity**: Low  
**Target Coverage**: 90%  
**Dependencies**: None

#### Description
Implement morale check mechanics for NPCs and monsters.

#### Acceptance Criteria
- [ ] Morale score definition (2-12 scale)
- [ ] Morale check triggers (casualties, leader death, etc.)
- [ ] Morale check resolution (2d6)
- [ ] Morale modifiers (leadership, magic, situation)
- [ ] Morale results (stand, flee, surrender)
- [ ] NPC loyalty checks (for henchmen)
- [ ] Unit tests for morale mechanics
- [ ] Module docstring
- [ ] Function docstrings
- [ ] Exported in __init__.py

#### Design Considerations
- Integration with combat system
- When to trigger automatic morale checks
- Morale recovery mechanics
- Elite/fearless units

#### Estimated Effort
- Development: 10-15 hours
- Testing: 8-12 hours
- Documentation: 4-6 hours
- **Total**: 22-33 hours

---

## Development Workflow

### For Each New Module

1. **Planning Phase**
   - Review this tracker document
   - Verify dependencies are complete
   - Create detailed design notes
   - Identify AD&D 1E source material to reference

2. **Implementation Phase**
   - Create module file in `src/rules/`
   - Write module docstring with overview
   - Implement core functionality
   - Add comprehensive docstrings
   - Add type hints throughout

3. **Testing Phase**
   - Create test file in `tests/`
   - Write unit tests for all public functions
   - Aim for target coverage percentage
   - Test edge cases and error conditions
   - Test integration with dependencies

4. **Documentation Phase**
   - Update this tracker (move to Complete section)
   - Add module documentation to src/rules/README.md
   - Add usage examples
   - Update __init__.py exports

5. **Review Phase**
   - Run linters (black, ruff)
   - Check test coverage
   - Review code for clarity
   - Validate against AD&D 1E sources

## Summary Statistics

### Completed Work
- **Modules Complete**: 2
- **Test Coverage**: 93.5% (abilities: 92%, combat_system: 95%)
- **Total Functions**: 15+ public functions
- **Total Classes**: 3 dataclasses

### Planned Work
- **Modules Remaining**: 7
- **Estimated Total Effort**: 386-563 hours
- **High Priority Modules**: 3 (character_classes, races, saving_throws)
- **Medium Priority Modules**: 2 (experience, spells)
- **Low Priority Modules**: 2 (magic_items, morale)

### Coverage Goals
- **Overall Target**: 90% for all rules modules
- **Current Status**: 93.5% (above target)
- **Critical Modules**: Targeting 95% (abilities, combat_system)

---

**Last Updated**: 2025-12-06  
**Document Version**: 1.0  
**Status**: Living document - update as modules progress
