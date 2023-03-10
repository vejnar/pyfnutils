# -*- coding: utf-8 -*-

#
# Copyright © 2015 Charles E. Vejnar
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/MPL/2.0/.
#

import concurrent.futures

def run(fn, jobs, num_processor=1, return_when=concurrent.futures.FIRST_EXCEPTION):
    """
    Runs tasks in parallel using ThreadPoolExecutor.

    Args:
        fn (function): Function to execute
        jobs (list, dict or any): Defines argument of fn
        num_processor (int): Number of processor(s)
        return_when (str): Indicates when this function should return

    Returns:
        Status code (int): 0 or 130 if KeyboardInterrupt was captured
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_processor) as executor:
        # Add jobs to queue
        fs = []
        for job in jobs:
            if isinstance(job, list) or isinstance(job, tuple):
                fs.append(executor.submit(fn, *job))
            elif isinstance(job, dict):
                fs.append(executor.submit(fn, **job))
            else:
                fs.append(executor.submit(fn, job))
        # Wait
        try:
            rfs = concurrent.futures.wait(fs, return_when=return_when)
        except KeyboardInterrupt:
            for j in fs:
                j.cancel()
            executor.shutdown()
            return 130
        else:
            for t in rfs.not_done:
                t.cancel()
            for t in rfs.done:
                t.result()
    return 0
