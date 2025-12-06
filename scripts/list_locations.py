#!/usr/bin/env python
"""List and display all location data files.

This script loads all location JSON files from the data/locations/ directory
and its subdirectories, displaying summary information about each location.

Usage:
    python scripts/list_locations.py [--verbose] [--filter LOCATION_NAME]
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure stdout uses UTF-8 encoding to handle unicode characters on all platforms
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_location(filepath: Path) -> dict:
    """Load and parse a location JSON file."""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def format_location_summary(location: dict, verbose: bool = False) -> str:
    """Format a location dictionary as a human-readable summary."""
    lines = []
    lines.append(f"ID: {location.get('id', 'N/A')}")
    lines.append(f"Name: {location.get('name', 'N/A')}")
    
    if verbose:
        if 'description' in location:
            lines.append(f"Description: {location['description']}")
        
        if 'dimensions' in location:
            dims = location['dimensions']
            lines.append(f"Dimensions: {dims.get('width', '?')}x{dims.get('height', '?')}")
        
        if 'exits' in location and location['exits']:
            lines.append(f"Exits: {len(location['exits'])}")
            for exit_info in location['exits']:
                direction = exit_info.get('direction', '?')
                target = exit_info.get('target', '?')
                locked = " (locked)" if exit_info.get('locked', False) else ""
                lines.append(f"  - {direction.capitalize()} to {target}{locked}")
        
        if 'light_level' in location:
            lines.append(f"Light: {location['light_level']}")
        
        if 'items' in location and location['items']:
            lines.append(f"Items: {', '.join(location['items'])}")
        
        if 'monsters' in location and location['monsters']:
            lines.append(f"Monsters: {', '.join(location['monsters'])}")
    
    return "\n".join(lines)


def list_locations(locations_dir: Path, verbose: bool = False, filter_name: str = None) -> None:
    """List all locations in the locations directory and subdirectories."""
    if not locations_dir.exists():
        print(f"Error: Locations directory not found: {locations_dir}")
        sys.exit(1)
    
    # Find all JSON files recursively
    location_files = sorted(locations_dir.glob("**/*.json"))
    
    if not location_files:
        print(f"No location files found in {locations_dir}")
        return
    
    # Group locations by subdirectory
    locations_by_area = {}
    for filepath in location_files:
        # Get the relative path from locations_dir
        rel_path = filepath.relative_to(locations_dir)
        
        # Determine the area (subdirectory name or "root")
        if len(rel_path.parts) > 1:
            area = rel_path.parts[0]
        else:
            area = "other"
        
        if area not in locations_by_area:
            locations_by_area[area] = []
        
        try:
            location_data = load_location(filepath)
            
            # Apply filter if specified
            if filter_name:
                name = location_data.get('name', '').lower()
                loc_id = location_data.get('id', '').lower()
                if filter_name.lower() not in name and filter_name.lower() not in loc_id:
                    continue
            
            locations_by_area[area].append({
                'filepath': filepath,
                'data': location_data
            })
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse {filepath}: {e}")
        except Exception as e:
            print(f"Warning: Error loading {filepath}: {e}")
    
    # Display locations grouped by area
    total_count = 0
    for area in sorted(locations_by_area.keys()):
        locations = locations_by_area[area]
        if not locations:
            continue
        
        print(f"\n{'='*60}")
        print(f"Area: {area.upper()}")
        print(f"{'='*60}")
        print(f"Locations found: {len(locations)}\n")
        
        for loc_info in locations:
            filepath = loc_info['filepath']
            location = loc_info['data']
            
            print(f"File: {filepath.relative_to(locations_dir)}")
            print(format_location_summary(location, verbose))
            print()
            total_count += 1
    
    print(f"{'='*60}")
    print(f"Total locations loaded: {total_count}")
    print(f"{'='*60}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List and display all location data files"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed information for each location"
    )
    parser.add_argument(
        "-f", "--filter",
        type=str,
        help="Filter locations by name or ID (case-insensitive)"
    )
    parser.add_argument(
        "--locations-dir",
        type=Path,
        default=None,
        help="Path to locations directory (default: data/locations/ relative to repo root)",
    )
    args = parser.parse_args()
    
    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    if args.locations_dir:
        locations_dir = args.locations_dir
    else:
        locations_dir = repo_root / "data" / "locations"
    
    list_locations(locations_dir, args.verbose, args.filter)


if __name__ == "__main__":
    main()
