#!/usr/bin/python3

import glob
import subprocess
import os
import random
import subprocess
from getch import Getch
from send2trash import send2trash

getch = Getch()
file_list = sorted(glob.glob("./*"), key=os.path.getsize)
pre_file = ''
pre_size = ''

for file in file_list:
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
