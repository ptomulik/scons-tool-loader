# -*- coding: utf-8 -*-
"""sconstool.loader

A little package that helps loading SCons tools installed via pip.
"""

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

import sys
import os

__all__ = ('this_toolpath', 'find_toolpath', 'toolpath', 'extend_toolpath')

def _tp(path, **kw):
    ns = kw.get('namespace', 'sconstool')
    if kw.get('transparent'):
        return os.path.abspath(os.path.join(path, ns))
    else:
        return os.path.abspath(path)

def this_toolpath(**kw):
    here = os.path.abspath(os.path.dirname(__file__))
    return [_tp(os.path.dirname(os.path.dirname(here)), **kw)]

def find_toolpath(**kw):
    path = []
    ns = kw.get('namespace', 'sconstool')
    for p in kw.get('path', sys.path):
        if os.path.isdir(os.path.join(p, ns)):
            tp = _tp(p, **kw)
            if not tp in path:
                path.append(tp)
    return path

def toolpath(**kw):
    path = []
    if kw.get('find', False):
        path = path + find_toolpath(**kw)
    if kw.get('this', True):
        path = this_toolpath(**kw) + path
    return path

try:
    import SCons.Tool
except ImportError:
    pass
else:
    def extend_toolpath(**kw):
        SCons.Tool.DefaultToolpath.extend(toolpath(**kw))

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
