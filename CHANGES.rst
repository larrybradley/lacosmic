1.5.0 (unreleased)
------------------

General
^^^^^^^

New Features
^^^^^^^^^^^^

Bug Fixes
^^^^^^^^^

API Changes
^^^^^^^^^^^


1.4.0 (2026-01-20)
------------------

General
^^^^^^^

- The minimum required NumPy version is 2.0. [#59]

- The minimum required SciPy version is 1.13. [#59]

- The minimum required Astropy version is 6.1. [#59]

API Changes
^^^^^^^^^^^

- The ``lacosmic`` function has been renamed to ``remove_cosmics``.
  The ``lacosmic`` function is still available as an alias for backward
  compatibility, but it is deprecated and will be removed in a future
  release. [#72]


1.3.0 (2025-07-07)
------------------

General
^^^^^^^

- The ``lacosmic.test`` function has been removed. Instead, use the
  ``pytest --pyarg lacosmic`` command. [#25]

- The minimum required Python version is 3.11. [#26, #47]

- The minimum required NumPy version is 1.26. [#26, #47]

- The minimum required SciPy version is 1.12. [#26, #47]

- The minimum required Astropy version is 6.0. [#26, #47, #49]


1.2.0 (2025-07-07)
------------------

General
^^^^^^^

- Version 1.2.0 was yanked from PyPI due to a packaging error.


1.1.0 (2023-11-16)
------------------

General
^^^^^^^

- The minimum required Python version is 3.9. [#19]

- The minimum required NumPy version is 1.22. [#19]

- The minimum required SciPy version is 1.7.2. [#19]

- The minimum required Astropy version is 5.0. [#19]

- The project metadata is now stored in ``pyproject.toml`` (PEP 621).
  [#19]


1.0.0 (2022-04-19)
------------------

General
^^^^^^^

- The minimum required Python version is 3.8. [#11]

- The minimum required NumPy version is 1.18. [#11]

- The minimum required SciPy version is 1.6.0. [#11]

- The minimum required Astropy version is 4.1. [#11]


0.1.1 (2016-08-16)
------------------

- Initial release.
