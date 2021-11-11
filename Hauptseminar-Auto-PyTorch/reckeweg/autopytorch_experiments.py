import os
import warnings
import statistics
import random

import tempfile as tmp
import pandas as pd

from autoPyTorch.api.tabular_classification import TabularClassificationTask
from autoPyTorch.api.tabular_regression import TabularRegressionTask


os.environ['JOBLIB_TEMP_FOLDER'] = tmp.gettempdir()
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)




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





def run_experiments(n, model_type, autopytorch_instance_params, autopytorch_search_params):
    if model_type == "regression":
        X_train, y_train, X_test, y_test = load_and_prepare_reg_data()
        api = TabularRegressionTask
    else:
        X_train, y_train, X_test, y_test = load_and_prepare_cls_data()
        api = TabularClassificationTask
    
    models = []
    scores = []
    
    for i in range(n):
        api_instance = api(
                seed = random.randint(0, 1000000),
                **autopytorch_instance_params
                )    
        print("Started experiment number {0}".format(i))
        api_instance.search(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test.copy(),
                y_test=y_test.copy(),
                **autopytorch_search_params,
                )
        models.append(api_instance)
        prediction = api_instance.predict(X_test)
        score = api_instance.score(prediction, y_test)

        if model_type == "classification":
            scores.append(score["f1"])
        else:
            scores.append(score["root_mean_squared_error"])

        print(api_instance.run_history, api_instance.trajectory)
        print(api_instance.show_models())
        print(
            "Finished experiment number {0}, the {1} model reached a {2} score of {3}".format(
            i, 
            model_type, 
            autopytorch_search_params["optimize_metric"], 
            score,
            )      
        )
        
    mean_score = statistics.mean(scores)

    print("The scores of the {0} models were {1}".format(n, scores))
    print(
            "The mean {0} score of the {1} {2} models is {3}".format(
                autopytorch_search_params["optimize_metric"], 
                n, 
                model_type, 
                mean_score
                )
            )
        
    return models, scores, mean_score





if __name__ == "__main__":

    autopytorch_cls_instance_params_dict = {
        "n_jobs": 4,
    }

    autopytorch_cls_search_params_dict = {
        "total_walltime_limit": 600,
        "func_eval_time_limit_secs": 50,
        "memory_limit": None,
        "optimize_metric": "f1",
        "all_supported_metrics": False,
    }



    autopytorch_reg_instance_params_dict = {
        "n_jobs": 4,
    }

    autopytorch_reg_search_params_dict = {
        "total_walltime_limit": 600,
        "func_eval_time_limit_secs": 50,
        "memory_limit": None,
        "optimize_metric": "root_mean_squared_error",
        "all_supported_metrics": False,
    }





    run_experiments(
            3, 
            "classification", 
            autopytorch_cls_instance_params_dict,
            autopytorch_cls_search_params_dict
    )

    run_experiments(
            3,
            "regression",
            autopytorch_reg_instance_params_dict,
            autopytorch_reg_search_params_dict
    )

