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
    7. Visual Studio Code application needs System-Settings > Full Disk Access for things to work
    8. update rsync from version 2.6.9 (buggy) to version 3.3.0
"""

import sys
from sys import platform
import os
import subprocess
import psutil

def backup(source):
    """
    backup files and folders from current host to remote NAS share 'myMacMini'
    using: rsync [options] Source Destination
    options:
        -rlpt       
            -r = Recursive, traverse into subdirectories
            -l = Treat symlinks as symlinks; don’t follow them
            -p = Preserve permissions
            -t = Preserve creation and modification dates and times
        -- exclude '.*'
        -- include '.gitignore'
        -- stats    Show file transfer statistics
        --del       Delete files that don’t exist on the sending side
    """
    try:
        print("Backup folder: "+source)
        destination = "/Volumes/myMacMini"
        sp = subprocess.run( 
            ["rsync", "-rlpt", "--stats", "--del", 
             "--exclude", "'.*'", "--include", "'.gitignore'", 
             source, destination], 
            capture_output=True, text=True
        )
        print("RSYNC statistics for: "+source)
        print(sp.stdout)
        return (sp.stderr)
        #
    except subprocess.CalledProcessError as err:
        return err.output
    pass

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
location = "/Volumes/myMacMini/"
folder="#recycle"
if os.path.exists(location+folder):
    print('Mount point: exists')
    # backup important Mac-Mini folders and files
    errors = ''
    errors += backup("/Users/mart/Desktop")   # folder scripts and it's contents
    errors += backup("/Users/mart/Documents") # folder scripts and it's contents
    errors += backup("/Users/mart/Projects")  # folder scripts and it's contents
    errors += backup("/Users/mart/Scripts")   # folder scripts and it's contents
    errors += backup("/Users/mart/Dropbox")   # folder scripts and it's contents
    print(errors)
else:
    print('Error: cannot find NAS share, is it mounted?')
pass

# ====
# Close script
sys.exit(0) # finished
