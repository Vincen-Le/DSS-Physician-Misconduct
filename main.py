from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import requests as requests
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# PyTesseract Imports
import os
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

options = webdriver.ChromeOptions()
options.add_argument(
    "user-data-dir=/Users/vincentle/Library/Application Support/Google/Chrome/Default"
)

driver = webdriver.Chrome(
    '/Desktop/Berkeley/DSS-Physician-Misconduct/chromedriver', options=options)

case_contents = {}


def main():

    url = 'https://mqa-internet.doh.state.fl.us/MQASearchServices/EnforcementActionsPractitioner'
    driver.get(url)
    time.sleep(5)
    performSearch("BoardDD", "15")
    time.sleep(5)
    case_num = openCase('//*[@id="content"]/div/table/tbody[1]/tr[1]/td[7]/a')

    # Get all case numbers from column of current table in window
    # all_cases = getAllCases('//*[@id="content"]/div/table')

    #print(all_cases)
    print(case_num)


# Performs initial search on medical board's homepage
def performSearch(id, value):
    board_dropdown = Select(driver.find_element(By.ID, id))
    board_dropdown.select_by_value(value)
    search_button = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/form[1]/fieldset/p/input')
    search_button.click()


# Opens case pdf
def openCase(xpath):
    case = driver.find_element(By.XPATH, xpath)
    case_number = driver.find_element(By.XPATH, xpath).text
    case.click()
    return case_number


# Collects all case numbers
def getAllCases(xpath):
    all_cases = []
    size_of_table = len(driver.find_elements(By.XPATH, xpath + '/tbody[1]/tr'))
    print(size_of_table)

    for i in range(1, size_of_table + 1):
        temp = xpath + '/tbody[1]/tr[{}]/td[7]/a'.format(i)
        exists = check_exists_by_xpath(temp)
        if exists:
            case_num = case_num = driver.find_element(By.XPATH, temp).text
            #case_num = openCase(temp)
        else:
            temp = xpath + '/tbody[1]/tr[{}]/td[7]'.format(i)
            case_num = case_num = driver.find_element(By.XPATH, temp).text
            #case_num = openCase(temp)
        all_cases.append(case_num)

    return all_cases


# Checks if element exists
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# PyTesseract
def pyTest():
    filePath = 'Florida_Sample.pdf'
    doc = convert_from_path(filePath)
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)

    for page_number, page_data in enumerate(doc):
        parray = np.asarray(page_data)
        txt = pytesseract.image_to_string(
            Image.fromarray(parray)).encode("utf-8")
        print("Page # {} - {}".format(str(page_number), txt))


main()