#!/usr/bin/env python

"""Print lines for all files matching glob pattern on a remote host
"""

from optparse import OptionParser
from multilog import rml_cat

def main():
    USAGE = "usage: %prog [options] host:glob"
    parser = OptionParser(usage=USAGE)
    parser.add_option("--skip-files",
                      action="store",
                      dest="skip_files",
                      type="int",
                      default=0,
                      help="number of files to skip (default=0)",)
    (options, args) = parser.parse_args()
    host, glob = args[0].split(':', 1)

    rml_cat(host, glob, options.skip_files)

if __name__ == '__main__':
    main()
