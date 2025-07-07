********
lacosmic
********

``lacosmic`` is a Python package to remove cosmic rays from an
astronomical image using the `L.A.Cosmic algorithm
<http://www.astro.yale.edu/dokkum/lacosmic/>`_.  The algorithm is
based on Laplacian edge detection and is described in `van Dokkum
(2001; PASP 113, 1420)
<https://ui.adsabs.harvard.edu/abs/2001PASP..113.1420V/abstract>`_.


Requirements
============

``lacosmic`` has the following requirements:

* `Python <https://www.python.org/>`_ 3.11 or later

* `NumPy <https://numpy.org/>`_ 1.26 or later

* `SciPy <https://scipy.org/>`_ 1.12 or later

* `Astropy`_ 6.0 or later


Installation
============

The latest released (stable) version of lacosmic can be installed with
`pip`_::

    pip install lacosmic

.. _pip: https://pip.pypa.io/en/latest/


User Documentation
==================

.. automodapi:: lacosmic
    :no-heading:


Changelog
=========

.. toctree::
    :maxdepth: 1

    changelog.rst


Developer Documentation
=======================

.. toctree::
    :maxdepth: 1

    dev/releasing.rst
