
.. |br| raw:: html

    <div style="min-height:0.1em;"></div>

********
lacosmic
********

| **Version**: |release|
| **Date**: |today|

``lacosmic`` is a Python package to remove cosmic
rays from an astronomical image using the `L.A.Cosmic
<http://www.astro.yale.edu/dokkum/lacosmic/>`_ algorithm.
The algorithm is based on Laplacian edge detection
and is described in `van Dokkum 2001 (PASP 113, 1420)
<https://ui.adsabs.harvard.edu/abs/2001PASP..113.1420V/abstract>`_.

.. admonition:: Important

    If you use ``lacosmic`` for a project that leads to a
    publication, please include a citation to the `Zenodo record
    <https://doi.org/10.5281/zenodo.6468623>`_.

|br|


Installation
============

Requirements
------------

``lacosmic`` has the following runtime dependencies:

* `Python <https://www.python.org/>`_ 3.11 or later

* `NumPy <https://numpy.org/>`_ 2.0 or later

* `SciPy <https://scipy.org/>`_ 1.13 or later

* `Astropy <https://www.astropy.org/>`_ 6.1 or later


Installing the latest released version
--------------------------------------

The latest released version can be installed with
`pip`_::

    python -m pip install lacosmic

.. _pip: https://pip.pypa.io/en/latest/


User Guide
==========

.. toctree::
    :maxdepth: 1

    Getting Started <user_guide/index>

.. toctree::
    :maxdepth: 1
    :hidden:

    Development <development/releasing>
    Release Notes <changelog>
