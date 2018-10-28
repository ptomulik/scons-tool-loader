# -*- coding: utf-8 -*-
"""scons-tool-loader
"""

from setuptools import setup
import os
import sys

if sys.version_info < (3, 0):
    from io import open as uopen
else:
    uopen = open

here = os.path.abspath(os.path.dirname(__file__))

readme_rst = os.path.join(here, 'README.rst')
with uopen(readme_rst, encoding='utf-8') as f:
    readme = f.read()

about = {}
about_py = os.path.join(here, 'lib', 'sconstool', 'loader', 'about.py')
with open(about_py) as f:
    exec(f.read(), about)

setup(
        name='scons-tool-loader',
        version=about['__version__'],
        package_dir={'': 'lib'},
        packages=['sconstool.loader'],
        namespace_packages=['sconstool'],
        description='A little module that helps loading SCons tools ' +
                    'installed via pip',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/ptomulik/scons-tool-loader',
        author='Paweł Tomulik',
        author_email='ptomulik@meil.pw.edu.pl'
)

# vim: set expandtab tabstop=4 shiftwidth=4:
