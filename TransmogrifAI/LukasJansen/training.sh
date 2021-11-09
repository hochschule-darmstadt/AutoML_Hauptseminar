#!/usr/bin/env bash
set -e
gradle="/opt/gradle/gradle-5.2/bin/gradle "

cd /wdir/automlproject
$gradle -q installDist
$gradle -q sparkSubmit -Dmaster="spark://spark:7077" -Dmain=de.lukas_jansen.automl.Main -Dargs="train_college /wdir/college_train_headerfix.csv /resdir/college_model.json"