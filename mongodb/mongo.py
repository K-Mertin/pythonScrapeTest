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
    print(requestId)
    documents = g.dataAccess.get_all_documents(requestId,10,1)

    results = []

    for doc in documents:
        results.append({
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


if __name__ == '__main__':
    app.run(debug=True)
