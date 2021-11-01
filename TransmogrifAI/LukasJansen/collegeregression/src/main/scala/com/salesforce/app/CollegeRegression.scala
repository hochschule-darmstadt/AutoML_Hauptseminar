package com.salesforce.app

import de.lukas_jansen.hda.seminar.College
import com.salesforce.op._
import com.salesforce.op.readers._
import com.salesforce.op.evaluators._
import com.salesforce.op.features.types._
import com.salesforce.op.stages.impl.classification._
import com.salesforce.op.stages.impl.preparators._
import com.salesforce.op.stages.impl.regression._
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{Dataset, SparkSession}

object CollegeRegression extends OpAppWithRunner with Features {

  val randomSeed = -1698841601

  ////////////////////////////////////////////////////////////////////////////////
  // READER DEFINITIONS
  /////////////////////////////////////////////////////////////////////////////////
  val schema = College.getClassSchema

  type Data = Either[RDD[College], Dataset[College]]

  trait TrainTestSplit {
    def isTrain: Boolean

    protected def split(data: Data, weights: Array[Double] = Array(0.9, 0.1)): Data = data match {
      case Left(rdd) =>
        val Array(train, test) = rdd.randomSplit(weights, randomSeed)
        Left(if (isTrain) train else test)
      case Right(ds) =>
        val Array(train, test) = ds.randomSplit(weights, randomSeed)
        Right(if (isTrain) train else test)
    }
  }

  abstract class ReaderWithHeaders
      extends CSVAutoReader[College](
        readPath = None,
        headers = Seq.empty,
        recordNamespace = schema.getNamespace,
        recordName = schema.getName,
        key = _.getUNITID.toString
      )
      with TrainTestSplit {
    override def read(params: OpParams)(implicit spark: SparkSession): Data = split(super.read(params))
  }

  abstract class ReaderWithNoHeaders
      extends CSVReader[College](
        readPath = None,
        schema = schema.toString,
        key = _.getUNITID.toString
      )
      with TrainTestSplit {
    override def read(params: OpParams)(implicit spark: SparkSession): Data = split(super.read(params))
  }

  class SampleReader(val isTrain: Boolean) extends ReaderWithHeaders

    class ManualReader(envvar: String)
      extends CSVAutoReader[College](
        readPath = Some(sys.env(envvar)),
        headers = Seq.empty,
        recordNamespace = schema.getNamespace,
        recordName = schema.getName,
        key = _.getUNITID.toString
      ){
    override def read(params: OpParams)(implicit spark: SparkSession): Data = super.read(params)
  }

  ////////////////////////////////////////////////////////////////////////////////
  // WORKFLOW DEFINITION
  /////////////////////////////////////////////////////////////////////////////////

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

  val label =
    Seq(percent_pell_grant)
      .transmogrify()
      .map[RealNN](_.value(0).toRealNN)

  val checkedFeatures = new SanityChecker()
    .setCheckSample(0.10)
    .setInput(label, featureVector)
    .getOutput()

  val pred = RegressionModelSelector()
    .setInput(label, checkedFeatures)
    .getOutput()

  val evaluator =
    Evaluators
      .Regression()
      .setLabelCol(label)
      .setPredictionCol(pred)

  val workflow = new OpWorkflow().setResultFeatures(pred)

  def runner(opParams: OpParams): OpWorkflowRunner =
    new OpWorkflowRunner(
      workflow = workflow,
      trainingReader = new SampleReader(isTrain = true),
      scoringReader = new SampleReader(isTrain = false),
      evaluationReader = Option(new ManualReader("EVALFILE")),
      evaluator = Option(evaluator),
      scoringEvaluator = Option(evaluator)
    )

}
