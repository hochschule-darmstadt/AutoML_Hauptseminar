#!/usr/bin/env bash
set -e
gradle="/opt/gradle/gradle-5.2/bin/gradle "

cd /wdir/collegeregression
EVALFILE=/wdir/college_test_headerfix.csv $gradle -q sparkSubmit -Dmaster="spark://spark:7077" -Dmain=com.salesforce.app.CollegeRegression -Dargs="--run-type=train --model-location /resdir/CollegeRegression.model --read-location College=/wdir/college_train_headerfix.csv"