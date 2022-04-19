.. doctest-skip-all

****************************
Package Release Instructions
****************************

This document outlines the steps for releasing lacosmic to PyPI. This
process currently requires admin-level access to the lacosmic GitHub
repository, as it relies on the ability to commit to main directly. It
also requires a PyPI account with admin-level access for lacosmic.

These instructions assume the name of the git remote for the repo is
called ``origin``.

#. Check out the branch that you are going to release. This will usually
   be the ``main`` branch, unless you are making a bugfix release.

   For a bugfix release, check out the ``A.B.x`` branch. Use ``git
   cherry-pick <hash>`` (or ``git cherry-pick -m1 <hash>`` for merge
   commits) to backport fixes to the bugfix branch. Also, be sure to
   push all changes to the ``origin`` repo so that CI can run on the
   bugfix branch.

#. Ensure that CI tests are passing for the branch you are going to
   release. Also, ensure that Read the Docs builds are passing.

#. Locally run the tests using ``tox`` to thoroughly test the code in
   isolated environments::

        tox -e test-alldeps -- --remote-data=any
        tox -e build_docs
        tox -e linkcheck

#. Update the ``CHANGES.rst`` file to make sure that all the changes are
   listed and update the release date, which should currently be set to
   ``unreleased``, to the current date in ``yyyy-mm-dd`` format. Then
   commit the changes::

        git add CHANGES.rst
        git commit -m'Finalizing changelog for version <X.Y.Z>'

#. Remove any untracked files (WARNING: this will permanently remove any
   files that have not been previously committed, so make sure that you
   don't need to keep any of these files)::

        git clean -dfx

#. Update the package version number to the version you’re about to
   release by creating an annotated git tag (optionally signing with the
   ``-s`` option)::

        git tag -a <X.Y.Z> -m'<X.Y.Z>'
        git show <X.Y.Z>  # show the tag
        git tag  # show all tags

#. Check out the release commit::

        git checkout <X.Y.Z>

#. Make sure the `build <https://pypi.org/project/build/>`_ package is
   installed and up to date::

        pip install build --upgrade

   Then create the source distribution and its wheel with::

        python -m build --sdist --wheel .

#. Run tests on the generated source distribution by going inside the
   ``dist`` directory, expanding the tar file, going inside the expanded
   directory, and running the tests with::

        cd dist
        tar xvfz <file>.tar.gz
        cd <file>
        tox -e test-alldeps -- --remote-data=any
        tox -e build_docs

   Optionally, install and test the source distribution in a virtual
   environment::

        <install and activate virtual environment>
        pip install -e '.[all,test]'
        pytest --remote-data=any

   or::

        <install and activate virtual environment>
        pip install '../<file>*.whl[all,test]'
        cd <any-directory-outside-of-lacosmic-source>
        python
        >>> import lacosmic
        >>> lacosmic.__version__
        >>> lacosmic.test(remote_data=True)

#. Go back to the package root directory and remove the generated files
   with::

        git clean -dfx

#. Make sure the source distribution doesn't inherit limited permissions
   from your default umask::

        umask 0022
        chmod -R a+Xr .

#. Make sure the `twine <https://pypi.org/project/twine/>`_ package is
   installed and up to date::

        pip install twine --upgrade

#. Generate the source distribution and its wheel, and then upload them
   to PyPI::

        python -m build --sdist --wheel .
        twine check --strict dist/*
        twine upload dist/*

   Check that the entry on PyPI (https://pypi.org/project/lacosmic/) is
   correct, and that the tarfile is present.

#. Go back to the main branch::

    git checkout main

#. Push the released tag to the ``origin`` repo::

        git push origin <X.Y.Z>

#. Update ``CHANGES.rst``. After releasing a minor (bugfix) version,
   update its release date. After releasing a major version, add a new
   section to ``CHANGES.rst`` for the next ``x.y.z`` version, with a
   single entry ``No changes yet``, e.g.,::

       x.y.z (unreleased)
       ------------------

       - No changes yet

   Then commit the changes and push to the ``origin`` repo::

        git add CHANGES.rst
        git commit -m'Add version <x.y.z> to the changelog'
        git push origin main

#. After releasing a major version, tag this new commit with the
   development version of the next major version and push the tag to
   the ``origin`` repo. This is needed if the latest package release
   is the first bugfix release tagged on a bugfix branch (not the main
   branch)::

        git tag -a <x.y.z.dev> -m'<x.y.z.dev>'
        git push origin <x.y.z.dev>

#. Create a GitHub Release
   (https://github.com/larrybradley/lacosmic/releases) by clicking on
   "Draft a new release", select the tag of the released version, add
   a release title with the released version, and add the following
   description::

        See the [changelog](https://lacosmic.readthedocs.io/en/stable/changelog.html) for release notes.

   Then click "Publish release". This step will trigger an automatic
   update of the package on Zenodo (see below).

#. Close the GitHub Milestone
   (https://github.com/larrybradley/lacosmic/milestones) for the released
   version and, if needed, open a new Milestone for the next release.

#. Go to Read the Docs
   (https://readthedocs.org/projects/lacosmic/versions/) and check that
   the "stable" docs correspond to the new released version. Deactivate
   any older released versions (i.e., uncheck "Active").

#. Check that Zenodo is updated with the released version
   (https://doi.org/10.5281/zenodo.6468623). Zenodo is already
   configured to automatically update with a new published GitHub
   Release (see above).
