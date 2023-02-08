# Imports
import pandas as pd
import os
import time
import logging
import glob
import shutil
from datetime import date

# Setting program up.
today = date.today()
logfilename = os.getenv("LOG_PATH") + str(today) + "-Final.log"
finaldocument = os.getenv("FINAL_DOC_PATH") + str(today) + "-Mimik-Final.xlsx"
logging.basicConfig(filename=logfilename, filemode="w", level=logging.INFO)
startTime = time.time()

Business = {"Name": "Business"}
Book_Review = {"Name": "Book Review"}
Gaming = {"Name": "Gaming"}
Health_SA = {"Name": "Health SA"}
Tech = {"Name": "Tech"}
Energy = {"Name": "Energy"}
Broadcast = {"Name": "Broadcast"}
Consumer = {"Name": "Consumer"}
Education = {"Name": "Education"}
Newspaper = {"Name": "Newspaper"}
Housing = {"Name": "Housing"}
Tourism = {"Name": "Tourism"}
Property = {"Name": "Property"}
Decor_and_Home_Design = {"Name": "Decor and Home Design"}
Women = {"Name": "Women"}
Beauty = {"Name": "Beauty"}


beatList = [
    Business,
    Book_Review,
    Gaming,
    Health_SA,
    Tech,
    Energy,
    Broadcast,
    Consumer,
    Education,
    Newspaper,
    Housing,
    Tourism,
    Property,
    Decor_and_Home_Design,
    Women,
    Beauty,
]


directoriesDict = {
    "TM": os.getenv("TM_PATH"),
    "MM": os.getenv("MM_PATH"),
}

writer = pd.ExcelWriter(finaldocument, engine="xlsxwriter")

# Finds and concatinates beats together into a single csv, files this under workings
for dictionary in beatList:
    csvlist = []
    namelist = []
    for directory in directoriesDict:
        Files = glob.glob(directory + "/*.csv")
        for file in Files:
            if dictionary["Name"] in file:
                filePath = os.path.abspath(file)
                namelist.append(filePath)

    # Generates csv for each beat
    for file in sorted(namelist):
        csvlist.append(pd.read_csv(file))
    try:
        csvmerged = pd.concat(csvlist, ignore_index=True)
        csvmerged.to_csv(
            os.getenv("WORKING_SPATH") + dictionary["Name"] + ".csv",
            index=False,
        )
    except:

        pass
    for file in sorted(namelist):
        # This is the archive function.
        filepath = os.path.abspath(file)
        if "MM/" in filepath:
            shutil.move(file, filepath.replace("MM/", "MM/Archive/"))
        if "TM/" in filepath:
            shutil.move(file, filepath.replace("TM/", "TM/Archive/"))


# Creating Unspecified.csv
namelist = []
for directory in directoriesDict:
    Files = glob.glob(directory + "/*.csv")
    for file in Files:
        filePath = os.path.abspath(file)
        namelist.append(filePath)
    csvlist = []
    for file in sorted(namelist):
        csvlist.append(pd.read_csv(file))


csvmerged = pd.concat(csvlist, ignore_index=True)
csvmerged.to_csv(os.getenv("WORKING_SPATH") + "/Unspecified.csv", index=False)

# this is archive function for Unspecified
for file in sorted(namelist):
    csvlist.append(pd.read_csv(file).assign(File_Name=os.path.basename(file)))
    # This is the archive function.
    filepath = os.path.abspath(file)
    if "MM/" in filepath:
        shutil.move(file, filepath.replace("MM/", "MM/Archive/"))
    if "TM/" in filepath:
        shutil.move(file, filepath.replace("TM/", "TM/Archive/"))

# Setting new directory
directory = os.getenv("WORKING_SPATH")
Files = glob.glob(directory + "/*.csv")

# Cleaning csv's final: Deleting mysterious 'Last Name' Column that appears.
for file in Files:
    df = pd.read_csv(file)
    headerslist = list(df.columns)
    if len(headerslist) > 9:
        df = df.iloc[:, :-1]
    df.to_csv(file, index=False)

# Writing to excel
today = date.today()
writer = pd.ExcelWriter(finaldocument, engine="xlsxwriter")


nameDict = {}
for file in Files:
    filename = os.path.basename(file)
    filename = filename.replace(".csv", "")
    nameDict[filename] = pd.read_csv(file)


for sheet_name in nameDict.keys():
    nameDict[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

writer.save()

# Cleaning out Workings folder
for file in Files:
    os.remove(file)

# Finish and Quit Prorgam
endTime = time.time()
totalTime = round(endTime - startTime, 2)

logging.info("FinalOutput took %s seconds to run" % (totalTime))
print("\n\n PROGRAM COMPLETE")
logging.info("\n\n FinalOutput PROGRAM COMPLETE")
