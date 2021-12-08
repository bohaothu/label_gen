from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import ujson
import numpy as np

app = Flask(__name__)
CORS(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017")

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
    if request.method == "GET":
        db = mongo.cx[f"{dfname}_{dftype}"]
        docs = db[f"tsne_{tsnetype}"].find({})
        res = []
        for doc in docs:
            res.append([doc["v1"],doc["v2"],doc["_id"]])
        resp = ujson.dumps({"dataset": dfname, "dataset_type": dftype,
        "tsne_type": tsnetype, "result": res})
        return resp

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