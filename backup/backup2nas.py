#!/bin/sh
"""
Backup a list of folders to a NAS, using macOS CLI modules and Python.
"""

from decouple import config
import sys
from sys import platform
import os
import subprocess
from subprocess import check_output

print("Username: "+os.getlogin())

# ====
# check that script is running in macOS
if platform != "darwin":
    print("*** Error: script not compatible with the current operating system")
    sys.exit(1)  

# ====
# check that Finder app is running
sp = subprocess.run( ["pgrep", "Finder"], capture_output=True, text=True )
pid = sp.stdout
if pid == '':
    print("*** Error: the Finder application must be active/running.")
    sys.exit(2)

# ====
# Mount NAS: //username:password@servername/rootdirectory
# get NAS parameters
servername = config('NASSERVERNAME')       # the network share name of the NAS
rootdirectory = config('NASROOTDIRECTORY') # the root directory from above example
# get credentials
username = config('NASUSERNAME') # user name in NAS
password = config('NASPASSWORD') # user password in NAS
# set mount parameters
fqn = "//"+username+":"+password+"@"+servername+"/"+rootdirectory
mountpoint = "/Volumes/smb"
# mount action
result = subprocess.run( ["mount", "-t", "smbfs", fqn, mountpoint], capture_output=True, text=True )
if result.returncode != 0:
    print("*** Error: mount operation was unsuccessfull, code: "+str(result.returncode))
    print("stdout: "+result.stdout)
    print("stderr: "+result.stderr)
    sys.exit(3)
    """
    mount: /Volumes/smb: invalid file system.
    mount_smbfs: mount error: /Volumes/smb: Operation not permitted
        mount: /Volumes/smb failed with 64
    mount_smbfs: mount error: /Volumes/smb: Operation not permitted
        mount: /Volumes/smb failed with 64
    mount_smbfs: server connection failed: Operation timed out
        mount: /Volumes/smb failed with 68
    """

print("Successfully mounted NAS.")
""" 
    work in progress, see: 
        https://apple.stackexchange.com/questions/697/how-can-i-mount-an-smb-share-from-the-command-line
        https://discussions.apple.com/thread/4927134?sortBy=rank
"""

# ====
# Close script
result = subprocess.run( ["umount", mountpoint] )
sys.exit(0) # finished
