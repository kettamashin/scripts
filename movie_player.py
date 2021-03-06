#!/usr/bin/python3
import csv
import glob
import os
import pathlib
import psutil
import random
import shutil
import subprocess
import sys
from getch import Getch
from send2trash import send2trash
from transitions import Machine


class EmptyListException(Exception):
    pass


class HistoryManager(object):
    FIELD_NAMES = ['file', 'num_played', 'num_finished']
    CSV_NAME = './.history.csv'

    def __init__(self):
        self._history_data = {}
        # If history file doesn't exist, create it.
        if not os.path.isfile(self.CSV_NAME):
            with open(self.CSV_NAME, 'w') as f:
                csv_file = csv.DictWriter(f, fieldnames=self.FIELD_NAMES)
                csv_file.writeheader()
        # Read history file and make history list.
        with open(self.CSV_NAME, 'r') as f:
            rows = csv.DictReader(f)
            for row in rows:
                # key : file
                # item: [num_played, num_finished]
                self._history_data[row[self.FIELD_NAMES[0]]] = [
                    int(row[self.FIELD_NAMES[1]]),
                    int(row[self.FIELD_NAMES[2]])]

    def played(self, file):
        self._history_data[file][0] += 1

    def finished(self, file):
        if file in self._history_data.keys():
            self._history_data[file][1] += 1
        with open(self.CSV_NAME, 'w') as f:
            csv_file = csv.DictWriter(f, fieldnames=self.FIELD_NAMES)
            csv_file.writeheader()
            for file in self._history_data.keys():
                csv_file.writerow(
                    {self.FIELD_NAMES[0]: file,
                     self.FIELD_NAMES[1]: self._history_data[file][0],
                     self.FIELD_NAMES[2]: self._history_data[file][1]})
            print(self.CSV_NAME + ' closed')

    def play_list(self, files_in_current):
        # Add new files to history.
        for file in files_in_current:
            if file not in self._history_data.keys():
                self._history_data[file] = [0, 0]
        # Delete files from history which are not in current.
        deleted_files = []
        for file in self._history_data.keys():
            if file not in files_in_current:
                deleted_files.append(file)
        for file in deleted_files:
            self._history_data.pop(file)
        # Get list of files which have min played number.
        min = sys.maxsize
        for nums in self._history_data.values():
            if min > nums[0]:  # num of played
                min = nums[0]
        play_list = []
        for file in self._history_data.keys():
            if self._history_data[file][0] == min:
                play_list.append(file)
        random.shuffle(play_list)
        return play_list


class MoviePlayerMachine(object):
    states = ['INIT', 'WAIT', 'PLAYED']

    def __init__(self, name, mv_path):
        self._name = name
        self._machine = Machine(
            model=self, states=MoviePlayerMachine.states, initial='INIT', auto_transitions=False)
        self._machine.add_transition(
            trigger='start', source='INIT', dest='WAIT', before='make_list', after='next_file')
        self._machine.add_transition(
            trigger='skip', source='WAIT', dest='WAIT', after='next_file')
        self._machine.add_transition(
            trigger='play', source='WAIT', dest='PLAYED', after='play_movie')
        self._machine.add_transition(
            trigger='play', source='PLAYED', dest='PLAYED', after='play_movie')
        self._machine.add_transition(
            trigger='delete', source='PLAYED', dest='WAIT', before='delete_movie', after='next_file')
        self._machine.add_transition(
            trigger='move', source='PLAYED', dest='WAIT', before='move_movie', after='next_file')
        self._machine.add_transition(
            trigger='nothing', source='PLAYED', dest='WAIT', after='next_file')
        self._mv_path = mv_path

        self._history_manager = HistoryManager()
        self._file = ''

    def next_file(self):
        # raise exception if file list becomes empty.
        if(len(self._play_list) == 0):
            print('play list is empty.')
            self._file = ''
            raise EmptyListException
        # Choose file from play list.
        self._file = self._play_list.pop()
        print('\n('+str(self._num_files-len(self._play_list)) +
              '/'+str(self._num_files)+')')
        print(self._file.replace('./', ''))

    def make_list(self):
        # Make list of files that are in current.
        files_in_current = glob.glob("./*")
        self._play_list = self._history_manager.play_list(files_in_current)
        self._num_files = len(self._play_list)

    def play_movie(self):
        subprocess.call(["open",
                         "/Applications/VLC.app",
                         self._file])
        self._history_manager.played(self._file)

    def delete_movie(self):
        # Move file to Trashbox.
        send2trash(self._file)

        # Show empty space of disks.
        disc_list = glob.glob("/Volumes/*")
        for path in disc_list:
            print(path)
            print("  {:.1f} GB free"
                  .format(psutil.disk_usage(path).free/1024/1024/1024))

    def move_movie(self):
        # Force to move file to destination.
        cwd = os.getcwd() + "/"
        dst = pathlib.Path(self._mv_path)
        print('move to ' + str(dst.resolve()))
        shutil.move(os.path.join(cwd, self._file),
                    dst.resolve())

    def quit(self):
        self._history_manager.finished(self._file)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("no path input. use current dir as mv's destination.")
        mv_path = "./"
    elif len(sys.argv) == 2:
        mv_path = sys.argv[1]
        if not os.path.exists(mv_path):
            print(mv_path+' does not exist')
            exit()
    else:
        print('usage: python3 movie_player.py (path to move dir)')
    machine = MoviePlayerMachine('movie_player_machine', mv_path)
    getch = Getch()

    try:
        machine.start()
        while True:
            if machine.state == 'WAIT':
                print('q:exit  /:play  \':skip')
                while True:
                    key = getch()
                    if(key == '\''):
                        machine.skip()
                        break
                    elif(key == '/'):
                        machine.play()
                        break
                    elif(key == 'q'):
                        exit()
            if machine.state == 'PLAYED':
                print('q:exit  /:next  m:move  k:delete  p:replay')
                while True:
                    key = getch()
                    if(key == '/'):
                        machine.nothing()
                        break
                    elif(key == 'p'):
                        machine.play()
                        break
                    elif(key == 'k'):
                        machine.delete()
                        break
                    elif(key == 'm'):
                        machine.move()
                        break
                    elif(key == 'q'):
                        exit()
    except EmptyListException:
        pass
    else:
        import traceback
        traceback.print_exc()
    finally:
        machine.quit()
        print('finish')
