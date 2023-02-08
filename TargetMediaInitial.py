"""READ ME - Trouble Shooting

1. Media lists are listed alphabecially on the site, when adding new items to media lists. All positional arguments need to be updated.
2. Positional arguments are used because of the containers TM uses.
3. Their site (TM) for some reason will stop you from adding to certain Media lists, if you're getting dropping contact numbers, refresh these lists. 
4. ?? Might be future problem... If media lists have 0 entries, the program get's stuck. . . Might need to work-around.  
5. Dowloads folder needs to be empty to work. 
"""


# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
import time
import re
from datetime import date
import TMCSVTransferRename


# Program setup
print("Launching...")
today = date.today()
filename = os.getenv("LOG_PATH") + str(today) + "-TM.log"
logging.basicConfig(filename=filename, filemode="w", level=logging.INFO)
chromedriver = os.getenv("CHROMEDRIVER_PATH")
link = os.getenv("TM_LINK")
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
browser = webdriver.Chrome(chromedriver, options=options)
# browser = webdriver.Chrome(chromedriver)
print("Driver Set...")
browser.maximize_window()
actions = ActionChains(browser)

beauty = {
    "Name": "Beauty",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[15]/div/div[2]/div/div[5]/div/span/div/input",
    "Station": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[15]/div/div[3]/div/div[5]/div/span/div/input",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[13]/div/div[3]/div/div[5]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[1]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[1]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[1]/td[4]",
}

business = {
    "Name": "Business",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[16]/div/div[2]/div/div[4]/div/span/div/input",
    "Station": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[16]/div/div[3]/div/div[4]/div/span/div/input",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[14]/div/div[3]/div/div[4]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[2]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[2]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[2]/td[4]",
}

fashion = {
    "Name": "Fashion",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[15]/div/div[2]/div/div[9]/div/span/div/input",
    "Station": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[15]/div/div[3]/div/div[9]/div/span/div/input",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[13]/div/div[3]/div/div[9]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[3]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[3]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[3]/td[4]",
}

financialServices = {
    "Name": "Financial services",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[16]/div/div[2]/div/div[9]/div/span/div/input",
    "Station": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[16]/div/div[3]/div/div[9]/div/span/div/input",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[14]/div/div[3]/div/div[9]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[4]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[4]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[4]/td[4]",
}

womenFocus = {
    "Name": "Women Focus",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[13]/div/div[2]/div/div[13]/div/span/div/input",
    "Station": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[13]/div/div[3]/div/div[13]/div/span/div/input",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[11]/div/div[3]/div/div[13]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[6]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[6]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

##########################################################################################

dailyNewspaper = {
    "Name": "Daily Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[1]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

localRuralNewspaper = {
    "Name": "Local Rural Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[4]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

saturdayNewspaper = {
    "Name": "Saturday Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[7]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

governmentInsert = {
    "Name": "Government Insert",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[2]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

localUrbanNewspaper = {
    "Name": "Local Urban Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[5]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

sundayNewspaper = {
    "Name": "Sunday Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[8]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

localNewspaperInsert = {
    "Name": "Local Newspaper Insert",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[3]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

monthlyNewspaper = {
    "Name": "Monthly Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[6]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

weeklyNewspaper = {
    "Name": "Weekly Newspaper",
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[2]/div/div[9]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

articleSite = {
    "Name": "Article Site",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[3]/div[4]/div/div[1]/div/span/div/div",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}

blogSite = {
    "Name": "Blog Site",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[3]/div[4]/div/div[2]/div/span/div/input",
    "MlAdds": '//*[@id="my-media-lists-modal"]/div/div/div[2]/section/div/div[2]/table/tbody/tr[5]/td[1]/input',
    "MlSelect": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[3]",
    "listLength": "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div[3]/table/tbody/tr[5]/td[4]",
}


sa = {
    "Publication": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[18]/div[3]/div/div[53]/div/div[1]/div/span[2]/div/input",
    "Station": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[18]/div[4]/div/div[53]/div/div[1]/div/span[2]/div/input",
    "Website": "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[16]/div[4]/div/div[53]/div/div[1]/div/span[2]/div/input",
}

beatList = [
    business,
    financialServices,
    beauty,
    womenFocus,
    fashion,
    dailyNewspaper,
    localRuralNewspaper,
    saturdayNewspaper,
    governmentInsert,
    localUrbanNewspaper,
    sundayNewspaper,
    localNewspaperInsert,
    monthlyNewspaper,
    weeklyNewspaper,
    blogSite,
]

typelist = ["Publication", "Station", "Website"]


# Functions
def Type(name):
    string = "//*[ text() = '" + name + "']"

    type = WDW(browser, 30).until(EC.presence_of_element_located((By.XPATH, string)))
    type.click()


def Adv():

    adv = WDW(browser, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@ng-click='showAdvancedSearch = true;']")
        )
    )
    adv.click()


def Dropdowns():

    # Industry -> Clicks the dropdown elements of those which are clickable
    industries = WDW(browser, 30).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//button[@ng-click='limitCategory == 3 ? limitCategory = 99 : limitCategory = 3']",
            )
        )
    )
    for industry in industries:
        try:
            industry.click()
        except:
            pass


def Region():
    Adv()
    time.sleep(5)
    region = WDW(browser, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[@ng-click='limitRegion == 3 ? limitRegion = 99 : limitRegion = 3']",
            )
        )
    )
    region.click()


def SA(Sa):
    # Opens regional dropdown
    Region()
    # click's Sa
    sa = WDW(browser, 30).until(EC.presence_of_element_located((By.XPATH, Sa)))
    sa.click()


def MlChecks(rng1, rng2, top):
    Tcount = 0
    for num in range((rng2 - rng1), top):

        # Get Xpath
        xpath = (
            "/html/body/div[2]/div/div/div/div/div[2]/section/div/div[2]/div[3]/div[3]/table/tbody/tr["
            + str(num)
            + "]/td[1]/input"
        )
        try:
            check = WDW(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            check.click()
            time.sleep(0.1)
            Tcount += 1
        except:
            pass
    print("Counted clicks ->", Tcount)


def MlcContacts():

    for i in range(2, 13):
        xpath = (
            "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/section/div[2]/div/div[2]/table/tbody/tr["
            + str(i)
            + "]/td[1]/input"
        )
        check = WDW(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        check.click()


def downloadWait(directory, timeout, nfiles=None):

    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith(".crdownload"):
                dl_wait = True

        seconds += 1
    return seconds


# Chromedriver Initial naviatgion
browser.get(link)
startTime = time.time()


# Enter passwords

email = os.getenv("TM_USER")
password = os.getenv("TM_PW")


# Navigate -> Accept Cookies
cookies = WDW(browser, 30).until(
    EC.presence_of_element_located((By.XPATH, "//button[@onclick='AcceptCookies()']"))
)
cookies.click()
print("Cookies Accepted...")

# Navitgate -> login
Login = WDW(browser, 10).until(EC.presence_of_element_located((By.ID, "footer-login")))
Login.click()
browser.implicitly_wait(5)
print("logging in...")

# Fill Login
enterEmail = WDW(browser, 10).until(
    EC.presence_of_element_located((By.ID, "txtLoginEmail"))
)
enterEmail.send_keys(email)
enterPw = WDW(browser, 10).until(
    EC.presence_of_element_located((By.ID, "txtLoginPassword"))
)
enterPw.send_keys(password)
time.sleep(1)

# Enter site
loginButton = WDW(browser, 10).until(
    EC.presence_of_element_located((By.ID, "btnLogin"))
)
loginButton.click()
time.sleep(10)

# Looping through publication type
for beat in beatList:
    for type in typelist:
        try:
            print("Starting", type, "for", beat["Name"])
            logging.info("Starting %s for %s" % (type, beat["Name"]))
            # Captures the total number of proposed contacts in the beat
            numberTotal = 0

            # Navigation -> search
            browser.get(os.getenv("TM_SEARCH_LINK"))
            time.sleep(2)

            # Navigation of Type of publication
            Type(type)

            # Select South Africa as region
            SA(sa[type])

            # Opening the dropdown of all
            Dropdowns()

            # While loop to catch a fragile click -> This is very fragile when not run in Headless. How goes in headless?
            while True:
                try:
                    # Finding the correct beat.
                    currentBeat = WDW(browser, 30).until(
                        EC.presence_of_element_located((By.XPATH, beat[type]))
                    )

                    print("Beginning page ups...")
                    time.sleep(5)
                    html = browser.find_element_by_tag_name("html")
                    html.send_keys(Keys.PAGE_UP)
                    time.sleep(0.5)
                    html.send_keys(Keys.PAGE_UP)
                    time.sleep(0.5)
                    html.send_keys(Keys.PAGE_UP)
                    time.sleep(0.5)
                    html.send_keys(Keys.PAGE_UP)
                    time.sleep(5)
                    print("Paged up...")
                    if "ewspaper" in beat["Name"]:
                        # Media -> Clicks the dropdown elements of those which are clickable
                        medias = WDW(browser, 30).until(
                            EC.presence_of_all_elements_located(
                                (
                                    By.XPATH,
                                    "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/div/div[2]/div[3]/span/div[5]/div[1]/button",
                                )
                            )
                        )
                        for media in medias:
                            try:
                                media.click()
                            except:
                                pass
                    currentBeat.click()
                    break
                except:
                    logging.info(
                        'This thing failed to click category at %s @ "Finding the Correct beat." Common fragility. '
                        % beat[type]
                    )
                    continue

            # Searching for the beat
            search = WDW(browser, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[@ng-click="SearchFVC();"]')
                )
            )
            search.click()

            # Finding Max list -> Achives this by counting the list items within the scroll-able body centre screen.
            number = 0
            body = WDW(browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//tbody[@class="ml-body"]'))
            )
            numbers = WDW(body, 30).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//td[@class="text-center"]')
                )
            )

            for item in numbers:
                number += 1
            print("This is count ->", number)
            logging.info(" %s of clicks in media for %s" % (number, beat["Name"]))

            # The below list is of the xpath for each grey box we want the text of.
            lbuttonlist = [
                "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/span[2]",
                "/html/body/div[2]/div/div/div/div/div[1]/div[2]/section/span[3]",
            ]
            # Logging results
            lloggingl = []

            # Ensuring the correct categories were found
            for item in lbuttonlist:
                result = WDW(browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, item))
                )
                print("This is item list text ->", result.text)
                lloggingl.append(result.text)
            logging.info(
                "\n\nThe below list should not have any surprise Region or beat."
            )
            logging.info(lloggingl)

            # Setting comapny selector.
            rng2 = 200
            rng1 = rng2

            limit = number + 1

            # Company selector loop
            while number > 0:

                top = min(rng2, limit)

                # Checking boxes
                print("Selecting boxes...")
                MlChecks(rng1, rng2, top)

                # Adding selected items to a Media List
                add = WDW(browser, 30).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div/div/div/div/div[2]/section/div/div[2]/div[4]/button[3]",
                        )
                    )
                )
                add.click()

                # Selecting Media List for beat -> Try/Except is a plaster for the iterator in MLchecks not working
                Ml = WDW(browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, beat["MlAdds"]))
                )
                Ml.click()

                # Commiting add to selected Media list
                MlAdd = WDW(browser, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//button[@class="btn"]')
                    )
                )
                counta = 1
                for item in MlAdd:
                    try:
                        item.click()
                    except:
                        counta += 1

                # Unselecting Boxes
                print("Unselecting Boxes...")
                MlChecks(rng1, rng2, top)
                # Selecting next range to work
                number -= rng1
                rng2 += rng1
        except:
            print("No", type, "in", beat["Name"])
            pass
    #'''
    # Exporting Contacts
    # Media lists
    browser.get(os.getenv("TM_MY_MEDIA"))
    print("Working In Media List.")
    # Logging number of available and total captured contact companies.
    maxi = WDW(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, beat["listLength"]))
    )
    maxi = maxi.text
    logging.info("\n\n %s captured %s \n" % (beat["Name"], maxi))

    # Click selected Media list
    Ml = WDW(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, beat["MlSelect"]))
    )
    Ml.click()

    # Click on Media List Contacts
    Mlc = WDW(browser, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div/div[2]/ul/li[2]/a",
            )
        )
    )
    Mlc.click()

    # Logging Number of Contacts per beat
    contNumber = 0
    while contNumber == 0:
        try:
            contNumber = WDW(browser, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="list-well"]/span[1]')
                )
            )
            contNumber = contNumber.text
            reg = re.findall(r"\d+", contNumber)
            contNumber = max(reg)
            logging.info("%s contacts in %s" % (contNumber, beat["Name"]))
        except:
            print("Max Contact number reader failed...\nRetrying...")
            continue

    # Cycling through Media List Contact pages
    next = WDW(browser, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="list-well"]/span[2]/button[3]')
        )
    )
    while True:
        try:
            MlcContacts()
            time.sleep(1)
            next.click()
            time.sleep(1)
        except:
            break

    # Export To CSV -> Download times Affect download quality.
    breturn = False
    while breturn == False:
        csvButton = WDW(browser, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/section/div[2]/div/div[4]/div/span[2]/button",
                )
            )
        )
        csvButton.click()
        print("Clicking csv download button.")
        fileends = "crdownload"
        downloadWait(os.getenv("DOWNLOADS_PATH"), 20, 1)
        breturn = TMCSVTransferRename.check(beat["Name"])


# Finish and Quit Prorgam
endTime = time.time()
totalTime = round(endTime - startTime, 2)
time.sleep(10)
logging.info("Program took %s seconds" % (totalTime))

browser.quit()
print("\n\n PROGRAM COMPLETE")
logging.info("\n\n PROGRAM COMPLETE")
