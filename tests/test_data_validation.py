"""Tests for the data validation script."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


# Get paths
REPO_ROOT = Path(__file__).parent.parent
VALIDATOR_SCRIPT = REPO_ROOT / "scripts" / "validate_data.py"
DATA_DIR = REPO_ROOT / "data"
SCHEMAS_DIR = DATA_DIR / "schemas"


class TestSchemaFilesExist:
    """Test that required schema files exist."""

    def test_monster_schema_exists(self):
        """Monster schema file should exist."""
        assert (SCHEMAS_DIR / "monster.schema.json").exists()

    def test_location_schema_exists(self):
        """Location schema file should exist."""
        assert (SCHEMAS_DIR / "location.schema.json").exists()

    def test_item_schema_exists(self):
        """Item schema file should exist."""
        assert (SCHEMAS_DIR / "item.schema.json").exists()


class TestSchemasAreValidJson:
    """Test that schema files are valid JSON."""

    def test_monster_schema_valid_json(self):
        """Monster schema should be valid JSON."""
        with open(SCHEMAS_DIR / "monster.schema.json") as f:
            schema = json.load(f)
        assert "$schema" in schema
        assert "properties" in schema

    def test_location_schema_valid_json(self):
        """Location schema should be valid JSON."""
        with open(SCHEMAS_DIR / "location.schema.json") as f:
            schema = json.load(f)
        assert "$schema" in schema
        assert "properties" in schema

    def test_item_schema_valid_json(self):
        """Item schema should be valid JSON."""
        with open(SCHEMAS_DIR / "item.schema.json") as f:
            schema = json.load(f)
        assert "$schema" in schema
        assert "properties" in schema


class TestSampleDataExists:
    """Test that sample data files exist."""

    def test_sample_monster_exists(self):
        """At least one sample monster file should exist."""
        monsters_dir = DATA_DIR / "monsters"
        assert monsters_dir.exists()
        json_files = list(monsters_dir.glob("*.json"))
        assert len(json_files) >= 1

    def test_sample_location_exists(self):
        """At least one sample location file should exist."""
        locations_dir = DATA_DIR / "locations"
        assert locations_dir.exists()
        json_files = list(locations_dir.glob("*.json"))
        assert len(json_files) >= 1

    def test_sample_item_exists(self):
        """At least one sample item file should exist."""
        items_dir = DATA_DIR / "items"
        assert items_dir.exists()
        json_files = list(items_dir.glob("*.json"))
        assert len(json_files) >= 1


class TestValidatorScript:
    """Test the validator script."""

    def test_validator_script_exists(self):
        """Validator script should exist."""
        assert VALIDATOR_SCRIPT.exists()

    def test_validator_runs_successfully(self):
        """Validator should run successfully on sample data."""
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"Validator failed: {result.stderr}"
        assert "All files valid" in result.stdout

    def test_validator_verbose_mode(self):
        """Validator should work in verbose mode."""
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_SCRIPT), "--verbose"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0
        assert "Validating monsters" in result.stdout


class TestSampleDataValidation:
    """Test that sample data validates against schemas."""

    def test_sample_monster_validates(self):
        """Sample monster files should validate against monster schema."""
        from jsonschema import Draft7Validator

        with open(SCHEMAS_DIR / "monster.schema.json") as f:
            schema = json.load(f)
        
        validator = Draft7Validator(schema)
        
        for monster_file in (DATA_DIR / "monsters").glob("*.json"):
            with open(monster_file) as f:
                data = json.load(f)
            errors = list(validator.iter_errors(data))
            assert len(errors) == 0, f"{monster_file}: {errors}"

    def test_sample_location_validates(self):
        """Sample location files should validate against location schema."""
        from jsonschema import Draft7Validator

        with open(SCHEMAS_DIR / "location.schema.json") as f:
            schema = json.load(f)
        
        validator = Draft7Validator(schema)
        
        for location_file in (DATA_DIR / "locations").glob("*.json"):
            with open(location_file) as f:
                data = json.load(f)
            errors = list(validator.iter_errors(data))
            assert len(errors) == 0, f"{location_file}: {errors}"

    def test_sample_item_validates(self):
        """Sample item files should validate against item schema."""
        from jsonschema import Draft7Validator

        with open(SCHEMAS_DIR / "item.schema.json") as f:
            schema = json.load(f)
        
        validator = Draft7Validator(schema)
        
        for item_file in (DATA_DIR / "items").glob("*.json"):
            with open(item_file) as f:
                data = json.load(f)
            errors = list(validator.iter_errors(data))
            assert len(errors) == 0, f"{item_file}: {errors}"
