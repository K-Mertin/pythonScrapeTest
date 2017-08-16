from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys
import configparser
import json

class FBPostParser:

    def __init__(self):
        self.Setting()
        self.LoadDriver()
         
    def Setting(self):
        print('setting')
        self.config = configparser.ConfigParser()
        self.config.read('Config.ini')
        self.listFilePath = self.config.get('SeleniumOptions','Facebook_List')
        self.browserLocation = self.config.get('SeleniumOptions','Chrome_Location')
        self.userData = self.config.get('SeleniumOptions','Chrome_UserData')

        #load list
        with open(self.listFilePath) as file:
            self.fbUserList = json.load(file)

        print('setted')

    def LoadDriver(self):
        print('loading')
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = self.browserLocation
        self.options.add_argument(self.userData)
        self.options.add_argument('headless')
        self.options.add_argument(self.userData)
       
        self.driver = webdriver.Chrome(chrome_options=self.options)
        print('loaded')
    
    def ProcessPosts(self, yearCount, postsCount):
        try:
            self.driver.implicitly_wait(10)
            contents = self.driver.find_elements_by_class_name('userContent')
            unExanded = self.driver.find_elements_by_class_name('fbTimelineTimePeriodUnexpanded')
            print('{}/{}'.format(len(contents) ,len(unExanded)))

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

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass

def main():
    print(__name__)
    parser = FBPostParser()
    
    print(parser.fbUserList)

    parser.driver.get('https://www.facebook.com/')

    try:
        parser.driver.get_screenshot_as_file('a.jpg')
        email = parser.driver.find_element_by_css_selector('input[type=email]')
        password = parser.driver.find_element_by_css_selector('input[type=password]')
        login = parser.driver.find_element_by_css_selector('input[value="登入"]')
        
        email.send_keys('')
        password.send_keys('')
        login.click()
    except NoSuchElementException:
        pass
    except:
        return
    
    for i in parser.fbUserList:
        parser.driver.get(i['url'])
        parser.driver.get_screenshot_as_file(i['name']+'.jpg')
        parser.ProcessPosts(0,10)

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
