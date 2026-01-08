# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Tools for making simulated data.

These functions are intended only for testing and demonstration
purposes. They are not part of the package API and may change without
warning.
"""

import numpy as np
from astropy.modeling.models import Gaussian2D
from scipy.ndimage import gaussian_filter


def make_cosmic_rays(shape, n_cosmics=50, intensity_range=(200, 1000),
                     length_range=(4, 50), width=0, seed=None):
    """
    Make synthetic cosmic ray trails.

    Parameters
    ----------
    shape : tuple
        Shape of the output image (height, width).

    n_cosmics : int
        Number of cosmic ray trails to generate.

    intensity_range : tuple
        Range of total intensities for the cosmic rays.

    length_range : tuple
        Range of lengths for the cosmic ray trails.

    width : float
        Standard deviation for Gaussian smoothing of cosmic rays. If 0,
        no smoothing is applied.

    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    cr_image : ndarray
        Image containing synthetic cosmic ray trails.
    """
    rng = np.random.default_rng(seed=seed)
    cr_image = np.zeros(shape, dtype=np.float32)
    h, w = shape

    for _ in range(n_cosmics):
        length = rng.uniform(*length_range)
        angle = rng.uniform(0, 2 * np.pi)
        intensity = rng.uniform(*intensity_range)

        # Start and end points
        r0 = rng.uniform(0, h)
        c0 = rng.uniform(0, w)
        r1 = r0 + length * np.sin(angle)
        c1 = c0 + length * np.cos(angle)

        # Interpolate points along the trail
        num_points = int(length * 3) + 2
        t = np.linspace(0, 1, num_points)
        rr = (r0 + t * (r1 - r0)).astype(int)
        cc = (c0 + t * (c1 - c0)).astype(int)

        mask = (rr >= 0) & (rr < h) & (cc >= 0) & (cc < w)
        value = intensity / (num_points / length)
        np.add.at(cr_image, (rr[mask], cc[mask]), value)

    if width > 0:
        cr_image = gaussian_filter(cr_image, sigma=width)

    return cr_image


def make_gaussian_sources(shape, n_sources=50, amplitude_range=(50, 200),
                          sigma_range=(1, 7), noise_level=5, seed=None):
    """
    Make elliptical Gaussian sources with random orientations and noise.

    Parameters
    ----------
    shape : tuple
        Shape of the output image (height, width).

    n_sources : int
        Number of Gaussian sources to generate.

    amplitude_range : tuple
        Range of amplitudes for the Gaussian sources.

    sigma_range : tuple
        Range of standard deviations for the Gaussian sources.

    noise_level : float
        Standard deviation of the Gaussian noise to add to the image.

    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    data : ndarray
        Image containing the Gaussian sources with added noise.

    error : ndarray
        Image containing the error (standard deviation) at each pixel.
    """
    rng = np.random.default_rng(seed=seed)
    h, w = shape
    y, x = np.mgrid[0:h, 0:w]

    data = rng.normal(loc=0, scale=noise_level, size=shape)

    for _ in range(n_sources):
        amp = rng.uniform(*amplitude_range)
        x0 = rng.uniform(0, w)
        y0 = rng.uniform(0, h)
        x_std = rng.uniform(*sigma_range)
        y_std = rng.uniform(*sigma_range)
        theta = rng.uniform(0, np.pi)

        model = Gaussian2D(amplitude=amp, x_mean=x0, y_mean=y0,
                           x_stddev=x_std, y_stddev=y_std, theta=theta)
        data += model(x, y)

    error = np.full(shape, noise_level)

    return data, error
