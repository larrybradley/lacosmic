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


Reference/API
=============

.. automodapi:: lacosmic
