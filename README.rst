scons-tool-loader
==================

.. image:: https://badge.fury.io/py/scons-tool-loader.svg
    :target: https://badge.fury.io/py/scons-tool-loader
    :alt: PyPi package version

A little module that supports loading SCons_ tools installed via pip.

Installation
------------

To install module from pypi_, type

.. code-block:: shell

      pip install scons-tool-loader

or, if your project uses pipenv_:

.. code-block:: shell

      pipenv install --dev scons-tool-loader

Alternativelly, you may add this to your ``Pipfile``

.. code-block::

    [dev-packages]
    scons-tool-loader = "*"

This will install a namespaced package ``sconstool.loader`` in project's
virtual environment.


Usage example
-------------

.. code-block:: python

  # SConstruct
  import sconstool.loader
  sconstool.loader.extend_toolpath()
  # provided that scons-tool-clang is installed...
  env = Environment(tools = ['default', 'sconstool.clang'])
  print(env.subst("using $CC $CCVERSION"))
  env.Program('test.c')

LICENSE
-------

Copyright (c) 2018 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>

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

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
