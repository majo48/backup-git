#!/bin/sh
"""
Backup a NAS to a portable disk (WD Elements) using macOS CLI modules and Python.
See DEPENDENCIES.md, backingup a NAS is not without it's problems.
"""

import sys
from sys import platform
import os
import subprocess
from backup_module import backup
import psutil
from decouple import config

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
source_location = config("NAS_MOUNT_POINT") # pattern: /Volumes/<share name>
folder="#recycle"
if os.path.exists(source_location + "/" + folder):
    print('Source Mount point: exists')
    # backup important Mac-Mini folders and files
    errors = 'WD_Elements not compatible with Sequoia 15.3.1!'
    print(errors)
    sys.exit(3)
else:
    print('Error: cannot find NAS share, is it mounted?')
pass

# ====
# Close script
sys.exit(0) # finished