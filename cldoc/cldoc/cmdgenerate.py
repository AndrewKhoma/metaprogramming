from __future__ import absolute_import

import argparse
import os
import sys

from . import generators
from . import log


def run_generate(t, opts):
    generator = generators.Xml(t, opts)
    xml_out = os.path.join(opts.output, 'xml')
    generator.generate(xml_out)


def run(args):
    try:
        sep = args.index('--')
    except ValueError:
        if not '--help' in args:
            sys.stderr.write('Please use: cldoc generate [CXXFLAGS] -- [OPTIONS] [FILES]\n')
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

    parser.add_argument('--type', default='html', metavar='TYPE',
                        help='specify the type of output (html or xml, default html)')

    parser.add_argument('--merge', default=[], metavar='FILES', action='append',
                        help='specify additional description files to merge into the documentation')

    parser.add_argument('--merge-filter', default=None, metavar='FILTER',
                        help='specify program to pass merged description files through')

    parser.add_argument('--basedir', default=None, metavar='DIR',
                        help='the project base directory')

    parser.add_argument('--static', default=False, action='store_const', const=True,
                        help='generate a static website (only for when --output is html, requires globally installed cldoc-static via npm)')

    parser.add_argument('--custom-js', default=[], metavar='FILES', action='append',
                        help='specify additional javascript files to be merged into the html (only for when --output is html)')

    parser.add_argument('--custom-css', default=[], metavar='FILES', action='append',
                        help='specify additional css files to be merged into the html (only for when --output is html)')

    parser.add_argument('files', nargs='+', help='files to parse')

    restargs = args[sep + 1:]
    cxxflags = args[:sep]

    opts = parser.parse_args(restargs)

    if opts.quiet:
        sys.stdout = open(os.devnull, 'w')

    log.setLevel(opts.loglevel)

    from . import tree

    if not opts.output:
        sys.stderr.write("Please specify the output directory\n")
        sys.exit(1)

    if opts.static and opts.type != 'html':
        sys.stderr.write("The --static option can only be used with the html output format\n")
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

    if opts.merge:
        t.merge(opts.merge_filter, opts.merge)

    t.cross_ref()

    run_generate(t, opts)
