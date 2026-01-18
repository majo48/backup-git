#!/bin/sh
"""
Search for (find) duplicates in folder(s) in a NAS, using macOS CLI modules and Python.
"""

import sys
import os
import psutil
import datetime
import hashlib
from decouple import config
from backup_module import is_macos, finder_active
from Dbsql import Dbsql

# Constants
HASH_DUMMY = "xxx"

def compute_file_hash(file_path, algorithm='md5'):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)
    pass
    return hash_func.hexdigest()

def list_files_walk(start_path='.'):
    with Dbsql(config("DB_FILENAME")) as db_metadata:
        # initialize database
        cnt = 0
        db_metadata.del_rows()
        # loop through all files in start_path
        for root, dirs, files in os.walk(start_path):
            for file in files:
                if file == '.DS_Store':
                    break
                fqn = os.path.join(root, file)
                siz = os.path.getsize(fqn)
                mdt = datetime.datetime.fromtimestamp(os.path.getmtime(fqn))
                # hsh = compute_file_hash(fqn)
                hsh = HASH_DUMMY
                print(cnt, " ", fqn, " ", file, " ", siz, " ", mdt, " ", hsh)
                id = db_metadata.set_row(fqn, file, siz, mdt, hsh)
                if id is None:
                    return False # failed
                cnt += 1
            pass
        pass
    return True # success

def check_recursive(top_folder):
    messages = []
    messages.append('Check point top folder: '+top_folder)
    list_files_walk(top_folder)
    return messages

def run_code():
    # current user
    print("Username: "+os.getlogin())
    # ====
    # check that script is running in macOS
    if not is_macos():
        return 1 # error
    # ====
    # process name
    p = psutil.Process(os.getpid())
    print("Process name: "+p.name())
    # ====
    # check that Finder app is running
    if not finder_active():
        return 2 # error
    # ====
    # check that NAS is mounted
    check_point = config("NAS_CHECK_POINT") # pattern: /Volumes/<share name>
    if os.path.exists(check_point):
        print('Check point: exists')
        # check folders (recursive) for duplicate files
        msgs = check_recursive(check_point)
        for msg in msgs:
            print(msg)
        pass
    else:
        print('Error: cannot find NAS share, is it mounted in Finder?')
        return 3 # error
    return 0 # success

# main ========
rtrn = run_code()
sys.exit(rtrn) # finished