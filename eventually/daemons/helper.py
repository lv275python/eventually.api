"""
Daemon utils
=============

This module provides useful utils for daemons utils.
"""

import argparse

def arg_parcer():
    """
    Function that parces frequency arguments to run new daemon.

    """

    parcer = argparse.ArgumentParser()
    parcer.add_argument('frequency',
                        type=int,
                        help='amount of seconds between two sequences of daemon execute method.')
    group = parcer.add_mutually_exclusive_group()
    group.add_argument('-M',
                       '--minutes',
                       action='store_true',
                       help='flag that determines the frequency parameter as number of minutes.')
    group.add_argument('-H',
                       '--hours',
                       action='store_true',
                       help='flag that determines the frequency parameter as number of hours.')
    args = parcer.parse_args()

    arg_frequency = args.frequency
    if args.minutes:
        arg_frequency = args.frequency * 60
    elif args.hours:
        arg_frequency = args.frequency * 60 * 60
    return arg_frequency
