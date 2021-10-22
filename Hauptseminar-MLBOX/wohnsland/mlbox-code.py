from typing_extensions import Literal
import pandas as pd
import random
import numpy as np
from mlbox.preprocessing import Reader, Drift_thresholder
from mlbox.optimisation import Optimiser
from mlbox.prediction import Predictor
from sklearn.metrics import mean_squared_error, make_scorer, f1_score

from preparation import prepare_data, pretty_print

import warnings
warnings.filterwarnings("ignore")


def select_config(dataset: Literal["college", "phishing"]):
    """Decides according to instructions what is target and scorer, trows error if unknown dataset"""
    # For College Dataset, Goal: RMSE, we need to build own scorer, since only MSE exists per string default
    if dataset == "college":
        target_name = "percent_pell_grant"
        used_scorer = make_scorer(mean_squared_error, squared=False, greater_is_better=False)
        def scoring_function(x, y): return mean_squared_error(x, y, squared=False)
    # For Phising Dataset Goal: F1 score
    elif dataset == "phishing":
        target_name = "Result"
        used_scorer = "f1"
        scoring_function = f1_score
    else:
        raise NameError("We don't got this dataset!")
    return (target_name, used_scorer, scoring_function)


def apply_auto_ml(dataset: Literal["college", "phishing"], rs: int):
    # Get needed target and scorer
    target_name, used_scorer, scoring_function = select_config(dataset)
    # Don't need this anymore, got new train/test from master
    # Need train test split as files ...
    # prepare_data(dataset, target_name)

    paths = [f"data/{dataset}_train.csv", f"data/{dataset}_test.csv"]
    data = Reader(sep=",").train_test_split(paths, target_name)
    data = Drift_thresholder().fit_transform(data)

    opt = Optimiser(scoring=used_scorer, n_folds=10, random_state=rs)
    score = opt.evaluate(None, data)
    pretty_print(f"Score is: {score}")

    best = opt.optimise(None, data, 10)
    pred = Predictor(verbose=False).fit_predict(best, data)
    # return score

    test_target = pd.read_csv(f"data/{dataset}_test_target.csv")
    y_true = test_target[target_name].to_list()
    pred_df = pd.read_csv(f"save/{target_name}_predictions.csv")
    y_pred = pred_df[f"{target_name}_predicted"].to_list()
    score_test = scoring_function(y_true, y_pred)
    return (score, score_test)


def main():
    """Run each dataset three times and print scores at the end"""
    college = []
    phishing = []
    rs = [42, 1337, 543]
    for i in range(1, 4):
        np.random.seed(rs[i - 1])
        random.seed(rs[i - 1])
        print(f"Round {i}")
        college.append(apply_auto_ml("college", rs[i - 1]))
        phishing.append(apply_auto_ml("phishing", rs[i - 1]))
    print("#" * 100)
    print(f"College Dataset got Scores (crossvalidation, testing/validation DS): {college}")
    print(f"Phishing Dataset got Scores (crossvalidation, testing/validation DS): {phishing}")
    print("#" * 100)


if __name__ == "__main__":
    main()
