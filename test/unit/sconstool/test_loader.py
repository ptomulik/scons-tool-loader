# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Pawel Tomulik
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

import os
import sys
import unittest
import unittest.mock as mock
import sconstool.loader as loader
import contextlib


class this_toolpath_Tests(unittest.TestCase):
    def test__without_args(self):
        tp = loader.this_toolpath()
        there = os.path.dirname(loader.__file__)
        upupthere = os.path.dirname(os.path.dirname(there))
        self.assertEqual(tp, [os.path.abspath(upupthere)])

    def test__with_transparent(self):
        tp = loader.this_toolpath(transparent=True)
        there = os.path.dirname(loader.__file__)
        upupthere = os.path.dirname(os.path.dirname(there))
        self.assertEqual(tp, [os.path.abspath(os.path.join(upupthere, 'sconstool'))])

    def test__with_namespace(self):
        tp = loader.this_toolpath(namespace='foo')
        there = os.path.dirname(loader.__file__)
        upupthere = os.path.dirname(os.path.dirname(there))
        self.assertEqual(tp, [os.path.abspath(upupthere)])

    def test__with_transparent_and_namespace(self):
        tp = loader.this_toolpath(transparent=True, namespace='foo')
        there = os.path.dirname(loader.__file__)
        upupthere = os.path.dirname(os.path.dirname(there))
        self.assertEqual(tp, [os.path.abspath(os.path.join(upupthere, 'foo'))])

class existsing_toolpath_dirs_Tests(unittest.TestCase):

    def existing_dirs(self, namespace='sconstool'):
        return [
            '/existing/dir/one',        '/existing/dir/one/%s' % namespace,
            '/existing/dir/two',        # no sconstool within it
            '/another/existing/dir',    '/another/existing/dir/%s' % namespace,
        ]

    def fake_isdir(self, namespace='sconstool'):
        return lambda path: path in self.existing_dirs(namespace)

    def test__without_args(self):
        syspath = [ '/existing/dir/one', '/existing/dir/two', '/inexistent/dir' ]
        with mock.patch('sys.path', new=syspath), \
             mock.patch('os.path.isdir', side_effect = self.fake_isdir()):
            self.assertEqual(loader.existing_toolpath_dirs(), ['/existing/dir/one'])

    def test__with_transparent(self):
        syspath = [ '/existing/dir/one', '/existing/dir/two', '/inexistent/dir' ]
        with mock.patch('sys.path', new=syspath), \
             mock.patch('os.path.isdir', side_effect = self.fake_isdir()):
            self.assertEqual(loader.existing_toolpath_dirs(transparent=True), ['/existing/dir/one/sconstool'])

    def test__with_namespace(self):
        syspath = [ '/existing/dir/one', '/existing/dir/two', '/inexistent/dir' ]
        with mock.patch('sys.path', new=syspath), \
             mock.patch('os.path.isdir', side_effect = self.fake_isdir(namespace='foo')):
            self.assertEqual(loader.existing_toolpath_dirs(namespace='foo'), ['/existing/dir/one'])
            self.assertEqual(loader.existing_toolpath_dirs(namespace='bar'), [])

    def test__with_transparent_and_namespace(self):
        syspath = [ '/existing/dir/one', '/existing/dir/two', '/inexistent/dir' ]
        with mock.patch('sys.path', new=syspath), \
             mock.patch('os.path.isdir', side_effect = self.fake_isdir(namespace='foo')):
            self.assertEqual(loader.existing_toolpath_dirs(transparent=True, namespace='foo'), ['/existing/dir/one/foo'])
            self.assertEqual(loader.existing_toolpath_dirs(transparent=True, namespace='bar'), [])

    def test__with_transparent_namespace_and_path(self):
        syspath = [ '/existing/dir/one', '/existing/dir/two', '/inexistent/dir' ]
        with mock.patch('os.path.isdir', side_effect = self.fake_isdir(namespace='foo')):
            scan_dirs = syspath + ['/another/existing/dir']
            self.assertEqual(loader.existing_toolpath_dirs(transparent=True, namespace='foo', scan_dirs=scan_dirs), ['/existing/dir/one/foo', '/another/existing/dir/foo'])
            self.assertEqual(loader.existing_toolpath_dirs(transparent=True, namespace='bar', scan_dirs=scan_dirs), [])

class toolpath_Tests(unittest.TestCase):
    def existing_dirs(self, namespace='sconstool'):
        return [
            '/existing/dir/one',        '/existing/dir/one/%s' % namespace,
            '/existing/dir/two',        # no sconstool within it
            '/another/existing/dir',    '/another/existing/dir/%s' % namespace,
        ]

    def fake_isdir(self, namespace='sconstool'):
        return lambda path: path in self.existing_dirs(namespace)

    def test__without_scan(self):
        self.assertEqual(loader.toolpath(), loader.this_toolpath())
        self.assertEqual(loader.toolpath(transparent=True), loader.this_toolpath(transparent=True))
        self.assertEqual(loader.toolpath(namespace='foo'), loader.this_toolpath(namespace='foo'))
        self.assertEqual(loader.toolpath(transparent=True, namespace='foo'), loader.this_toolpath(transparent=True, namespace='foo'))
        self.assertEqual(loader.toolpath(this=False), [])
        self.assertEqual(loader.toolpath(transparent=True, this=False), [])
        self.assertEqual(loader.toolpath(transparent=True, namespace='foo', this=False), [])

    def test__with_scan(self):
        syspath = [ '/existing/dir/one', '/existing/dir/two', '/inexistent/dir' ]
        with mock.patch('sys.path'), \
             mock.patch('os.path.isdir', side_effect = self.fake_isdir()):
            sys.path = syspath
            for kw in [
                            {},
                            {'transparent': True},
                            {'namespace': 'foo'},
                            {'transparent': True, 'namespace': 'foo'}
                      ]:
                self.assertEqual(loader.toolpath(scan=True, **kw), loader.this_toolpath(**kw) + loader.existing_toolpath_dirs(**kw))
                self.assertEqual(loader.toolpath(scan=True, this=False, **kw), loader.existing_toolpath_dirs(**kw))

class extend_toolpath_Tests(unittest.TestCase):
    def existing_dirs(self, namespace='sconstool'):
        return [
            '/existing/dir/one',        '/existing/dir/one/%s' % namespace,
            '/existing/dir/two',        # no sconstool within it
            '/another/existing/dir',    '/another/existing/dir/%s' % namespace,
        ]

    def fake_isdir(self, namespace='sconstool'):
        return lambda path: path in self.existing_dirs(namespace)

    @contextlib.contextmanager
    def default_toolpath(self, defaultToolpath):
        with mock.patch.object(loader, 'SCons', create=True), \
             mock.patch.object(loader.SCons, 'Tool', create=True), \
             mock.patch.object(loader.SCons.Tool, 'DefaultToolpath', create=True, new=defaultToolpath) as d:
                 yield d

    def test__all(self):
        for kw in [
                        {},
                        {'transparent': True},
                        {'namespace': 'foo'},
                        {'this': False},
                        {'scan': True},
                        {'transparent': True, 'namespace': 'foo'},
                        {'transparent': True, 'this': False},
                        {'transparent': True, 'scan': True},
                        {'transparent': True, 'namespace': 'foo', 'this': False},
                        {'transparent': True, 'namespace': 'foo', 'scan': True},
                        {'transparent': True, 'namespace': 'foo', 'this': False, 'scan': True},
                  ]:
            with mock.patch('sconstool.loader._have_scons', new=True), \
                 self.default_toolpath(['/default/toolpath']):
                msg =  ("extend_toolpath(%s)" % ', '.join([("%s=%s" % (k, repr(v))) for k,v in kw.items()]))
                retval = loader.extend_toolpath(**kw)
                retval_expect = loader.toolpath(**kw)
                self.assertEqual(retval, retval_expect, msg)
                side = loader.SCons.Tool.DefaultToolpath
                side_expect = ['/default/toolpath'] + retval_expect
                self.assertEqual(side, side_expect, msg)

    def test__warning(self):
        with self.default_toolpath(['/default/toolpath']), \
             mock.patch('sconstool.loader._have_scons', new=False), \
             mock.patch('warnings.warn') as warn:
                 self.assertEqual(loader.extend_toolpath(), loader.toolpath())
                 self.assertEqual(loader.SCons.Tool.DefaultToolpath, ['/default/toolpath']) # no side effects
                 warn.assert_called_once_with("No SCons available. Can't extend SCons.Tool.DefaultToolpath.")


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
