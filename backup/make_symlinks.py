#!/bin/sh
"""
Search for (find) duplicates in folder(s) in a NAS, using macOS CLI modules and Python.
"""

import sys
import os
import pathlib
import psutil
from decouple import config
from backup_module import is_macos, finder_active
from Dbsql import Dbsql

def is_symlink(file_path):
    """
    Check if a file is a symlink
    """
    path = pathlib.Path(file_path)
    return path.is_symlink()

def make_symlink(file_path, duplicate_path):
    """
    make one symlink in duplicate_path and delete duplicate file
    this function is reentrant (in case errors are detected)
    """
    try:
        if os.path.exists(duplicate_path):
            # delete duplicate file
            os.remove(duplicate_path)
            print("Duplicate deleted: "+duplicate_path)
        if os.path.exists(file_path):
            # create symlink file
            os.symlink(file_path, duplicate_path)
            print("Link created: "+duplicate_path)
    except FileExistsError:
        print("Symlink already exists.")
    except PermissionError:
        print("Permission denied: You might need admin rights.")
    except OSError as e:
        print("OS error occurred:", e)
    finally:
        return 0 # ignore any errors

def run_code():
    """
    Script run code, called from main
    """
    # current user
    print("Username: "+os.getlogin())
    # ====
    # check that script is running in macOS
    if not is_macos():
        return 1 # exit code
    # ====
    # process name
    p = psutil.Process(os.getpid())
    print("Process name: "+p.name())
    # ====
    # check that Finder app is running
    if not finder_active():
        return 2 # exit code
    # ====
    # check that NAS is mounted
    check_point = config("NAS_CHECK_POINT") # pattern: /Volumes/<share name>
    if os.path.exists(check_point):
        print("Top folder : "+check_point)
        with Dbsql(config("DB_FILENAME")) as db_metadata:
            print("Database name: "+config("DB_FILENAME"))
            files = db_metadata.get_duplicate_files()
            for file in files:
                rows = db_metadata.get_duplicate_rows(file[0])
                file_path = None
                for row in rows:
                    # all occurrences of each file with duplicates
                    occurrence = row[6]
                    if occurrence == 0:
                        file_path = row[1]
                    else: # occurrence >0
                        duplicate_path = row[1]
                        if not (is_symlink(file_path) or is_symlink(duplicate_path)):
                            make_symlink(file_path, duplicate_path)
                        pass
                    pass
                pass
            pass
        return 0 # exit code
    else:
        print("Folder does not exist: "+check_point)
        return 3 # exit code

# main ========
exit_code = run_code()
sys.exit(exit_code) # finished

