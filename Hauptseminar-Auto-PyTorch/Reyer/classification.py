"""
======================
Tabular Classification
======================

The following shows how to fit a classification model to the phishing dataset with AutoPyTorch

This is built to use the current (09-11-2021) development branch of AutoPyTorch

It also depends on automl_common as a submodule which isn't loaded automatically
to load it run "git submodule update --init --recursive" in the Auto-PyTorch folder
"""
import os
import tempfile as tmp
import warnings

import pandas as pd

from autoPyTorch.api.tabular_classification import TabularClassificationTask

# These settings are ported from Auto-PyTorch/examples/20_basics/example_tabular_classification.py
os.environ['JOBLIB_TEMP_FOLDER'] = tmp.gettempdir()
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    ############################################################################
    # Data Loading
    # ============
    train = pd.read_csv("phishing_train.csv", quotechar='\'')
    test = pd.read_csv("phishing_test.csv", quotechar='\'')

    # Seperate target column (Result) from the data
    y_train = train["Result"]
    X_train = train.drop(["Result"], axis=1)

    y_test = test["Result"]
    X_test = test.drop(["Result"], axis=1)

    ############################################################################
    # Build and fit a classifier
    # ==========================
    api = TabularClassificationTask()

    ############################################################################
    # Search for an ensemble of machine learning algorithms
    # =====================================================
    api.search(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        optimize_metric='f1',
        total_walltime_limit=600  # Total time limit for the search process (seconds)
    )

    ############################################################################
    # Print the final ensemble performance
    # ====================================
    print(api.run_history, api.trajectory)
    y_pred = api.predict(X_test)
    score = api.score(y_pred, y_test)
    print(score)
    # Print the final ensemble built by AutoPyTorch
    print(api.show_models())
    return score


if __name__ == "__main__":
    main()
