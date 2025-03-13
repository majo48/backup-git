#!/bin/sh

"""
    get total rsync progress using Python
    credits: https://libbits.wordpress.com/2011/04/09/get-total-rsync-progress-using-python/
"""

import subprocess
import re
import sys
import time


def clean(line):
    """
    Remove all commas from line (output by rsync version 3.4.1),
    these commas lead to wrong numbers greater than 999.
        line: bytearray   (with commas)
        return: bytearray (without commas)
    """
    cln = bytearray()
    for bite in line:
        if bite != 44: # comma
            cln.append(bite)
    return cln

def empty_trash():
    """
    Remove all files and folders in the Trash Can.
    Testing rsync can fill your SSD/HDD in no time.
    """
    cmd = "rm -rf ~/.Trash/*"
    proc = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )

source_folder = "TIXI" # tested: Public, MyDocuments, Bilder
source_location = "/volumes/myArchive/" + source_folder + "/"  # NAS share (61GB)
destination_location = "/volumes/drive2000G/myArchive/" + source_folder # portable disk
excluded_files = "--exclude '/Virtual*' --exclude '*.iso' --exclude '*.vmem' --exclude '*.vmdk' --exclude '*.vhd' --exclude '*.vhdx' --exclude '*.vdi'"

print('Empty the host Trash Can.')
empty_trash()

print('Dry run: calculate number of files.')
cmd = 'rsync -aW --blocking-io --stats --dry-run ' + excluded_files + ' ' + source_location + ' ' + destination_location
proc = subprocess.Popen(
    cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
)
remainder = clean(proc.communicate()[0])
mn = re.findall(b'Number of files: (\d+)', remainder)
total_files = int(mn[0])
print('Number of files: ' + str(total_files))

print('Start Backup: this is a non-linear process!')
tic = time.perf_counter()
cmd = 'rsync -avW --blocking-io --progress ' + excluded_files + ' ' + source_location + ' ' + destination_location
proc = subprocess.Popen(
    cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
)
tix = 0
while True:
    output = proc.stdout.readline()
    if b'ir-chk' in output:
        m = re.findall(b'ir-chk=(\d+)/(\d+)', output)
        progress = round(((100 * (int(m[0][1]) - int(m[0][0]))) / total_files), 1)
        if progress > 0:
            tix = time.perf_counter() - tic
            sys.stdout.write("\rProgress: " + str(progress) + "% in " + str(round(tix/60,1)) + " minutes")
            sys.stdout.flush()
    elif b'total size' in output and b'speedup' in output:
        break
    pass

print("\n" + output[0:-1].decode("utf-8"))
print('Finished backup in ' + str(round(tix/60,1)) + " minutes.")
