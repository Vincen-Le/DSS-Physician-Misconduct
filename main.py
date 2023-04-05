from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import requests as requests
import time

driver = webdriver.Chrome(
    '/Desktop/Berkeley/DSS-Physician-Misconduct/chromedriver')


def main():
    url = 'https://mqa-internet.doh.state.fl.us/MQASearchServices/EnforcementActionsPractitioner'
    driver.get(url)
    time.sleep(5)
    performSearch("BoardDD", "15")
    time.sleep(5)


def performSearch(id, value):
    board_dropdown = Select(driver.find_element(By.ID, id))
    board_dropdown.select_by_value(value)
    search_button = driver.find_element(
        By.XPATH, '//*[@id="content"]/div/form[1]/fieldset/p/input')
    search_button.click()


main()