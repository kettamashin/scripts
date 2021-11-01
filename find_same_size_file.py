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
    print('  find_same_size_file.py [dir1] [dir2] ...\n')
    exit()

paths = sys.argv[1:]

for path in paths:
    if not os.path.exists(path):
        print(path + ' does not exist.')
        exit()

files = []
for path in paths:
    files += glob.glob(path + '/*')

sorted_files = sorted(files, key=os.path.getsize)

pre_file = ''
pre_size = ''

for file in sorted_files:
    size = os.path.getsize(file)

    if size == pre_size:
        print('-----------------------')
        print('['+pre_file+']')
        print('['+file+']')
        print('    are same size files (' + str(size/1000000) + 'MB)')
        print('  /:open')
        print('  \':skip')
        print('  k:delete [' + pre_file + ']')
        print('  l:delete [' + file + ']')
        while True:
            key = getch()
            if(key == '/'):
                subprocess.call(
                    ["open", "/Applications/VLC.app", file, pre_file])
            elif(key == '\''):
                break
            elif(key == 'k'):
                send2trash(pre_file)
                break
            elif(key == 'l'):
                send2trash(file)
                break

    pre_file = file
    pre_size = size
