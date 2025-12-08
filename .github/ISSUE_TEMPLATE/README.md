# GitHub Issue Templates

This directory contains templates for creating structured issues in the Temple of Elemental Evil roguelike project.

## Available Templates

### General Templates

#### Epic Template (`epic.md`)
Use this template for high-level tracking issues that encompass multiple sub-issues.

**When to use:**
- Tracking major features across multiple issues
- Organizing related work into cohesive units
- Long-term development initiatives

#### Feature Request (`feature_request.md`)
Template for suggesting new features or enhancements.

#### Bug Report (`bug_report.md`)
Template for reporting bugs or issues.

### Specific Feature Templates

#### Save/Load System (`save-load-system.md`)
Template for implementing the game state persistence system.

**Scope:**
- `save_manager.py` enhancements
- `state_exporter.py` implementation  
- `log_writer.py` implementation
- Testing and documentation

**Related Documentation:** [Documentation/save-load-format.md](../../Documentation/save-load-format.md)

#### Admin Commands (`admin-commands.md`)
Template for implementing administrative commands for world inspection and debugging.

**Scope:**
- Admin command infrastructure
- World inspection commands
- World manipulation commands
- State export commands
- Debugging commands

**Related Documentation:** [Documentation/admin-commands.md](../../Documentation/admin-commands.md)

### Development Phase Templates

These templates correspond to the major development phases outlined in the [Next Development Phase Plan](../../Documentation/Temple%20of%20Elemental%20Evil%20-%20Next%20Development%20Phase.md).

#### Phase A: Character System Foundation (`phase-a-character-system.md`)
Template for implementing AD&D 1E character creation with classes and races.

**Scope:**
- Character classes (Fighter, Cleric, Magic-User, Thief)
- Races (Human, Elf, Dwarf, Halfling)
- Saving throws system
- Character entity implementation
- Full AD&D 1E stat calculations

**Duration:** 3-4 weeks  
**Priority:** HIGH (blocking)

#### Phase B: Faction & Location Systems (`phase-b-faction-location.md`)
Template for implementing faction management and location system for world simulation.

**Scope:**
- Faction registry and relationship tracking
- Location manager with movement graph
- Faction AI for autonomous behavior
- Temple of Elemental Evil factions (7 factions)
- Territory control mechanics

**Duration:** 3-4 weeks  
**Priority:** HIGH (required for simulation)

#### Phase C: Creatures & Encounters (`phase-c-creatures-encounters.md`)
Template for implementing monster and NPC entities for encounters.

**Scope:**
- Monster entity system
- NPC entity system
- Item system (weapons, armor, equipment)
- Encounter manager
- Enhanced NPC AI behaviors

**Duration:** 2-3 weeks  
**Priority:** HIGH (required for gameplay)

#### Phase D: Dungeon Crawling & Exploration (`phase-d-dungeon-exploration.md`)
Template for enabling player exploration and dungeon mechanics.

**Scope:**
- Movement and collision detection
- Map management system
- Line of sight and visibility
- Trap and secret door mechanics
- Basic dialogue system
- Enhanced player actions

**Duration:** 2-3 weeks  
**Priority:** MEDIUM

#### Phase E: Temple Content Population (`phase-e-content-population.md`)
Template for populating Temple of Elemental Evil locations and NPCs.

**Scope:**
- Hommlet village (20+ locations)
- Moathouse ruins (first dungeon)
- Nulb village
- Temple exterior and dungeon levels
- All named NPCs with stats
- Monster spawns and treasure

**Duration:** 4-6 weeks (incremental)  
**Priority:** MEDIUM (can be incremental)

#### Phase F: Remaining Rules & Polish (`phase-f-rules-polish.md`)
Template for completing remaining AD&D 1E rules and polishing features.

**Scope:**
- Experience and leveling system
- Spell system (initial subset)
- Morale system
- Magic items (basic)
- Enhanced admin commands
- Performance optimization
- Documentation completion

**Duration:** 3-4 weeks  
**Priority:** MEDIUM

## Creating Issues from Templates

### Via GitHub Web Interface

1. Go to the repository's Issues page
2. Click "New Issue"
3. Select the appropriate template
4. Fill in the template fields
5. Submit the issue

### For Development Phases

The six development phase templates (Phase A-F) are designed to be created as issues to track the implementation of the [Next Development Phase Plan](../../Documentation/Temple%20of%20Elemental%20Evil%20-%20Next%20Development%20Phase.md).

**Recommended workflow:**

1. **Create issues for all phases** to establish the backlog
2. **Work phases in order** (A → B → C → D → E → F)
   - Phase A is blocking for most other work
   - Phase B is required for simulation features
   - Phase C depends on A and B
   - Phase E can be done incrementally alongside other phases
3. **Track progress** by checking off items within each phase issue
4. **Link related work** by referencing issue numbers in commits and PRs

**Dependencies:**
- Phase A → Enables Phase C (NPCs need character system)
- Phase B → Enables Phase C, D, E (need locations and factions)
- Phase C → Enables Phase D (need creatures for encounters)
- Phase D → Enhances Phase E (exploration for content)

**Timeline:** 17-24 weeks total for complete core implementation

### For Epic: Persistence & Admin

To properly set up the "Epic: Persistence & Admin" issue with sub-issues:

1. **Create the sub-issues first:**
   - Create "Implement Save/Load System" issue using `save-load-system.md` template
   - Create "Implement Admin Commands System" issue using `admin-commands.md` template
   - Note the issue numbers (e.g., #42, #43)

2. **Create or update the epic issue:**
   - Use the `epic.md` template (or update existing epic)
   - Link the sub-issues by their numbers in the "Sub-Issues" section
   - Link the documentation in the "Documentation" section

3. **Example Epic Issue Content:**

```markdown
---
name: Epic: Persistence & Admin
about: Tracking save/load system and admin commands implementation
title: 'Epic: Persistence & Admin'
labels: ['epic', 'persistence', 'admin']
assignees: ''
---

## Epic Description

This epic tracks the implementation of game state persistence (save/load system) and administrative commands for world inspection and debugging. These features are essential for testing, demonstrating the simulation system, and providing a complete player experience.

## Objectives

- [ ] Implement robust save/load system with multiple formats
- [ ] Implement human-readable state export capabilities
- [ ] Implement comprehensive admin command system
- [ ] Create detailed documentation for save format and admin commands

## Sub-Issues

This epic tracks the following sub-issues:

- [ ] #42 - Implement Save/Load System
- [ ] #43 - Implement Admin Commands System

## Acceptance Criteria

- [ ] Sub-issues for persistence and admin exist and are linked
- [ ] Documentation for save/load format and admin commands
- [ ] All sub-issues are completed
- [ ] Tests are passing for all new functionality
- [ ] Code review completed

## Documentation

Related documentation:

- [Save/Load Format Documentation](../Documentation/save-load-format.md)
- [Admin Commands Reference](../Documentation/admin-commands.md)

## Notes

Part of Phase 5 of the implementation plan. These features enable both player convenience (save/load) and developer/tester productivity (admin commands). The admin commands are also valuable for demonstrating the autonomous simulation capabilities.
```

## Linking Issues

### In Issue Descriptions
```markdown
Related to #42
Depends on #43
Blocks #44
```

### In Commit Messages
```
git commit -m "Add save manager tests (#42)"
```

### In Pull Requests
```markdown
Closes #42
Fixes #43
Resolves #44
```

## Labels

Recommended labels for these issues:

### General Labels
- `epic` - For epic tracking issues
- `enhancement` - For new features
- `bug` - For bug reports
- `documentation` - For documentation tasks
- `testing` - For test-related work

### Domain-Specific Labels
- `persistence` - For save/load related work
- `admin` - For admin command work
- `rules` - For AD&D 1E rules implementation
- `character-system` - For character creation and management
- `faction-system` - For faction and territory management
- `world-simulation` - For world simulation features
- `monsters` - For monster implementation
- `npcs` - For NPC implementation
- `encounters` - For encounter generation
- `exploration` - For dungeon crawling features
- `dungeon-crawling` - For exploration mechanics
- `content` - For game content (locations, NPCs, etc.)
- `temple-of-elemental-evil` - For ToEE-specific content
- `spells` - For spell system
- `magic-items` - For magic item system

### Phase Labels
- `phase-a` - Phase A: Character System Foundation
- `phase-b` - Phase B: Faction & Location Systems
- `phase-c` - Phase C: Creatures & Encounters
- `phase-d` - Phase D: Dungeon Crawling & Exploration
- `phase-e` - Phase E: Temple Content Population
- `phase-f` - Phase F: Remaining Rules & Polish

### Priority Labels (Recommended)
- `priority-high` - Blocking or critical work
- `priority-medium` - Important but not blocking
- `priority-low` - Nice to have, can be deferred

## Checklist Format

Use GitHub's task list format for tracking progress:

```markdown
- [ ] Incomplete task
- [x] Completed task
```

These automatically update in the GitHub UI and provide progress tracking.

## Best Practices

1. **Be Specific**: Fill in all template sections with detailed information
2. **Link Documentation**: Always link to relevant documentation
3. **Cross-Reference**: Link related issues and PRs
4. **Update Regularly**: Check off items as they're completed
5. **Use Labels**: Apply appropriate labels for discoverability
6. **Assign Owners**: Assign issues to team members
7. **Add Milestones**: Group issues into milestones for release planning

## Contributing

When creating new issue templates:

1. Follow the YAML front matter format
2. Include clear acceptance criteria
3. Link to relevant documentation
4. Provide examples where helpful
5. Keep templates focused and actionable

## Questions?

For questions about issue templates or the issue tracking process, see [CONTRIBUTING.md](../../CONTRIBUTING.md) or open a discussion.
