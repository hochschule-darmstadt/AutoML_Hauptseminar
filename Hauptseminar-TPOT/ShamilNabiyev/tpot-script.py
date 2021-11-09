from sklearn.model_selection import train_test_split
from tpot import TPOTClassifier, TPOTRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from ipywidgets import IntProgress
import pandas as pd
import numpy as np


# Classification
df = pd.read_csv('data/phishing_train.csv', quotechar='\'', skipinitialspace=True)
df.head()

df_test = pd.read_csv('data/phishing_test.csv', quotechar='\'', skipinitialspace=True)
df_test.head()

# Classification
TARGET = 'Result'
feature_names = df.columns.difference([TARGET])

X_train = df[feature_names]
y_train = df[[TARGET]].values.ravel()

X_test = df_test[feature_names]
y_test = df_test[[TARGET]].values.ravel()


# Classification
ITERATIONS = 3
TIME_LIMIT=10
f1_scores = []

print('Starting classification experiment')

for i in range(0, ITERATIONS):
    print('%s. iteration ...' % (i+1))
    tpot = TPOTClassifier(scoring='f1', max_time_mins=TIME_LIMIT)
    tpot.fit(X_train, y_train)
    f1_scores.append(tpot.score(X_test, y_test))
    

print("#####################")
print("F1-Scores list for TPOT lib:", f1_scores)
print("AVG F1-Score for  TPOT lib:", sum(f1_scores)/len(f1_scores))
print("#####################")

# tpot.export('./tpot-optimized-classification-pipeline.py')

# Regression
df_train = pd.read_csv('data/college_train.csv', quotechar='\'', delimiter=',', skipinitialspace=True, na_values=["?"])
df_train['train'] = True

df_test = pd.read_csv('data/college_test.csv', quotechar='\'', delimiter=',', skipinitialspace=True, na_values=["?"])
df_test['train'] = False

df_all = pd.concat([df_train, df_test], ignore_index=True)

TARGET = 'percent_pell_grant'
feature_names = df_all.columns.difference([TARGET, 'train'])

categorial_columns = df_all.select_dtypes(include='object').columns
num_columns = df_all.columns.difference(categorial_columns)
num_columns = num_columns.drop('train')

most_frequent_imputer = SimpleImputer(strategy='most_frequent')
df_all[categorial_columns] = most_frequent_imputer.fit_transform(df_all[categorial_columns])

median_imputer = SimpleImputer(strategy='median')
df_all[num_columns] = median_imputer.fit_transform(df_all[num_columns])

df_all[categorial_columns] = df_all[categorial_columns].apply(func=LabelEncoder().fit_transform)
df_all[categorial_columns]


TARGET = 'percent_pell_grant'
feature_names = df_all[df_all['train'] == True].columns.difference([TARGET])
feature_names = feature_names.drop('train')

X_train = df_all[df_all['train'] == True][feature_names]
y_train = df_all[df_all['train'] == True][[TARGET]].values.ravel()

X_test = df_all[df_all['train'] == False][feature_names]
y_test = df_all[df_all['train'] == False][[TARGET]].values.ravel()


rmse_list = []

print('Starting regression experiment')

for i in range(0, ITERATIONS):
    print('%s. iteration ...' % (i+1))
    tpot = TPOTRegressor(scoring='neg_mean_squared_error', max_time_mins=TIME_LIMIT)
    tpot.fit(X_train, y_train)
    rmse_list.append(tpot.score(X_test, y_test))

# Convert negative MSE to RMSE
rmse_list = np.multiply(rmse_list, -1)
rmse_list = list(map(np.sqrt, rmse_list))

print('RMSE list: ', rmse_list)

print("============================================================")
print('Evaluation of regression models created using TPOT lib')
print("RMSE list:", rmse_list)
print("Average RMSE:", sum(rmse_list) / len(rmse_list))
print("============================================================")

# tpot.export('./tpot-optimized-regression-pipeline.py')