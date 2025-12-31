#!/bin/sh
"""
Backup a list of folders to a NAS, using macOS CLI modules and Python.
See DEPENDENCIES.md, backing up to NAS is not without its problems.
"""

import sys
import os
import psutil
from decouple import config
from backup_module import backup_with_progress, is_macos, finder_active

# main ========
folders = ["Desktop", "Documents", "Projects", "Scripts"]
# ====
# current user
print("Username: "+os.getlogin())
# ====
# check that script is running in macOS
if not is_macos():
    sys.exit(1)
# ====
# process name
p = psutil.Process(os.getpid())
print("Process name: "+p.name())
# ====
# check that Finder app is running
if not finder_active():
    sys.exit(2)
# ====
# check that NAS is mounted
destination = config("NAS_MOUNT_POINT") # pattern: /Volumes/<share name>
if os.path.exists(destination):
    print('Mount point: exists')
    # backup important folders and files
    errors = []
    user = config("MAC_USERNAME")
    for folder in folders:
        source = "/Users/" + user +"/" + folder # without trailing slash
        error = backup_with_progress(source, destination)
        errors.append(error)
    pass
    for error in errors:
        if error:
            lines = error.split('\n')
            for line in lines:
                print(line)
            pass
        pass
    pass
else:
    print('Error: cannot find NAS share, is it mounted?')
    sys.exit(3)
pass

# ====
# Close script
sys.exit(0) # finished
