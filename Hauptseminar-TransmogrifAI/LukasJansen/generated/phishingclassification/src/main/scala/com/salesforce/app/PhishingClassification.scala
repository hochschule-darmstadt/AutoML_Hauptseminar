package com.salesforce.app

import de.lukas_jansen.hda.seminar.Phishing
import com.salesforce.op._
import com.salesforce.op.readers._
import com.salesforce.op.evaluators._
import com.salesforce.op.features.types._
import com.salesforce.op.stages.impl.classification._
import com.salesforce.op.stages.impl.preparators._
import com.salesforce.op.stages.impl.regression._
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{Dataset, SparkSession}

object PhishingClassification extends OpAppWithRunner with Features {

  val randomSeed = -2095899090

  ////////////////////////////////////////////////////////////////////////////////
  // READER DEFINITIONS
  /////////////////////////////////////////////////////////////////////////////////
  val schema = Phishing.getClassSchema

  type Data = Either[RDD[Phishing], Dataset[Phishing]]

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
      extends CSVAutoReader[Phishing](
        readPath = None,
        headers = Seq.empty,
        recordNamespace = schema.getNamespace,
        recordName = schema.getName,
        key = _.getID.toString
      )
      with TrainTestSplit {
    override def read(params: OpParams)(implicit spark: SparkSession): Data = split(super.read(params))
  }

  abstract class ReaderWithNoHeaders
      extends CSVReader[Phishing](
        readPath = None,
        schema = schema.toString,
        key = _.getID.toString
      )
      with TrainTestSplit {
    override def read(params: OpParams)(implicit spark: SparkSession): Data = split(super.read(params))
  }

  class SampleReader(val isTrain: Boolean) extends ReaderWithNoHeaders

  ////////////////////////////////////////////////////////////////////////////////
  // WORKFLOW DEFINITION
  /////////////////////////////////////////////////////////////////////////////////

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

  val label =
    Seq(result)
      .transmogrify()
      .map[RealNN](_.value(0).toRealNN)

  val checkedFeatures = new SanityChecker()
    .setCheckSample(0.10)
    .setInput(label, featureVector)
    .getOutput()

  val pred = BinaryClassificationModelSelector()
    .setInput(label, checkedFeatures)
    .getOutput()

  val evaluator =
    Evaluators
      .BinaryClassification()
      .setLabelCol(label)
      .setPredictionCol(pred)

  val workflow = new OpWorkflow().setResultFeatures(pred)

  def runner(opParams: OpParams): OpWorkflowRunner =
    new OpWorkflowRunner(
      workflow = workflow,
      trainingReader = new SampleReader(isTrain = true),
      scoringReader = new SampleReader(isTrain = false),
      evaluationReader = Option(new SampleReader(isTrain = false)),
      evaluator = Option(evaluator),
      scoringEvaluator = Option(evaluator)
    )

}
