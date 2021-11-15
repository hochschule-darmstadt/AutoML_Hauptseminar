"""
======================
Tabular Regression
======================

The following shows how to fit a regression model to the college dataset with AutoPyTorch

This is built to use the current (09-11-2021) development branch of AutoPyTorch

It also depends on automl_common as a submodule which isn't loaded automatically
to load it run "git submodule update --init --recursive" in the Auto-PyTorch folder
"""
import os
import tempfile as tmp
import warnings

import pandas as pd

from autoPyTorch.api.tabular_regression import TabularRegressionTask

# These settings are ported from Auto-PyTorch/examples/20_basics/example_tabular_regression.py
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

    # Both datasets are loaded with dtype=object because otherwise the column dtypes are inconsistent between train and test
    #   which leads to problems during model search
    train = pd.read_csv("college_train.csv", quotechar='\'', dtype=object)
    test = pd.read_csv("college_test.csv", quotechar='\'', dtype=object)

    # Remove superfluous quotation marks from column names. This is not a must but it helps with readability of the
    #   other statements.
    train.columns = train.columns.str.replace('"', '')
    test.columns = test.columns.str.replace('"', '')

    # Seperate target column (percent_pell_grant) from the data
    y_train = train["percent_pell_grant"]
    X_train = train.drop(["percent_pell_grant"], axis=1)

    y_test = test["percent_pell_grant"]
    X_test = test.drop(["percent_pell_grant"], axis=1)

    ############################################################################
    # Build and fit a regressor
    # ==========================
    api = TabularRegressionTask()

    ############################################################################
    # Search for an ensemble of machine learning algorithms
    # =====================================================
    api.search(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        optimize_metric='root_mean_squared_error',
        total_walltime_limit=600,  # Total time limit for the search process (seconds)
    )

    ############################################################################
    # Print the final ensemble performance
    # ====================================
    print(api.run_history, api.trajectory)
    y_pred = api.predict(X_test)

    # Rescale the Neural Network predictions into the original target range
    score = api.score(y_pred, y_test)

    print(score)
    # Print the final ensemble built by AutoPyTorch
    print(api.show_models())

    return score


if __name__ == "__main__":
    main()
