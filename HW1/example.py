# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# load train.csv
df = pd.read_csv('./train.csv')
objfeatures = df.select_dtypes(include="object").columns
le = preprocessing.LabelEncoder()

# Use Label Encoder
# TODO 
# Any Better Way to encode the data? How to deal with missing values
for feat in objfeatures:
    df[feat] = le.fit_transform(df[feat].astype(str))

df=df.values
X = df[:,1:17]
y = df[:,18]

# Normalization
X = preprocessing.StandardScaler().fit_transform(X.astype(int))

# Split data to training and validation part
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=4)

acc = []

# Applying KNNC. It will take some time
from sklearn import metrics
for i in range(1,40):

    print(f"Doing KNNC in round {i}")
    # TODO
    # Parameters may be adjusted following the document
    # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    # Since we use weighted categories accuracy, maybe other metrics works better
    neigh = KNeighborsClassifier(weights='distance', n_neighbors=i).fit(X_train,y_train)
    yhat = neigh.predict(X_val)
    
    acc.append(metrics.accuracy_score(y_val, yhat))
print (acc)
# Load test.csv
testdf = pd.read_csv('./test.csv')
objfeatures = testdf.select_dtypes(include="object").columns
le = preprocessing.LabelEncoder()
for feat in objfeatures:
    testdf[feat] = le.fit_transform(testdf[feat].astype(str))

testdf=testdf.values

testX = testdf[:,1:17]
testX = preprocessing.StandardScaler().fit_transform(testX.astype(int))

# Start Predict
knn = KNeighborsClassifier(weights='distance', n_neighbors=22).fit(X_train,y_train)
pred = knn.predict(testX)

# output the answer
fp = open("sol.csv", "w")
fp.write("index,label\n")
for index, i in enumerate(pred):
    fp.write(f"{index+20000},{int(i)}\n")
