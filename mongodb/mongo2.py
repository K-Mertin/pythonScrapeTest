# mongo2.py

# from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017/')
# mydb = client['test-database-1']

import datetime, time

filters = ['A','B']

filters= list(map(lambda x : [{'keyA':x},{'keyB':x},{'keyC':x}],filters ))
filters = sum(filters,[])
# mydb.mytable.insert(myrecord2)
# myrecord2[0]["status"]="test"
print(filters)