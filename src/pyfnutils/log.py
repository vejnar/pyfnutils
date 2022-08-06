# -*- coding: utf-8 -*-

#
# Copyright (C) 2011-2022 Charles E. Vejnar
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/MPL/2.0/.
#

import logging
import sys
import traceback

def define_root_logger(logger_name, std=None, filename=None, lformat=None, level=None, log_uncaught=None):
    """
    Initializes a logger using Python standard library logging.

    Args:
        logger_name (str): Logger name
        std (bool): Log to stdout
        filename (str): Log to filename
        lformat (str): Log with lformat
        level (str): Log level
        log_uncaught (bool): Uncaught exceptions logging

    Returns:
        Logger
    """
    # Parameters
    if std is None:
        std = True
    if lformat is None:
        lformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if level is None:
        level = logging.DEBUG
    else:
        level = level.upper()
    if log_uncaught is None:
        log_uncaught = False

    # Construct the logger
    logger = logging.getLogger()
    logger.name = logger_name
    logger.setLevel(level)
    if std:
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(logging.Formatter(lformat))
        logger.addHandler(console)
    if filename:
        filel = logging.FileHandler(filename)
        filel.setLevel(level)
        filel.setFormatter(logging.Formatter(lformat))
        logger.addHandler(filel)

    # Add uncaught exceptions logging
    if log_uncaught:
        def catch_exception(logger, typ, value, tback):
            logger.critical(''.join(traceback.format_exception(typ, value, tback)))
        eh = lambda typ, value, tback: catch_exception(logger, typ, value, tback)
        sys.excepthook = eh

    return logger
