""" Converts to csv
    Performs cleaning
    Archives xlsx
"""


# Imports
import os
import logging
import time
import glob
import shutil
from datetime import date
import xlsx2csv
import pandas as pd


# Program setup
today = date.today()
filename = os.getenv("LOG_PATH") + str(today) + "-MM.log"
logging.basicConfig(filename=filename, filemode="w", level=logging.INFO)
startTime = time.time()


ExcelFiles = glob.glob(os.getenv("MM_PATH") + "/*.xlsx")


# Loop through each file
for sFile in ExcelFiles:
    print("\n\nthis is sFile", sFile)

    # Name
    fcsvname = sFile.replace(".xlsx", ".csv")
    fcsvname = fcsvname.replace("_ ", "_")
    fcsvname = fcsvname.replace(" ", "_")
    x2cws = xlsx2csv.Xlsx2csv(sFile, outputencoding="utf-8").convert(fcsvname)

    # Creating and cleaning csv to useable
    df = pd.read_csv(fcsvname)
    df.drop("Portfolios", inplace=True, axis=1)
    df.drop("Portfolio Type", inplace=True, axis=1)
    df.dropna(how="all", inplace=True)

    # Clean out Suspended publications.
    df = df[~df.Medium.str.contains("SuspendedPublication:")]

    # Cleaning out Advertising Titles.
    df = df[~df.Job.str.contains("Adverti", na=False)]

    # Concatinate Mediums Column per contact
    df = df.mask(df == 0).ffill()
    df["Medium"] = df.groupby("Name")["Medium"].transform(
        lambda Medium: "; ".join(Medium)
    )
    df.drop_duplicates(subset=None, inplace=True)

    # Renaming column 'Name' to 'Last Name'
    df.rename(columns={"Name": "Last Name"}, inplace=True)

    # Creating and moving First Name column
    df["First Name"] = pd.Series(dtype="str")
    column_to_move = df.pop("First Name")
    df.insert(0, "First Name", column_to_move)

    # Splitting out names to First and Last
    df[["Last Name", "First Name"]] = df["Last Name"].str.split(", ", expand=True)

    # Creating and moving Prefix column
    df["Prefix"] = pd.Series(dtype="str")
    column_to_move = df.pop("Prefix")
    df.insert(0, "Prefix", column_to_move)

    # Splitting out Prefix
    df[["Prefix", "First Name"]] = df["First Name"].str.split(r"\.\s", expand=True)

    # Creating Contact Source column
    df.insert(10, "Contact Source", "Media Manager")

    # Creating Sub-Beat Column -> Need to fill it
    sbeatname = fcsvname.replace(".csv", "")
    sbeatname = sbeatname.replace(os.getenv("KEY_PEOPLE_FROM_PATH"), "")
    df.insert(10, "Sub Beat", sbeatname)

    # Renaming 'Job' To 'Title'
    df = df.rename(columns={"Job": "Title"})

    # Renaming 'Medium' To 'Publication'
    df = df.rename(columns={"Medium": "Publication"})

    # Moving Publication column
    column_to_move = df.pop("Publication")
    df.insert(4, "Publication", column_to_move)

    # Renaming 'Medium' To 'Publication'
    df = df.rename(columns={"Medium": "Publication"})

    # Renaming 'Contact Details' To 'Telephone'
    df = df.rename(columns={"Contact Details": "Telephone"})

    # Deleting column 'Company'
    df = df.drop("Company", 1)

    # Deleting column 'Branch'
    df = df.drop("Branch", 1)

    # Deleting column 'Branch Physical Address'
    df = df.drop("Branch Physical Address", 1)

    # Deleting column 'Branch Postal Address'
    df = df.drop("Branch Postal Address", 1)

    # Resetting index
    df.reset_index(drop=True, inplace=True)

    # Cleaning out Advertising Titles.
    df = df[~df.Title.str.contains("Adverti", na=False)]

    print(df)
    # Saving to csv
    df.to_csv(fcsvname, index=False)

    # Moving .xlsx to Archive
    sArchivepath = sFile.replace("MM/", "MM/Archive/")
    shutil.move(sFile, sArchivepath)


# Finish and Quit Prorgam
endTime = time.time()
totalTime = round(endTime - startTime, 2)

logging.info("MMExcelHandler took %s seconds to run" % (totalTime))
print("\n\n PROGRAM COMPLETE")
logging.info("\n\n MMExcelHandler PROGRAM COMPLETE")
