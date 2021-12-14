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
    drop_nolabel = True if int(request.args.get("nolabel",default="0")) else False
    db = mongo.cx[f"{dfname}_{dftype}"]

    if request.method == "POST":
        request_body = ujson.loads(request.data)
        points_to_keep = request_body["points_to_keep"]
        points_to_drop = request_body["points_to_drop"]
        try:
            filter_id = request_body["filter_id"]
        except:
            filter_id = "undefined"

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

        if len(points_to_keep):
            docs=db[f"tsne_{tsnetype}"].find({"_id": {"$in": points_to_keep,"$nin": nolabel_arr}})
        elif len(points_to_drop):
            mask=list( set(points_to_drop).union( set(nolabel_arr) ) )
            docs=db[f"tsne_{tsnetype}"].find({"_id": {"$nin": mask}})
        else:
            docs=db[f"tsne_{tsnetype}"].find({"_id": {"$nin": nolabel_arr}})

        res = []
        for doc in docs:
            res.append([doc["v1"],doc["v2"],doc["_id"]])
        resp = ujson.dumps({"dataset": dfname, "dataset_type": dftype,
        "tsne_type": tsnetype, "result": res, "filter_id": filter_id})

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

@app.route("/group/save")
def save_group():
    db

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)