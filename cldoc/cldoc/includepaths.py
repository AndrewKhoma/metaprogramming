import os
import subprocess
import sys

from . import utf8


def flags(f):
    devnull = open(os.devnull)

    try:
        p = subprocess.Popen(['clang++', '-E', '-xc++'] + f + ['-v', '-'],
                             stdin=devnull,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except OSError as e:
        sys.stderr.write(
            "\nFatal: Failed to run clang++ to obtain system include headers, please install clang++ to use cldoc\n")

        message = str(e)

        if message:
            sys.stderr.write("  Error message: " + message + "\n")

        sys.stderr.write("\n")
        sys.exit(1)

    devnull.close()

    lines = p.communicate()[1].splitlines()
    init = False
    paths = []

    for line in lines:
        line = utf8.utf8(line)

        if line.startswith('#include <...>'):
            init = True
        elif line.startswith('End of search list.'):
            init = False
        elif init:
            p = line.strip()

            suffix = ' (framework directory)'

            if p.endswith(suffix):
                p = p[:-len(suffix)]

            paths.append(p)

    return ['-I{0}'.format(x) for x in paths] + f
