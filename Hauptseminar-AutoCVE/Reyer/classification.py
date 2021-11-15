from AUTOCVE.AUTOCVE import AUTOCVEClassifier
from sklearn.metrics import f1_score
import pandas as pd


def main():
    ############################################################################
    # Data Loading
    # ============
    train = pd.read_csv("phishing_train.csv", quotechar='\'')
    test = pd.read_csv("phishing_test.csv", quotechar='\'')

    # Separate the target column "Result" from the train and test data
    # This also converts all the pandas DataFrames to numpy arrays since autocve can't handle DataFrames
    y_train = train["Result"].to_numpy()
    X_train = train.drop(["Result"], axis=1).to_numpy()

    y_test = test["Result"].to_numpy()
    X_test = test.drop(["Result"], axis=1).to_numpy()

    ############################################################################
    # Build and fit a classifier
    # ==========================
    # Build classifier
    autocve = AUTOCVEClassifier(max_evolution_time_secs=600,
                                grammar='grammarTPOT',
                                n_jobs=-1,
                                verbose=1)

    autocve.optimize(X_train, y_train, subsample_data=1.0)

    print("Best ensemble")
    best_voting_ensemble = autocve.get_best_voting_ensemble()
    print(best_voting_ensemble.estimators)
    print("Ensemble size: " + str(len(best_voting_ensemble.estimators)))

    best_voting_ensemble.fit(X_train, y_train)
    print("Train Score: {}".format(best_voting_ensemble.score(X_train, y_train)))
    print("Test Score: {}".format(best_voting_ensemble.score(X_test, y_test)))

    y_pred = best_voting_ensemble.predict(X_test)
    f_one_score = f1_score(y_test, y_pred, average="macro")
    print("F1 Score: {}".format(f_one_score))

    return f_one_score


if __name__ == "__main__":
    main()
