# mongo.py
from flask import Flask, jsonify, request, g
from DataAccess import DataAccess
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.before_request
def before_request():
    g.dataAccess = DataAccess()

@app.route('/requests', methods=['GET'])
def get_all_requests():
    requests = g.dataAccess.get_created_requests()
    
    results = []

    for request in requests:
        print(request["searchKeys"])
        results.append({
            "_id":str(request["_id"]),
            "requestId":request["requestId"],
            "status":request["status"],
            "searchKeys":list(map(lambda x : x['key'], request['searchKeys']))  ,
            "referenceKeys":request["referenceKeys"],
            "createDate":request["createDate"]
        })
    # print((requests))
    return jsonify(results)

@app.route('/documents/<requestId>', methods=['GET'])
def get_all_documents(requestId):
    pageSize = request.args.get('pageSize', default = 10, type = int)
    pageNumber = request.args.get('pageNumber', default = 1, type = int)
    sortBy = request.args.get('sortBy', default = 'keys', type= str)
    totalCount = g.dataAccess.get_documents_count(requestId)

    print(requestId)
    documents = g.dataAccess.get_all_documents(requestId,pageSize,pageNumber,sortBy)

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
    data=json.loads(request.data)

    g.dataAccess.add_request({
        "searchKeys": data['searchKeys'],
        "referenceKeys": data['referenceKeys']
    })
    return jsonify("recevied")

@app.route('/requests', methods=['PUT'])
def change_request():
    data=json.loads(request.data)

    print(data)
    g.dataAccess.change_reference(data['_id'],data['referenceKeys'])
    
    return jsonify("updated")

if __name__ == '__main__':
    app.run(debug=True)
