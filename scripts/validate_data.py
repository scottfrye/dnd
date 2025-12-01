#!/usr/bin/env python
"""Validate data files against JSON schemas.

This script reads data files from the data/ directory and validates them
against the corresponding JSON schemas in data/schemas/.

Usage:
    python scripts/validate_data.py [--verbose]
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator, ValidationError
except ImportError:
    print("Error: jsonschema package not installed.")
    print("Install it with: pip install jsonschema")
    sys.exit(1)


# Map data directories to their schema files
DATA_TYPE_SCHEMA_MAP = {
    "monsters": "monster.schema.json",
    "locations": "location.schema.json",
    "items": "item.schema.json",
}


def load_json_file(filepath: Path) -> dict:
    """Load and parse a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_file(
    data_file: Path, schema: dict, validator: Draft7Validator, verbose: bool = False
) -> list[str]:
    """Validate a data file against a schema.
    
    Returns a list of error messages (empty if valid).
    """
    errors = []
    try:
        data = load_json_file(data_file)
    except json.JSONDecodeError as e:
        errors.append(f"  JSON parse error: {e}")
        return errors
    
    for error in validator.iter_errors(data):
        path = ".".join(str(p) for p in error.path) if error.path else "(root)"
        errors.append(f"  [{path}] {error.message}")
    
    if verbose and not errors:
        print(f"  ✓ {data_file.name}")
    
    return errors


def validate_data_directory(data_dir: Path, schemas_dir: Path, verbose: bool = False) -> int:
    """Validate all data files in the data directory.
    
    Returns the total number of validation errors found.
    """
    total_errors = 0
    total_files = 0
    
    # Load all schemas
    schemas = {}
    for data_type, schema_file in DATA_TYPE_SCHEMA_MAP.items():
        schema_path = schemas_dir / schema_file
        if not schema_path.exists():
            print(f"Warning: Schema file not found: {schema_path}")
            continue
        try:
            schemas[data_type] = load_json_file(schema_path)
        except json.JSONDecodeError as e:
            print(f"Error loading schema {schema_path}: {e}")
            return 1
    
    # Validate each data type directory
    for data_type, schema in schemas.items():
        type_dir = data_dir / data_type
        if not type_dir.exists():
            if verbose:
                print(f"Skipping {data_type}: directory not found")
            continue
        
        validator = Draft7Validator(schema)
        json_files = list(type_dir.glob("*.json"))
        
        if verbose:
            print(f"\nValidating {data_type} ({len(json_files)} files):")
        
        for data_file in json_files:
            total_files += 1
            errors = validate_file(data_file, schema, validator, verbose)
            
            if errors:
                total_errors += len(errors)
                print(f"\n✗ {data_file}:")
                for error in errors:
                    print(error)
    
    return total_errors, total_files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate data files against JSON schemas"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed validation progress"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Path to data directory (default: data/ relative to repo root)"
    )
    args = parser.parse_args()
    
    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    if args.data_dir:
        data_dir = args.data_dir
    else:
        data_dir = repo_root / "data"
    
    schemas_dir = data_dir / "schemas"
    
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        sys.exit(1)
    
    if not schemas_dir.exists():
        print(f"Error: Schemas directory not found: {schemas_dir}")
        sys.exit(1)
    
    print(f"Validating data files in: {data_dir}")
    print(f"Using schemas from: {schemas_dir}")
    
    result = validate_data_directory(data_dir, schemas_dir, args.verbose)
    total_errors, total_files = result
    
    print(f"\n{'='*50}")
    print(f"Validation complete: {total_files} files checked")
    
    if total_errors == 0:
        print("✓ All files valid!")
        sys.exit(0)
    else:
        print(f"✗ {total_errors} error(s) found")
        sys.exit(1)


if __name__ == "__main__":
    main()
