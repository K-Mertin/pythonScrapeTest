import json
import re

line = '這是測試'

key ='123'

# data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

# json = json.dumps(data)
if re.search( key, line):
    print( re.search( key, line).group())
else:
    print('no exist')

