# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Package to remove cosmic rays from an astronomical image using the
L.A.Cosmic algorithm (van Dokkum 2001; PASP 113, 1420).
"""

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''


from . import core
from .core import *  # noqa: F403


def __getattr__(name):
    """
    Return the deprecated ``lacosmic`` function on attribute access.

    The deprecated function is provided through this hook, instead of
    an import, so that it remains importable from the package without
    being added to the package namespace or the documented API.
    """
    if name == 'lacosmic':
        return core.lacosmic

    msg = f'module {__name__!r} has no attribute {name!r}'
    raise AttributeError(msg)
