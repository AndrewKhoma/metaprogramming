from __future__ import absolute_import

import argparse
import sys


def run(args):
    try:
        sep = args.index('--')
    except ValueError:
        if not '--help' in args:
            sys.stderr.write('Please use: cldoc inspect [CXXFLAGS] -- [OPTIONS] [FILES]\n')
            sys.exit(1)
        else:
            sep = 0

    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s inspect [CXXFLAGS] -- [OPTIONS] DIRECTORY')

    parser.add_argument('files', nargs='*', help='files to parse')

    restargs = args[sep + 1:]
    cxxflags = args[:sep]

    opts = parser.parse_args(restargs)

    from . import tree
    from . import inspecttree

    t = tree.Tree(opts.files, cxxflags)
    inspecttree.inspect(t)
