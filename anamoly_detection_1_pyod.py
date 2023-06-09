# -*- coding: utf-8 -*-
"""Anamoly Detection_1 PyOD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JdUcvuuuJrK8PqUQHFtQNg_3Ev5CabgT
"""

!pip install pyod
!pip install --upgrade pyod  # to make sure that the latest version is installed!

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pyod.models.abod import ABOD
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.ocsvm import OCSVM
from pyod.utils.data import generate_data, get_outliers_inliers
from pyod.utils.data import evaluate_print

# %matplotlib inline
import matplotlib.font_manager
state=42

import pandas as pd

titanic = pd.read_excel("titanic3.xls")
titanic.shape

titanic['age'].fillna(titanic['age'].mode()[0], inplace=True)
titanic['cabin'].fillna(titanic['cabin'].mode()[0], inplace=True)
titanic['boat'].fillna(titanic['boat'].mode()[0], inplace=True)
titanic['body'].fillna(titanic['body'].mode()[0], inplace=True)
titanic['sex'].fillna(titanic['sex'].mode()[0], inplace=True)
titanic['survived'].fillna(titanic['survived'].mode()[0], inplace=True)
titanic['home.dest'].fillna(titanic['home.dest'].mode()[0], inplace=True)

titanic['age'].plot.hist(
  bins = 50,
  title = "Histogram of the age"
)







score = pd.read_csv("score.csv")
score

from sklearn.ensemble import IsolationForest
model=IsolationForest(n_estimators=1000,max_samples='auto',contamination=float(0.2),max_features=1.0)
model.fit(score[['Scores']])



score['Scores_scores']=model.decision_function(score[['Scores']])
score['Scores_anomaly']=model.predict(score[['Scores']])
score.head(20)



"""uNIVARIATE ANALYSIS FOR dIFFERENR COLUMNS"""



score2 = pd.read_csv("score2.csv")
score2.shape

score2.columns

columns = ['Match1Runs', 'Match2Runs', 'Match3Runs']

for column in columns:
  print("running for:" , column)
  model=IsolationForest(n_estimators=1000,max_samples='auto',contamination=float(0.2),max_features=1.0)
  model.fit(score2[[column]])
  score_column = column + "_scores"
  anamoly = column + "_anamoly"
  score2[score_column]=model.decision_function(score2[[column]])
  score2[anamoly]=model.predict(score2[[column]])
print("Completed")

score2.to_csv("score2_with_anamoly.csv")



"""**Student Marks Anlysis**"""

file_name = "student_marks.xlsx"
columns = ['Marks_20', 'Marks_50', 'Marks_100']
df_student = pd.read_excel(file_name)
df_student.columns



def get_univariate_iforest_anamoly(df , columns):
  for column in columns:
    print("running for:" , column)
    model=IsolationForest(n_estimators=1000,max_samples='auto',contamination=float(0.2),max_features=1.0)
    model.fit(df[[column]])
    score_column = column + "_scores"
    anamoly = column + "_anamoly"
    df[score_column]=model.decision_function(df[[column]])
    df[anamoly]=model.predict(df[[column]])
  return df

df_student_with_anamoly = get_univariate_iforest_anamoly(df_student ,columns )
df_student_with_anamoly.head()

df_student_with_anamoly.to_excel("df_student_with_anamoly.xlsx")



"""MutiVariable with IFORST"""

column2 = ['Marks_20', 'Marks_50', 'Marks_100']

def get_multivariate_iforest_anamoly(df, columns):
  model_IF = IsolationForest(contamination=float(0.1),random_state=42)
  model_IF.fit(df[column2])
  df['combine_scores']=model_IF.decision_function(df[columns])
  df['combine_anomaly']=model_IF.predict(df[columns])
  return df

df_student_with_anamoly = get_multivariate_iforest_anamoly(df_student_with_anamoly ,column2 )

model_IF = IsolationForest(contamination=float(0.1),random_state=42)

model_IF.fit(score2[column2])

score2['combine_scores']=model_IF.decision_function(score2[column2])
score2['combine_anomaly']=model_IF.predict(score2[column2])

score2.to_csv("score2_with_combine anamoly.csv")



contamination = 0.1 # percentage of outliers

X_train = df_student["Marks_20"].to_numpy().reshape(-1, 1)
X_train

# train IForest detector
from pyod.models.iforest import IForest
clf_name = 'IForest'
clf = IForest()
clf.fit(X_train)

# get the prediction labels and outlier scores of the training data
y_train_pred = clf.labels_ # binary labels (0: inliers, 1: outliers)

y_train_pred

df_student["Marks20_Anamoly"] = list(y_train_pred)
df_student[['RollNumber',	'Marks_20' ,'Marks_20_anamoly', 'Marks20_Anamoly']]





"""**PyOD Library**"""

file_name = "student_marks.xlsx"
columns = ['Marks_20', 'Marks_50', 'Marks_100']
df_student = pd.read_excel(file_name)
df_student.columns

def fit_model(model, data, column):
    
    df = data.copy()
    data_to_predict = data[column].to_numpy().reshape(-1, 1)
    predictions = model.fit_predict(data_to_predict)
    c_name = column + "_Predictions"
    df[c_name] = predictions
    
    
    
    return df

# Not for iForest
def get_anomaly_scores(model):
  anomaly_scores = model.decision_scores_
  threshold = model.threshold_
  return anomaly_scores, threshold

import numpy as np
import matplotlib.pyplot as plt
def plot_anomalies(df, x='date', y='amount' , prediction_columns='Marks_20_Predictions'):

    # categories will be having values from 0 to n
    # for each values in 0 to n it is mapped in colormap
    categories = df[prediction_columns].to_numpy()
    colormap = np.array(['g', 'r'])

    f = plt.figure(figsize=(12, 4))
    f = plt.scatter(df[x], df[y], c=colormap[categories])
    f = plt.xlabel(x)
    f = plt.ylabel(y)
    f = plt.xticks(rotation=90)
    plt.show()

iso_forest = IsolationForest(n_estimators=125)
column = "Marks_20"
iso_df = fit_model(iso_forest,df_student , column)
c_name = column + "_Predictions"
iso_df[c_name] = iso_df[c_name].map(lambda x: 1 if x==-1 else 0)
iso_df.head()



plot_anomalies(iso_df ,'RollNumber', "Marks_20" )

iso_df

"""**MAD Model**"""

"""Median Absolute Deviation"""
from pyod.models.mad import MAD

mad_model = MAD()
column = "Marks_20"
mad_df = fit_model(mad_model,df_student , column)
plot_anomalies(mad_df ,'RollNumber', "Marks_20" )

mad_df

anomaly_scores, threshold = get_anomaly_scores(mad_model)
print(f"Anomaly Scores: {anomaly_scores}, \nThreshold: {threshold}")

"""**KNN Model**"""

"""KNN Based Outlier Detection"""
from pyod.models.knn import KNN
knn_model = KNN()
column = "Marks_20"
knn_df = fit_model(knn_model,df_student , column)
plot_anomalies(knn_df ,'RollNumber', column )

knn_df

anomaly_scores, threshold = get_anomaly_scores(knn_model)
print(f"Anomaly Scores: {anomaly_scores}, \nThreshold: {threshold}")

"""**Local Outlier Factor Model(LOF)**"""

"""LOF Based Outlier Detection"""
from pyod.models.lof import LOF
lof_model = LOF()
column = "Marks_20"
lof_df = fit_model(lof_model,df_student , column)
plot_anomalies(lof_df ,'RollNumber', column )

lof_df

anomaly_scores, threshold = get_anomaly_scores(lof_model)
print(f"Anomaly Scores: {anomaly_scores}, \nThreshold: {threshold}")



# PyOD More

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pyod.models.abod import ABOD
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.ocsvm import OCSVM
from pyod.utils.data import generate_data, get_outliers_inliers
from pyod.utils.data import evaluate_print

# %matplotlib inline
import matplotlib.font_manager
state=42

# by default the outlier fraction is 0.1 in generate data function 
outlier_fraction = 0.1

model_list= [''Angle-based Outlier Detector (ABOD)']

models = {
     'Angle-based Outlier Detector (ABOD)'   : ABOD(contamination=outlier_fraction),

     'Isolation Forest': IForest(contamination=outlier_fraction,random_state=state),

     'Cluster-based Local Outlier Factor (CBLOF)':CBLOF(contamination=outlier_fraction,check_estimator=False, random_state=state),

     'Histogram-base Outlier Detection (HBOS)': HBOS(contamination=outlier_fraction),

     'K Nearest Neighbors (KNN)' :  KNN(contamination=outlier_fraction),
     
     "Support Vector Machine":OCSVM(kernel='rbf', degree=3, gamma=0.1,nu=0.05,max_iter=-1)
}

def fit_model_2(model, data, column):
    
    df = data.copy()
    data_to_predict = data[column].to_numpy().reshape(-1, 1).astype(float)
    model.fit(data_to_predict)
    # predict raw anomaly score
    scores_pred = model.decision_function(X_train)*-1

    # prediction of a datapoint category outlier or inlier
    y_pred = model.predict(data_to_predict)
    #predictions = model.fit_predict(data_to_predict)
    c_name_prediction = column + "_Predictions"
    c_name_score = column + "_Score"
    df[c_name_prediction] = y_pred
    df[c_name_score] = scores_pred
    # threshold value to consider a datapoint inlier or outlier
    threshold = stats.scoreatpercentile(scores_pred,100 *outlier_fraction)
    return df,threshold

#model = models["Angle-based Outlier Detector (ABOD)"]
model = models["Isolation Forest"]
column = "Marks_20"
df_ABOD,threshold = fit_model_2(model, df_student,column)
print(threshold)

df_ABOD

model = models["Isolation Forest"]
column = "Marks_20"
df_IF = fit_model_2(model, df_student,column)

df_IF

model = models["Cluster-based Local Outlier Factor (CBLOF)"]
column = "Marks_20"
df_CBLOF = fit_model_2(model, df_student,column)

df_CBLOF

model = models["Histogram-base Outlier Detection (HBOS)"]
column = "Marks_20"
df_HBOS = fit_model_2(model, df_student,column)

df_HBOS

model = models["K Nearest Neighbors (KNN)"]
column = "Marks_20"
df_HBOS = fit_model_2(model, df_student,column)

df_HBOS

model = models["Support Vector Machine"]
column = "Marks_20"
df_SVM = fit_model_2(model, df_student,column)

df_SVM



for i, (model_name,model) in enumerate(models.items()) :
    data_to_predict = data[column].to_numpy().reshape(-1, 1)
    # fit the dataset to the model
    model.fit(X_train)

    # predict raw anomaly score
    scores_pred = model.decision_function(X_train)*-1

    # prediction of a datapoint category outlier or inlier
    y_pred = model.predict(X_train)

