#!/usr/bin/env python

"""Use scp to copy files bewteen two remote hosts directly.
Copies the ssh key needed to get from host1 to host2.
Requires ~/.ssh/config file
"""

import os
from optparse import OptionParser
from paramiko import SSHConfig

def main():
    USAGE = "usage: %prog [options] host1:path1 host2:path2"
    parser = OptionParser(usage=USAGE)
    parser.add_option("-F", "--config-file",
                      action="store",
                      dest="config_file",
                      default="%s/.ssh/config" % os.environ['HOME'],
                      help="SSH config file (default: ~/.ssh/config)",)
    (options, args) = parser.parse_args()
    host1, path1 = args[0].split(':', 1)
    host2, path2 = args[1].split(':', 1)

    # ssh config file
    config = SSHConfig()
    config.parse(open(options.config_file))
    o = config.lookup(host2)

    # copy keyfile
    keyfile_remote = '/tmp/%s' % os.path.basename(o['identityfile'])
    run('scp %s %s:%s' % (o['identityfile'], host1, keyfile_remote))

    # copy actual file
    ssh_options = ' -o'.join(['='.join([k, v]) for k, v in o.iteritems()
                              if k != 'hostname' and k != 'identityfile'])
    run('ssh %s scp -p -i %s -oStrictHostKeyChecking=no -o%s %s %s:%s' % (
            host1, keyfile_remote, ssh_options, path1, o['hostname'], path2))

def run(cmd):
    print cmd
    os.system(cmd)

if __name__ == '__main__':
    main()
