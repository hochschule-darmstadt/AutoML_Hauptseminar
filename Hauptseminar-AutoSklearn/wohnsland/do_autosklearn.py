from typing_extensions import Literal
import autosklearn.classification
import autosklearn.regression
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
from sklearn.metrics import mean_squared_error, f1_score

import pandas as pd


def select_config(dataset: Literal["college", "phishing"]):
    """Decides according to instructions what is target and scorer, trows error if unknown dataset"""
    # For College Dataset, Goal: RMSE, we need to build own scorer, since only MSE exists per string default
    if dataset == "college":
        target_name = "percent_pell_grant"
        def used_scorer(x, y): return mean_squared_error(x, y, squared=False)
    # For Phising Dataset Goal: F1 score
    elif dataset == "phishing":
        target_name = "Result"
        used_scorer = f1_score
    else:
        raise NameError("We don't got this dataset!")
    return (target_name, used_scorer)


def generate_data(dataset: Literal["college", "phishing"]):
    target_name, _ = select_config(dataset)
    train = pd.read_csv(f"{dataset}_train.csv", quotechar="'", na_values="?")  # , na_values="?"
    test = pd.read_csv(f"{dataset}_test.csv", quotechar="'", na_values="?")
    if dataset == "college":
        to_drop = ["school_name", "city", "zip", "school_webpage"]
        to_change = ["state", "predominant_degree", "highest_degree", "ownership", "region", "gender",
                     "carnegie_basic_classification", "carnegie_undergraduate", "carnegie_size", "religious_affiliation"]
        train["dstype"] = "train"
        test["dstype"] = "test"
        combined = pd.concat([train, test])
        is_train = combined['dstype'] == "train"
        combined.drop(['dstype'], axis=1, inplace=True)
        combined.drop(to_drop, axis=1, inplace=True)
        combined = pd.get_dummies(combined, prefix=to_change)
        train = combined.loc[is_train]
        test = combined.loc[[not x for x in is_train]]
    X_train = train.drop(target_name, axis=1)
    y_train = train[target_name]
    X_test = test.drop(target_name, axis=1)
    y_test = test[target_name]
    return (X_train, X_test, y_train, y_test)


def do_classification(X_train, X_test, y_train, y_test, scorer, seed=1):
    automl = autosklearn.classification.AutoSklearnClassifier(time_left_for_this_task=600, seed=seed)
    automl.fit(X_train, y_train)
    y_hat = automl.predict(X_test)
    print("Accuracy score Classification", scorer(y_test, y_hat))


def do_regression(X_train, X_test, y_train, y_test, scorer, seed=1):
    automl = autosklearn.regression.AutoSklearnRegressor(time_left_for_this_task=600, seed=seed)
    automl.fit(X_train, y_train)
    y_hat = automl.predict(X_test)
    print("Accuracy score", scorer(y_test, y_hat))


def main():
    # First Classification
    X_train, X_test, y_train, y_test = generate_data("phishing")
    _, scorer = select_config("phishing")
    for i in range(1, 4):
        print(f"Doing classification No. {i}")
        do_classification(X_train, X_test, y_train, y_test, scorer, seed=i)

    # Then regression
    X_train, X_test, y_train, y_test = generate_data("college")
    _, scorer = select_config("college")
    for i in range(1, 4):
        print(f"Doing regression No. {i}")
        do_regression(X_train, X_test, y_train, y_test, scorer, seed=i)


if __name__ == "__main__":
    main()
