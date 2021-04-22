#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 14:19:48 2021

@author: lavran_pagano
"""

#set wd import packages
os.chdir('/Users/lavran_pagano/Downloads/PythonB Project')
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn import preprocessing
from sklearn  import r2_score
import numpy as np
import matplotlib.pyplot as plt
# csvs
percent=pd.read_csv("/Users/lavran_pagano/Downloads/PythonB Project/UMBSStats_percentiles.csv")
Biomass = pd.read_csv("/Users/lavran_pagano/Downloads/PythonB Project/UMBSStats.csv")
# inspect
Biomass.head()
percent.head()
#recude to only inportnat columns for Biomass
col_list = ["Plot_ID","AGB","MAX","MIN"]
Biomass =Biomass[col_list]
#recude to only inportnat columns for percent
col_list = ["Plot_ID","PCT10","PCT20","PCT30","PCT40","PCT50","PCT60","PCT70","PCT80","PCT90"]
percent =percent[col_list]
#merge
Training_Data = pd.merge(Biomass,percent, on= "Plot_ID")
# inspect
Training_Data.head()
#Look for corelations
corelations = Training_Data.corr()
corelations.iloc[:1,1:len(corelations)]
# split data into independent and dependent variables
X,y = Training_Data.iloc[:,12:13],Training_Data.iloc[:,1]
#Train test split
setseed(50)
X_train, Xtest, ytrain, ytest =train_test_split(X,y, test_size =0.2)
#linear model
lm = linear_model.LinearRegression()# create a linear model
lm.fit(X_train, ytrain)#fit
lm.score(Xtest,ytest)
predictions = lm.predict(Xtest)
plt.scatter(predictions,ytest)
#Random forest
rf = RandomForestRegressor()
rf.fit(X_train, ytrain)#fit
rf.score(Xtest,ytest)
predictions = rf.predict(Xtest)
plt.scatter(predictions,ytest)




