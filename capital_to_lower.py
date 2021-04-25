#!/usr/bin/python3
import os
import sys
import glob
import shutil
from getch import Getch

if __name__ == "__main__":
    file_list = glob.glob("./*")
    getch = Getch()
    for file in file_list:
        file_name = file.replace("./", "")
        new_name = file_name.replace(file_name, file_name.lower())
        if (new_name == file_name):
            continue
        print("Rename from [" + file_name + "]\n"
              + "         to [" + new_name + "]?  y/n")
        key = getch()
        if key == 'y':
            os.rename(file_name, new_name)
        elif key == 'n':
            print("skip rename [" + file_name + "]")
