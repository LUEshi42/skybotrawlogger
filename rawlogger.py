
"""
log.py: written by Scaevolus 2009
        modified 2018 by LUEshi42
"""

import os
import codecs
import time
import re

from util import hook


log_fds = {}  # '%(net)s %(chan)s' : (filename, fd)

timestamp_format = '[%H:%M]'


def get_log_filename(dir, server, chan):
    return os.path.join(dir, 'log', gmtime('%Y'), server, gmtime('%m'), gmtime('%d'),
                        (gmtime('%%s.%m-%d.log') % chan).lower())


def gmtime(format):
    return time.strftime(format, time.gmtime())

def get_log_fd(dir, server, chan):
    fn = get_log_filename(dir, server, chan)
    cache_key = '%s %s' % (server, chan)
    filename, fd = log_fds.get(cache_key, ('', 0))

    if fn != filename:  # we need to open a file for writing
        if fd != 0:     # is a valid fd
            fd.flush()
            fd.close()
        dir = os.path.split(fn)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        fd = codecs.open(fn, 'a', 'utf-8')
        log_fds[cache_key] = (fn, fd)

    return fd


@hook.singlethread
@hook.event('*')
def log(paraml, input=None, bot=None):
    timestamp = gmtime(timestamp_format)

    fd = get_log_fd(bot.persist_dir, input.server +  input.chan, 'raw')
    fd.write(timestamp + input.chan + input.raw + '\n')

    print timestamp, input.chan, input.raw
