# mongo.py
from flask import Flask, jsonify, request, g
from DataAccess import DataAccess
from flask_cors import CORS
import json
import configparser
import logging
import os

app = Flask(__name__)
CORS(app)

@app.before_request
def before_request():
    g.dataAccess = DataAccess()

@app.route('/requests', methods=['GET'])
def get_all_requests():
    app.logger.info('get_all_requests')
    pageSize = request.args.get('pageSize', default =10, type = int)
    pageNumber = request.args.get('pageNumber', default = 1, type = int)
    
    result = g.dataAccess.get_created_requests(pageSize,pageNumber)
    requests =  result['data']
    totalCount = result["totalCount"]
    totalPages = int( totalCount/ pageSize) + 1

    results = {
        "pagination" : {
            "pageSize":pageSize,
            "pageNumber":pageNumber,
            "totalCount":totalCount,
            "totalPages":totalPages
        },
        "data" : []
    }
    
    # sortBy = request.args.get('sortBy', default = 'keys', type= str)
    # totalCount = g.dataAccess.get_documents_count(requestId)

    for r in requests:
        # print(request["searchKeys"])
        results["data"].append({
            "_id":str(r["_id"]),
            "requestId":r["requestId"],
            "status":r["status"],
            "searchKeys":list(map(lambda x : x['key'], r['searchKeys']))  ,
            "referenceKeys":r["referenceKeys"],
            "createDate":r["createDate"]
        })
    # print((requests))
    return jsonify(results)

@app.route('/documents/<requestId>', methods=['GET'])
def get_all_documents(requestId):
    app.logger.info('get_all_documents'+ requestId)
    pageSize = request.args.get('pageSize', default = 10, type = int)
    pageNumber = request.args.get('pageNumber', default = 1, type = int)
    sortBy = request.args.get('sortBy', default = 'keys', type= str)
    filters = request.args.getlist('filters')
    totalCount = g.dataAccess.get_documents_count(requestId, filters)

    documents = g.dataAccess.get_all_documents(requestId,pageSize,pageNumber,sortBy,filters)

    totalPages = int(totalCount / pageSize) + 1

    results = {
        "pagination" : {
            "pageSize":pageSize,
            "pageNumber":pageNumber,
            "totalCount":totalCount,
            "totalPages":totalPages
        },
        "data" : []
    }
    print(results)

    for doc in documents:
        results["data"].append({
            "title": doc["title"],
            "searchKeys":doc["searchKeys"],
            "referenceKeys":doc["referenceKeys"],
            "tags":doc["tags"],
            "source":doc["source"]
        })

    return jsonify(results)

@app.route('/requests', methods=['POST'])
def add_request():
    app.logger.info('add_request')
    data=json.loads(request.data)

    g.dataAccess.add_request({
        "searchKeys": data['searchKeys'],
        "referenceKeys": data['referenceKeys']
    })
    return jsonify("recevied")

@app.route('/requests', methods=['PUT'])
def change_request():
    app.logger.info('change_request')
    data=json.loads(request.data)
    print(data['referenceKeys'])
    # print()
    g.dataAccess.change_reference(data['_id'],data['referenceKeys'])
    
    return jsonify("updated")

@app.route('/requests/delete', methods=['PUT'])
def remove_request():
    app.logger.info('remove_request')
    data=json.loads(request.data)

    # print(data)
    g.dataAccess.remove_request(data['_id'])
    
    return jsonify("deleted")

def Setting():
    config = configparser.ConfigParser()
    with open('Config.ini') as file:
        config.readfp(file)

    logPath = config.get('Options','Log_Path')
    

    formatter = logging.Formatter('[%(name)-12s %(levelname)-8s] %(asctime)s - %(message)s')
    # app.logger=logging.getLogger(__class__.__name__)
    app.logger.setLevel(logging.DEBUG)
    
    if not os.path.isdir(logPath):
        os.mkdir(logPath)

    fileHandler = logging.FileHandler(logPath+'FlaskService.log')
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)

    app.logger.info('Finish Setting')
        
if __name__ == '__main__':
    Setting()
    app.run(debug=True)
