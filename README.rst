scons-tool-loader
==================

.. image:: https://badge.fury.io/py/scons-tool-loader.svg
    :target: https://badge.fury.io/py/scons-tool-loader
    :alt: PyPi package version
.. image:: https://readthedocs.org/projects/scons-tool-loader/badge/?version=latest
    :target: https://scons-tool-loader.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.org/ptomulik/scons-tool-loader.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-loader
.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-loader?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-loader
.. image:: https://coveralls.io/repos/github/ptomulik/scons-tool-loader/badge.svg?branch=master
    :target: https://coveralls.io/github/ptomulik/scons-tool-loader?branch=master
.. image:: https://api.codeclimate.com/v1/badges/4c43a53855f688da6bde/maintainability
   :target: https://codeclimate.com/github/ptomulik/scons-tool-loader/maintainability
   :alt: Maintainability

A little python package that helps loading externally managed SCons_ tools.

Installation
------------

To install module from pypi_, type

.. code-block:: shell

      pip install scons-tool-loader

or, if your project uses pipenv_:

.. code-block:: shell

      pipenv install --dev scons-tool-loader

Alternativelly, you may add this to your ``Pipfile``

.. code-block:: ini

    [dev-packages]
    scons-tool-loader = "*"

This will install a namespaced package ``sconstool.loader`` in project's
virtual environment.


Usage examples
--------------

Using tools istalled into "standard" namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The "standard" namespace for pip-managed SCons tools is assumed to be
``sconstool`` namespace. In the following examples we assume that tools are
installed as namespaced packages, under ``sconstool`` namespace. This is
exactly how all the tools developed by the original author of the
scons-tool-loader_ get installed.

For example, the following code

.. code-block:: shell

   pip install scons-tool-clang

will install ``clang`` tool as ``sconstool.clang`` package. Once installed, it
may be used in a SCons script by extending default toolpath and loading the
tool to the construction environment

.. code-block:: python

  # SConstruct
  import sconstool.loader
  sconstool.loader.extend_toolpath()
  env = Environment(tools=['default', 'sconstool.clang'])
  env.Program('test.c')


If, for some reason, fully qualified package name can't be used as the tool
name, one may use "transparent" mode when extending toolpath

.. code-block:: python

  # SConstruct
  import sconstool.loader
  sconstool.loader.extend_toolpath(transparent=True)
  env = Environment(tools=['default', 'clang'])
  env.Program('test.c')

The above code will still load the ``sconstool.clang`` tool.


Using tools installed into "non-standard" namespaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose, some tools get installed into ``vendor`` namespace. For example,
``vendor.foo`` and ``vendor.bar`` are installed somewhere under ``sys.path``.
These tools may be made visible to scons by using ``namespace`` parameter,
and ``scan``.

.. code-block:: python

  # SConstruct
  import sconstool.loader
  sconstool.loader.extend_toolpath(namespace='vendor', scan=True)
  env = Environment(tools=['default', 'sconstool.clang', 'vendor.foo', 'vendor.bar'])
  # ...


More documentation
------------------

See the `online documentation`_.

LICENSE
-------

Copyright (c) 2018-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader
.. _SCons: http://scons.org
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
.. _online documentation: https://scons-tool-loader.readthedocs.io/

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
