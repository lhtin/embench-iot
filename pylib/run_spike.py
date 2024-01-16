#!/usr/bin/env python3

# Python module to run programs natively.

# Copyright (C) 2019 Clemson University
#
# Contributor: Ola Jeppsson <ola.jeppsson@gmail.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Embench module to run benchmark programs.

This version is suitable for running programs natively.
"""

__all__ = [
    'get_target_args',
    'build_benchmark_cmd',
    'decode_results',
]

import argparse
import re

from embench_core import log


def get_target_args(remnant):
    """Parse left over arguments"""
    parser = argparse.ArgumentParser(description='Get target specific args')

    parser.add_argument(
        '--spike',
        type=str,
        required=True,
        help='spike path'
    )

    parser.add_argument(
        '--pk',
        type=str,
        default="",
        required=False,
        help='pk path'
    )

    # No target arguments
    return parser.parse_args(remnant)


def build_benchmark_cmd(bench, args):
    """Construct the command to run the benchmark.  "args" is a
       namespace with target specific arguments"""

    run = f"{args.spike} --isa=rv64gc_zicntr_zihpm"
    if args.pk:
        run += f" {args.pk}"

    # Due to way the target interface currently works we need to construct
    # a command that records both the return value and execution time to
    # stdin/stdout. Obviously using time will not be very precise.
    return ['sh', '-c', f'{run} {bench}; echo RET=$?']


def decode_results(stdout_str, stderr_str):
    """Extract the results from the output string of the run. Return the
       cycles or zero if the run failed."""

    # Match "RET=rc"
    rcstr = re.search('^RET=(\d+)', stdout_str, re.S | re.M)
    if not rcstr:
        log.debug('Warning: Failed to find return code')
        return 0

    # Match "real s.mm?m?"
    cycle = re.search(r'^Total cycle: (\d+)', stdout_str, re.S | re.M)
    if cycle:
        return int(cycle.group(1))

    # We must have failed to find a time
    log.debug('Warning: Failed to find timing')
    return 0
