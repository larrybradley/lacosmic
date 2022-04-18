# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Tests for the core module.
"""

import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
import pytest

from ..core import lacosmic

size = 25
npts = 20
rng = np.random.default_rng(12345)
IMG = rng.standard_normal((size, size))
x = rng.integers(0, size - 1, npts)
y = rng.integers(0, size - 1, npts)
ERROR = np.ones(IMG.shape) * 0.1
CR = np.zeros(IMG.shape)
CR[y, x] = 10.
CR_IMG = IMG + CR
MASK_REF = CR.astype(bool)


class TestLACosmic:
    """
    Tests for lacosmic.
    """

    def test_lacosmic(self):
        """Test basic lacosmic."""
        crclean_img, crmask_img = lacosmic(CR_IMG, 1, 40, 50, error=ERROR)
        assert_allclose(crclean_img, IMG, atol=2.)
        assert_array_equal(crmask_img, MASK_REF)

    def test_background_scalar(self):
        """Test lacosmic with a background scalar."""
        crclean_img, crmask_img = lacosmic(CR_IMG, 1, 40, 50, error=ERROR,
                                           background=10)
        assert_allclose(crclean_img, IMG, atol=2.)
        assert_array_equal(crmask_img, MASK_REF)

    def test_background_maxiter(self):
        """Test lacosmic with a background scalar."""
        crclean_img, crmask_img = lacosmic(CR_IMG, 1, 40, 50, error=ERROR,
                                           background=10, maxiter=1)
        assert_allclose(crclean_img, IMG, atol=2.)
        assert_array_equal(crmask_img, MASK_REF)

    def test_background_image(self):
        """Test lacosmic with a 2D background image."""
        bkgrd_img = np.ones(IMG.shape) * 10.
        crclean_img, crmask_img = lacosmic(CR_IMG, 1, 40, 50, error=ERROR,
                                           background=bkgrd_img)
        assert_allclose(crclean_img, IMG, atol=2.)
        assert_array_equal(crmask_img, MASK_REF)

    def test_mask_image(self):
        """Test lacosmic with an input mask image."""
        mask = MASK_REF.copy()
        mask[0:10, 0:10] = False
        mask_ref2 = np.logical_and(MASK_REF, ~mask)
        crclean_img, crmask_img = lacosmic(CR_IMG, 1, 40, 50, error=ERROR,
                                           mask=mask)
        assert_allclose(crclean_img * mask_ref2, IMG * mask_ref2, atol=2.)
        assert_array_equal(crmask_img, mask_ref2)

    def test_large_cosmics(self):
        """Test lacosmic cleaning with large cosmic rays."""
        test_img = np.ones((7, 7))
        test_img[1:6, 1:6] = 100.
        mask_ref2 = np.zeros((7, 7), dtype=bool)
        mask_ref2[1:6, 1:6] = True
        _, crmask_img = lacosmic(test_img, 3, 2, 2, effective_gain=1,
                                 readnoise=0)
        assert_array_equal(crmask_img, mask_ref2)

    def test_error_image_size(self):
        """
        Test if AssertionError raises if shape of error doesn't match
        image.
        """
        error = np.zeros((7, 7))
        with pytest.raises(ValueError):
            lacosmic(CR_IMG, 3, 2, 2, effective_gain=1, readnoise=0,
                     error=error)

    def test_error_inputs(self):
        with pytest.raises(ValueError):
            lacosmic(CR_IMG, 3, 2, 2, effective_gain=1, error=None)

        with pytest.raises(ValueError):
            lacosmic(CR_IMG, 3, 2, 2, readnoise=0, error=None)
