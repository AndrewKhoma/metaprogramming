from __future__ import absolute_import

import sys

from . import cmdgenerate
from . import cmdinspect


def print_available_commands():
    sys.stderr.write('Available commands:\n')

    commands = ['inspect', 'generate']

    for c in commands:
        sys.stderr.write('  ' + c + '\n')

    sys.stderr.write('\n')


def run():
    if len(sys.argv) <= 1:
        sys.stderr.write('Please use: autodoc [command] [OPTIONS] [FILES...]\n\n')
        print_available_commands()
        sys.exit(1)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == 'inspect':
        cmdinspect.run(rest)
    elif cmd == 'generate':
        cmdgenerate.run(rest)
    elif cmd == '--help' or cmd == '-h':
        sys.stderr.write('Please use: autodoc [command] --help\n\n')
        print_available_commands()
        sys.exit(1)
    else:
        sys.stderr.write('Unknown command `{0}\'\n'.format(cmd))
        sys.exit(1)


if __name__ == '__main__':
    run()
