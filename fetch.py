from flask import Flask
import numpy as np
import pandas as pd
from faker import Faker
import json

f=Faker(locale="en_CA")

app = Flask(__name__)

@app.route('/hello')
def hello_world():
  return "Hello World!"

@app.route('/random')
def random_data():
  fake_features=np.random.rand(100,20)
  fake_labels=[np.random.randint(0,2,30) for x in range(100)]
  df=pd.DataFrame(data=fake_features,columns=[str("feature")+str(i+1) for i in range(20)])
  df["labels"]=fake_labels
  return df.to_json(orient="split")

@app.route('/random/label')
def random_label():
  return json.dumps([f.word() for x in range(30)])

if __name__ == "__main__":
  app.run()