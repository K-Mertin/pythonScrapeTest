import pymongo
import datetime
import time
from bson.objectid import ObjectId

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:37017', username='mertin',
                         password='mertin', authSource='konew')
    db = client['konew']
    return db

def add_request(db, request):
    request['status'] = 'created'
    request['createDate'] = datetime.datetime.now()
    request['requestId'] = time.time()
    return db['Requests'].insert(request)

def remove_request(db, id):
    return db['Requests'].update_one({'_id': ObjectId(id)}, {'$set': {'status': 'removed'}})

def change_reference(db, id, refKey):
    return db['Requests'].update_one({'_id': ObjectId(id)}, {'$set': {'referenceKey': refKey, 'status': 'modified'}})

def get_process_requests(db):
    return db['Requests'].find({'status': {"$in": ['created']}})

def get_modified_requests(db):
    return db['Requests'].find({'status': {"$in": ['modified']}})

def get_processing_requests(db):
    return db['Requests'].find({'status': {"$in": ['processing']}})

def processing_requests(db, id, totalCount):
    return db['Requests'].update_one({'_id': ObjectId(id)}, {'$set': {'status': 'processing', 'totalCount': totalCount}})

def insert_documents(db, collection, documents):
    return db[collection].insert(documents)

if __name__ == "__main__":
    request = {
        "searchKeys": ["康業資本"],
        "referenceKeys": ["台北"]
    }
    documents = [
        {
            "searchKeys":["康業資本"],
            "referenceKeys":["RK1"],
            "tags":["tagA","tagB"],
            "title": "title A",
            "content":"content A"
        },
        {
             "searchKeys":["康業資本"],
            "referenceKeys":["RK2"],
            "tags":["tagA","tagC"],
            "title": "title B",
            "content":"content B"
        }
    ]
    db = get_db()

    # refKey = ['A']
    # refKey.append('B')

    # remove_request(db,id)
    results = get_process_requests(db)
    for result in results :
        print(result['requestId'])
        # processing_requests(db,result['_id'])
        insert_documents(db,str(result['requestId'])+result['searchKey'][0],documents)
    # result=add_request(db,request)
