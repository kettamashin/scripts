#!/usr/bin/python3
import glob
import subprocess
import os
import random
import subprocess
import sys
from getch import Getch
from send2trash import send2trash

getch = Getch()

if len(sys.argv) == 1:
    print('\nHow to use:')
    print('  find_same_name_file.py [dir1] [dir2] ...\n')
    exit()

paths = sys.argv[1:]

for path in paths:
    if not os.path.exists(path):
        print(path + ' does not exist.')
        exit()

files = []
for path in paths:
    files += glob.glob(path + '/*')

ref_files = files[:]

for file in files:
    for ref_file in ref_files:
        if file == ref_file:
            break
        if os.path.basename(file) != os.path.basename(ref_file):
            break

        print('-----------------------')
        print('[size=' + str(os.path.getsize(file)) + ' ' + file + ']')
        print('[size=' + str(os.path.getsize(ref_file)) + ' ' + ref_file + ']')
        print('  /:open')
        print('  \':skip')
        print('  k:delete [size=' +
              str(os.path.getsize(file)) + ' ' + file + ']')
        print(
            '  l:delete [size=' + str(os.path.getsize(ref_file)) + ' ' + ref_file + ']')
        while True:
            key = getch()
            if(key == '/'):
                subprocess.call(
                    ["open", "/Applications/VLC.app", file, ref_file])
            elif(key == '\''):
                break
            elif(key == 'k'):
                send2trash(file)
                break
            elif(key == 'l'):
                send2trash(ref_file)
                break
