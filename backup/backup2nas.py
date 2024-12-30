#!/bin/sh
"""
Backup a list of folders to the local NAS
"""
from decouple import config

secret_key = config('SECRET_KEY')
print("SECRET_KEY: "+secret_key)
