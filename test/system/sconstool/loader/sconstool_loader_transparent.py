#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import TestSCons
import re
import sys

if sys.platform == 'win32':
    test = TestSCons.TestSCons(program='scons.bat', interpreter=None)
else:
    test = TestSCons.TestSCons()

test.write('SConstruct', r"""\
from sconstool.loader import extend_toolpath
extend_toolpath(scan=True, scan_dirs=['vendor'], transparent=True)
env = Environment(tools=['foo'])
env.Foo('xxx')
""" % locals())

test.write('xxx.foi', r"""This is input""")

_python_ = TestSCons._python_
_workpath_ = test.workpath()

_init_py = test.workpath('vendor/sconstool/foo/__init__.py')
_build_py_ = test.workpath('vendor/sconstool/foo/build.py')

test.subdir(['vendor'])
test.subdir(['vendor', 'sconstool'])
test.subdir(['vendor', 'sconstool', 'foo'])

test.write(_init_py, r"""\
import SCons.Builder

def generate(env):
    env['FOOCMD'] = r"%(_python_)s %(_build_py_)s $TARGET $SOURCE"
    env['BUILDERS']['Foo'] = SCons.Builder.Builder(action = "$FOOCMD", suffix='.foo', src_suffix='.foi')

def exists(env):
    return 1
""" % locals())

test.write(_build_py_, r"""\
import sys
with open(sys.argv[2], 'r') as i, open(sys.argv[1], 'w') as o:
    c = i.read().replace('input', 'vendor output')
    o.write(c)
""")


test.run(['-Q'])

test.must_exist('xxx.foo')
test.must_contain('xxx.foo', r"""This is vendor output""")

test.run(['-Q', '-c'])

test.must_not_exist('xxx.foo')

### Local site_tools should be preferred over the external ones ###

_build_py_ = test.workpath('site_scons/site_tools/foo/build.py')
_init_py = test.workpath('site_scons/site_tools/foo/__init__.py')

test.subdir(['site_scons'])
test.subdir(['site_scons', 'site_tools'])
test.subdir(['site_scons', 'site_tools', 'foo'])

test.write(_init_py, r"""\
import SCons.Builder

def generate(env):
    env['FOOCMD'] = r"%(_python_)s %(_build_py_)s $TARGET $SOURCE"
    env['BUILDERS']['Foo'] = SCons.Builder.Builder(action = "$FOOCMD", suffix='.foo', src_suffix='.foi')

def exists(env):
    return 1
""" % locals())

test.write(_build_py_, r"""\
import sys
with open(sys.argv[2], 'r') as i, open(sys.argv[1], 'w') as o:
    c = i.read().replace('input', 'site output')
    o.write(c)
""")

test.run(['-Q'])

test.must_exist('xxx.foo')
test.must_contain('xxx.foo', r"""This is site output""")

test.run(['-Q', '-c'])

test.must_not_exist('xxx.foo')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
