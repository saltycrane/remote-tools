"""Assumes SSH config file at ~/.ssh/config
"""

import fnmatch
import gzip
import os
import re
import sys
from paramiko import SSHClient, SSHConfig

def rml_cat(host, glob, ascending=False):
    rml = RemoteMultiLog()
    rml.connect(host)
    lines = rml.get_lines(glob)
    for line in lines:
        print line.rstrip()
    rml.close()

class RemoteMultiLog(object):
    def connect(self, host):
        # ssh config file
        config = SSHConfig()
        config.parse(open('%s/.ssh/config' % os.environ['HOME']))
        o = config.lookup(host)

        # ssh client
        self.ssh_client = ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(o['hostname'], username=o['user'], key_filename=o['identityfile'])
        self.sftp_client = ssh.open_sftp()

    def get_lines(self, glob, ascending=False):
        """wildcards only allowed in filename (not path)
        """
        (dirname, filepattern) = os.path.split(glob)
        filelist = self.sftp_client.listdir(dirname)
        filelist = fnmatch.filter(filelist, filepattern)
        filelist = [os.path.join(dirname, filename) for filename in filelist]
        filelist = sorted(filelist, self.sort_by_integer_suffix, reverse=ascending)

        for filepath in filelist:
            sys.stderr.write("Processing %s...\n" % filepath)
            sftp_file = self.sftp_client.open(filepath)
            if filepath.endswith('.gz'):
                fh = gzip.GzipFile(fileobj=sftp_file)
            else:
                fh = sftp_file
            if not ascending:
                fh = reversed(fh.readlines())
            for line in fh:
                yield line
            sftp_file.close()

    def close(self):
        self.sftp_client.close()
        self.ssh_client.close()

    def sort_by_integer_suffix(self, a, b):
        """Files are sorted by the integer in the suffix of the log filename.
        Suffix may be one of the following:
            .X (where X is an integer)
            .X.gz (where X is an integer)
        If the filename does not end in either suffix, it is treated as if X=0
        """
        def get_suffix(fname):
            m = re.search(r'.(?:\.(\d+))?(?:\.gz)?$', fname)
            if m.lastindex:
                suf = int(m.group(1))
            else:
                suf = 0
            return suf
        return get_suffix(a) - get_suffix(b)
