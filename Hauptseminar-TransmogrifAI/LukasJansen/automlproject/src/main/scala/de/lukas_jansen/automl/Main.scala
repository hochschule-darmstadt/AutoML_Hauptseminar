package de.lukas_jansen.automl

import com.salesforce.op.evaluators.{EvaluationMetrics, Evaluators, OpRegressionEvaluator, OpRegressionEvaluatorBase, RegressionMetrics}
import de.lukas_jansen.automl.schema.Phishing
import de.lukas_jansen.automl.schema.College
import com.salesforce.op.{features, _}
import com.salesforce.op.features.{FeatureBuilder, FeatureLike}
import com.salesforce.op.features.types.{City => _, State => _, _}
import com.salesforce.op.readers.{CSVAutoReader, DataReaders}
import com.salesforce.op.stages.impl.classification._
import com.salesforce.op.stages.impl.preparators.SanityChecker
import com.salesforce.op.stages.impl.regression.RegressionModelSelector
import com.salesforce.op.stages.impl.regression.{RegressionModelsToTry => RMTT}
import com.salesforce.op.stages.impl.classification.{BinaryClassificationModelsToTry => BMTT}
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

import scala.concurrent.duration.Duration
import scala.util.Failure

object Main extends Features{

  val college_schema = College.getClassSchema
  def getCollegeWorkflow(datapath: Option[String] ): (OpWorkflow, FeatureLike[RealNN], FeatureLike[Prediction]) ={
    val reader = new CSVAutoReader[College](
      readPath = datapath,
      headers = Seq.empty,
      recordNamespace = college_schema.getNamespace,
      recordName = college_schema.getName,
      key = _.getUNITID.toString
    )
    val response =
      Seq(percent_pell_grant)
        .transmogrify()
        .map[RealNN](_.value(0).toRealNN)
    val featureVector =
      Seq(
        school_name,
        city,
        state,
        zip,
        school_webpage,
        latitude,
        longitude,
        admission_rate,
        sat_verbal_midrange,
        sat_math_midrange,
        sat_writing_midrange,
        act_combined_midrange,
        act_english_midrange,
        act_math_midrange,
        act_writing_midrange,
        sat_total_average,
        undergrad_size,
        percent_white,
        percent_black,
        percent_hispanic,
        percent_asian,
        percent_part_time,
        average_cost_academic_year,
        average_cost_program_year,
        tuition_instate,
        tuition_out_of_state,
        spend_per_student,
        faculty_salary,
        percent_part_time_faculty,
        completion_rate,
        predominant_degree,
        highest_degree,
        ownership,
        region,
        gender,
        carnegie_basic_classification,
        carnegie_undergraduate,
        carnegie_size,
        religious_affiliation,
        percent_female,
        agege24,
        faminc,
        mean_earnings_6_years,
        median_earnings_6_years,
        mean_earnings_10_years,
        median_earnings_10_years
      ).transmogrify()
    val checkedFeatures = new SanityChecker()
      .setCheckSample(1.0)
      .setRemoveBadFeatures(true)
      .setInput(response, featureVector)
      .getOutput()
    val prediction = RegressionModelSelector
      .withCrossValidation(numFolds=5,
      //broken, just crashes after this time :(
        maxWait = Duration(10L, "hours"),
        modelTypesToUse = Seq(RMTT.OpLinearRegression, RMTT.OpRandomForestRegressor, RMTT.OpGBTRegressor, RMTT.OpDecisionTreeRegressor))
      .setInput(response, checkedFeatures).getOutput()
    /* https://github.com/salesforce/TransmogrifAI/blob/44a5dce4b90015a71028ed28002018f5db0b0bb2/docs/developer-guide/index.md#fitted-workflows */
     val wf = new OpWorkflow().setResultFeatures(prediction).setReader(reader)
    (wf, response, prediction)
  }


  val phishing_schema = Phishing.getClassSchema
  def getPhishingWorkflow(datapath: Option[String] ): (OpWorkflow, FeatureLike[RealNN], FeatureLike[Prediction]) ={
    val reader = new CSVAutoReader[Phishing](
      readPath = datapath,
      headers = Seq.empty,
      recordNamespace = phishing_schema.getNamespace,
      // Another bug in the genrator, this was missing for binary classification:
      recordName = phishing_schema.getName,
      key = _.getID.toString
    )
    val response = Seq(result)
      .transmogrify()
      .map[RealNN](_.value(0).toRealNN)
    val featureVector =
      Seq(
        having_ip_address,
        url_length,
        shortining_service,
        having_at_symbol,
        double_slash_redirecting,
        prefix_suffix,
        having_sub_domain,
        sslfinal_state,
        domain_registeration_length,
        favicon,
        port,
        https_token,
        request_url,
        url_of_anchor,
        links_in_tags,
        sfh,
        submitting_to_email,
        abnormal_url,
        redirect,
        on_mouseover,
        rightclick,
        popupwidnow,
        iframe,
        age_of_domain,
        dnsrecord,
        web_traffic,
        page_rank,
        google_index,
        links_pointing_to_page,
        statistical_report
      ).transmogrify()
    val checkedFeatures = new SanityChecker()
      .setCheckSample(1.0)
      .setRemoveBadFeatures(true)
      .setInput(response, featureVector)
      .getOutput()

    val prediction = BinaryClassificationModelSelector
      .withCrossValidation(numFolds=5,
        maxWait = Duration(10L, "hours"),
        modelTypesToUse = Seq(BMTT.OpLogisticRegression, BMTT.OpRandomForestClassifier, BMTT.OpGBTClassifier, BMTT.OpDecisionTreeClassifier, BMTT.OpLinearSVC, BMTT.OpNaiveBayes))
      .setInput(response, checkedFeatures).getOutput()
    /* https://github.com/salesforce/TransmogrifAI/blob/44a5dce4b90015a71028ed28002018f5db0b0bb2/docs/developer-guide/index.md#fitted-workflows */
    val wf = new OpWorkflow().setResultFeatures(prediction).setReader(reader)
    (wf, response, prediction)
  }


  def trainModel(implicit spark: SparkSession, wf: OpWorkflow, prediction: FeatureLike[Prediction]): OpWorkflowModel ={
    import spark.implicits._
    val model = wf.train()
    println(s"Model summary:\n${model.summaryPretty()}")
    val modelInsights = model.modelInsights(prediction)
    val modelFeatures = modelInsights.features.flatMap( feature => feature.derivedFeatures)
    val featureContributions = modelFeatures.map( feature => (feature.derivedFeatureName,
      feature.contribution.map( contribution => math.abs(contribution))
        .foldLeft(0.0) { (max, contribution) => math.max(max, contribution)}))
    val sortedContributions = featureContributions.sortBy( contribution => -contribution._2)
    val topNum = math.min(20, sortedContributions.size)
    println(s"Top $topNum feature contributions:")
    sortedContributions.take(topNum).foreach( featureInfo => println(s"${featureInfo._1}: ${featureInfo._2}"))
    model
  }

    def evaluateRegressionModel(implicit spark: SparkSession, wf: OpWorkflow, path:String,response: FeatureLike[RealNN], prediction:FeatureLike[Prediction]): Unit ={
      val evaluator = Evaluators.Regression().setLabelCol(response).setPredictionCol(prediction)
      // the reader is set to the test data during wf construction
      val model = wf.loadModel(path).setReader(wf.getReader())
      val (scores, metrics) = model.scoreAndEvaluate(evaluator = evaluator)
      println("Metrics:\n" + metrics)
    }

  def evaluateBinaryClassificationModel(implicit spark: SparkSession, wf: OpWorkflow, path:String,response: FeatureLike[RealNN], prediction:FeatureLike[Prediction]): Unit ={
    val evaluator = Evaluators.BinaryClassification().setLabelCol(response).setPredictionCol(prediction)
    val model = wf.loadModel(path).setReader(wf.getReader())
    val (scores, metrics) = model.scoreAndEvaluate(evaluator = evaluator)
    println("Metrics:\n" + metrics)
  }

  def main(args: Array[String]): Unit = {
    println("Starting")
    implicit val spark = SparkSession.builder.config(new SparkConf()).getOrCreate()
    val problem = args(0)
    val datapath = args(1)
    val modelpath = args(2)
    if(problem == "train_college") {
      println("Training College...")
      val (wf, response, prediction) = getCollegeWorkflow(Some(datapath))
      val model = trainModel(spark, wf, prediction)
      model.save(modelpath)
    }else if(problem == "eval_college") {
      println("Evaluating College...")
      val (wf, response, prediction) = getCollegeWorkflow(Some(datapath))
      evaluateRegressionModel(spark, wf, modelpath, response, prediction)
    }else if(problem == "train_phishing") {
      println("Training Phishing...")
      val (wf, response, prediction) = getPhishingWorkflow(Some(datapath))
      val model = trainModel(spark, wf, prediction)
      model.save(modelpath)
    }else if(problem == "eval_phishing") {
      println("Evaluating Phishing...")
      val (wf, response, prediction) = getPhishingWorkflow(Some(datapath))
      evaluateBinaryClassificationModel(spark, wf, modelpath, response, prediction)
    }else {
      Failure(new RuntimeException("Invalid Problem!"))
    }
  }

}