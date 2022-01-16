import pandas as pd
import numpy as np
from flaml import AutoML
from sklearn.metrics import mean_squared_error

train = pd.read_csv('../../Hauptseminar-ATM/Scheppat/college_train.csv', quotechar="'")
test = pd.read_csv('../../Hauptseminar-ATM/Scheppat/college_test.csv', quotechar="'")

X_train, y_train = train.drop('percent_pell_grant', axis=1), train[['percent_pell_grant']].values.flatten()
X_test, y_test = test.drop('percent_pell_grant', axis=1), test[['percent_pell_grant']].values.flatten()

automl_settings = {
    "time_budget": 60 * 10, # 10 min
    "metric": 'rmse',
    "task": 'regression',
    "log_file_name": 'log/flaml-regression.log',
    "verbose": -1
}

rmse_scores = []
for i in range(3):
    automl = AutoML()
    automl.fit(X_train = X_train, y_train = y_train, **automl_settings)
    rmse_scores.append(mean_squared_error(y_test, automl.predict(X_test), squared=False))
    print(f'#{i+1} {rmse_scores[i]}')
print(f'mean: {np.mean(rmse_scores)}')