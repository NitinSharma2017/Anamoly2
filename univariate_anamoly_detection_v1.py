# -*- coding: utf-8 -*-
"""UniVariate Anamoly Detection V1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J55tGsLem03tOkF4LjvqbCxjvFjAbnBb
"""

!pip install pyod
!pip install --upgrade pyod  # to make sure that the latest version is installed!

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.font_manager
import matplotlib.pyplot as plt
state=42

from scipy import stats
import matplotlib.pyplot as plt
from pyod.models.iforest import IForest
from pyod.models.abod import ABOD
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.ocsvm import OCSVM



class UnivariateAnamolyDetection():
  def __init__(self ):
    #self.input_file = input_file
    # by default the outlier fraction is 0.1 in generate data function
    self.outlier_fraction = 0.2
    self.models = {
     'ABOD'   : ABOD(contamination=self.outlier_fraction),
     'IF': IForest(contamination=self.outlier_fraction,random_state=state),
     'CBLOF':CBLOF(contamination=self.outlier_fraction,check_estimator=False, random_state=state),
     'HBOS': HBOS(contamination=self.outlier_fraction),
     'KNN' :  KNN(contamination=self.outlier_fraction),     
     "OCSVM":OCSVM(kernel='rbf', degree=3, gamma=0.1,nu=0.05,max_iter=-1)
     
}

  def fit_model_2(self, model, data, column , model_name):
      
      df = data.copy()
      data_to_predict = data[column].to_numpy().reshape(-1, 1).astype(float)
      model.fit(data_to_predict)
      # predict raw anomaly score
      scores_pred = model.decision_function(data_to_predict)*-1

      # prediction of a datapoint category outlier or inlier
      y_pred = model.predict(data_to_predict)
      #predictions = model.fit_predict(data_to_predict)
      c_name_prediction = column + "_" + model_name + "_Predictions"
      c_name_score = column + "_" + model_name + "_Score"
      df[c_name_prediction] = y_pred
      df[c_name_score] = scores_pred
      # threshold value to consider a datapoint inlier or outlier
      threshold = stats.scoreatpercentile(scores_pred,100 * self.outlier_fraction)
      return df,threshold

  def get_anamoly(self , data, column , evaluation_model = "IF" ):
    model = self.models[evaluation_model]
    df,threshold = self.fit_model_2(model, data,column , evaluation_model)
    return df,threshold

file_name = "student_marks.xlsx"
columns = ['Marks_20', 'Marks_50', 'Marks_100']
df_student = pd.read_excel(file_name)
df_student.columns

uad = UnivariateAnamolyDetection()
df_student_anamoly = df_student.copy(deep = True)
for column in columns:
  print("Running for " , column)
  df_student_anamoly,threshhold = uad.get_anamoly(df_student_anamoly,column , "ABOD")
  #break
display(df_student_anamoly)

df_student_anamoly,threshhold = uad.get_anamoly(df_student_anamoly,columns[1] , "IF")
df_student_anamoly

display(df_student_anamoly)

outlier_fraction = 0.1
models = {
     'Angle-based Outlier Detector (ABOD)'   : ABOD(contamination=outlier_fraction),

     'Isolation Forest': IForest(contamination=outlier_fraction,random_state=state),

     'Cluster-based Local Outlier Factor (CBLOF)':CBLOF(contamination=outlier_fraction,check_estimator=False, random_state=state),

     'Histogram-base Outlier Detection (HBOS)': HBOS(contamination=outlier_fraction),

     'K Nearest Neighbors (KNN)' :  KNN(contamination=outlier_fraction),
     
     "Support Vector Machine":OCSVM(kernel='rbf', degree=3, gamma=0.1,nu=0.05,max_iter=-1)
}


models.keys()