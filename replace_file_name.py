#!/usr/bin/python3
import os
import sys
import glob
import shutil

if __name__ == "__main__":

    if len(sys.argv) == 2:
        before = sys.argv[1]
        after = ""
    elif len(sys.argv) == 3:
        before = sys.argv[1]
        after = sys.argv[2]
    else:
        print("Argument must be one.")
        exit()

    file_list = glob.glob("./*")
    for file in file_list:
        file_name = file.replace("./", "")
        new_name = file_name.replace(before, after)
        if (new_name == file_name):
            continue
        key = input("Rename from [" + file_name + "]\n"
                    + "         to [" + new_name + "]?  Yes:Enter  No:else ")
        if key == "":
            os.rename(file_name, new_name)
        else:
            print("skip rename [" + file_name + "]")
