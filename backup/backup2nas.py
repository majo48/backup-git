#!/bin/sh
"""
Backup a list of folders to a NAS, using macOS CLI modules and Python.
"""

from decouple import config

# network share example: //username:password@servername/rootdirectory
# get NAS parameters
servername = config('SERVERNAME')       # the network share name of the NAS
rootdirectory = config('ROOTDIRECTORY') # the root directory from above example
# get credentials
username = config('USERNAME') # user name in NAS
password = config('PASSWORD') # user password in NAS

# set result vars
listSharedFolders = ["work in progress"]

# work in progress

print("Shared Folders: ", listSharedFolders)
