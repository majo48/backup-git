#!/bin/sh
"""
Backup a list of folders to the local NAS,
    using package pysmb and examples from:
        https://stackoverflow.com/questions/37024334/list-all-folders-on-a-nas-with-python
        https://stackoverflow.com/questions/10248796/example-of-pysmb
        https://github.com/miketeo/pysmb/tree/dev-1.2.x/python3/tests/SMBConnectionTests
"""

from decouple import config
from smb.SMBConnection import SMBConnection

# get credential vars
user_name = config('USERNAME')     # user name in NAS
password = config('PASSWORD')      # user password in NAS

# network share example: //SHARENAME/RootDirectory/Subdirectory
# get NAS vars
server_name = config('SERVERNAME') # the network share name of the NAS in full UNC notation
root_dir = config('ROOTDIRECTORY') # the root directory from above example
client_name = config('CLIENTNAME') # the name of the current host

# set result vars
listSharedFileObjs = []

# using context manager
with SMBConnection(user_name, password, client_name, server_name) as smbconn:
    
    # open connection to NAS using port 139/445
    smbconn.connect(server_name, 445) # fatal error: socket.gaierror: [Errno 8] nodename nor servname provided, or not known
    """
    Traceback (most recent call last):
        File "/Users/mart/Projects/backup-git/backup/backup2nas.py", line 29, in <module> smbconn.connect(server_name)
        File "/Users/mart/Projects/backup-git/.venv/lib/python3.9/site-packages/smb/SMBConnection.py", line 120, in connect self.sock = socket.create_connection(( ip, port ), timeout = timeout)
        File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/socket.py", line 822, in create_connection for res in getaddrinfo(host, port, 0, SOCK_STREAM):
        File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/socket.py", line 953, in getaddrinfo for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
            socket.gaierror: [Errno 8] nodename nor servname provided, or not known
    """ 

    listSharedFileObjs = smbconn.listPath(root_dir,"/")

print(listSharedFileObjs)
