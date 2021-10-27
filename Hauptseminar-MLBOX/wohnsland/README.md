# Sub Repo for MLBOX

## Getting started

Using `Python 3.6` and run pip to set up requirements. Doc states that `v3.5` - `v3.7` should work.

```bash
pip install -r requirements.txt
```

The `mlbox.py` file shows a sample execution code for a vanilla setup to achieve a running AutoML-Pipeline.

## Boundary Conditions

To be comparable with the other AutoML Libs, some conditions were defined. Theses were

- Using for classification: [PhishingWebsites Dataset](https://www.openml.org/d/4534) with Target: Result, Score: F1
- Using for regression: [colleges Dataset](https://www.openml.org/d/42727) with Target: percent_pell_grant, Loss: RMSE
- Doing three repeats for each dataset
- Use as limitation either a maximum of 10 minutes or 10 repeats / epochs

## Pitfalls

### Using RMSE

By default, `MLBOX` only delivers MSE as selection. The doc shows that differnt strings can be used for Loss. An inspection of the code shows that also scorer classes from the `sklearn.metrics` can be used. In this case the RMSE was created using the `sklearn.metrics.make_scorer` and `sklearn.metrics.mean_squared_error` function, setting `greater_is_better` to False, since RMSE is used as a loss function:

```python
from sklearn.metrics import mean_squared_error, make_scorer
used_scorer = make_scorer(mean_squared_error, squared=False, greater_is_better=False)
```

### Data Input Format

`MLBOX` needs either two input datasets to work, or one dataset, where a part of the data got no target value. The "test" dataset needs to have the target column removed. Otherwise it will result in an error. I used the first approach dividing the data into two datasets with a 70/30 split, using the function `prepare_data` to write the original data to two corresponding files.

This is the corresponding code for causing this behaviour of the library:

```python
# Here the lib iterates over each file, dividing into train and test
# depending on the existence of the target value
for path in Lpath:
    df = self.clean(path, drop_duplicate=False)
    if (target_name in df.columns):

        is_null = df[target_name].isnull()
        df_train[path] = df[~is_null].drop(target_name, axis=1)
        df_test[path] = df[is_null].drop(target_name, axis=1)
        y_train[path] = df[target_name][~is_null]

    else:
        df_test[path] = df

# if one of the two dicts (test or train) got not data, an error will
# be thrown. This will force you to remove some of the target values
# from your dataset before using it
if (sum([df_train[path].shape[0]
          for path in df_train.keys()]) == 0):
    raise ValueError("You have no train dataset. "
                      "Please check that the "
                      "target name is correct.")

if ((sum([df_test[path].shape[0]
          for path in df_test.keys()]) == 0) & (self.verbose)):
    print("")
    print("You have no test dataset !")
```

### Classifier Always Return same Predictions with Multiple Runs

This is a problem with the library. The source code defines a fixed seed, therefore the model will always start with the same initial weights. This will also (with the same input data) result in the same model and score of test data in our case.

```python
# Somewhere in the classifier.py and Classifier()
elif(strategy == "LightGBM"):
    self.__classifier = LGBMClassifier(
        n_estimators=500, learning_rate=0.05,
        colsample_bytree=0.8, subsample=0.9, nthread=-1, seed=0)
```
