# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Documentation build configuration file.
"""

import os
import tomllib
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path

# Get configuration information from pyproject.toml
with (Path(__file__).parents[1] / 'pyproject.toml').open('rb') as fh:
    project_meta = tomllib.load(fh)['project']

# -- General configuration ----------------------------------------------------
# By default, highlight as Python 3.
highlight_language = 'python3'

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'py:obj'

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '8.2'  # keep in sync with pyproject.toml

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_automodapi.automodapi',
    'sphinx_copybutton',
    'matplotlib.sphinxext.plot_directive',
    'numpydoc',
    'pytest_doctestplus.sphinx.doctestplus',
    'sphinx_astropy.ext.changelog_links',
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
root_doc = 'index'

# -- Intersphinx configuration ------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'astropy': ('https://docs.astropy.org/en/stable/', None),
}

# -- numpydoc configuration ---------------------------------------------------
numpydoc_show_class_members = False

# -- Project information ------------------------------------------------------
project = project_meta['name']
author = project_meta['authors'][0]['name']
project_copyright = f'2014-{datetime.now(tz=UTC).year}, {author}'
github_project = 'larrybradley/lacosmic'

# The version info for the project you're documenting, acts as
# replacement for |version| and |release|, also used in various other
# places throughout the built documents.

# The full version, including alpha/beta/rc tags.
release = metadata.version(project)
# The short X.Y version.
version = '.'.join(release.split('.')[:2])
dev = 'dev' in release

# -- Options for HTML output --------------------------------------------------
html_static_path = ['_static']
html_css_files = ['custom.css']
html_title = f'{project} {release}'
html_favicon = '_static/favicon.ico'

html_theme = 'pydata_sphinx_theme'
html_show_sourcelink = False

# Remove (left) sidebars
html_sidebars = {
    '**': [],
}

html_theme_options = {
    'show_toc_level': 2,
    'navbar_align': 'left',
    'use_edit_page_button': False,
    'logo': {'text': 'lacosmic', 'alt_text': 'lacosmic'},
    'icon_links': [
        {'name': 'GitHub',
         'url': 'https://github.com/larrybradley/lacosmic',
         'icon': 'fa-brands fa-github',
         'type': 'fontawesome',
         },
    ],
}

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# Set canonical URL from the Read the Docs Domain
html_baseurl = os.environ.get('READTHEDOCS_CANONICAL_URL', '')

# A dictionary of values to pass into the template engine's context for
# all pages.
html_context = {
    'default_mode': 'light',
    'to_be_indexed': ['stable', 'latest'],
    'is_development': dev,
    'github_user': 'larrybradley',
    'github_repo': 'lacosmic',
    'github_version': 'main',
    'doc_path': 'docs',
    # Tell Jinja2 templates the build is running on Read the Docs
    'READTHEDOCS': os.environ.get('READTHEDOCS', '') == 'True',
}

# -- Options for LaTeX output -------------------------------------------------
# Grouping the document tree into LaTeX files. List of tuples (source
# start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + ' Documentation',
                    author, 'manual')]

# -- Options for manual page output -------------------------------------------
# One entry per manual page. List of tuples (source start file, name,
# description, authors, manual section).
man_pages = [('index', project.lower(), project + ' Documentation',
              [author], 1)]

# -- Resolving issue number to links in changelog -----------------------------
github_issues_url = f'https://github.com/{github_project}/issues/'

# -- Turn on nitpicky mode for sphinx (to warn about references not found) ----
nitpicky = True
nitpick_ignore = []

# Some warnings are impossible to suppress, and you can list specific
# references that should be ignored in a nitpick-exceptions file which
# should be inside the docs/ directory. The format of the file should be:
#
# <type> <class>
#
# for example:
#
# py:class astropy.io.votable.tree.Element
# py:class astropy.io.votable.tree.SimpleElement
# py:class astropy.io.votable.tree.SimpleElementWithContent
#
# Uncomment the following lines to enable the exceptions:
nitpick_filename = 'nitpick-exceptions.txt'
if os.path.isfile(nitpick_filename):
    with open(nitpick_filename) as fh:
        for line in fh:
            if line.strip() == '' or line.startswith('#'):
                continue
            dtype, target = line.split(None, 1)
            target = target.strip()
            nitpick_ignore.append((dtype, target))

# -- Options for linkcheck output ---------------------------------------------
linkcheck_retry = 5
linkcheck_ignore = ['http://data.astropy.org',
                    r'https://github\.com/larrybradley/lacosmic/(?:issues|pull)/\d+']
linkcheck_timeout = 180
