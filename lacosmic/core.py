# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Module to remove cosmic rays from an astronomical image using the
L.A.Cosmic algorithm (van Dokkum 2001; PASP 113, 1420).
"""

import numpy as np
from astropy import log
from astropy.nddata import block_reduce, block_replicate
from scipy import ndimage

__all__ = ['lacosmic']


def lacosmic(data, contrast, cr_threshold, neighbor_threshold,
             error=None, mask=None, background=None, effective_gain=None,
             readnoise=None, maxiter=4, border_mode='mirror'):
    r"""
    Remove cosmic rays from an astronomical image using the L.A.Cosmic
    algorithm.

    The `L.A.Cosmic algorithm
    <http://www.astro.yale.edu/dokkum/lacosmic/>`_ is based on Laplacian
    edge detection and is described in `van Dokkum (2001; PASP 113,
    1420)
    <https://ui.adsabs.harvard.edu/abs/2001PASP..113.1420V/abstract>`_.

    Parameters
    ----------
    data : array_like
        The 2D array of the image.

    contrast : float
        Contrast threshold between the Laplacian image and the
        fine-structure image.  If your image is critically sampled, use
        a value around 2.  If your image is undersampled (e.g., HST
        data), a value of 4 or 5 (or more) is more appropriate.  If your
        image is oversampled, use a value between 1 and 2.  For details,
        please see `PASP 113, 1420 (2001)
        <https://ui.adsabs.harvard.edu/abs/2001PASP..113.1420V/abstract>`_,
        which calls this parameter :math:`f_{\mbox{lim}}`.  In
        particular, Figure 4 shows the approximate relationship between
        the ``contrast`` parameter and the full-width half-maximum (in
        pixels) of stars in your image.

    cr_threshold : float
        The Laplacian signal-to-noise ratio threshold for cosmic-ray
        detection.

    neighbor_threshold : float
        The Laplacian signal-to-noise ratio threshold for detection of
        cosmic rays in pixels neighboring the initially-identified
        cosmic rays.

    error : array_like, optional
        The 1-sigma errors of the input ``data``.  If ``error`` is not
        input, then ``effective_gain`` and ``readnoise`` will be used to
        construct an approximate model of the ``error``.  If ``error``
        is input, it will override the ``effective_gain`` and
        ``readnoise`` parameters.  ``error`` must have the same shape as
        ``data``.

    mask : array_like (bool), optional
        A boolean mask, with the same shape as ``data``, where a `True`
        value indicates the corresponding element of ``data`` is masked.
        Masked pixels are ignored when identifying cosmic rays.  It is
        highly recommended that saturated stars be included in ``mask``.

    background : float or array_like, optional
        The background level previously subtracted from the input
        ``data``.  ``background`` may either be a scalar value or a 2D
        image with the same shape as the input ``data``.  If the input
        ``data`` has not been background subtracted, then set
        ``background=None`` (default).

    effective_gain : float, array-like, optional
        Ratio of counts (e.g., electrons or photons) to the units of
        ``data``.  For example, if your input ``data`` are in units of
        ADU, then ``effective_gain`` should represent electrons/ADU.  If
        your input ``data`` are in units of electrons/s then
        ``effective_gain`` should be the exposure time (or an exposure
        time map).  ``effective_gain`` and ``readnoise`` must be
        specified if ``error`` is not input.

    readnoise : float, optional
        The read noise (in electrons) in the input ``data``.
        ``effective_gain`` and ``readnoise`` must be specified if
        ``error`` is not input.

    maxiter : float, optional
        The maximum number of iterations. The default is 4. The routine
        will automatically exit if no additional cosmic rays are
        identified in an iteration. If the routine is still identifying
        cosmic rays after four iterations, then you are likely digging
        into sources (e.g., saturated stars) and/or the noise. In
        that case, try inputing a ``mask`` or increasing the value of
        ``cr_threshold``.

    border_mode : {'reflect', 'constant', 'nearest', 'mirror', 'wrap'}, \
            optional
        The mode in which the array borders are handled during
        convolution and median filtering.  For 'constant', the fill
        value is 0.  The default is 'mirror', which matches the original
        L.A.Cosmic algorithm.

    Returns
    -------
    cleaned_image : `~numpy.ndarray`
        The cosmic-ray cleaned image.

    crmask : `~numpy.ndarray` (bool)
        A mask image of the identified cosmic rays.  Cosmic-ray pixels
        have a value of `True`.
    """
    block_size = 2.0
    kernel = np.array([[0.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 0.0]])

    clean_data = data.copy()
    if background is not None:
        clean_data += background
    final_crmask = np.zeros(data.shape, dtype=bool)

    if error is not None and data.shape != error.shape:
        msg = 'error must have the same shape as data'
        raise ValueError(msg)
    clean_error_image = error

    ncosmics, ncosmics_tot = 0, 0
    for iteration in range(maxiter):
        sampled_img = block_replicate(clean_data, block_size)
        convolved_img = ndimage.convolve(sampled_img, kernel,
                                         mode=border_mode).clip(min=0.0)
        laplacian_img = block_reduce(convolved_img, block_size)

        if clean_error_image is None:
            if effective_gain is None or readnoise is None:
                msg = ('effective_gain and readnoise must be input if error '
                       'is not input')
                raise ValueError(msg)
            med5_img = ndimage.median_filter(clean_data, size=5,
                                             mode=border_mode).clip(min=1.e-5)
            error_image = (np.sqrt(effective_gain * med5_img + readnoise ** 2)
                           / effective_gain)
        else:
            error_image = clean_error_image

        snr_img = laplacian_img / (block_size * error_image)
        # this is used to remove extended structures (larger than ~5x5)
        snr_img -= ndimage.median_filter(snr_img, size=5, mode=border_mode)

        # used to remove compact bright objects
        med3_img = ndimage.median_filter(clean_data, size=3, mode=border_mode)
        med7_img = ndimage.median_filter(med3_img, size=7, mode=border_mode)
        finestruct_img = ((med3_img - med7_img) / error_image).clip(min=0.01)

        cr_mask1 = snr_img > cr_threshold
        # NOTE: to follow the paper exactly, this condition should be
        # "> contrast * block_size".  "lacos_im.cl" uses simply "> contrast"
        cr_mask2 = (snr_img / finestruct_img) > contrast
        cr_mask = cr_mask1 * cr_mask2
        if mask is not None:
            cr_mask = np.logical_and(cr_mask, ~mask)

        # grow cosmic rays by one pixel and check in snr_img
        selem = np.ones((3, 3))
        neigh_mask = ndimage.binary_dilation(cr_mask, selem)
        cr_mask = cr_mask1 * neigh_mask
        # now grow one more pixel and lower the detection threshold
        neigh_mask = ndimage.binary_dilation(cr_mask, selem)
        cr_mask = (snr_img > neighbor_threshold) * neigh_mask

        # previously unknown cosmic rays found in this iteration
        crmask_new = np.logical_and(~final_crmask, cr_mask)
        ncosmics = np.count_nonzero(crmask_new)

        final_crmask = np.logical_or(final_crmask, cr_mask)
        ncosmics_tot += ncosmics
        log.info(f'Iteration {iteration + 1}: Found {ncosmics} cosmic-ray '
                 f'pixels, Total: {ncosmics_tot}')
        if ncosmics == 0:
            if background is not None:
                clean_data -= background
            return clean_data, final_crmask
        clean_data = _clean_masked_pixels(clean_data, final_crmask, size=5,
                                          exclude_mask=mask)

    if background is not None:
        clean_data -= background
    return clean_data, final_crmask


def _clean_masked_pixels(data, mask, size=5, exclude_mask=None):
    """
    Clean masked pixels in an image.

    Each masked pixel is replaced by the median of unmasked pixels in a
    2D window of ``size`` centered on it. If all pixels in the window
    are masked, then the window is increased in size until unmasked
    pixels are found.

    Pixels in ``exclude_mask`` are not cleaned, but they are excluded
    when calculating the local median.
    """
    if (size % 2) != 1:  # pragma: no cover
        msg = 'size must be an odd integer'
        raise ValueError(msg)

    if data.shape != mask.shape:  # pragma: no cover
        msg = 'mask must have the same shape as data'
        raise ValueError(msg)

    ny, nx = data.shape
    mask_coords = np.argwhere(mask)
    if exclude_mask is not None:
        if data.shape != exclude_mask.shape:  # pragma: no cover
            msg = 'exclude_mask must have the same shape as data'
            raise ValueError(msg)

        maskall = np.logical_or(mask, exclude_mask)
    else:
        maskall = mask
    mask_idx = maskall.nonzero()
    data_nanmask = data.copy()
    data_nanmask[mask_idx] = np.nan

    nexpanded = 0
    for coord in mask_coords:
        y, x = coord
        median_val, expanded = _local_median(data_nanmask, x, y, nx, ny,
                                             size=size)
        data[y, x] = median_val
        if expanded:
            nexpanded += 1
    if nexpanded > 0:
        log.info(f'    Found {nexpanded} {size}x{size} masked regions while '
                 'cleaning.')
    return data


def _local_median(data_nanmask, x, y, nx, ny, *, size=5, expanded=False):
    """
    Compute the local median in a 2D window, excluding NaN.
    """
    hy, hx = size // 2, size // 2
    x0, x1 = np.array([x - hx, x + hx + 1]).clip(0, nx)
    y0, y1 = np.array([y - hy, y + hy + 1]).clip(0, ny)
    region = data_nanmask[y0:y1, x0:x1].ravel()
    goodpixels = region[np.isfinite(region)]
    if len(goodpixels) > 0:
        median_val = np.median(goodpixels)
    else:
        newsize = size + 2  # keep size odd
        median_val, expanded = _local_median(data_nanmask, x, y, nx, ny,
                                             size=newsize, expanded=True)
    return median_val, expanded
