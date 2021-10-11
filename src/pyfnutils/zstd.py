# -*- coding: utf-8 -*-

#
# Copyright (C) 2017-2021 Charles E. Vejnar
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/MPL/2.0/.
#

import os
import subprocess

def open(filename, mode='rb'):
    """
    Opens file compressed with Zstandard (https://facebook.github.io/zstd) using command-line zstd.

    Args:
        filename (str): Absolute or relative to the current working directory path to file
        mode (str): See open() in Python standard library (limited to r, w, t, and b values)

    Returns:
        File object
    """
    if mode == 'r' or mode == 'rb':
        p = subprocess.Popen(['zstd', '-d', '-f', '-c', filename], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return p.stdout
    elif mode == 'rt':
        p = subprocess.Popen(['zstd', '-d', '-f', '-c', filename], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
        return p.stdout
    elif mode == 'w' or mode == 'wb':
        assert not os.path.exists(filename), 'File already exists: %s'%filename
        p = subprocess.Popen(['zstd', '-', '-o', filename], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return p.stdin
    elif mode == 'wt':
        assert not os.path.exists(filename), 'File already exists: %s'%filename
        p = subprocess.Popen(['zstd', '-', '-o', filename], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, universal_newlines=True)
        return p.stdin
    else:
        raise ValueError('Invalid mode')
