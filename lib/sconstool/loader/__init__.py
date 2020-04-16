# -*- coding: utf-8 -*-
"""Main package.

A little package that helps loading SCons tools installed via pip.
"""

#
# Copyright (c) 2018-2020 by Paweł Tomulik
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
import warnings

from . import about

__version__ = about.__version__
"""Version of the package as a string."""


__all__ = ('this_toolpath',
           'existing_toolpath_dirs',
           'toolpath',
           'extend_toolpath')

_ns = 'sconstool'


def _tp(path, transparent=False, namespace=_ns):
    if transparent:
        return os.path.abspath(os.path.join(path, namespace))
    else:
        return os.path.abspath(path)


def _append_uniq_path(sequence, value):
    if value not in sequence:
        sequence.append(value)


def this_toolpath(transparent=False, namespace=_ns):
    """Returns toolpath related to this loader's installation.

    :example: Usage of :func:`.this_toolpath`.

    .. code-block:: python

        import sconstool.loader as loader

        # assume sconstool.loader installed in:
        #   "/my/virtualenv/lib/python3.6/site-packages/sconstool/loader"

        print(loader.this_toolpath())
        # output:
        # ["/my/virtualenv/lib/python3.6/site-packages"]

        print(loader.this_toolpath(transparent=True))
        # output:
        # ["/my/virtualenv/lib/python3.6/site-packages/sconstool"]

        print(loader.this_toolpath(transparent=True, namespace="foo"))
        # output:
        # ["/my/virtualenv/lib/python3.6/site-packages/foo"]


    :param bool transparent:
        whether to append **namespace** to every path of the generated toolpath
        list,
    :param str namespace:
        if **transparent** is true, **namespace** will be appended to every
        path of the generated toolpath list. Defaults to ``'sconstool'``,
    :rtype: list
    """
    here = os.path.abspath(os.path.dirname(__file__))
    dirname = os.path.dirname
    return [_tp(dirname(dirname(here)), transparent, namespace)]


def existing_toolpath_dirs(transparent=False, namespace=_ns, scan_dirs=None):
    """Returns a list of toolpath directories for existing directories from
    **scan_dirs**, or ``sys.path``.

    :example: Usage example for :func:`.existing_toolpath_dirs`

    .. code-block:: python

        import sys
        import sconstool.loader
        sys.path = ['/path/one', '/path/three']

        # assume '/path/one/sconstool' and '/path/two/sconstool' exist
        # and '/path/three' exists but there is no '/path/three/sconstool'

        print(sconstool.loader.existing_toolpath_dirs())
        # output: ['/path/one']

        print(sconstool.loader.existing_toolpath_dirs(transparent=True))
        # output: ['/path/one/sconstool']

        dirs = ['/path/one', '/path/two', '/path/three']
        print(sconstool.loader.existing_toolpath_dirs(scan_dirs=dirs))
        # output: ['/path/one', '/path/two']

    :param bool transparent:
        whether to append **namespace** to every path of the generated toolpath
        list,
    :param str namespace:
        if **transparent** is true, **namespace** will be appended to every
        path of the generated toolpath list. Defaults to ``'sconstool'``,
    :param list scan_dirs:
        list of paths to be examined. If ``None``, the ``sys.path`` is used.
    :rtype: list
    """
    dirs = []
    if scan_dirs is None:
        scan_dirs = sys.path
    for p in scan_dirs:
        if os.path.isdir(os.path.join(p, namespace)):
            _append_uniq_path(dirs, _tp(p, transparent, namespace))
    return dirs


def toolpath(transparent=False, namespace=_ns, this=True, scan=False,
             scan_dirs=None):
    """Returns a list of toolpath directories.

    The returned list mixes path lists from both: :func:`.this_toolpath` and
    :func:`existing_toolpath_dirs` for the given arguments.

    :param bool transparent:
        whether to append **namespace** to every path of the generated toolpath
        list,
    :param str namespace:
        if **transparent** is true, **namespace** will be appended to every
        path of the generated toolpath list. Defaults to ``'sconstool'``,
    :param bool this:
        include toolpath related to this loader installation. Defaults to
        ``True``,
    :param bool scan:
        also scan for existing directories from **scan_dirs** or ``sys.path``.
        Defaults to ``False``,
    :param list scan_dirs:
        list of paths to be examined if **scan** is ``True``. If ``None``
        given, and **scan** is ``True``, ``sys.path`` is examined. Defaults to
        ``None``.
    :rtype: list
    """
    tp = []
    if scan:
        tp = tp + existing_toolpath_dirs(transparent, namespace, scan_dirs)
    if this:
        tp = this_toolpath(transparent, namespace) + tp
    return tp


try:
    import SCons.Tool
except ImportError:
    _have_scons = False
else:
    _have_scons = True


def extend_toolpath(transparent=False, namespace=_ns, this=True, scan=False,
                    scan_dirs=None):
    """Appends to the default toolpath list the paths returned by
    :func:`toolpath` for the given arguments.

    .. note:: This function modifies the variable
             ``SCons.Tool.DefaultToolpath``.

    :param bool transparent:
        whether to append **namespace** to every path of the generated
        toolpath list,
    :param str namespace:
        if **transparent** is true, **namespace** will be appended to every
        path of the generated toolpath list. Defaults to ``'sconstool'``,
    :param bool this:
        include toolpath related to this loader installation. Defaults to
        ``True``,
    :param bool scan:
        also scan for existing directories from **scan_dirs** or ``sys.path``.
        Defaults to ``False``,
    :param list scan_dirs:
        list of paths to be examined if **scan** is ``True``. If ``None``
        given, and **scan** is ``True``, ``sys.path`` is examined. Defaults to
        ``None``.
    :rtype: list
    """
    tp = toolpath(transparent, namespace, this, scan, scan_dirs)
    if _have_scons:
        SCons.Tool.DefaultToolpath.extend(tp)
    else:
        warnings.warn("No SCons available. " +
                      "Can't extend SCons.Tool.DefaultToolpath.")
    return tp


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
