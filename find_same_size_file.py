#!/usr/bin/env python

import glob
import subprocess
import os
import random

file_list = sorted(glob.glob("./*"), key=os.path.getsize)
pre_size = ""

for file_name in file_list:
    cur_size = os.path.getsize(file_name)
    if cur_size == pre_size:
        print(str(cur_size/1000000) +
              " MB [" + file_name + "] is same as previous file.")
    pre_size = cur_size
