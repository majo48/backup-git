# Dependencies

# Development environment

- operating system:  mac Sequoia (15.2)
- hardware platform: mac mini M4pro
- preinstalled:      python3 (3.9.3), includes python-decouple (3.8)
- preinstalled:      pgrep
- installed:         Visual Studio Code (1.96.2)
- installed:         homebrew (4.4.14)
- upgraded:          rsync (3.3.0)

# Setup auto-connect for NAS

Setup Mac OS to auto-connect to NAS, mounting through CLI commands seems to be impossible: 

1. Use Finder Go > Connect to server > servername > connect > username + password 
2. Select folder myMacMini
3. Open Finder-Settings > General > set Connected servers > creates myMacMini icon
4. Open System-Setting > Login Items & Extensions > Open at Login > drag myMacMini icon to list
5. Restart computer
6. Location /Volumes/myMacMini is permanent

# System Settings

Mac OS version Sequoia has new Privacy & Security Settings:

1. System Settings > Full Disk Access > Add (+) Visual Studio Code
2. System Settings > Full Disk Access > Add (+) Terminal

# Dot env file

MAC_USERNAME=username

NAS_MOUNT_POINT=/volumes/nas_share_name

PORTABLE_MOUNT_POINT=/volumes/drive_name1

PORTABLE_MOUNT_POINTS=["/volumes/drive_name1", "/volumes/drive_name2"]

# Python packages

The following Python packages are needed for this application:

- installed:  pip (24.3.1)
- installed:  .venv
- installed:  psutil (6.1.1)
