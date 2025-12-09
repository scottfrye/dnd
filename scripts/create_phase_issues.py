#!/usr/bin/env python3
"""
Script to create GitHub issues from phase template files.

This script reads the phase template markdown files from .github/ISSUE_TEMPLATE/
and creates actual GitHub issues for each phase in the project backlog.

Usage:
    export GITHUB_TOKEN=your_token_here
    python scripts/create_phase_issues.py

Requirements:
    - PyGithub: pip install PyGithub
    - GITHUB_TOKEN environment variable with repo access
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from github import Github, GithubException
except ImportError:
    print("Error: PyGithub is not installed.")
    print("Please install it with: pip install PyGithub")
    sys.exit(1)


def parse_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter from markdown file."""
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        return {}
    
    frontmatter_text = frontmatter_match.group(1)
    frontmatter = {}
    
    for line in frontmatter_text.split('\n'):
        if ':' not in line:
            continue
            
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        
        # Handle labels array
        if key == 'labels':
            # Parse labels from format like ['label1', 'label2'] or ["label1", "label2"]
            labels_match = re.findall(r"['\"]([^'\"]+)['\"]", value)
            frontmatter[key] = labels_match
        else:
            frontmatter[key] = value
    
    return frontmatter


def extract_body(content: str) -> str:
    """Extract the body content (everything after frontmatter)."""
    # Remove frontmatter
    body_match = re.search(r'^---\n.*?\n---\n(.*)', content, re.DOTALL)
    if body_match:
        return body_match.group(1).strip()
    return content.strip()


def create_issue_from_template(
    repo,
    template_path: Path,
    dry_run: bool = False
) -> Optional[str]:
    """
    Create a GitHub issue from a template file.
    
    Args:
        repo: GitHub repository object
        template_path: Path to the template file
        dry_run: If True, only print what would be created
        
    Returns:
        Issue URL if created, None otherwise
    """
    print(f"\nProcessing: {template_path.name}")
    
    # Read template file
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter and body
    frontmatter = parse_frontmatter(content)
    body = extract_body(content)
    
    if not frontmatter:
        print(f"  ⚠️  Warning: No frontmatter found in {template_path.name}")
        return None
    
    # Extract issue details
    title = frontmatter.get('title', template_path.stem.replace('-', ' ').title())
    labels = frontmatter.get('labels', [])
    
    # Create full body with template about description
    about = frontmatter.get('about', '')
    if about:
        full_body = f"{about}\n\n---\n\n{body}"
    else:
        full_body = body
    
    print(f"  Title: {title}")
    print(f"  Labels: {', '.join(labels) if labels else 'None'}")
    print(f"  Body length: {len(full_body)} characters")
    
    if dry_run:
        print("  [DRY RUN] Would create issue")
        return None
    
    try:
        # Create the issue
        issue = repo.create_issue(
            title=title,
            body=full_body,
            labels=labels
        )
        print(f"  ✓ Created issue #{issue.number}: {issue.html_url}")
        return issue.html_url
    except GithubException as e:
        print(f"  ✗ Error creating issue: {e}")
        return None


def main():
    """Main function to create issues from all phase templates."""
    # Check for dry run mode
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("Running in DRY RUN mode - no issues will be created\n")
    
    # Check for GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token and not dry_run:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Please set it with: export GITHUB_TOKEN=your_token_here")
        sys.exit(1)
    
    # Determine repository
    repo_name = os.environ.get('GITHUB_REPOSITORY', 'scottfrye/dnd')
    
    # Connect to GitHub (skip in dry-run mode)
    repo = None
    if not dry_run:
        print(f"Connecting to GitHub repository: {repo_name}")
        try:
            g = Github(github_token)
            repo = g.get_repo(repo_name)
            print(f"✓ Connected to {repo.full_name}\n")
        except GithubException as e:
            print(f"Error connecting to GitHub: {e}")
            sys.exit(1)
    else:
        print(f"Target repository: {repo_name}\n")
    
    # Define phase template files to process
    phase_files = [
        'phase-a-character-system.md',
        'phase-b-faction-location.md',
        'phase-c-creatures-encounters.md',
        'phase-d-dungeon-exploration.md',
        'phase-e-content-population.md',
        'phase-f-rules-polish.md',
    ]
    
    # Get repository root - handle both running from repo root and scripts dir
    script_path = Path(__file__).resolve()
    if script_path.parent.name == 'scripts':
        repo_root = script_path.parent.parent
    else:
        repo_root = script_path.parent
    
    # Allow override via environment variable
    template_dir_override = os.environ.get('ISSUE_TEMPLATE_DIR')
    if template_dir_override:
        template_dir = Path(template_dir_override)
    else:
        template_dir = repo_root / '.github' / 'ISSUE_TEMPLATE'
    
    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}")
        sys.exit(1)
    
    # Process each template
    created_issues = []
    found_templates = 0
    print("=" * 60)
    print("Creating GitHub Issues from Phase Templates")
    print("=" * 60)
    
    for phase_file in phase_files:
        template_path = template_dir / phase_file
        
        if not template_path.exists():
            print(f"\n⚠️  Warning: Template not found: {template_path}")
            continue
        
        found_templates += 1
        issue_url = create_issue_from_template(repo, template_path, dry_run)
        if issue_url:
            created_issues.append((phase_file, issue_url))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if dry_run:
        print(f"\nDry run complete. Would have created {found_templates} issues.")
        if found_templates < len(phase_files):
            print(f"  Note: Only {found_templates}/{len(phase_files)} template files were found")
        print("\nTo actually create the issues, run without --dry-run flag:")
        print("  python scripts/create_phase_issues.py")
    else:
        print(f"\n✓ Created {len(created_issues)} issues:")
        for filename, url in created_issues:
            print(f"  - {filename}: {url}")
        
        if len(created_issues) < found_templates:
            print(f"\n⚠️  Warning: Only {len(created_issues)}/{found_templates} issues created")
            print("  Check the output above for errors")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
