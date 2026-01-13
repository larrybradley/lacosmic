# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Configuration file for the pytest test suite.
"""

import tomllib
from importlib.metadata import version
from pathlib import Path

try:
    from pytest_astropy_header.display import (PYTEST_HEADER_MODULES,
                                               TESTED_VERSIONS)
    ASTROPY_HEADER = True
except ImportError:
    ASTROPY_HEADER = False


def _get_dependencies_from_pyproject():
    """
    Extract project dependencies and name from pyproject.toml.

    Returns
    -------
    result : tuple of (str, list of str)
        Project name and list of package names extracted from the
        dependencies and optional-dependencies.all.
    """
    pyproject_path = Path(__file__).parent.parent / 'pyproject.toml'
    with open(pyproject_path, 'rb') as f:
        pyproject_data = tomllib.load(f)

    project_name = pyproject_data.get('project', {}).get('name', '')
    dependencies = pyproject_data.get('project', {}).get('dependencies', [])

    # Also include optional dependencies under "all" if present
    optional_deps = (
        pyproject_data.get('project', {})
        .get('optional-dependencies', {})
        .get('all', [])
    )
    all_deps = dependencies + optional_deps

    # Extract package names from dependency specifications
    # (e.g., 'numpy >= 2.0' -> 'numpy')
    package_names = []
    for dep in all_deps:
        # Split on common version specifiers and take the first part
        pkg_name = dep.split('[')[0].split('>')[0].split('<')[0].split(
            '=')[0].split('!')[0].split('~')[0].strip()
        # Skip self-references to the project itself
        if pkg_name.lower() == project_name.lower():
            continue
        package_names.append(pkg_name)

    # Sort alphabetically for consistent output
    package_names.sort(key=str.lower)

    return project_name, package_names


def pytest_configure(config):
    """
    Configure pytest settings.

    Parameters
    ----------
    config : pytest.Config
        The pytest configuration object.
    """
    if ASTROPY_HEADER:
        config.option.astropy_header = True

        # Customize the following lines to add/remove entries from the
        # list of packages for which version numbers are displayed when
        # running the tests.
        PYTEST_HEADER_MODULES.clear()

        # Get dependencies from pyproject.toml
        project_name, deps = _get_dependencies_from_pyproject()

        for dep in deps:
            PYTEST_HEADER_MODULES[dep] = dep

        TESTED_VERSIONS[project_name] = version(project_name)
