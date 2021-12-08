import numpy as np
import pandas as pd
import os
import pickle
import uuid
from sklearn.manifold import TSNE
import nltk
from nltk.corpus import stopwords

dataset_directory=os.path.join(".","dataset","v2")
output_directory=os.path.join(".","dataset","v3")

avail = [{"name": "birds", "domain": "audio"},
{"name": "bibtex", "domain": "text"}]

def shortid(num):
    return [str(uuid.uuid4())[:8] for i in range(num)]

def label_encode(string):
    return string.replace("\\'",".").replace(" ","_")

def build_dataset(df_name,df_type, df_domain):
    print("start", df_name,df_type)

    with open(os.path.join(dataset_directory, df_name, df_type+'.pickle'), 'rb') as f:
        df_x, df_y, feature_names, label_names = pickle.load(f)

    index=shortid(df_x.shape[0])

    df_x = pd.DataFrame(df_x.todense(),columns=[feature_names[x][0] for x in range(df_x.shape[1])],index=index)

    if df_name == "bibtex":
        with open(os.path.join(dataset_directory, df_name, 'train.pickle'), 'rb') as f:
            X_train, _, _, _ = pickle.load(f)
        X_train=pd.DataFrame(X_train.todense(),columns=[feature_names[x][0] for x in range(X_train.shape[1])])
        sw = stopwords.words('english')
        tobedrop = set(X_train.columns) & set(sw)
        tobedrop = tobedrop | set(X_train.sum()[X_train.sum() < 100].index) | set(X_train.sum()[X_train.sum() > 300].index)
        tobedrop = tobedrop | (set(X_train.columns) & set([chr(x) for x in range(97,97+26)])) | set([item for item in X_train.columns if len(item) <= 2])
        df_x.drop(columns=tobedrop, inplace=True)
    
    df_x["id"]=index
    
    df_y=pd.DataFrame(df_y.todense(),columns=[label_encode(label_names[x][0]) for x in range(df_y.shape[1])],index=index)
    df_y["id"]=index

    if df_name == "bibtex":
        df_x = df_x.sample(frac=0.2)
        df_x.to_pickle(os.path.join(output_directory,df_name,df_type,"feature.pkl"))
        df_y = df_y.drop(index=(set(df_y.index)-set(df_x.index)))
        df_y.to_pickle(os.path.join(output_directory,df_name,df_type,"label.pkl"))
    
    print(df_x.shape,df_y.shape)

    t_sne = TSNE()
    t_sne.fit(df_x.drop("id",axis=1))
    t_sne_df = pd.DataFrame(t_sne.embedding_, columns=["x","y"], index=df_x.index)
    t_sne_df["id"]=df_x.index
    t_sne_df.to_pickle(os.path.join(output_directory,df_name, df_type,"tsne_feature.pkl"))
    
    t_sne = TSNE()
    t_sne.fit(df_y.drop("id",axis=1))
    t_sne_df = pd.DataFrame(t_sne.embedding_, columns=["x","y"], index=df_y.index)
    t_sne_df["id"]=df_y.index
    t_sne_df.to_pickle(os.path.join(output_directory,df_name,df_type,"tsne_label.pkl"))

    if df_type == "train":
        res = {"name": df_name, "domain": df_domain, "instances": df_x.shape[0],
        "labels": df_y.shape[1] - 1,"features": df_x.shape[1] - 1}
    elif df_type == "test":
        res = {"name": df_name+"_test", "domain": df_domain, "instances": df_x.shape[0],
        "labels": df_y.shape[1] - 1,"features": df_x.shape[1] - 1}

    if df_type == "train":
        attribute=pd.DataFrame(feature_names,columns=["attribute","type"])
        attribute["type"]=attribute["type"].apply(lambda x: "numeric" if x == "NUMERIC" else "nominal")
        attribute.to_pickle(os.path.join(output_directory,df_name,"attribute.pkl"))

        pd.Series(map(lambda x: x[0],label_names)).apply(lambda x: label_encode(x)).to_pickle(os.path.join(output_directory,df_name,"labels.pkl"))

    print("finish", df_name,df_type)

    return res

if __name__ == "__main__":
    z = []
    for df in avail:
        z.append(build_dataset(df["name"],"train",df["domain"]))
        z.append(build_dataset(df["name"],"test",df["domain"]))

    print(z)
    pd.DataFrame(z).to_pickle(os.path.join(output_directory,"available.pkl"))