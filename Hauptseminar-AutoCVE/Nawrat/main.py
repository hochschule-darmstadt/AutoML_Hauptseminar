import pandas as pd
import numpy as np
from AUTOCVE.AUTOCVE import AUTOCVEClassifier

def make_x_y(df):
    y_df = df["'Result'"]
    X_df = df.drop(["'Result'"], axis=1)
    return X_df, y_df

train = pd.read_csv('../dataset/classification/phishing_train.csv')
test = pd.read_csv('../dataset/classification/phishing_test.csv')

X_train, y_train = make_x_y(train)
X_test, y_test = make_x_y(test)

X_train = X_train.to_numpy()
y_train = y_train.to_numpy()
X_test = X_test.to_numpy()
y_test = y_test.to_numpy()
 
y_train = np.reshape(y_train, (y_train.shape[0], 1))
y_test = np.reshape(y_test, (y_test.shape[0], 1))

autocve=AUTOCVEClassifier(grammar='grammarTPOT', n_jobs=-1, scoring='f1')

autocve.optimize(X_train, y_train, subsample_data=1.0)

print("Best ensemble")
best_voting_ensemble=autocve.get_best_voting_ensemble()
print(best_voting_ensemble.estimators)
print("Ensemble size: "+str(len(best_voting_ensemble.estimators)))

best_voting_ensemble.fit(X_train, y_train)
print("Train F1: {:.2f}".format(best_voting_ensemble.score(X_train, y_train)))
print("Test F1: {:.2f}".format(best_voting_ensemble.score(X_test, y_test)))
