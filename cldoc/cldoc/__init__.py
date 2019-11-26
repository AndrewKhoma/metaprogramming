from __future__ import absolute_import

import sys


def run_generate(args):
    from . import cmdgenerate
    cmdgenerate.run(args)


def print_available_commands():
    sys.stderr.write('Available commands:\n')

    commands = ['inspect', 'serve', 'generate', 'gir']

    for c in commands:
        sys.stderr.write('  ' + c + '\n')

    sys.stderr.write('\n')


def run():
    if len(sys.argv) <= 1:
        sys.stderr.write('Please use: cldoc [command] [OPTIONS] [FILES...]\n\n')
        print_available_commands()
        sys.exit(1)

    rest = sys.argv[2:]

    run_generate(rest)


if __name__ == '__main__':
    run()
