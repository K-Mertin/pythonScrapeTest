from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import sys


try:
    options = webdriver.ChromeOptions()
    options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    #options.add_argument('headless')
    options.add_argument('window-size=1600x900')

    driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.PhantomJS(r'C:\Users\Mertin\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get("http://easymap.land.moi.gov.tw/P02/Index")

    #driver.execute_script("redirectEntranceR02();")
    #elem = driver.find_element_by_id('system')
    #elem.click()

    elem = driver.find_element_by_id("landno")
    elem.send_keys("1") 

    select = Select(driver.find_element_by_id("select_city_id"))
    select.select_by_visible_text("基隆市")
    
    time.sleep(0.5)

    select = Select(driver.find_element_by_id("select_town_id"))
    select.select_by_visible_text("七堵區")
    select.
    time.sleep(0.5)

    elem = driver.find_element_by_id("select_sect_id")
    elem.send_keys("(0027)")
    elem.send_keys(Keys.RETURN)

    time.sleep(0.5)

    elem = driver.find_element_by_id('land_button')
    elem.click()

    time.sleep(3)

    try:
        #driver.save_screenshot('test.jpg')
        alert = driver.switch_to_alert()
        print (alert.text)
        alert.accept()
    except:
        print("Unexpected error1:", sys.exc_info()[0])
        print ("no alert")
        #elem = driver.find_element_by_class_name('tip-yellowsimple')
        #driver.execute_script("document.getElementsByClassName('tip-yellowsimple')[0].style = '';")
        driver.save_screenshot('test.jpg')
except:
    print("Unexpected error2:", sys.exc_info()[0])
finally:
    driver.close()
    driver.quit()
