import pandas as pd
from sklearn.model_selection import train_test_split


def prepare_data(name: str, target: str, folder: str = "data"):
    """Prepares the data according to the boxml needed formats.
    mlbox needs two (train, test) datasets, the test dataset can not contain the target.

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
    test.drop(columns=[target], inplace=True)
    train.to_csv(f"{folder}/{name}_train.csv")
    test.to_csv(f"{folder}/{name}_test.csv")


def pretty_print(text: str):
    """Just makes a 'pretty' box around the printing"""
    print("#" * 80)
    print(f" {text} ".center(80, "-"))
    print("#" * 80)


if __name__ == "__main__":
    prepare_data("college", "percent_pell_grant")
    prepare_data("phishing", "Result")
