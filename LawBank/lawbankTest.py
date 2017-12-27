from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import time, json


options = webdriver.ChromeOptions()
options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

#options.add_argument('headless')
options.add_argument('incognito')
driver = webdriver.Chrome(chrome_options=options)

driver.get('http://fyjud.lawbank.com.tw/index.aspx')

elements =driver.find_elements_by_css_selector('input[type=checkbox]')

for element in elements:
    if not element.is_selected():
        element.click()

keyword = driver.find_element_by_id('kw')
keyword.clear()
keyword.send_keys('郭國勝')

form = driver.find_element_by_id('form1')
form.submit()

driver.switch_to_default_content()
driver.switch_to_frame('menuFrame')
lists = driver.find_elements_by_css_selector('li')

courts = []


for li in lists:
    if not li.text.endswith('(0)'):
        courts.append(li.find_element_by_css_selector('a').get_attribute('href'))

for c in courts:
    driver.get(c)
    driver.find_elements_by_css_selector('#table3 a')[0].click()
    print(driver.find_element_by_css_selector('.Table-List tr:nth-child(1)').text)
    
    nextPage = driver.find_element_by_css_selector('tbody > tr:nth-child(1) > td:nth-child(2) > a:nth-child(3)')
    
    print(nextPage.text)
    while nextPage.is_displayed():
        nextPage.click()
        with open('1.txt','a',encoding='UTF-8') as fileWriter:
            fileWriter.write(driver.find_element_by_css_selector('.Table-List tr:nth-child(1)').text)
            fileWriter.write(driver.find_element_by_css_selector('.Table-List tr:nth-child(2)').text)
            fileWriter.write(driver.find_element_by_css_selector('.Table-List tr:nth-child(3)').text)
            fileWriter.write(driver.find_element_by_css_selector('.Table-List tr:nth-child(4)').text)
            fileWriter.write(driver.find_element_by_css_selector('.Table-List tr:nth-child(5)').text)
        print(driver.find_element_by_css_selector('.Table-List tr:nth-child(1)').text)
        nextPage = driver.find_element_by_css_selector('tbody > tr:nth-child(1) > td:nth-child(2) > a:nth-child(3)')
