#!/bin/sh
"""
Backup a list of folders to a NAS, using macOS CLI modules and Python.
Connecting to the NAS using the terminal or scripts is not without problems.

Prerequisites:
=============
    1. Use Finder Go > Connect to server > servername > connect > username + password 
    2. Select folder myMacMini
    3. Open Finder-Settings > General > set Connected servers > creates myMacMini icon
    4. Open System-Setting > Login Items & Extensions > Open at Login > drag myMacMini icon to list
    5. Restart computer
    6. Location /Volumes/myMacMini is permanent
"""

import sys
from sys import platform
import os
import subprocess
from subprocess import check_output

# ====
# current user
print("Username: "+os.getlogin())

# ====
# check that script is running in macOS
if platform != "darwin":
    print("*** Error: script not compatible with the current operating system")
    sys.exit(1)  
print("Operating System: mac OS")

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
location = "/Volumes/myMacMini"
file="_readme.txt"
if os.path.isfile(location+"/"+file):
    print('Mount point: exists')
else:
    print('Error: cannot find /Volumes/myMacMini/_readme.txt')

# ====
# Close script
sys.exit(0) # finished
