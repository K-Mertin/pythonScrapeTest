from bs4 import BeautifulSoup


soup = BeautifulSoup(open('test.html'),'html.parser')

print (soup.prettify())
print (soup.title)
print (soup.a)
print (soup.select('#a2')[0].text)

input()
print ('sdfsdf')