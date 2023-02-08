""" Recive Beat from MediaManagerInitial.py
"""
# Imports
import os
import logging
import shutil
import glob
import time
from datetime import date

# Setting up Program
startTime = time.time()
today = date.today()
loggingfilename = os.getenv("LOG_PATH") + str(today) + "-MM.log"
logging.basicConfig(filename=loggingfilename, filemode="w", level=logging.INFO)


# User Set Constants
downloadsPath = os.getenv("DOWNLOADS_PATH")
fileDestination = os.getenv("MM_PATH")
fileArchive = os.getenv(" MM_ARCHIVE")
allFiles = glob.glob(downloadsPath + "/*.xlsx")

# Functions


def Move(allFiles):
    for item in allFiles:
        shutil.move(item, fileDestination)


Move(allFiles)


endTime = time.time()
totalTime = round(endTime - startTime, 2)
logging.info("MMExcleTransferRename took %s seconds to run" % (totalTime))
print("\n\n PROGRAM COMPLETE")
logging.info("\n\n MMExcelHandler PROGRAM COMPLETE")
