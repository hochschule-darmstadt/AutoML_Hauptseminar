#!/usr/bin/env bash
set -ex
gradle="/opt/gradle/gradle-5.2/bin/gradle "

cd /wdir/automlproject
$gradle -q installDist
sleep 10
for i in {1..3}; do
    $gradle -q sparkSubmit -Dmaster="spark://spark:7077" -Dmain=de.lukas_jansen.automl.Main -Dargs="train_college /wdir/college_train_headerfix.csv /resdir/college_model_$i" &> "/resdir/college_train_$i.log"
    $gradle -q sparkSubmit -Dmaster="spark://spark:7077" -Dmain=de.lukas_jansen.automl.Main -Dargs="eval_college /wdir/college_test_headerfix.csv /resdir/college_model_$i" &> "/resdir/college_test_$i.log"
    $gradle -q sparkSubmit -Dmaster="spark://spark:7077" -Dmain=de.lukas_jansen.automl.Main -Dargs="train_phishing /wdir/phishing_train_headerfix.csv /resdir/phishing_model_$i"  &> "/resdir/phishing_train_$i.log"
    $gradle -q sparkSubmit -Dmaster="spark://spark:7077" -Dmain=de.lukas_jansen.automl.Main -Dargs="eval_phishing /wdir/phishing_test_headerfix.csv /resdir/phishing_model_$i" &> "/resdir/phishing_test_$i.log"
done