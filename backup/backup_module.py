
"""
Backup with RSYNC methode.
"""

import subprocess

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
        -- exclude '.*'
        -- include '.gitignore'
        -- stats    Show file transfer statistics
        --del       Delete files that don’t exist on the sending side
    """
    if "/Users" in destination:
        raise AssertionError("ASSERTION ERROR: NEVER BACKUP TO HOST "+destination)
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
