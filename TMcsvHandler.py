# Imports
import os
import logging
import time
import glob
import shutil
import regex
from datetime import date
import xlsx2csv
import pandas as pd


# Program setup
today = date.today()
filename = os.getenv("LOG_PATH") + str(today) + "-MM.log"
logging.basicConfig(filename=filename, filemode="w", level=logging.INFO)
startTime = time.time()


# File Paths etc.

csvFiles = glob.glob(os.getenv("TM_PATH") + "/*.csv")


# Loop through each file
for sFile in csvFiles:
    print("\n\nthis is sFile", sFile)

    # Opening csv and replacing header with first row
    df = pd.read_csv(sFile, header=[1])
    df.head()
    df.drop(index=df.index[0], axis=0, inplace=True)

    # Deleting column 'Phone'
    df = df.drop("Phone", 1)

    # Deleting column 'Fax'
    df = df.drop("Fax", 1)

    # Renaming 'Mobile' To 'Telephone'
    df = df.rename(columns={"Mobile": "Telephone"})

    # Renaming 'Media' To 'Publication'
    df = df.rename(columns={"Media": "Publication"})

    # Inserting Prefix at correct location
    df.insert(0, "Prefix", " ")

    # Renaming 'Designation' To 'Title'
    df = df.rename(columns={"Designation": "Title"})

    # Moving Title column
    column_to_move = df.pop("Title")
    df.insert(4, "Title", column_to_move)

    # Moving Publication column
    column_to_move = df.pop("Publication")
    df.insert(4, "Publication", column_to_move)

    # Creating Sub-Beat Column -> Need to fill it
    sbeatname = sFile.replace(".csv", "")
    sbeatname = sbeatname.replace(os.getenv("TM_PATH"), "")
    sbeatname = regex.sub(r"\-\w\w\-\d\d\d\d.*", "", sbeatname)
    df.insert(7, "Sub Beat", sbeatname)

    # Creating Contact Source column
    df.insert(8, "Contact Source", "Target Media")

    # Placing '; ' as delimiter in Email
    df["Email"] = df["Email"].str.replace(" ", "; ")

    # Removing non numeric characters from Telephone
    df["Telephone"] = df["Telephone"].str.replace(r"\D+", "")

    # Iterating through each value in column Telephone and seperating telephone numbers
    for key, value in df.iterrows():
        location = location = df.index.get_loc(key) + 1
        tel = value["Telephone"]
        tel = str(tel)
        print("This is Tel ->", tel)
        if tel != "nan":
            lengthT = len(tel)
            print("This is len of Tel ->", lengthT)
            split_strings = []
            n = 10
            for index in range(0, lengthT, n):
                split_strings.append(tel[index : index + n])
            Telephone = "; ".join(split_strings)
            print("This is telephone ->", Telephone)

        else:
            Telephone = "N/a"

        # Writing to Telephone
        df.at[location, "Telephone"] = Telephone

    # Cleaning out Advertising Titles.
    df = df[~df.Title.str.contains("Adverti", na=False)]

    # Displaying output
    print(df)

    # Saving to csv
    archive = sFile.replace("/TM/", "/TM/Archive/")
    shutil.move(sFile, archive)
    df.to_csv(sFile, index=False)

# Finish and Quit Prorgam
endTime = time.time()
totalTime = round(endTime - startTime, 2)
logging.info("TMcsvHandler took %s seconds to run" % (totalTime))
print("\n\n PROGRAM COMPLETE")
logging.info("\n\n TMcsvHandler PROGRAM COMPLETE")
