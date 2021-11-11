import statistics
import random

import pandas as pd
import sklearn.datasets

from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor
from autosklearn.metrics import root_mean_squared_error
from autosklearn.metrics import f1


def load_and_prepare_cls_data():
    cls_train, cls_test = [pd.read_csv(file) for file in ["phishing_train.csv", "phishing_test.csv"]]

    y_cls_train, y_cls_test = [data_frame["'Result'"] for data_frame in [cls_train, cls_test]]
    X_cls_train, X_cls_test = [data_frame.drop("'Result'", axis=1) for data_frame in [cls_train, cls_test]]

    return X_cls_train, y_cls_train, X_cls_test, y_cls_test


def load_and_prepare_reg_data():
    reg_train, reg_test = [
        pd.read_csv(
            file,
            on_bad_lines="warn",
            na_values="?",
            quotechar="'",
            sep=",",
            usecols=lambda x: x not in ["school_name", "school_webpage", "UNITID"],
            dtype={
                "city": "category",
                "state": "category",
                "zip": "category",
                "predominant_degree": "category",
                "highest_degree": "category",
                "ownership": "category",
                "region": "category",
                "gender": "category",
                "carnegie_basic_classification": "category",
                "carnegie_undergraduate": "category",
                "carnegie_size": "category",
                "religious_affiliation": "category"
            }
        )
        for file in ["college_train.csv", "college_test.csv"]
    ]

    y_reg_train, y_reg_test = [data_frame["percent_pell_grant"] for data_frame in [reg_train, reg_test]]
    X_reg_train, X_reg_test = [data_frame.drop("percent_pell_grant", axis=1) for data_frame in [reg_train, reg_test]]

    return X_reg_train, y_reg_train, X_reg_test, y_reg_test



def run_experiments(n, model_type, autosklearn_params):
    if model_type == "regression":
        X_train, y_train, X_test, y_test = load_and_prepare_reg_data()
        automl = AutoSklearnRegressor
        metric = root_mean_squared_error
    else:
        X_train, y_train, X_test, y_test = load_and_prepare_cls_data()
        automl = AutoSklearnClassifier
        metric = f1

    models = []
    scores = []


    for i in range(n):
        automl_instance = automl(
                seed = random.randint(0, 1000000),
                **autosklearn_params
                )
        print("Started experiment number {0}".format(i))
        automl_instance.fit(X_train, y_train)
        models.append(automl_instance)
        prediction = automl_instance.predict(X_test)
        score = metric(y_test, prediction)
        scores.append(score)
        print(
            "Finished experiment number {0}, the {1} model reached a {2} score of {3}".format(
            i,
            model_type,
            metric.name,
            score
            )
        )
        print(automl_instance.leaderboard())

    mean_score = statistics.mean(scores)

    print("The mean {0} score of the {1} {2} models is {3}".format(metric.name, n, model_type, mean_score))

    return models, scores, mean_score




if __name__ == "__main__":
	
    autosklearn_cls_params_dict = {
        "time_left_for_this_task": 600,
        "n_jobs": -1,
    }

    autosklearn_reg_params_dict = {
        "time_left_for_this_task": 600,
        "n_jobs": -1,
    }


    run_experiments(3, "classification", autosklearn_cls_params_dict)

    run_experiments(3, "regression", autosklearn_reg_params_dict)
