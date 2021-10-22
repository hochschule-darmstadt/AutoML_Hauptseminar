"""Preparation Script for the data. Since the new test / train data became available, the function
extract_target_for_mlbox was used to prepare the data for mlbox.
Primarly used for documentation issues, don't need to be run anymore."""

import pandas as pd
from sklearn.model_selection import train_test_split


def prepare_data(name: str, target: str, folder: str = "data"):
    """Prepares the data according to the boxml needed formats.
    mlbox needs two (train, test) datasets, the test dataset can not contain the target.
    Deprecated, currently not needed anymore.

    Args:
        name (str): filename without extension
        target (str): targetname
        folder (str, optional): Folder where data lies. Defaults to "data".
    """
    X = pd.read_csv(f"{folder}/{name}.csv", quotechar="'", na_values="?")
    # NOT USING random state since we want 3x execution with differnt results.
    # rs = 42
    # train, test = train_test_split(X, test_size=0.3, random_state=rs)
    train, test = train_test_split(X, test_size=0.3)
    test_target = test[target].copy()
    test.drop(columns=[target], inplace=True)
    train.to_csv(f"{folder}/{name}_train.csv", index=False)
    test.to_csv(f"{folder}/{name}_test.csv", index=False)
    test_target.to_csv(f"{folder}/{name}_test_target.csv", header=[target], index=False)


def extract_target_for_mlbox(name: str, target: str, folder: str = "data"):
    """MLBOX treats things different, therefore we need to extract the target from 
    the new received test data.
    In addition also prepares (removes '?') the data for mlbox"""
    train = pd.read_csv(f"{folder}/{name}_train.csv", quotechar="'", na_values="?")
    test = pd.read_csv(f"{folder}/{name}_test.csv", quotechar="'", na_values="?")
    test_target = test[target].copy()
    test_target.to_csv(f"{folder}/{name}_test_target.csv", header=[target], index=False)
    test.drop(columns=[target], inplace=True)
    train.to_csv(f"{folder}/{name}_train.csv", index=False)
    test.to_csv(f"{folder}/{name}_test.csv", index=False)


def pretty_print(text: str):
    """Just makes a 'pretty' box around the printing"""
    print("#" * 80)
    print(f" {text} ".center(80, "-"))
    print("#" * 80)


if __name__ == "__main__":
    extract_target_for_mlbox("college", "percent_pell_grant")
    extract_target_for_mlbox("phishing", "Result")
