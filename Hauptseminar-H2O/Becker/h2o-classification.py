import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
import h2o
from h2o.automl import H2OAutoML

train = pd.read_csv('phishing_train.csv', quotechar="'")
test = pd.read_csv('phishing_test.csv', quotechar="'")

rmse_scores = []
for i in range(3):
    h2o.init()

    train_hf = h2o.H2OFrame(train)
    test_hf = h2o.H2OFrame(test)

    x = train_hf.columns
    y = "Result"
    x.remove(y)

    train_hf[y] = train_hf[y].asfactor()
    test_hf[y] = test_hf[y].asfactor()

    aml = H2OAutoML(max_runtime_secs=60 * 10)
    aml.train(x=x, y=y, training_frame=train_hf)

    preds = aml.predict(test_hf)['predict'].as_data_frame().to_numpy()
    y_test = test_hf[y].as_data_frame().to_numpy()
    rmse_scores.append(f1_score(y_test, preds))
    print(f'#{i + 1} {rmse_scores[i]}')
print(f'mean: {np.mean(rmse_scores)}')