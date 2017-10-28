# copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

# based on code provided by raymond mosteller (thanks!)

import base64
import getpass
import os
import re
import socket
import sys
import traceback

import paramiko
from paramiko.py3compat import input

REGEX = re.compile("[wxt]*\.\d{18}\.\d{6}\.xml\.gz")


# setup logging
paramiko.util.log_to_file('demo_sftp.log')

# Paramiko client configuration
UseGSSAPI = False        # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = False
Port = 22

username = 'gckaiser'
password = '1B6a5c0'
hostname = 'sft.globalcollect.com'

# get host key, if we know one
hostkeytype = None
hostkey = None
try:
    host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
except IOError:
    try:
        # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
        host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
    except IOError:
        print('*** Unable to open host keys file')
        host_keys = {}

if hostname in host_keys:
    hostkeytype = host_keys[hostname].keys()[0]
    hostkey = host_keys[hostname][hostkeytype]
    print('Using host key of type %s' % hostkeytype)


# now, connect and use paramiko Transport to negotiate SSH2 across the connection
try:
    t = paramiko.Transport((hostname, Port))
    t.connect(hostkey, username, password, gss_host=socket.getfqdn(hostname),
              gss_auth=UseGSSAPI, gss_kex=DoGSSAPIKeyExchange)
    sftp = paramiko.SFTPClient.from_transport(t)
    
    sftp.chdir('/home/gckaiser/out')

    file_list = [ f for f in sftp.listdir() if f.endswith(".gz") ]
    
    wx_files = [m.group(0) for l in file_list for m in [REGEX.search(l)] if m]
    print(wx_files)

    for wx in wx_files:
        sftp.get(wx,'./wx/{}'.format(wx))
 
    t.close()

except Exception as e:
    print('*** Caught exception: %s: %s' % (e.__class__, e))
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)
