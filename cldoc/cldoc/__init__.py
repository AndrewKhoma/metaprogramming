from __future__ import absolute_import

import sys


def run_inspect(args):
    from . import cmdinspect
    cmdinspect.run(args)


def run_serve(args):
    from . import cmdserve
    cmdserve.run(args)


def run_generate(args):
    from . import cmdgenerate
    cmdgenerate.run(args)


def run_gir(args):
    from . import cmdgir
    cmdgir.run(args)


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

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == 'inspect':
        run_inspect(rest)
    elif cmd == 'serve':
        run_serve(rest)
    elif cmd == 'generate':
        run_generate(rest)
    elif cmd == 'gir':
        run_gir(rest)
    elif cmd == '--help' or cmd == '-h':
        sys.stderr.write('Please use: cldoc [command] --help\n\n')
        print_available_commands()
        sys.exit(1)
    else:
        sys.stderr.write('Unknown command `{0}\'\n'.format(cmd))
        sys.exit(1)


if __name__ == '__main__':
    run()
