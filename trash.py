#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}


import os
import shutil
import subprocess
import sys
import time


def trashfunc(trashfolder, oldversionsname = 'old_versions'):
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
