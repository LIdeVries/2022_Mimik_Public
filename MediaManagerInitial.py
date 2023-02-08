""" Include the Beat name in all so Sjarn can do secondary filtering. . . 




"""


# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
import dotenv
import os
import logging
import time
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains


today = date.today()
filename = os.getenv("LOGPATH") + str(today) + "-MM.log"

# Program setup
logging.basicConfig(filename=filename, filemode="w", level=logging.INFO)
chromedriver = os.getenv("CHROMEDRIVER")
link = "CHROMEDRIVER_PATH"
# options.add_argument("--headless")
# browser = webdriver.Chrome(chromedriver,options=options)
browser = webdriver.Chrome(chromedriver)


beatList = ["Business:", "Beauty", "Women", "Fashion", "Broadcast", "Newspapers"]


# Chromedriver Initial naviatgion
browser.get(link)
browser.maximize_window()
actions = ActionChains(browser)
startTime = time.time()

# Enters passwords
email = os.getenv("MM_USER")
password = os.getenv("MM_PW")


# Navigate -> Accept Cookies
cookies = WDW(browser, 10).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Got it!"))
)
cookies.click()
time.sleep(2)

# Logging into MM
enterEmail = WDW(browser, 10).until(EC.presence_of_element_located((By.ID, "email")))
enterEmail.clear()
enterEmail.send_keys(email)

enterPW = WDW(browser, 10).until(EC.presence_of_element_located((By.ID, "password")))
enterPW.clear()
enterPW.send_keys(password)

# Enter site
loginButton = WDW(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]'))
)
loginButton.click()
time.sleep(2)


# Entering into beat
for beat in beatList:
    browser.get(os.getenv("CATEGORIES_URL"))
    print("This is Beat", beat)
    logging.info("\n\nFor %s :" % beat)

    # Localising search for industries to main body
    body = WDW(browser, 10).until(EC.presence_of_element_located((By.ID, "main_body")))

    # Creating list of Publication type per beat
    hrefList = []
    industries = WDW(body, 10).until(
        EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, beat))
    )
    for industry in industries:

        href = industry.get_attribute("href")
        logging.info("\nCaptured, %s at %s." % (industry.text, href))
        print("Captured", industry.text, "for", beat, "at", href)
        if href != os.getenv("IGNORE_LINK"):
            hrefList.append(href)

    # Cycling through Publication Type
    for href in hrefList:
        browser.get(href)

        # Navigating to media section
        mediaTab = WDW(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Media"))
        )
        mediaTab.click()
        time.sleep(2)

        # Selecting All Partaing Companies
        selectAll = WDW(browser, 10).until(
            EC.presence_of_element_located((By.ID, "months_all"))
        )
        selectAll.click()

        # Clicking Export to Key People
        export = WDW(browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="target_form"]/div[2]/button')
            )
        )
        export.click()

        # Choosing Editorial People
        editorial = WDW(browser, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="target_form"]/div[2]/ul/li[1]/a')
            )
        )
        editorial.click()

        # Selecting Excel
        excel = WDW(browser, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="export_people_modal"]/div/div/div[2]/div[2]/button[3]',
                )
            )
        )
        excel.click()

        # Closing window
        close = WDW(browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="export_people_modal"]/div/div/div[2]/div[2]/button[1]',
                )
            )
        )
        close.click()

        time.sleep(3)
        browser.back()
        time.sleep(3)


# FTinish and Quit Prorgam
endTime = time.time()
totalTime = round(endTime - startTime, 2)
time.sleep(10)
logging.info("Program took %s seconds" % (totalTime))
browser.quit()
print("\n\n PROGRAM COMPLETE")
logging.info("\n\n PROGRAM COMPLETE")
