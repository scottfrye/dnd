# GitHub Issue Templates

This directory contains templates for creating structured issues in the Temple of Elemental Evil roguelike project.

## Available Templates

### Epic Template (`epic.md`)
Use this template for high-level tracking issues that encompass multiple sub-issues.

**When to use:**
- Tracking major features across multiple issues
- Organizing related work into cohesive units
- Long-term development initiatives

### Save/Load System (`save-load-system.md`)
Template for implementing the game state persistence system.

**Scope:**
- `save_manager.py` enhancements
- `state_exporter.py` implementation  
- `log_writer.py` implementation
- Testing and documentation

**Related Documentation:** [Documentation/save-load-format.md](../../Documentation/save-load-format.md)

### Admin Commands (`admin-commands.md`)
Template for implementing administrative commands for world inspection and debugging.

**Scope:**
- Admin command infrastructure
- World inspection commands
- World manipulation commands
- State export commands
- Debugging commands

**Related Documentation:** [Documentation/admin-commands.md](../../Documentation/admin-commands.md)

## Creating Issues from Templates

### Via GitHub Web Interface

1. Go to the repository's Issues page
2. Click "New Issue"
3. Select the appropriate template
4. Fill in the template fields
5. Submit the issue

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

- `epic` - For epic tracking issues
- `enhancement` - For new features
- `persistence` - For save/load related work
- `admin` - For admin command work
- `documentation` - For documentation tasks
- `testing` - For test-related work

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
