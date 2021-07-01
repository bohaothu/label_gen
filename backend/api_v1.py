from flask import Flask, jsonify, request
from flask import flash, redirect, url_for
from flask import send_from_directory
import numpy as np
import pandas as pd
from faker import Faker
import ujson
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from helpers import gen_matrix, gen_label
from skmultilearn.dataset import load_dataset
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.svm import SVC
from sklearn.manifold import TSNE

f=Faker(locale="zh_CN")

UPLOAD_FOLDER = os.path.join(".","uploads")
ALLOWED_EXTENSIONS = {'txt', 'json', 'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/hello')
def hello_world():
  print("hello")
  return jsonify(message="Hello World!")

@app.route('/hello/echo')
def hello_echo():
  msg = request.args.get("msg")
  print("Just received: ", msg)
  return msg, 200

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
  df_decoded["labels_count"] = ujson.loads(pd.Series(np.sum(df["labels"],axis=0)).to_json(orient="records"))
  return ujson.dumps(df_decoded), 200

@app.route('/random/label')
def random_label():
  labels_no = int(request.args.get("labels"))
  z=set()
  while (len(z) < labels_no):
    z.add(f.word())
  return ujson.dumps(list(z)), 200

@app.route('/random/suggest')
def random_suggest():
  row = int(request.args.get("row"))
  features_no = int(request.args.get("features"))
  labels_no = int(request.args.get("labels"))

  gen_mat = gen_matrix(features_no,labels_no)
  fake_features=np.random.rand(row,features_no)
  fake_suggestion=[gen_label(item, gen_mat).tolist() for item in fake_features]

  return ujson.dumps(fake_suggestion)

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    if f and allowed_file(f.filename):
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return jsonify(message="success",url=url_for('uploaded_file', filename=filename))
    elif not allowed_file(f.filename):
      return jsonify(message="unsupported format")
    else:
      return jsonify(message="unknown error")

@app.route('/upload_csv', methods=['POST', 'GET'])
def upload_csv():
  if request.method == 'POST':
    # save file
    f = request.files['file']
    filename = secure_filename(f.filename)
    file_fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(file_fullpath)

    # read file
    df = pd.read_csv(file_fullpath,index_col="#")
    df["labels"]=df["labels"].apply(lambda x: np.array(ujson.loads(x)))

    # create stat
    df1=pd.DataFrame(data=pd.concat([df.select_dtypes(['number']).min(), df.select_dtypes(['number']).max(),
    df.median(),df.mean(),df.std(),df.var()],axis=1))
    df1.columns=["min", "max", "median","mean","std","var"]
    df1.to_json(orient="index")

    # append df
    df_decoded = ujson.loads(df.to_json(orient="table"))

    # append stat
    df_decoded["stat"] = ujson.loads(df1.to_json(orient="index"))
    df_decoded["labels_count"] = ujson.loads(pd.Series(np.sum(df["labels"],axis=0)).to_json(orient="records"))

    return jsonify(csvResult=ujson.dumps(df_decoded), message="success"), 200


@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/builtin/list')
def builtin_list():
  available=sorted(["emotions","birds"])
  return ujson.dumps(available), 200

@app.route('/builtin/load')
def builtin_load():
  dataset_name=request.args.get("dataset")
  # load dataset and transform to pandas dataframe
  X_train, y_train, feature_names, label_names = load_dataset(dataset_name, 'train')
  df=pd.DataFrame.sparse.from_spmatrix(X_train)
  df.columns=list(map(lambda x: x[0], feature_names))
  df["labels"]=pd.DataFrame.sparse.from_spmatrix(y_train).apply(lambda x: x.to_numpy(),axis=1)

  # create statistic data
  df_to_dense=df.select_dtypes(['number','Sparse[int]','Sparse[float]']).sparse.to_dense()
  df1=pd.DataFrame(data=pd.concat([
  df_to_dense.min(), df_to_dense.max(),
  df_to_dense.median(), df.mean(),
  df_to_dense.std(), df_to_dense.var()],axis=1))
  df1.columns=["min", "max", "median","mean","std","var"]
  df1.to_json(orient="index")

  # generate output
  result_decoded = ujson.loads(df.to_json(orient="table"))
  result_decoded["stat"] = ujson.loads(df1.to_json(orient="index"))
  result_decoded["labels_count"] = ujson.loads(pd.Series(np.sum(df["labels"],axis=0)).to_json(orient="records"))
  result_decoded["labels_name"] = list(map(lambda x: x[0], label_names))
  result_decoded["features_name"] = [{"feature": x[0], "type": x[1]} for x in feature_names]

  #tsne axis
  data_set = pd.DataFrame(y_train.todense(),columns=[label_names[x][0] for x in range(y_train.shape[1])])
  t_sne = TSNE()
  t_sne.fit(data_set)
  t_sne_df = pd.DataFrame(t_sne.embedding_, index=data_set.index)

  result_decoded["tsne"] = ujson.loads(t_sne_df.to_json(orient="values"))

  return ujson.dumps(result_decoded), 200

@app.route('/builtin/predict')
def builtin_predict():
  dataset_name=request.args.get("dataset")

  # load training and testing set
  X_train, y_train, feature_names, label_names = load_dataset(dataset_name, 'train')
  X_test, y_test, _, _ = load_dataset(dataset_name, 'test')

  # create classifier
  clf = BinaryRelevance(classifier=SVC(probability=True), require_dense=None)
  clf.fit(X_train, y_train)

  predict_proba = clf.predict_proba(X_test)

  return ujson.dumps(predict_proba.todense().tolist())


if __name__ == "__main__":
  app.run()