#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')


import os
import shutil
import subprocess
import sys
import time

with open(__projectdir__ / Path('trashfolder.txt')) as f:
    trashfolder = f.read()
if trashfolder[-1] == '\n':
    trashfolder = trashfolder[: -1]
trashfolder = trashfolder.replace('~', os.path.expanduser('~'), 1)


def trashfunc(trashfolder = trashfolder, oldversionsname = 'old_versions'):
    if not os.path.exists(trashfolder + oldversionsname):
        os.makedirs(trashfolder + oldversionsname)

    for filename in sys.argv[1:]:

        if not os.path.exists(filename):
            print(filename + ' does not exist')
            continue

        if os.path.islink(filename):
            os.remove(filename)
            continue

        basefilename=os.path.basename(os.path.abspath(filename))


        # rename if called old_versions
        # first remove / from end of olversionsname to ensure comparison correct
        if oldversionsname[-1] == '/':
            oldversionsname = oldversionsname[: -1]
        if basefilename == oldversionsname:
            basefilename = oldversionsname + '2'

        trashname = os.path.join(trashfolder, basefilename)
        # move oldversion to an oldversions folder with timestamp + issuenum appended
        if os.path.exists(trashname):
            thetime = time.strftime("%Y-%m-%d_%H-%M-%S")
            issuenum = 0
            while True:
                if not os.path.exists(os.path.join(trashfolder, oldversionsname, basefilename + '_' + thetime + '_' + str(issuenum))):
                    shutil.move(trashname, os.path.join(trashfolder, oldversionsname, basefilename + '_' + thetime + '_' + str(issuenum)))
                    break
                issuenum += 1

                if issuenum > 1000:
                    raise ValueError("Can't move to trash folder since file repeatedly defined.")
        shutil.move(filename, trashname)


# Run:{{{1
if __name__ == '__main__':
    trashfunc()

