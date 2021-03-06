#!/usr/bin/env python

import glob
import os
import re

file_list = sorted(glob.glob("./*"), key=os.path.getsize)
pre_size = ""

for file_name1 in file_list:
    ref_name = file_name1.replace("./", "")
    for file_name2 in file_list:
        if ref_name in file_name2\
        or ref_name.upper() in file_name2\
        or ref_name.lower() in file_name2:
            if file_name1 != file_name2:
                print("Hit [" + file_name1 + "] and [" + file_name2 + "].")
