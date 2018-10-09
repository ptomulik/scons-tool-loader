# -*- coding: utf-8 -*-
"""scons-tool-loader
"""

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
        name='scons-tool-loader',
        version='0.1.4',
        package_dir={'': 'lib'},
        packages=['sconstool.loader'],
        namespace_packages=['sconstool'],
        description='A little module that helps loading SCons tools installed via pip',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/ptomulik/scons-tool-loader',
        author='Paweł Tomulik',
        author_email='ptomulik@meil.pw.edu.pl'
)

# vim: set expandtab tabstop=4 shiftwidth=4:
