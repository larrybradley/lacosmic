# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Tests for the utils module.
"""

from numpy.testing import assert_allclose
from scipy.ndimage import gaussian_filter

from lacosmic.utils import make_cosmic_rays


def test_make_cosmic_rays_width():
    """
    Test that a nonzero width smooths the cosmic ray trails with a
    Gaussian filter.
    """
    shape = (50, 50)
    sharp = make_cosmic_rays(shape, n_cosmics=10, seed=0)
    smooth = make_cosmic_rays(shape, n_cosmics=10, width=1.5, seed=0)
    assert_allclose(smooth, gaussian_filter(sharp, sigma=1.5))
