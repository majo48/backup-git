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
    """
    Compute the hash of a file using the specified algorithm.
    """
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)
    pass
    return hash_func.hexdigest()

def list_files_walk(start_path='.'):
    """
    List all files in all folders in start_path
    """
    with Dbsql(config("DB_FILENAME")) as db_metadata:
        # initialize database
        cnt = 0
        db_metadata.del_rows()
        print('Build database of file metadata: '+start_path)
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
                # print(cnt, " ", fqn, " ", file, " ", siz, " ", mdt, " ", hsh)
                idx = db_metadata.set_row(fqn, file, siz, mdt, hsh)
                if idx is None:
                    return False # failed
                cnt += 1
            pass
        pass
    return True # success

def check_recursive(top_folder):
    """
    Check if all files in top_folder are really identical
        true:  delete the oldest file
        false: do nothing
    """
    print('Check for duplicates in '+top_folder)
    list_files_walk(top_folder)
    with Dbsql(config("DB_FILENAME")) as db_metadata:
        totals = 0 # total bytes in duplicate files
        names = db_metadata.get_duplicate_filenames()
        for name in names:
            file_name = name[0]
            rows = db_metadata.get_duplicate_rows(file_name)
            original_size = None
            for row in rows:
                file_id = row[0]
                file_path = row[1]
                file_size = row[3]
                if original_size is None:
                    # the first candidate is the oldest file version
                    original_size = file_size
                    original_hash = compute_file_hash(file_path, algorithm='md5')
                    pass
                else:
                    # duplicate candidates
                    if file_size == original_size:
                        # both files have same size
                        duplicate_hash = compute_file_hash(file_path, algorithm='md5')
                        if duplicate_hash == original_hash:
                            # both files have the same content
                            totals += file_size
                            print("Duplicate file ["+str(file_id)+"]: "+file_path+", size: "+str(file_size))
                        pass # not a duplicate hash
                    pass # not a duplicate size
                pass # not a candidate
            pass # checked all rows
        pass # checked all names
    return totals # success

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
        print('Check point: exists')
        # check folders (recursive) for duplicate files
        totals = check_recursive(check_point)
        print('Total bytes in duplicate files: '+str(totals))
    else:
        print('Error: cannot find NAS share, is it mounted in Finder?')
        return 3 # exit code
    return 0 # exit code, success

# main ========
exit_code = run_code()
sys.exit(exit_code) # finished