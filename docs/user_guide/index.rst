Getting Started
===============

Introduction
------------

``lacosmic`` is a Python package to remove cosmic
rays from an astronomical image using the `L.A.Cosmic
<http://www.astro.yale.edu/dokkum/lacosmic/>`_ algorithm.
The algorithm is based on Laplacian edge detection
and is described in `van Dokkum 2001 (PASP 113, 1420)
<https://ui.adsabs.harvard.edu/abs/2001PASP..113.1420V/abstract>`_.


Preliminaries
-------------

Let’s start by making a synthetic image with cosmic rays::

    >>> from lacosmic.utils import make_cosmic_rays, make_gaussian_sources
    >>> shape = (512, 512)
    >>> data, error = make_gaussian_sources(shape, seed=0)
    >>> cr_img = make_cosmic_rays(shape, n_cosmics=200, seed=0)
    >>> data2 = data + cr_img

Let's visualize the image with cosmic rays:

.. plot::

    import matplotlib.pyplot as plt
    from astropy.visualization import simple_norm
    from lacosmic.utils import make_cosmic_rays, make_gaussian_sources

    shape = (512, 512)
    data, error = make_gaussian_sources(shape, seed=0)
    norm = simple_norm(data, 'sqrt', percent=99.5)
    cr_img = make_cosmic_rays(shape, n_cosmics=200, seed=0)
    data2 = data + cr_img

    fig, ax = plt.subplots()
    axim = ax.imshow(data2, norm=norm, origin='lower')
    plt.tight_layout()
    plt.show()


Removing Cosmic Rays
--------------------

Now we can use the :func:`~lacosmic.remove_cosmics` function to identify
and remove the cosmic rays. There are several parameters that can be
adjusted to optimize the detection of cosmic rays. Please refer to
the :func:`~lacosmic.remove_cosmics` API documentation for details on
the available parameters. Here, we will input simple values for the
``contrast``, ``cr_threshold``, and ``neighbor_threshold`` along with an
``error`` array:

.. doctest-skip::

    >>> from lacosmic import remove_cosmics
    >>> clean_img, cr_mask = remove_cosmics(data2, 1, 5, 5, error=error)

``clean_img`` is the cleaned image with cosmic rays removed, and
``cr_mask`` is a boolean mask indicating the locations of the detected
cosmic rays.

Now let’s visualize the results:

.. plot::

    import matplotlib.pyplot as plt
    from astropy.visualization import simple_norm
    from lacosmic import remove_cosmics
    from lacosmic.utils import make_cosmic_rays, make_gaussian_sources

    # Create synthetic data
    shape = (512, 512)
    data, error = make_gaussian_sources(shape, seed=0)
    norm = simple_norm(data, 'sqrt', percent=99.5)
    cr_img = make_cosmic_rays(shape, n_cosmics=200, seed=0)
    data2 = data + cr_img

    # Remove cosmic rays
    clean_img, cr_mask = remove_cosmics(data2, 1, 5, 5, error=error)

    # True cosmic ray mask for comparison
    true_crmask = cr_img > 0

    # Plotting
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    ax = ax.ravel()
    ax[0].imshow(data, norm=norm)
    ax[0].set_title('Synthetic Data')
    ax[1].imshow(data2, norm=norm)
    ax[1].set_title('Synthetic Data with Cosmic Rays')
    ax[2].imshow(clean_img, norm=norm)
    ax[2].set_title('CR-cleaned Data')
    ax[3].imshow(cr_mask)
    ax[3].set_title('Cosmic Ray mask')

    plt.tight_layout()
    plt.show()

The top row shows the synthetic image without and with cosmic rays. The
bottom row shows the cleaned image and the detected cosmic ray mask.
While this is a simple example, you can see that the cosmic rays have
been successfully identified and removed from the image.


API Documentation
-----------------

.. automodapi:: lacosmic
   :no-heading:
   :no-main-docstr:
