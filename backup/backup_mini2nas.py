#!/bin/sh
"""
Backup a list of folders to a NAS, using macOS CLI modules and Python.
See DEPENDENCIES.md, backing up to NAS is not without its problems.
"""

import sys
from sys import platform
import os
import subprocess
import psutil
from decouple import config
from backup_module import backup

# main ========

# ====
# current user
print("Username: "+os.getlogin())

# ====
# check that script is running in macOS
if platform != "darwin":
    print("*** Error: script not compatible with the current operating system")
    sys.exit(1)  
print("Operating System: mac OS")
# process name
p = psutil.Process(os.getpid())
print("Process name: "+p.name())

# ====
# check that Finder app is running
sp = subprocess.run( ["pgrep", "Finder"], capture_output=True, text=True )
pid = sp.stdout
if pid == '':
    print("*** Error: the Finder application must be active/running.")
    sys.exit(2)
print("Finder app: active")

# ====
# check that NAS is mounted
location = config("NAS_MOUNT_POINT") # pattern: /Volumes/<share name>
folder="#recycle"
if os.path.exists(location+"/"+folder):
    print('Mount point: exists')
    # backup important Mac-Mini folders and files
    errors = ''
    user=config("MAC_USERNAME") # pattern: valid Mac OS username
    errors += backup("/Users/"+user+"/Desktop", location)   # folder scripts and it's contents
    errors += backup("/Users/"+user+"/Documents", location) # folder scripts and it's contents
    errors += backup("/Users/"+user+"/Projects", location)  # folder scripts and it's contents
    errors += backup("/Users/"+user+"/Scripts", location)   # folder scripts and it's contents
    errors += backup("/Users/"+user+"/Dropbox", location)   # folder scripts and it's contents
    print(errors)
else:
    print('Error: cannot find NAS share, is it mounted?')
pass

# ====
# Close script
sys.exit(0) # finished
