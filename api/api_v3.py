import numpy as np
import pandas as pd
import ujson
import os
from flask import Flask, jsonify, request
from flask import flash, redirect, url_for
from flask import send_from_directory
from flask_cors import CORS
from helper.dataset_v3 import load_dataset, available_datasets

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_root():
  return "Hello World! v3", 200

@app.route('/echo',  methods = ['GET', 'POST'])
def echo():
  if request.method == 'GET':
    return ujson.dumps(request.args.to_dict()), 200
  if request.method == 'POST':
    print(request.args)
    print(request.form)
    return "this is post", 200

@app.route('/v3/builtin/available')
def builtin_available():
  return available_datasets(), 200

@app.route('/v3/builtin/load')
def builtin_load_feature():
  dataset_name=request.args.get("dataset")
  file_name=request.args.get("filename")
  result = load_dataset(dataset_name=dataset_name,variant="train",file_name=file_name)
  return result.to_json(orient="index"), 200

if __name__ == "__main__":
  app.run(debug=True,host="127.0.0.1",port=5003)