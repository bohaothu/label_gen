from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from faker import Faker
import ujson
from flask_cors import CORS

f=Faker(locale="en_CA")

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello_world():
  return jsonify(message="Hello World!")

@app.route('/random')
def random_data():
  row = int(request.args.get("row"))
  features_no = int(request.args.get("features"))
  labels_no = int(request.args.get("labels"))
  fake_features=np.random.rand(row,features_no)
  fake_labels=[np.random.randint(0,2,labels_no) for x in range(row)]
  df=pd.DataFrame(data=fake_features,columns=[str("feature")+str(i+1) for i in range(features_no)])
  df["labels"]=fake_labels
  df1=pd.DataFrame(data=pd.concat([df.select_dtypes(['number']).min(), df.select_dtypes(['number']).max(),
  df.median(),df.mean(),df.std(),df.var()],axis=1))
  df1.columns=["min", "max", "median","mean","std","var"]
  df1.to_json(orient="index")
  df_decoded = ujson.loads(df.to_json(orient="table"))
  df_decoded["stat"] = ujson.loads(df1.to_json(orient="index"))
  return ujson.dumps(df_decoded), 200

@app.route('/random/label')
def random_label():
  labels_no = int(request.args.get("labels"))
  return ujson.dumps([f.word() for x in range(labels_no)]), 200

if __name__ == "__main__":
  app.run()