from __future__ import absolute_import

import argparse
import os
import sys

from . import generators
from . import log
from . import tree


def run_generate(t, opts):
    generator = generators.Xml(t, opts)
    generator.generate(opts.output)


def run(args):
    try:
        sep = args.index('--')
    except ValueError:
        if not '--help' in args:
            sys.stderr.write('Please use: autodoc [CXXFLAGS] -- [OPTIONS] [FILES]\n')
            sys.exit(1)
        else:
            sep = -1

    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s generate [CXXFLAGS] -- [OPTIONS] [FILES]')

    parser.add_argument('--quiet', default=False, action='store_const', const=True,
                        help='be quiet about it')

    parser.add_argument('--loglevel', default='error', metavar='LEVEL',
                        help='specify the logevel (error, warning, info)')

    parser.add_argument('--report', default=False,
                        action='store_const', const=True, help='report documentation coverage and errors')

    parser.add_argument('--output', default=None, metavar='DIR',
                        help='specify the output directory')

    parser.add_argument('--language', default='c++', metavar='LANGUAGE',
                        help='specify the default parse language (c++, c or objc)')

    parser.add_argument('--basedir', default=None, metavar='DIR',
                        help='the project base directory')

    parser.add_argument('files', nargs='+', help='files to parse')

    restargs = args[sep + 1:]
    cxxflags = args[:sep]

    opts = parser.parse_args(restargs)

    if opts.quiet:
        sys.stdout = open(os.devnull, 'w')

    log.setLevel(opts.loglevel)

    if not opts.output:
        sys.stderr.write("Please specify the output directory\n")
        sys.exit(1)

    haslang = False

    for x in cxxflags:
        if x.startswith('-x'):
            haslang = True

    if not haslang:
        cxxflags.append('-x')
        cxxflags.append(opts.language)

    t = tree.Tree(opts.files, cxxflags)

    t.process()
    t.cross_ref()

    run_generate(t, opts)
