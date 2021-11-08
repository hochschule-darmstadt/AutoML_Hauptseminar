import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import h2o
from h2o.automl import H2OAutoML

train = pd.read_csv('college_train.csv', quotechar="'")
test = pd.read_csv('college_test.csv', quotechar="'")

rmse_scores = []
for i in range(3):
    h2o.init()

    train_hf = h2o.H2OFrame(train)
    test_hf = h2o.H2OFrame(test)

    # h2o interprets these columns in one of the two sets as categorical -> declare them manually as numeric
    train_hf['average_cost_academic_year'] = train_hf['average_cost_academic_year'].asnumeric()
    test_hf['average_cost_academic_year'] = test_hf['average_cost_academic_year'].asnumeric()
    train_hf['average_cost_program_year'] = train_hf['average_cost_program_year'].asnumeric()
    test_hf['average_cost_program_year'] = test_hf['average_cost_program_year'].asnumeric()
    train_hf['tuition_(instate)'] = train_hf['tuition_(instate)'].asnumeric()
    test_hf['tuition_(instate)'] = test_hf['tuition_(instate)'].asnumeric()
    train_hf['tuition_(out_of_state)'] = train_hf['tuition_(out_of_state)'].asnumeric()
    test_hf['tuition_(out_of_state)'] = test_hf['tuition_(out_of_state)'].asnumeric()
    train_hf['faculty_salary'] = train_hf['faculty_salary'].asnumeric()
    test_hf['faculty_salary'] = test_hf['faculty_salary'].asnumeric()
    train_hf['percent_part_time_faculty'] = train_hf['percent_part_time_faculty'].asnumeric()
    test_hf['percent_part_time_faculty'] = test_hf['percent_part_time_faculty'].asnumeric()
    train_hf['percent_female'] = train_hf['percent_female'].asnumeric()
    test_hf['percent_female'] = test_hf['percent_female'].asnumeric()
    train_hf['agege24'] = train_hf['agege24'].asnumeric()
    test_hf['agege24'] = test_hf['agege24'].asnumeric()
    train_hf['faminc'] = train_hf['faminc'].asnumeric()
    test_hf['faminc'] = test_hf['faminc'].asnumeric()
    train_hf['mean_earnings_10_years'] = train_hf['mean_earnings_10_years'].asnumeric()
    test_hf['mean_earnings_10_years'] = test_hf['mean_earnings_10_years'].asnumeric()
    train_hf['median_earnings_10_years'] = train_hf['median_earnings_10_years'].asnumeric()
    test_hf['median_earnings_10_years'] = test_hf['median_earnings_10_years'].asnumeric()

    x = train_hf.columns
    y = 'percent_pell_grant'
    x.remove(y)

    aml = H2OAutoML(max_runtime_secs=60 * 10)
    aml.train(x=x, y=y, training_frame=train_hf)

    preds = aml.predict(test_hf)['predict'].as_data_frame().to_numpy()
    y_test = test_hf[y].as_data_frame().to_numpy()
    rmse_scores.append(mean_squared_error(y_test, preds, squared=False))
    print(f'#{i + 1} {rmse_scores[i]}')
print(f'mean: {np.mean(rmse_scores)}')