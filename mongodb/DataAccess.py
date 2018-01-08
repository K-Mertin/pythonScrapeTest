import pymongo
import datetime
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import re

class DataAccess:

    def __init__(self):
        self.client = MongoClient('localhost:37017', username='mertin', password='mertin', authSource='konew')
        self.db = self.client['konew']

    def add_request(self, request):
        request['status'] = 'created'
        request['createDate'] = datetime.datetime.now()
        request['requestId'] = str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))+'-'+request['searchKeys'][0]
        request['searchKeys'] = list(map(lambda x:{"key":x, "count":0}, request['searchKeys']))
        return self.db['Requests'].insert(request)

    def remove_request(self, id):
        return self.db['Requests'].update_one({'_id': ObjectId(id)}, {'$set': {'status': 'removed'}})

    def change_reference(self, id, refKey):
        return self.db['Requests'].update_one({'_id': ObjectId(id)}, {'$set': {'referenceKeys': refKey, 'status': 'modified'}})
    
    def update_document_reference(self, collection, id, referenceKeys ):
        return self.db[collection].update_one({'_id': ObjectId(id)}, {'$set': {'referenceKeys': referenceKeys}})

    def get_created_requests(self):
        return self.db['Requests'].find().sort("createDate", pymongo.DESCENDING)

    def get_modified_requests(self):
        return self.db['Requests'].find({'status': {"$in": ['modified']}})

    def get_processing_requests(self):
        return self.db['Requests'].find({'status': {"$in": ['processing']}})

    def processing_requests(self, id, searchKey, totalCount):
        return self.db['Requests'].update_one({'_id': ObjectId(id), 'searchKeys.key':searchKey}, {'$set': {'status': 'processing', 'searchKeys.$.count':totalCount}})

    def finish_requests(self, id):
        return self.db['Requests'].update_one({'_id': ObjectId(id)}, {'$set': {'status': 'finished'}})

    def insert_documents(self, collection, documents):
        return self.db[collection].insert_many(documents)

    def get_all_documents(self, collection='1514966746.2558856', pageSize=10, pageNum=1, sortBy="keys"):
        skips = pageSize * (pageNum - 1)
        if sortBy == "keys":
            return self.db[collection].aggregate([
                    {
                        "$project":{
                            "searchKeys":1,
                            "referenceKeys":1,
                            "tags":1,
                            "title": 1,
                            "content":1,
                            "source":1,
                            "date":1,
                            "rkLength":{"$size":"$referenceKeys"},
                            "skLength":{"$size":"$searchKeys"},
                    }},
                    { "$sort": {"skLength":-1,"rkLength":-1, "date": -1}},
                    { "$skip": skips},
                    { "$limit": pageSize }
            ])
        else:
            return self.db[collection].aggregate([
                    {
                        "$project":{
                            "searchKeys":1,
                            "referenceKeys":1,
                            "tags":1,
                            "title": 1,
                            "content":1,
                            "source":1,
                            "date":1,
                            "rkLength":{"$size":"$referenceKeys"},
                            "skLength":{"$size":"$searchKeys"}
                    }},
                    { "$sort": {"skLength":-1,"date": -1,"rkLength":-1}},
                    { "$skip": skips},
                    { "$limit": pageSize }
            ])
        # return self.db[collection].find().skip(skips).limit(pageSize)
    
    def get_documents_count(self,collection):
        return self.db[collection].find().count()

if __name__ == "__main__":
    db = DataAccess()

    # request = {
    #     "searchKeys": ["郭國勝"],
    #     "referenceKeys": ["臺中"]
    # }
    # documents = [
    #     {
    #         "searchKeys":["康業資本"],
    #         "referenceKeys":["RK1"],
    #         "tags":["tagA","tagB"],
    #         "title": "title A",
    #         "content":"content A"
    #     },
    #     {
    #          "searchKeys":["康業資本"],
    #         "referenceKeys":["RK2"],
    #         "tags":["tagA","tagC"],
    #         "title": "title B",
    #         "content":"content B"
    #     }
    # ]
    # # refKey = ['A']
    # refKey.append('B')

    # remove_request(db,id)
    # results=db.get_all_documents()
    print(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))
    # results = db.db.get
    # db.change_reference('5a4ca418f6fadc82283bba6a',['臺中','基隆'])
    # print(db.get_modified_requests().count())
    # print(db.db['Requests'].update_one({'_id': ObjectId("5a4ca418f6fadc82283bba6a")},{'$set': {'requestId':'1514966746.2558856'}}))
    # results = db.get_all_documents('1514966746.2558856',5,2),z


    # db.change_reference('5a4ca418f6fadc82283bba6a',['嚴永誠','基隆','魏樹達','台北','臺北'])
    # # print(db.get_documents_count('1514966746.2558856'))
    # for re in results:
    #     print(re['referenceKeys'])


    # for result in results :
    #     print(result['requestId'])
        # processing_requests(db,result['_id'])
        # insert_documents(db,str(result['requestId'])+result['searchKey'][0],documents)
    # result=add_request(db,request)
