from __future__ import absolute_import

import sys, argparse

from . import tree
from . import inspecttree

import os


def run(args):
    try:
        sep = args.index('--')
    except ValueError:
        if not '--help' in args:
            sys.stderr.write('Please use: autodoc inspect [CXXFLAGS] -- [OPTIONS] [FILES]\n')
            sys.exit(1)
        else:
            sep = 0

    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s inspect [CXXFLAGS] -- [OPTIONS] DIRECTORY')

    parser.add_argument('--output', default=None, metavar='DIR',
                        help='specify the output directory')

    parser.add_argument('files', nargs='*', help='files to parse')

    restargs = args[sep + 1:]
    cxxflags = args[:sep]

    opts = parser.parse_args(restargs)

    if not opts.output and not os.path.isdir(opts.output):
        sys.stderr.write("Please specify the output directory\n")
        sys.exit(1)

    t = tree.Tree(opts.files, cxxflags)
    inspecttree.inspect(t, opts.output)
