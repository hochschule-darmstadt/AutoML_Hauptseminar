import tensorflow as tf
import numpy as np
import pandas as pd
import autokeras as ak
import keras_tuner as kt
from tensorflow.keras import backend as K
import time as t

#custom metric RMSE for AutoKeras usage
def rmse(y_true: float, y_pred: float):
	return tf.sqrt(tf.reduce_mean(tf.math.squared_difference(y_true, y_pred)))

#compute recall
def recall_m(y_true: float, y_pred: float):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

#compute precision
def precision_m(y_true: float, y_pred: float):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

#custom metric F1 score for AutoKeras usage
def f1_score(y_true: float, y_pred: float):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def print_experiment_result(target: str, exp_result_1, exp_result_2, exp_result_3):
	print("#######################")
	print("#######################")
	print("#######################")
	print("#######################")
	print("RESULTS")
	print(np.mean(exp_result_1.history[target]))
	print(np.mean(exp_result_2.history[target]))
	print(np.mean(exp_result_3.history[target]))
	print("MEAN VALUE")
	mean_value = np.mean(np.array(np.mean(exp_result_1.history[target]), np.mean(exp_result_2.history[target]), np.mean(exp_result_3.history[target])))
	print(mean_value)
	print("RESULTS")
	print("#######################")
	print("#######################")
	print("#######################")
	print("#######################")
	return

#Run Autokeras task
def run_experiment(is_classification: bool):
	#load dataset
	if is_classification == True:
		dataset = pd.read_csv(r"C:\Users\hda10126\source\repos\Hauptseminar-AutoKeras\Hauptseminar-AutoKeras\phishing.csv", quotechar='\'', skipinitialspace=True)
		x = dataset.drop('Result', axis=1)
		y = dataset.Result
	else:
		dataset = pd.read_csv(r"C:\Users\hda10126\source\repos\Hauptseminar-AutoKeras\Hauptseminar-AutoKeras\college.csv", quotechar='\'', skipinitialspace=True)
		x = dataset.drop('percent_pell_grant', axis=1)
		y = dataset.percent_pell_grant
	#run 3 experiments
	for i in range(3):
		#init AutoKeras task
		if is_classification == True:
			clf = ak.StructuredDataClassifier(overwrite=True, 
										   max_trials=10, 
										   objective=kt.Objective('val_f1_score', direction='max'),
										   metrics=[f1_score])
		else:
			clf = ak.StructuredDataRegressor(overwrite=True, 
										   max_trials=10, 
										   objective=kt.Objective('val_rmse', direction='min'),
										   metrics=[rmse])
		#run each experiment and save the f1 score in seperate variables
		time_at_start = t.time()
		if i == 0:
			exp_result_1 = clf.fit(x, y, epochs=10)
			time_experiment_1 = t.time() - time_at_start
		elif i == 1:
			exp_result_2 = clf.fit(x, y, epochs=10)
			time_experiment_2 = t.time() - time_at_start
		else:
			exp_result_3 = clf.fit(x, y, epochs=10)
			time_experiment_3 = t.time() - time_at_start
	
	print("TIMES")
	print(time_experiment_1)
	print(time_experiment_2)
	print(time_experiment_3)
	#print result at the end
	if is_classification == True:
		print_experiment_result('f1_score', exp_result_1, exp_result_2, exp_result_3)
	else:
		print_experiment_result('rmse', exp_result_1, exp_result_2, exp_result_3)
	return

if __name__ == "__main__":
	run_experiment(True)
	run_experiment(False)