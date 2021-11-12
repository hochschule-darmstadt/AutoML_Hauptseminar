# TransmogrifAI


There we two older attempts. One just starting from Scratch (Without the gradle plugin, Dependency distribution in the cluster is a mess, even with the plugin mechanism from spark) and the other using the project boostrap from the documentation (which is currently generating unusable code, see https://github.com/salesforce/TransmogrifAI/issues/408#issuecomment-540758245). The solution was to combine the two and start from scratch in a generated project and manually create classes for each Feature.

I recommend IntelliJ for the project directory (Avro generated Classes are not visible).
## Running

```sh
# This IP can be used to look at the UIs port 8080
docker-compose up -d --build
docker inspect lukasjansen_spark_1 | grep IPAddress
docker-compose exec spark tail -f /resdir/run.log
# Ctrl-c when finished
docker cp lukasjansen_spark_1:/resdir/ resdir
rm resdir/phishing_model_* resdir/college_model_*

```

## Project Creation:

Based on: https://docs.transmogrif.ai/en/stable/examples/Bootstrap-Your-First-Project.html

```sh
git clone -b 0.7.0 --depth 1 https://github.com/salesforce/TransmogrifAI.git transmogriftool
cd ./transmogriftool
./gradlew cli:shadowJar
fixdatafile () {
  sed '1,1s/["\(\)]//g' < $1 | sed 's/\x27/"/g; s/?//g' > $2
}
addid (){
  tmp=$(mktemp)
  echo '"ID"' > $tmp
  seq 2 $(wc -l < $1) >> $tmp
  paste -d ',' $tmp $1 > $2
  rm $tmp
}

# College 
fixdatafile ../../../Hauptseminar-AutoKeras/college_train.csv ../college_train_headerfix.csv
fixdatafile ../../../Hauptseminar-AutoKeras/college_test.csv ../college_test_headerfix.csv
python3 ../genavroschema.py -n College -p de.lukas_jansen.hda.seminar -r percent_pell_grant ../college_train_headerfix.csv > ../college.avsc
python3 ../countUniqueTextValues.py ../college_train_headerfix.csv
java -cp cli/build/libs/transmogrifai-0.7.0-all.jar com.salesforce.op.cli.CLI gen --input "../college_train_headerfix.csv" --id UNITID --response percent_pell_grant  --schema ../college.avsc CollegeRegression
mv collegeregression ../

# Phishing
fixdatafile ../../../Hauptseminar-AutoKeras/phishing_train.csv ../phishing_train_headerfix.csv
fixdatafile ../../../Hauptseminar-AutoKeras/phishing_test.csv ../phishing_test_headerfix.csv
addid ../phishing_test_headerfix.csv tmp.csv
mv tmp.csv ../phishing_test_headerfix.csv
addid ../phishing_train_headerfix.csv tmp.csv
mv tmp.csv ../phishing_train_headerfix.csv
python3 ../genavroschema.py -n Phishing -p de.lukas_jansen.hda.seminar -r Result ../phishing_train_headerfix.csv > ../phishing.avsc
python3 ../countUniqueTextValues.py ../phishing_train_headerfix.csv
java -cp cli/build/libs/transmogrifai-0.7.0-all.jar com.salesforce.op.cli.CLI gen --input "../phishing_train_headerfix.csv" --response Result --schema ../phishing.avsc --id ID PhishingClassification
mv phishingclassification ../ 
```

Answers for the College file:

```
'school_name' - what kind of feature is this? [0] text [1] categorical: 0
'city' - what kind of feature is this? [0] text [1] categorical: 0
'state' - what kind of feature is this? [0] text [1] categorical: 1
'zip' - what kind of feature is this? [0] text [1] categorical: 0
'school_webpage' - what kind of feature is this? [0] text [1] categorical: 0
'predominant_degree' - what kind of feature is this? [0] text [1] categorical: 1
'highest_degree' - what kind of feature is this? [0] text [1] categorical: 1
'ownership' - what kind of feature is this? [0] text [1] categorical: 1
'region' - what kind of feature is this? [0] text [1] categorical: 1
'gender' - what kind of feature is this? [0] text [1] categorical: 1
'carnegie_basic_classification' - what kind of feature is this? [0] text [1] categorical: 1
'carnegie_undergraduate' - what kind of feature is this? [0] text [1] categorical: 1
'carnegie_size' - what kind of feature is this? [0] text [1] categorical: 1
'religious_affiliation' - what kind of feature is this? [0] text [1] categorical: 1
```

Answers for the Phishing file:

```
Cannot infer the kind of problem based on response field 'Result'. What kind of problem is this? [0] regress [1] binclass [2] multiclass: 1
'Result' - what kind of feature is this? [0] integral [1] categorical: 1
'having_IP_Address' - what kind of feature is this? [0] integral [1] categorical: 1
'URL_Length' - what kind of feature is this? [0] integral [1] categorical: 1
'Shortining_Service' - what kind of feature is this? [0] integral [1] categorical: 1
'having_At_Symbol' - what kind of feature is this? [0] integral [1] categorical: 1
'double_slash_redirecting' - what kind of feature is this? [0] integral [1] categorical: 1
'Prefix_Suffix' - what kind of feature is this? [0] integral [1] categorical: 1
'having_Sub_Domain' - what kind of feature is this? [0] integral [1] categorical: 1
'SSLfinal_State' - what kind of feature is this? [0] integral [1] categorical: 1
'Domain_registeration_length' - what kind of feature is this? [0] integral [1] categorical: 1
'Favicon' - what kind of feature is this? [0] integral [1] categorical: 1
'port' - what kind of feature is this? [0] integral [1] categorical: 1
'HTTPS_token' - what kind of feature is this? [0] integral [1] categorical: 1
'Request_URL' - what kind of feature is this? [0] integral [1] categorical: 1
'URL_of_Anchor' - what kind of feature is this? [0] integral [1] categorical: 1
'Links_in_tags' - what kind of feature is this? [0] integral [1] categorical: 1
'SFH' - what kind of feature is this? [0] integral [1] categorical: 1
'Submitting_to_email' - what kind of feature is this? [0] integral [1] categorical: 1
'Abnormal_URL' - what kind of feature is this? [0] integral [1] categorical: 1
'Redirect' - what kind of feature is this? [0] integral [1] categorical: 1
'on_mouseover' - what kind of feature is this? [0] integral [1] categorical: 1
'RightClick' - what kind of feature is this? [0] integral [1] categorical: 1
'popUpWidnow' - what kind of feature is this? [0] integral [1] categorical: 1
'Iframe' - what kind of feature is this? [0] integral [1] categorical: 1
'age_of_domain' - what kind of feature is this? [0] integral [1] categorical: 1
'DNSRecord' - what kind of feature is this? [0] integral [1] categorical: 1
'web_traffic' - what kind of feature is this? [0] integral [1] categorical: 1
'Page_Rank' - what kind of feature is this? [0] integral [1] categorical: 1
'Google_Index' - what kind of feature is this? [0] integral [1] categorical: 1
'Links_pointing_to_page' - what kind of feature is this? [0] integral [1] categorical: 1
'Statistical_report' - what kind of feature is this? [0] integral [1] categorical: 1
```

The generated project was edited, to allow for a seperate evaluator file. This reader was added for this purpose and the  

Now the two projects were combined and the Feature Extractors converted from annon. classes to "real" classes for each feature (this took forever).