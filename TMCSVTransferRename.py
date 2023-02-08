""" Recive Beat Trom TargetMedia.py
"""
# Imports
import os, logging, shutil, glob, time
from datetime import date

# Setting up Program
today = date.today()
loggingfilename = str(today) + "-TM.log"
logging.basicConfig(filename=loggingfilename, filemode="w", level=logging.INFO)


# User Set Constants
downloadsPath = os.getenv("TM_CSV")
fileDestination = os.getenv("TM_PATH")
fileArchive = os.getenv("TM_ARCHIVE")
allFiles = glob.glob(fileDestination + "/*.csv")

# Functions


def Archive():
    """Archives files"""
    try:
        for item in allFiles:
            filename = item.replace(os.getenv("MIMIK_ROOT"), "")
            print("this is item now ->", filename)
            shutil.move(item, fileArchive)

    except:
        print("skipped", item)


def Move():
    try:
        shutil.move(downloadsPath, fileDestination)

    except:
        print("skipped")


# Renames file
def Rename(beat):
    while True:
        beat = beat.replace(" ", "-")
        sBeatcsv = beat + "-TM-" + str(today) + ".csv"
        os.rename(
            os.getenv("TM_MIMIK_CSV"),
            os.getenv("TM_PATH") + str(sBeatcsv),
        )


# Checks if file exists.
def check(beat):
    time.sleep(5)
    breturn = False
    global downloadsPath
    try:
        csvfile = open(downloadsPath)
        breturn = True
        Move()
        Rename(beat)
    except:
        logging.info("Csv File not found, TMCSVTransferRename retriggered csv click.")

    return breturn
