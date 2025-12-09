# Quick Start: Creating Phase Issues

## ✅ What's Ready

Three solutions have been implemented to create GitHub issues from the phase templates:

1. **`scripts/create_phase_issues.py`** - Python script using GitHub API
2. **`.github/workflows/create-phase-issues.yml`** - GitHub Actions workflow
3. **`scripts/README-create-issues.md`** - Comprehensive documentation

## 🚀 Quickest Method (Recommended)

### Using GitHub Actions Workflow

1. Go to: https://github.com/scottfrye/dnd/actions
2. Click on "Create Phase Issues" workflow in the left sidebar
3. Click "Run workflow" button (top right)
4. **First time:** Leave "dry_run" as `true` and click "Run workflow"
   - This previews what will be created without actually creating issues
   - Review the output to ensure everything looks correct
5. **Second time:** Change "dry_run" to `false` and click "Run workflow"
   - This creates the actual GitHub issues

### Result

You will have 6 new GitHub issues created:
- Phase A: Character System Foundation
- Phase B: Faction & Location Systems
- Phase C: Creatures & Encounters  
- Phase D: Dungeon Crawling & Exploration
- Phase E: Temple Content Population
- Phase F: Remaining Rules & Polish

Each issue will have:
- Proper title
- Appropriate labels (enhancement, phase-*, etc.)
- Complete description with objectives, modules, deliverables
- All content from the template files

## 📝 Alternative: Local Script

If you prefer to run locally:

```bash
# Install dependency
pip install PyGithub

# Set your GitHub token
export GITHUB_TOKEN=your_token_here

# Dry run first (safe)
python scripts/create_phase_issues.py --dry-run

# Create issues
python scripts/create_phase_issues.py
```

## 📚 Full Documentation

See `scripts/README-create-issues.md` for complete documentation including:
- Detailed instructions
- Troubleshooting guide
- Token setup
- Error handling

## ⚠️ Important Note

This solution creates the automation to generate issues but does not create them automatically. This is because:
1. Creating issues requires explicit GitHub credentials
2. Issue creation should be a deliberate action by the repository owner
3. The dry-run mode allows verification before creating issues

The workflow and script are ready to use immediately and will create all 6 phase issues when executed.
