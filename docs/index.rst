********
lacosmic
********

``lacosmic`` provides a Python function to remove cosmic rays from an
astronomical image using the `L.A.Cosmic
<http://www.astro.yale.edu/dokkum/lacosmic/>`_ algorithm.  The
algorithm is based on Laplacian edge detection and is described in
`PASP 113, 1420 (2001)`_.

.. _PASP 113, 1420 (2001): http://adsabs.harvard.edu/abs/2001PASP..113.1420V


Requirements
============

``lacosmic`` has the following strict requirements:

* `Python <http://www.python.org/>`_ 2.7, 3.3, 3.4 or 3.5

* `Numpy <http://www.numpy.org/>`_ 1.7 or later

* `Astropy`_ 1.1 or later


Installation
============

The latest released (stable) version of lacosmic can be installed with
`pip`_::

    pip install --no-deps lacosmic

.. note::

    The ``--no-deps`` flag is optional, but highly recommended if you
    already have Numpy and Astropy installed, since otherwise pip will
    sometimes try to "help" you by upgrading your Numpy and Astropy
    installations, which may not always be desired.

.. _pip: https://pip.pypa.io/en/latest/


User Documentation
==================

.. toctree::
    :maxdepth: 1

    lacosmic/index.rst
    changelog.rst
