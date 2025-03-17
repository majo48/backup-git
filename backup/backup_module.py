"""
Backup with RSYNC methode.
"""

import subprocess
import sys
from sys import platform
import re
import time
from decouple import config

EXCLUDE = ("--exclude '/Virtual*' --exclude '*.iso' --exclude '*.vmem' "
           "--exclude '*.vmdk' --exclude '*.vhd' --exclude '*.vhdx' "
           "--exclude '*.vdi' --exclude '.DS_Store'")

def _is_safe(source, destination):
    """
    check if the backup direction (info flow) is safe:
    User > NAS > portable is considered safe (legal)
    """
    if "/Users" in source:
        return True # backup mac mini to either NAS or portable
    portable = config("PORTABLE_MOUNT_POINT")
    if portable in destination:
        return True # backup to portable
    else:
        return False # illegal/unsafe

def backup(source, destination):
    """
    backup files and folders from current host to remote NAS share 'myMacMini'
    using: rsync [options] Source Destination
    options:
        -rlpt
            -r = Recursive, traverse into subdirectories
            -l = Treat symlinks as symlinks; don’t follow them
            -p = Preserve permissions
            -t = Preserve creation and modification dates and times
        --exclude '.*'
        --include '.gitignore'
        --stats   Show file transfer statistics
        --delete  Delete files that don’t exist on the sending side
    """
    if not _is_safe(source, destination):
        raise AssertionError("Illegal backup direction: from " + source + " to " + destination)
    try:
        print("Backup folder: "+source)
        sp = subprocess.run(
            ["rsync", "-rlpt", "--stats", "--del",
             "--exclude", "'.*'", "--include", "'.gitignore'",
             source, destination],
            capture_output=True, text=True
        )
        print("RSYNC statistics for: "+source)
        print(sp.stdout)
        return sp.stderr
        #
    except subprocess.CalledProcessError as err:
        return err.output
    pass

def _clean(line):
    """
        Remove all commas from line (output by rsync version 3.4.1),
        these commas lead to wrong numbers greater than 999.
            line: bytearray   (with commas)
            return: bytearray (without commas)
        """
    cln = bytearray()
    for bite in line:
        if bite != 44:  # comma
            cln.append(bite)
    return cln

def _get_backup_size(source, destination):
    """
    calculate backup size aka. number of files using:
    rsync [options] source destination
    options:
        -a = archive, -W = copy whole file
        --blocking-io, --stats, --dry-run
    """
    print('Dry run: calculate number of files')
    cmd = ('rsync -aW --blocking-io --stats --dry-run ' +
           EXCLUDE + ' ' + source + ' ' + destination)
    proc = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    remainder = _clean(proc.communicate()[0])
    mn = re.findall(b'Number of files: (\d+)', remainder)
    total_files = int(mn[0])
    print('Number of files: ' + str(total_files))
    return total_files

def backup_with_progress(source, destination):
    """
    backup files and folders using:
    rsync [options] Source Destination
    options:
        -a = archive, -v = verbose, -W = copy whole file
        --blocking-io, --progress, --delete
    """
    if not _is_safe(source, destination):
        raise AssertionError("Illegal backup direction: from " + source + " to " + destination)
    pass # get backup size ========
    print("Backup folder: " + source)
    total_files = _get_backup_size(source, destination) # with dry-run
    pass # start backup ========
    print('Start Backup: this is a non-linear process!')
    tic = time.perf_counter()
    cmd = 'rsync -avW --blocking-io --progress --delete ' + EXCLUDE + ' ' + source + ' ' + destination
    proc = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    tix = 0 # process rsync verbose output ========
    while True:
        output = proc.stdout.readline()
        if b'ir-chk' in output:
            if total_files  > 0:
                m = re.findall(b'ir-chk=(\d+)/(\d+)', output)
                progress = round(((100 * (int(m[0][1]) - int(m[0][0]))) / total_files), 1)
                if progress > 0:
                    tix = time.perf_counter() - tic
                    sys.stdout.write("\rProgress: " + str(progress) + "% in " + str(round(tix / 60, 1)) + " minutes")
                    sys.stdout.flush()
            else:
                sys.stdout.write(output)
                sys.stdout.flush()
        elif b'total size' in output and b'speedup' in output:
            break # rsync is finished
        pass
    # finished ========
    print("\n" + output[0:-1].decode("utf-8"))
    print('Finished backup in ' + str(round(tix / 60, 1)) + " minutes.")
    return proc.stderr

def is_macos():
    """
    check if this script is running in macos
    """
    if platform != "darwin":
        print("*** Error: script not compatible with the current operating system")
        return False
    print("Operating System: mac OS")
    return True

def finder_active():
    """
    check if the finder app is running
    """
    sp = subprocess.run(["pgrep", "Finder"], capture_output=True, text=True)
    pid = sp.stdout
    if pid == '':
        print("*** Error: the Finder application must be active/running.")
        return False
    print("Finder app: active")
    return True

if __name__ == "__main__":
    # this is an "import only" module
    raise AssertionError("This module shouldn't be run as a script.")

