from typing_extensions import Literal
from mlbox.preprocessing import Reader, Drift_thresholder
from mlbox.optimisation import Optimiser
from mlbox.prediction import Predictor
from sklearn.metrics import mean_squared_error, make_scorer

from preparation import prepare_data, pretty_print

import warnings
warnings.filterwarnings("ignore")


def select_config(dataset: Literal["college", "phishing"]):
    """Decides according to instructions what is target and scorer, trows error if unknown dataset"""
    # For College Dataset, Goal: RMSE, we need to build own scorer, since only MSE exists per string default
    if dataset == "college":
        target_name = "percent_pell_grant"
        used_scorer = make_scorer(mean_squared_error, squared=False, greater_is_better=False)
    # For Phising Dataset Goal: F1 score
    elif dataset == "phishing":
        target_name = "Result"
        used_scorer = "f1"
    else:
        raise NameError("We don't got this dataset!")
    return (target_name, used_scorer)


def apply_auto_ml(dataset: Literal["college", "phishing"]):
    # Get needed target and scorer
    target_name, used_scorer = select_config(dataset)
    # Need train test split as files ...
    prepare_data(dataset, target_name)

    paths = [f"data/{dataset}_train.csv", f"data/{dataset}_test.csv"]
    data = Reader(sep=",").train_test_split(paths, target_name)
    data = Drift_thresholder().fit_transform(data)

    opt = Optimiser(scoring=used_scorer, n_folds=10)
    score = opt.evaluate(None, data)
    pretty_print(f"Score is: {score}")
    return score

    # This does not the seem to make a difference when space is default (set to none)
    # Probably it will pick the best hyperparameter if multiple will be used
    # best = opt.optimise(None, data, max_evals=10)
    # opt_score = opt.evaluate(best, data)
    # pretty_print(f"Optimized Score is: {opt_score}")
    # Predictor().fit_predict(best, data)


def main():
    """Run each dataset three times and print scores at the end"""
    college = []
    phishing = []
    for i in range(1, 4):
        print(f"Round {i}")
        college.append(apply_auto_ml("college"))
        phishing.append(apply_auto_ml("phishing"))
    print("#" * 100)
    print(f"College Dataset got Scores: {college}")
    print(f"Phishing Dataset got Scores: {phishing}")
    print("#" * 100)


if __name__ == "__main__":
    main()
