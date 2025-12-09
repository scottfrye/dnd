# Creating GitHub Issues from Phase Templates

This directory contains a script and workflow to automatically create GitHub issues from the phase template files located in `.github/ISSUE_TEMPLATE/`.

## Overview

The issue templates in `.github/ISSUE_TEMPLATE/` define the various development phases:
- Phase A: Character System Foundation
- Phase B: Faction & Location Systems
- Phase C: Creatures & Encounters
- Phase D: Dungeon Crawling & Exploration
- Phase E: Temple Content Population
- Phase F: Remaining Rules & Polish

This automation creates actual GitHub issues from these templates, making it easy to track progress on each phase in the project backlog.

## Method 1: GitHub Actions Workflow (Recommended)

The easiest way to create the issues is using the GitHub Actions workflow.

### Steps:

1. Go to the **Actions** tab in the GitHub repository
2. Select the **"Create Phase Issues"** workflow from the left sidebar
3. Click **"Run workflow"** button
4. Choose whether to run in dry-run mode:
   - **dry_run = true**: Preview what would be created (default, safe)
   - **dry_run = false**: Actually create the issues
5. Click **"Run workflow"** to start

### First Run (Dry Run):
```
Run workflow → dry_run: true → Run workflow
```

Review the output to ensure everything looks correct.

### Second Run (Create Issues):
```
Run workflow → dry_run: false → Run workflow
```

This will create the actual GitHub issues.

## Method 2: Manual Script Execution

If you prefer to run the script locally or need more control:

## Requirements

The script is designed to work with GitHub issue templates that follow these conventions:
- YAML frontmatter enclosed in `---` markers
- Unix line endings (`\n`)
- Standard key: value format
- Labels in array format: `['label1', 'label2']`

The script works perfectly with the phase templates in this repository. For more complex YAML parsing needs, the script could be enhanced to use PyYAML.

### Python Dependencies

```bash
pip install PyGithub
```

### Setup:

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full access)
   - Copy the generated token

2. Set the environment variable:
   ```bash
   export GITHUB_TOKEN=your_token_here
   ```

### Usage:

**Dry run (preview only, no issues created):**
```bash
python scripts/create_phase_issues.py --dry-run
```

**Create issues:**
```bash
python scripts/create_phase_issues.py
```

## What Gets Created

The script will create 6 GitHub issues:

1. **Phase A: Character System Foundation**
   - Labels: enhancement, phase-a, character-system, rules
   - Tracks character classes, races, saving throws implementation

2. **Phase B: Faction & Location Systems**
   - Labels: enhancement, phase-b, faction-system, world-simulation
   - Tracks faction management and location system

3. **Phase C: Creatures & Encounters**
   - Labels: enhancement, phase-c, monsters, npcs, encounters
   - Tracks monster entities, NPCs, and encounter system

4. **Phase D: Dungeon Crawling & Exploration**
   - Labels: enhancement, phase-d, exploration, dungeon-crawling
   - Tracks movement, line of sight, traps, and dialogue

5. **Phase E: Temple Content Population**
   - Labels: enhancement, phase-e, content, temple-of-elemental-evil
   - Tracks content creation for Hommlet, Moathouse, and Temple

6. **Phase F: Remaining Rules & Polish**
   - Labels: enhancement, phase-f, rules, polish, spells, magic-items
   - Tracks experience, spells, morale, and final polish

## Troubleshooting

### "Error: GITHUB_TOKEN environment variable not set"
Make sure you've set the token:
```bash
export GITHUB_TOKEN=your_token_here
```

### "Error connecting to GitHub: 403"
Your token may not have the required permissions. Ensure it has `repo` scope.

### "Error connecting to GitHub: 404"
Check that the repository name is correct. The script uses `scottfrye/dnd` by default, but you can override it:
```bash
export GITHUB_REPOSITORY=username/repo
```

### Issues already exist
The script will fail if issues with the same title already exist. You'll need to either:
- Close or rename existing issues
- Modify the script to check for existing issues first

## Verifying Success

After running the script (without `--dry-run`), check:

1. Go to the repository's **Issues** page
2. You should see 6 new issues with titles starting with "Phase A" through "Phase F"
3. Each issue should have the appropriate labels applied
4. Each issue should contain the full content from the template

## Script Details

The `create_phase_issues.py` script:
- Parses the YAML frontmatter from each template
- Extracts title, labels, and body content
- Creates issues via the GitHub REST API
- Provides detailed logging of the process

## Notes

- The workflow requires `issues: write` permission (included in workflow file)
- Issues are created in the repository where the workflow runs
- The templates remain unchanged; only issues are created
- You can run the workflow multiple times in dry-run mode safely
- Only run without dry-run once to avoid duplicate issues

## Support

If you encounter any issues or need help:
1. Check the workflow run logs in the Actions tab
2. Review the script output for error messages
3. Ensure your GitHub token has the correct permissions
4. Verify the template files exist in `.github/ISSUE_TEMPLATE/`
