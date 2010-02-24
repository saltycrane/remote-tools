#!/usr/bin/env python

"""Print lines for all files matching glob pattern on a remote host
"""

from optparse import OptionParser
from multilog import rml_cat

def main():
    USAGE = "usage: %prog [options] host:glob"
    parser = OptionParser(usage=USAGE)
    parser.add_option("--ascending",
                      action="store_true",
                      dest="ascending",
                      default=False,
                      help="sort in ascending order",)
    (options, args) = parser.parse_args()
    host, glob = args[0].split(':', 1)

    rml_cat(host, glob, options.ascending)

if __name__ == '__main__':
    main()
