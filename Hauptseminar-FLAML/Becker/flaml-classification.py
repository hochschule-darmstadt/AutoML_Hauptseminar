import pandas as pd
import numpy as np
from flaml import AutoML
from sklearn.metrics import f1_score

train = pd.read_csv('phishing_train.csv', quotechar="'")
test = pd.read_csv('phishing_test.csv', quotechar="'")

X_train, y_train = train.drop('Result', axis=1), train[['Result']].values.flatten()
X_test, y_test = test.drop('Result', axis=1), test[['Result']].values.flatten()

f1_scores = []
for i in range(3):
    automl_settings = {
        "time_budget": 60 * 10, # 10 min
        "metric": 'f1',
        "task": 'classification',
        "log_file_name": 'flaml-classification.log',
        "verbose": -1
    }
    automl = AutoML()
    automl.fit(X_train = X_train, y_train = y_train, **automl_settings)
    f1_scores.append(f1_score(y_test, automl.predict(X_test)))
    print(f'#{i+1} {f1_scores[i]}')
print(f'mean: {np.mean(f1_scores)}')
