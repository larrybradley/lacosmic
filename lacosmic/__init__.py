# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Package to remove cosmic rays from an astronomical image using the
L.A.Cosmic (PASP 113, 1420, 2001) algorithm.
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

if not _ASTROPY_SETUP_:
    from .lacosmic import *
