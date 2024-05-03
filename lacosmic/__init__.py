# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Package to remove cosmic rays from an astronomical image using the
L.A.Cosmic algorithm (van Dokkum 2001; PASP 113, 1420).
"""

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''
