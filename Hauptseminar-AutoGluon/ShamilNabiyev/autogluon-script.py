from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor
import pandas as pd


def run_autogluon_experiment(train_dataset,
                             test_dataset,
                             target_column,
                             problem_type,
                             eval_metric,
                             time_limit=600,
                             num_iterations=3):
    """

    :param train_dataset: Training dataset
    :type train_dataset: pandas.DataFrame
    :param test_dataset: Test dataset
    :type test_dataset: pandas.DataFrame
    :param target_column: Name of target column in train_dataset
    :type target_column: str
    :param problem_type: 'binary' for classification, 'regression' for regression models
    :type problem_type: str
    :param eval_metric: Evaluation metrics, e.g. 'accuracy', 'f1', 'root_mean_squared_error' etc.
    :type eval_metric: str
    :param time_limit: Time limit in seconds
    :type time_limit: int
    :param num_iterations: Number of iterations
    :type num_iterations: int
    :return: A list of integer values
    """
    eval_results = []

    for i in range(num_iterations):
        predictor = TabularPredictor(
            label=target_column,
            problem_type=problem_type,
            eval_metric=eval_metric
        )

        predictor.fit(
            # train_data=train_data,
            train_data=train_dataset,
            # tuning_data=val_data,
            time_limit=time_limit
        )

        test_performance = predictor.evaluate(test_dataset)
        eval_results.append(test_performance[eval_metric])
        print('-----------------------------------------')

    return eval_results


if __name__ == '__main__':
    # Classification
    df_train = pd.read_csv('data/phishing_train.csv', quotechar='\'', skipinitialspace=True)
    df_test = pd.read_csv('data/phishing_test.csv', quotechar='\'', skipinitialspace=True)

    classification_results = run_autogluon_experiment(
        train_dataset=df_train,
        test_dataset=df_test,
        target_column='Result',
        problem_type='binary',
        eval_metric='f1',
        time_limit=60*10,
        num_iterations=3
    )

    print()
    print("============================================================")
    print('Evaluation of classification models created using AutoGluon lib')
    print("F1-Scores list:", classification_results)
    print("Average F1-Score:", sum(classification_results) / len(classification_results))
    print("============================================================")

    # Regression
    df_train = pd.read_csv('data/college_train.csv', quotechar='\'', skipinitialspace=True)
    df_test = pd.read_csv('data/college_test.csv', quotechar='\'', skipinitialspace=True)

    regression_results = run_autogluon_experiment(
        train_dataset=df_train,
        test_dataset=df_test,
        target_column='percent_pell_grant',
        problem_type='regression',
        eval_metric='root_mean_squared_error',
        time_limit=60*10,
        num_iterations=3
    )

    print()
    print("============================================================")
    print('Evaluation of regression models created using AutoGluon lib')
    print("RMSE list:", regression_results)
    print("Average RMSE:", sum(regression_results) / len(regression_results))
    print("============================================================")

