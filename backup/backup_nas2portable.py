#!/bin/sh
"""
Backup a NAS to a portable disk (WD Elements) using macOS CLI modules and Python.
See DEPENDENCIES.md, backing up a NAS is not without its problems.
Notes:
    WD_Elements are not properly supported by ARM architecture
    Connect to USB-A port in Belkin adapter, then wait a long time
    Eventually the golden WD_Elements icon will appear on the Desktop
"""

import sys
import os
from backup_module import backup, is_macos, finder_active
import psutil
from decouple import config

# main ========
folders = ["/volumes/myMacMini/", "/volumes/myArchive/"] # fully qualified mount point, ending with slash!
# folders = ["/volumes/myMacMini/", "/volumes/myArchive/", "/volumes/myMacBook/", "/volumes/myENVY/", "/volumes/myBigMac/", "/volumes/myTravelmate/"]

# ====
# current user
print("Username: "+os.getlogin())
# ====
# check that script is running in macOS
if not is_macos():
    sys.exit(1)
# process name
p = psutil.Process(os.getpid())
print("Process name: "+p.name())
# ====
# check that Finder app is running
if not finder_active():
    sys.exit(2)
# ====
# check that NAS is mounted
source_location = config("NAS_MOUNT_POINT") # pattern: /Volumes/<share name>
if os.path.exists(source_location):
    print('Source mount point: exists')
    destination_location = config("PORTABLE_MOUNT_POINT")
    if os.path.exists(destination_location):
        print("Destination mount point: exists.")
        # backup important Mac-Mini folders and files
        errors = []
        for folder in folders:
            subfolder = folder.split('/')
            error = backup(folder, destination_location+"/"+subfolder[2])
            errors.append(error)
        pass
        for error in errors:
            lines = error.split('\n')
            for line in lines:
                print(line)
            pass
        pass
    else:
        print('Error: cannot find WD_Elements share, is it mounted?')
        sys.exit(3)
else:
    print('Error: cannot find NAS share, is it mounted?')
    sys.exit(4)
pass

# ====
# Close script
sys.exit(0) # finished