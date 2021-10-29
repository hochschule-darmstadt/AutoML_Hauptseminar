import numpy as np
import time as t
from autogluon.tabular import TabularDataset, TabularPredictor

def print_experiment_result(target: str, exp_result_1, exp_result_2, exp_result_3):
	print("#######################")
	print("#######################")
	print("#######################")
	print("#######################")
	print("RESULTS")
	print(exp_result_1[target])
	print(exp_result_2[target])
	print(exp_result_3[target])
	print("MEAN VALUE")
	mean_value = np.mean(np.array([exp_result_1[target], exp_result_2[target], exp_result_3[target]]))
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
		train_data = TabularDataset("./phishing_train.csv")
		test_data = TabularDataset("./phishing_test.csv")
		target = '\'Result\''
	else:
		train_data = TabularDataset("./college_train.csv")
		test_data = TabularDataset("./college_test.csv")
		target = '\'percent_pell_grant\''
	#run 3 experiments
	for i in range(3):
		#init AutoGluon task
		if is_classification == True:
			clf = TabularPredictor(label=target, problem_type='binary', eval_metric='f1')
		else:
			clf = TabularPredictor(label=target, problem_type='regression', eval_metric='root_mean_squared_error')
		#run each experiment and save the f1 score in seperate variables
		time_at_start = t.time()
		if i == 0:
			predictor = clf.fit(train_data)
			predictor.leaderboard()
			exp_result_1 = predictor.evaluate(test_data)
			time_experiment_1 = t.time() - time_at_start
		elif i == 1:
			predictor = clf.fit(train_data)
			predictor.leaderboard()
			exp_result_2 = predictor.evaluate(test_data)
			time_experiment_2 = t.time() - time_at_start
		else:
			predictor = clf.fit(train_data)
			predictor.leaderboard()
			exp_result_3 = predictor.evaluate(test_data)
			time_experiment_3 = t.time() - time_at_start
	
	print("TIMES")
	print(time_experiment_1)
	print(time_experiment_2)
	print(time_experiment_3)
	#print result at the end
	if is_classification == True:
		print_experiment_result('f1', exp_result_1, exp_result_2, exp_result_3)
	else:
		#Scores are always higher_is_better. This metric score can be multiplied by -1 to get the metric value.
		print_experiment_result('root_mean_squared_error', exp_result_1, exp_result_2, exp_result_3)
	return

if __name__ == "__main__":
	run_experiment(True)
	run_experiment(False)