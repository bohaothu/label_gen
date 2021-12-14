from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import ujson
import numpy as np
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
mongo = PyMongo(app, uri="mongodb://localhost:27018")

@app.route("/hello/<string:dfname>/<string:dftype>")
def hello(dfname, dftype):
    db = mongo.cx[f"{dfname}_{dftype}"] # Database
    collection = db.list_collection_names()
    resp = ujson.dumps({"dataset": dfname, "dataset_type": dftype,
    "result": collection})
    return resp

@app.route("/hello/<string:dfname>/<string:dftype>/<string:colname>")
def hello_colname(dfname, dftype, colname):
    db = mongo.cx[f"{dfname}_{dftype}"]
    resp = db[colname].find_one() # Collection
    return resp

@app.route("/tsne/<string:tsnetype>/<string:dfname>/<string:dftype>", methods=["GET","POST"])
def tsne(dfname, dftype, tsnetype):
    drop_nolabel = True if int(request.args.get("nolabel",default="0")) else False
    filter_id = request.args.get("filter_id")

    db = mongo.cx[f"{dfname}_{dftype}"]
    col_group = db["graph_filters"]

    # if nolabel=1, drop data with 0 label
    nolabel_arr = []
    if drop_nolabel:
        label_col = mongo.cx[f"{dfname}_{dftype}"]["labels"]
        label_docs = label_col.find({})
        
        for label_doc in label_docs:         
            doc_dict = label_doc
            doc_id = label_doc["_id"]
            del doc_dict["_id"]
            if(sum(doc_dict.values()) == 0):
                nolabel_arr.append(doc_id)
                
    # if filter_id exist, add that filter into query            
    filter_result = col_group.find_one({"_id": ObjectId(filter_id) })

    if filter_result:
        docs=db[f"tsne_{tsnetype}"].find({"_id": {"$in": filter_result["points"], "$nin": nolabel_arr}})
    else:
        nogroup = set()
        docs_group = col_group.find({})
        for doc_group in docs_group:
            filter_points = ujson.loads(json_util.dumps(doc_group))["points"]
            nogroup = nogroup.union(set(filter_points))
        docs=db[f"tsne_{tsnetype}"].find({"_id": {"$nin": list(set(nolabel_arr).union(nogroup))}})

    res = []
    for doc in docs:
        res.append([doc["v1"],doc["v2"],doc["_id"]])
    resp = ujson.dumps({"dataset": dfname, "dataset_type": dftype,
    "tsne_type": tsnetype, "result": res, "filter_id": filter_id})

    return resp

@app.route("/example/<string:dfname>/<string:dftype>/<string:exid>", methods=["GET","POST"])
def example_details(dfname, dftype, exid):
    db = mongo.cx[f"{dfname}_{dftype}"]
    label_arr = dict(db["labels"].find_one({"_id": {"$eq": exid}}))
    del label_arr["_id"]
    return {"id": exid, "label": label_arr, "label_sum": sum(label_arr.values())}

@app.route("/group/load/<string:dfname>/<string:dftype>")
def load_group(dfname, dftype):
    db = mongo.cx[f"{dfname}_{dftype}"]
    docs = db["graph_filters"].find({})
    graph_filters = []
    for doc in docs:
        graph_filters.append(ujson.loads(json_util.dumps(doc)))
    return {"dataset_name": dfname, "dataset_type": dftype, "groups": graph_filters}

@app.route("/group/add",methods=["POST"])
def add_group():
    request_body = ujson.loads(request.data)
    dfname = request_body["dataset_name"]
    dftype = request_body["dataset_type"]
    group_name = request_body["group_name"]
    group_type = request_body["group_type"]

    if group_type == "selected":
        points = request_body["points"]
        db = mongo.cx[f"{dfname}_{dftype}"]
        db["graph_filters"].insert_one({"dataset_name": dfname, "dataset_type": dftype,
    "group_name": group_name, "group_type": group_type, "points": points})

    return {"status": "success"}

@app.route("/group/remove",methods=["POST"])
def remove_group():
    request_body = ujson.loads(request.data)
    dfname = request_body["dataset_name"]
    dftype = request_body["dataset_type"]
    group_id = request_body["group_id"]

    db = mongo.cx[f"{dfname}_{dftype}"]
    col = db["graph_filters"]
    col.delete_one({"_id": ObjectId(group_id)})

    return {"status": "success"}

@app.route("/available/list")
def available_list():
    db = mongo.cx["config"]
    docs = db["avaliable_dataset"].find({})
    res = []
    for doc in docs:
        feature_counts = sum(doc["features_count"].values())
        res.append({"dataset_name": doc["dataset_name"],
        "features_count": feature_counts,
        "labels_count": doc["labels_count"]})
    resp = ujson.dumps(res)
    return resp

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)