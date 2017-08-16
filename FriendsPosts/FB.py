from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys
import configparser
import json
import logging
import os
import pprint

class FBPostParser:

    def __init__(self):
        self.Setting()
        self.LoadDriver()
         
    def Setting(self):
        self.config = configparser.ConfigParser()
        print(os.getcwd())
        with open('Config.ini') as file:
            self.config.readfp(file)

        self.listFilePath = self.config.get('Options','Facebook_List')
        self.browserLocation = self.config.get('Options','Chrome_Location')
        self.userData = self.config.get('Options','Chrome_UserData')
        self.logPath = self.config.get('Options','Log_Path')
        
        formatter = logging.Formatter('[%(name)-12s %(levelname)-8s] %(asctime)s - %(message)s')
        self.logger=logging.getLogger(__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        
        if not os.path.isdir(self.logPath):
            os.mkdir(self.logPath)

        fileHandler = logging.FileHandler(self.logPath+'log.txt')
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.DEBUG)
        streamHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)
  
        #load list
        with open(self.listFilePath) as file:
            self.fbUserList = json.load(file)

        self.logger.info('Finish Setting')

    def LoadDriver(self):
        self.logger.info('Driver Loading')
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = self.browserLocation
        #self.options.add_argument(self.userData)
        #self.options.add_argument('headless')
        #self.options.add_argument(self.userData)
        self.options.add_argument('incognito')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.logger.info('Finish Driver Loading')
    
    def ProcessPosts(self, yearCount, postsCount):
        try:
            self.driver.implicitly_wait(10)
            contents = self.driver.find_elements_by_class_name('userContent')
            unExanded = self.driver.find_elements_by_class_name('fbTimelineTimePeriodUnexpanded')

            while len(unExanded)>yearCount and len(contents) < postsCount:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                self.driver.implicitly_wait(10)
                contents = self.driver.find_elements_by_class_name('userContent')
                unExanded = self.driver.find_elements_by_class_name('fbTimelineTimePeriodUnexpanded')      
            
            print('{}/{}'.format(contents,unExanded))
            for i in contents:
                print(i.text)

        except:
            print("Unexpected error1:", sys.exc_info()[0])
    
    def LoginFB(self,email,password):
        
        try:
            self.logger.info('try to login')
            self.driver.get('https://www.facebook.com/')

            # emailElement = self.driver.find_element_by_css_selector('input[type=email]')
            # passwordElement = self.driver.find_element_by_css_selector('input[type=password]')
            # loginElement = self.driver.find_element_by_css_selector('input[value="登入"]')
            emailElement = self.driver.find_element_by_xpath('//*[@id="email"]')
            passwordElement = self.driver.find_element_by_xpath('//*[@id="pass"]')
            loginElement = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')

            emailElement.send_keys(email)
            self.driver.implicitly_wait(100)
            passwordElement.send_keys(password)
            self.driver.implicitly_wait(100)
            loginElement.click()
            self.driver.get('https://www.facebook.com/profile/')
            try:
                self.driver.find_element_by_xpath('//*[@id="fb-timeline-cover-name"]')
            except NoSuchElementException:
                self.logger.error('login fail')
                return False,'login fail'
            
            self.logger.info('Success login')
            return True,'Success login'
        except NoSuchElementException:
            self.logger.info('already login')
            return True,'already login'
        except:
            self.logger.error(sys.exc_info()[0])
            pprint.pprint(sys.exc_info())
            return False,sys.exc_info()[0]
        

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass

def main():
    logging.info(__name__)
    parser = FBPostParser()

if __name__ == '__main__':
    main()



# try:
#     config = ConfigParser.ConfigParser()
#     config.read('Config.ini')

#     options = webdriver.ChromeOptions()
#     options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
#     #options.add_argument('headless')
#     options.add_argument('window-size=1600x900')
#     options.add_argument("user-data-dir=C:/Users/Mertin/AppData/Local/Google/Chrome/User Data")

    
#     driver = webdriver.Chrome(chrome_options=options)
#     #driver = webdriver.PhantomJS(r'C:\Users\Mertin\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
#     driver.get("https://www.facebook.com/yuke1015")
    
#     #  var name=document.getElementById("fb-timeline-cover-name").innerText;
#     #  var content= document.getElementsByClassName("_5pbx userContent");
#     #          var elem = document.getEle mentsByClassName("fbTimelineTimePeriodUnexpanded"); 
#     #          var id = setInterval(scroll, 10);
#     driver.implicitly_wait(10)
#     contents = driver.find_elements_by_class_name('userContent')

#     try:
#         unExanded = driver.find_elements_by_class_name('fbTimelineTimePeriodUnexpanded')
#         contents = driver.find_elements_by_class_name('userContent')
#         print('{}/{}'.format(len(unExanded),len(contents)))
#         while len(unExanded)>0 and len(contents) < 100:
#             driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
#             driver.implicitly_wait(10)
#             contents = driver.find_elements_by_class_name('userContent')
#             unExanded = driver.find_elements_by_class_name('fbTimelineTimePeriodUnexpanded')      
#             print('{}/{}'.format(len(unExanded),len(contents)))
#     except unExanded.NoSuchElementException:
#         print(len(contents))
#         print('{}/{}'.format(len(unExanded),len(contents)))
#     except:
#         print("Unexpected error1:", sys.exc_info()[0])
# except:
#     print("Unexpected error2:", sys.exc_info()[0])
# finally:
#     driver.close()
#     driver.quit()
