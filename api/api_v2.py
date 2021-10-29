import numpy as np
import pandas as pd
import ujson
import os
from flask import Flask, jsonify, request
from flask import flash, redirect, url_for
from flask import send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from helper.helpers import gen_matrix, gen_label
#from skmultilearn.dataset import load_dataset
#from helper.dataset import load_dataset
from helper.dataset_local import load_dataset, available_datasets
from sklearn.svm import SVC
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_root():
  return "Hello World! v2", 200

@app.route('/hello')
def hello_world():
  print("hello")
  return jsonify(message="Hello World! v2")

@app.route('/hello/echo')
def hello_echo():
  msg = request.args.get("msg")
  print("Just received: ", msg)
  return msg, 200

@app.route('/builtin/list')
def builtin_list():
  available=sorted(available_datasets())
  return ujson.dumps(available), 200

@app.route('/builtin/load')
def builtin_load():
  dataset_name=request.args.get("dataset")
  drop_nolabel=True if int(request.args.get("nolabel",default="0")) else False
  entities=request.args.get("entities",default="all")

  # load dataset and transform to pandas dataframe
  X_train, y_train, feature_names, label_names = load_dataset(dataset_name, 'train')

  df=pd.DataFrame.sparse.from_spmatrix(X_train)
  df.columns=list(map(lambda x: x[0], feature_names))

  #drop instance with no label when "nolabel=1"
  if(drop_nolabel):
    label_exist=[]
    y_sum = np.sum(y_train.todense(),axis=1)
    for i in range(len(y_train.todense())):
      if np.sum(y_sum[i]) > 0:
        label_exist.append(True)
      else:
        label_exist.append(False)
    df = df[label_exist]
    df_y = y_train[label_exist]
  else:
    df_y = y_train

  # filter entities
  try:
    wanted_index=ujson.loads(entities)
  except:
    wanted_index=None

  if(wanted_index):
    wanted_mask = [False] * len(df)
    for item in wanted_index:
      wanted_mask[int(item)] = True
    df, df_y = df[wanted_mask], df_y[wanted_mask]

  #attch label data to df
  df_labels=pd.DataFrame.sparse.from_spmatrix(df_y).apply(lambda x: x.to_numpy(),axis=1)
  df["labels"]=df_labels

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
  result_decoded["labels_count"] = ujson.loads(pd.Series(np.sum(df_labels,axis=0)).to_json(orient="records"))
  result_decoded["labels_name"] = list(map(lambda x: x[0], label_names))
  result_decoded["features_name"] = [{"feature": x[0], "type": x[1]} for x in feature_names]
  result_decoded["length"] = len(df)

  return ujson.dumps(result_decoded), 200

@app.route('/builtin/tsne')
def builtin_tsne():
  dataset_name=request.args.get("dataset")
  drop_nolabel=True if int(request.args.get("nolabel",default="0")) else False
  entities=request.args.get("entities",default="all")
  tsne_type = request.args.get("type",default="label")

  # load dataset
  X_train, y_train, feature_names, label_names = load_dataset(dataset_name, 'train')
  df=pd.DataFrame.sparse.from_spmatrix(X_train)
  df.columns=list(map(lambda x: x[0], feature_names))

  #drop instance with no label when "nolabel=1"
  if(drop_nolabel):
    label_exist=[]
    y_sum = np.sum(y_train.todense(),axis=1)
    for i in range(len(y_train.todense())):
      if np.sum(y_sum[i]) > 0:
        label_exist.append(True)
      else:
        label_exist.append(False)
    df = df[label_exist]
    df_y = y_train[label_exist]
  else:
    df_y = y_train

  # filter entities
  try:
    wanted_index=ujson.loads(entities)
  except:
    wanted_index=None

  if(wanted_index):
    wanted_mask = [False] * len(df)
    for item in wanted_index:
      wanted_mask[int(item)] = True
    df, df_y = df[wanted_mask], df_y[wanted_mask]

  if tsne_type == "label":
    data_set = pd.DataFrame(df_y.todense(),columns=[label_names[x][0] for x in range(y_train.shape[1])])
  elif tsne_type == "feature":
    data_set = pd.DataFrame(X_train.todense(),columns=[feature_names[x][0] for x in range(X_train.shape[1])])

  # tsne
  t_sne = TSNE()
  t_sne.fit(data_set)
  t_sne_df = pd.DataFrame(t_sne.embedding_, index=data_set.index)

  # generate output
  result_decoded = {}
  result_decoded["tsne"] = ujson.loads(t_sne_df.to_json(orient="values"))
  result_decoded["length"] = len(df)
  result_decoded["tsne_type"] = tsne_type

  return ujson.dumps(result_decoded), 200

@app.route('/builtin/cluster')
def builtin_cluster():
  dataset_name=request.args.get("dataset")
  cluster_num=int(request.args.get("num",default="4"))
  drop_nolabel=True if int(request.args.get("nolabel",default="0")) else False

  X_train, y_train, _, label_names = load_dataset(dataset_name, 'train')
  data_set = pd.DataFrame(y_train.todense(),columns=[label_names[x][0] for x in range(y_train.shape[1])])

  #drop instance with no label when "nolabel=1"
  if(drop_nolabel):
    label_exist=[]
    y_sum = np.sum(y_train.todense(),axis=1)
    for i in range(len(y_train.todense())):
      if np.sum(y_sum[i]) > 0:
        label_exist.append(True)
      else:
        label_exist.append(False)
    data_set = data_set[label_exist]

  estimator = KMeans(n_clusters=cluster_num)
  estimator.fit(data_set)

  cluster_result = [[] for _ in range(cluster_num)]

  for idx in range(len(estimator.labels_)):
    current_bucket = int(estimator.labels_[idx])
    cluster_result[current_bucket].append(idx)

  return ujson.dumps({"cluster_result": cluster_result, "cluster_num": cluster_num, "method": "kmeans"}), 200

@app.route('/builtin/search')
def builtin_search():
  dataset_name=request.args.get("dataset")
  field_name=request.args.get("field")
  entities=request.args.get("entities",default="all")
  drop_nolabel=True if int(request.args.get("nolabel",default="0")) else False

  # load dataset and transform to pandas dataframe
  X_train, y_train, feature_names, label_names = load_dataset(dataset_name, 'train')

  df=pd.DataFrame.sparse.from_spmatrix(X_train)
  df.columns=list(map(lambda x: x[0], feature_names))

  #drop instance with no label when "nolabel=1"
  if(drop_nolabel):
    label_exist=[]
    y_sum = np.sum(y_train.todense(),axis=1)
    for i in range(len(y_train.todense())):
      if np.sum(y_sum[i]) > 0:
        label_exist.append(True)
      else:
        label_exist.append(False)
    df = df[label_exist]
    df_y = y_train[label_exist]
  else:
    df_y = y_train

  # filter entities
  try:
    wanted_index=ujson.loads(entities)
  except:
    wanted_index=None

  if(wanted_index):
    wanted_mask = [False] * len(df)
    for item in wanted_index:
      wanted_mask[int(item)] = True
    df, df_y = df[wanted_mask], df_y[wanted_mask]

  return df[field_name].value_counts().to_json(orient="columns"), 200


if __name__ == "__main__":
  app.run(debug=True,host="127.0.0.1",port=5001)