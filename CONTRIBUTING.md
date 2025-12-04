# Contributing to Temple of Elemental Evil - AD&D 1E Roguelike

Thank you for your interest in contributing to this project! This document outlines the guidelines and best practices for contributing.

## Development Setup

### Requirements

- Python 3.12, 3.13, 3.14 or above
- Supported on Windows, macOS, and Linux
- Compatible with Anaconda/Miniconda environments

### Setting Up Your Development Environment

#### Using pip

```bash
# Clone the repository
git clone https://github.com/scottfrye/dnd.git
cd dnd

# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify setup
pytest
```

#### Using Anaconda

```bash
# Clone the repository
git clone https://github.com/scottfrye/dnd.git
cd dnd

# Create a new conda environment
conda create -n dnd python=3.12
conda activate dnd

# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify setup
pytest
```

## Branching Strategy

This project follows a development-to-main branching strategy:

### Branch Structure

- **`main`**: The stable production branch. Contains only released versions of the code.
- **`development`**: The active development branch. All feature branches should be merged here.

### Workflow

1. **All feature branches** should be created from `development`
2. **All pull requests** should target the `development` branch
3. **The `main` branch** is updated manually by project maintainers during releases

### Creating a Pull Request

1. Create your feature branch from `development`:
   ```bash
   git checkout development
   git pull origin development
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with clear, descriptive messages

3. Push your branch and create a pull request targeting `development`:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Ensure all CI checks pass before requesting review

### Release Process

Releases are handled manually by project maintainers:

1. Maintainers merge `development` into `main` when ready for a release
2. A new version tag is created on `main`
3. Release notes are published

### Version Tracking

This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

Version information is maintained in:
- `pyproject.toml`: The source of truth for the current version
- `CHANGELOG.md`: A human-readable history of changes between versions

When contributing, if your changes warrant a version bump:
1. Update the `[Unreleased]` section in `CHANGELOG.md` with your changes
2. Maintainers will update the version number in `pyproject.toml` during release

## Code Quality Standards

### Testing

- Write tests for all new features and bug fixes
- Ensure all existing tests pass before submitting a PR
- Aim for high test coverage

Run tests with:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src
```

### Code Style

- Follow PEP 8 Python style guidelines
- Write clear, self-documenting code
- Add docstrings to functions and classes

## Pull Request Guidelines

When submitting a pull request:

1. **Target the `development` branch** (not `main`)
2. Provide a clear description of the changes
3. Reference any related issues
4. Ensure all tests pass
5. Update documentation if needed
6. Keep changes focused and atomic

## Questions or Issues?

If you have questions or encounter issues:

1. Check existing issues on GitHub
2. Create a new issue with a clear description
3. Tag it appropriately (bug, enhancement, question, etc.)

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.
