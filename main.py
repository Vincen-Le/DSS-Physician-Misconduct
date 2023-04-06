from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import requests as requests
import time

driver = webdriver.Chrome(
    '/Desktop/Berkeley/DSS-Physician-Misconduct/chromedriver')
case_contents = {}


def main():
    url = 'https://mqa-internet.doh.state.fl.us/MQASearchServices/EnforcementActionsPractitioner'
    driver.get(url)
    time.sleep(5)
    performSearch("BoardDD", "15")
    time.sleep(5)
    xpath = '//*[@id="content"]/div/table/tbody[1]/tr[1]/td[7]/a'

    all_cases = getAllCases('//*[@id="content"]/div/table')
    print(all_cases)


def performSearch(id, value):
    board_dropdown = Select(driver.find_element(By.ID, id))
    board_dropdown.select_by_value(value)
    search_button = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/form[1]/fieldset/p/input')
    search_button.click()


def openCase(xpath):
    case = driver.find_element(By.XPATH, xpath)
    case_number = driver.find_element(By.XPATH, xpath).text
    print(case_number)
    case.click()


def getAllCases(xpath):
    all_cases = []
    size_of_table = len(driver.find_elements(By.XPATH, xpath + '/tbody[1]/tr'))
    print(size_of_table)

    for i in range(1, 21):
        temp = xpath + '/tbody[1]/tr[{}]/td[7]/a'.format(i)
        if driver.find_element(By.XPATH, temp):
            case_num = driver.find_element(By.XPATH, temp).text
        else:
            temp = xpath + '/tbody[1]/tr[{}]/td[7]'.format(i)
            case_num = driver.find_element(By.XPATH, temp).text
        print(case_num)

    return all_cases


main()