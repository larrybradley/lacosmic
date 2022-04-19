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

* `Python <https://www.python.org/>`_ 3.8 or later

* `Numpy <https://numpy.org/>`_ 1.18 or later

* `Scipy <https://scipy.org/>`_ 1.6.0 or later

* `Astropy`_ 4.1 or later

``lacosmic`` also depends on `pytest-astropy
<https://github.com/astropy/pytest-astropy>`_ (0.4 or later) to run the
test suite.


Installation
============

The latest released (stable) version of lacosmic can be installed with
`pip`_::

    pip install lacosmic

If you want to make sure that none of your existing dependencies get
upgraded, instead you can do::

    pip install lacosmic --no-deps

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
