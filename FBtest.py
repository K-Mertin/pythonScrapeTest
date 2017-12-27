from FriendsPosts.FB import FBPostParser

parser = FBPostParser()

success,errMsg = parser.LoginFB('martinkms@yahoo.com.tw','a227720059')

print(parser.fbUserList)

for i in parser.fbUserList:
    parser.driver.get(i['url'])
    parser.driver.get_screenshot_as_file(i['name']+'.jpg')
    # parser.ProcessPosts(0,10)