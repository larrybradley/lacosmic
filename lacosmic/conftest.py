# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Configuration file for the pytest test suite.
"""

import numpy as np
from astropy.utils import minversion

try:
    from pytest_astropy_header.display import (PYTEST_HEADER_MODULES,
                                               TESTED_VERSIONS)
    ASTROPY_HEADER = True
except ImportError:
    ASTROPY_HEADER = False

# do not remove until we drop support for NumPy < 2.0
if minversion(np, '2.0.0.dev0+git20230726'):
    np.set_printoptions(legacy='1.25')


def pytest_configure(config):
    if ASTROPY_HEADER:
        config.option.astropy_header = True

        # Customize the following lines to add/remove entries from the
        # list of packages for which version numbers are displayed when
        # running the tests.
        PYTEST_HEADER_MODULES.clear()
        deps = ['NumPy', 'SciPy', 'Astropy']
        for dep in deps:
            PYTEST_HEADER_MODULES[dep] = dep.lower()

        from lacosmic import __version__
        TESTED_VERSIONS['lacosmic'] = __version__
