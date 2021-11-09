package de.lukas_jansen.automl

import de.lukas_jansen.automl.schema.College
import com.salesforce.op.features.{FeatureBuilder => FB}
import com.salesforce.op.features.types.{City => _, State => _, _}
import de.lukas_jansen.automl.CollegeFeatures._

trait CollegeFeatures extends Serializable {

  val percent_pell_grant = FB
    .Real[College]
    .extract(new PercentPellGrant)
    .asResponse

  val school_name = FB.Text[College].extract(new SchoolName).asPredictor

  val city = FB.Text[College].extract(new City).asPredictor

  val state = FB
    .PickList[College]
    .extract(new State)
    .asPredictor

  val zip = FB.Text[College].extract(new Zip).asPredictor

  val school_webpage = FB.Text[College].extract(new SchoolWebpage).asPredictor

  val latitude = FB
    .Real[College]
    .extract(new Latitude)
    .asPredictor

  val longitude = FB
    .Real[College]
    .extract(new Longitude)
    .asPredictor

  val admission_rate = FB
    .Real[College]
    .extract(new AdmissionRate)
    .asPredictor

  val sat_verbal_midrange = FB
    .Real[College]
    .extract(new SatVerbalMidrange)
    .asPredictor

  val sat_math_midrange = FB
    .Real[College]
    .extract(new SatMathMidrange)
    .asPredictor

  val sat_writing_midrange = FB
    .Real[College]
    .extract(new SatWritingMidrange)
    .asPredictor

  val act_combined_midrange = FB
    .Real[College]
    .extract(new ActCombinedMidrange)
    .asPredictor

  val act_english_midrange = FB
    .Real[College]
    .extract(new ActEnglishMidrange)
    .asPredictor

  val act_math_midrange = FB
    .Real[College]
    .extract(new ActMathMidrange)
    .asPredictor

  val act_writing_midrange = FB
    .Real[College]
    .extract(new ActWritingMidrange)
    .asPredictor

  val sat_total_average = FB
    .Real[College]
    .extract(new SatTotalAverage)
    .asPredictor

  val undergrad_size = FB
    .Real[College]
    .extract(new UndergradSize)
    .asPredictor

  val percent_white = FB
    .Real[College]
    .extract(new PercentWhite)
    .asPredictor

  val percent_black = FB
    .Real[College]
    .extract(new PercentBlack)
    .asPredictor

  val percent_hispanic = FB
    .Real[College]
    .extract(new PercentHispanic)
    .asPredictor

  val percent_asian = FB
    .Real[College]
    .extract(new PercentAsian)
    .asPredictor

  val percent_part_time = FB
    .Real[College]
    .extract(new PercentPartTime)
    .asPredictor

  val average_cost_academic_year = FB
    .Real[College]
    .extract(new AverageCostAcademicYear)
    .asPredictor

  val average_cost_program_year = FB
    .Real[College]
    .extract(new AverageCostProgramYear)
    .asPredictor

  val tuition_instate = FB
    .Real[College]
    .extract(new TuitionInstate)
    .asPredictor

  val tuition_out_of_state = FB
    .Real[College]
    .extract(new TuitionOutOfState)
    .asPredictor

  val spend_per_student = FB
    .Real[College]
    .extract(new SpendPerStudent)
    .asPredictor

  val faculty_salary = FB
    .Real[College]
    .extract(new FacultySalary)
    .asPredictor

  val percent_part_time_faculty = FB
    .Real[College]
    .extract(new PercentPartTimeFaculty)
    .asPredictor

  val completion_rate = FB
    .Real[College]
    .extract(new CompletionRate)
    .asPredictor

  val predominant_degree = FB
    .PickList[College]
    .extract(new PredominantDegree)
    .asPredictor

  val highest_degree = FB
    .PickList[College]
    .extract(new HighestDegree)
    .asPredictor

  val ownership = FB
    .PickList[College]
    .extract(new Ownership)
    .asPredictor

  val region = FB
    .PickList[College]
    .extract(new Region)
    .asPredictor

  val gender = FB
    .PickList[College]
    .extract(new Gender)
    .asPredictor

  val carnegie_basic_classification = FB
    .PickList[College]
    .extract(new CarnegieBasicClassification)
    .asPredictor

  val carnegie_undergraduate = FB
    .PickList[College]
    .extract(new CarnegieUndergraduate)
    .asPredictor

  val carnegie_size = FB
    .PickList[College]
    .extract(new CarnegieSize)
    .asPredictor

  val religious_affiliation = FB
    .PickList[College]
    .extract(new ReligiousAffiliation)
    .asPredictor

  val percent_female = FB
    .Real[College]
    .extract(new PercentFemale)
    .asPredictor

  val agege24 = FB
    .Real[College]
    .extract(new Agege24)
    .asPredictor

  val faminc = FB
    .Real[College]
    .extract(new Faminc)
    .asPredictor

  val mean_earnings_6_years = FB
    .Real[College]
    .extract(new MeanEarnings6Years)
    .asPredictor

  val median_earnings_6_years = FB
    .Real[College]
    .extract(new MedianEarnings6Years)
    .asPredictor

  val mean_earnings_10_years = FB
    .Real[College]
    .extract(new MeanEarnings10Years)
    .asPredictor

  val median_earnings_10_years = FB
    .Real[College]
    .extract(new MedianEarnings10Years)
    .asPredictor

}

object CollegeFeatures {
  abstract class CollegeFeatureFunc[T] extends Function[College, T] with Serializable

  class RealExtract[T <: Real](f: College => Option[Double], f1: Option[Double] => T) extends CollegeFeatureFunc[T] {
    override def apply(v1: College): T = f1(f(v1))
  }
  class PickListExtract(f: College => Option[_]) extends CollegeFeatureFunc[PickList] {
    override def apply(v1: College): PickList = f(v1).map(_.toString).toPickList
  }
  class IntExtract[T <: Integral](f: College => Option[Int], f1: Option[Int] => T) extends CollegeFeatureFunc[T] {
    override def apply(v1: College): T = f1(f(v1))
  }
  class TextExtract(f: College => String) extends CollegeFeatureFunc[Text] {
    override def apply(v1: College): Text = Option(f(v1)).toText
  }

  // Based on https://github.com/salesforce/TransmogrifAI/blob/44a5dce4b90015a71028ed28002018f5db0b0bb2/helloworld/src/main/scala/com/salesforce/hw/titanic/TitanicFeatures.scala
  class PercentPellGrant extends RealExtract(p => Option(p.getPercentPellGrant).map(_.toDouble), _.get.toRealNN)
  class SchoolName extends TextExtract(_.getSchoolName)
  class City extends TextExtract(_.getCity)
  class State extends PickListExtract(p => Option(p.getState))
  class Zip extends TextExtract(_.getZip)
  class SchoolWebpage extends TextExtract(_.getSchoolWebpage)
  class Latitude extends RealExtract(p => Option(Double.unbox(p.getLatitude)), _.toReal)
  class Longitude extends RealExtract(p => Option(Double.unbox(p.getLongitude)), _.toReal)
  class AdmissionRate extends RealExtract(p => Option(Double.unbox(p.getAdmissionRate)), _.toReal)
  class SatVerbalMidrange extends RealExtract(p => Option(Double.unbox(p.getSatVerbalMidrange)), _.toReal)
  class SatMathMidrange extends RealExtract(p => Option(Double.unbox(p.getSatMathMidrange)), _.toReal)
  class SatWritingMidrange extends RealExtract(p => Option(Double.unbox(p.getSatWritingMidrange)), _.toReal)
  class ActCombinedMidrange extends RealExtract(p => Option(Double.unbox(p.getActCombinedMidrange)), _.toReal)
  class ActEnglishMidrange extends RealExtract(p => Option(Double.unbox(p.getActEnglishMidrange)), _.toReal)
  class ActMathMidrange extends RealExtract(p => Option(Double.unbox(p.getActMathMidrange)), _.toReal)
  class ActWritingMidrange extends RealExtract(p => Option(Double.unbox(p.getActWritingMidrange)), _.toReal)
  class SatTotalAverage extends RealExtract(p => Option(Double.unbox(p.getSatTotalAverage)), _.toReal)
  class UndergradSize extends RealExtract(p => Option(Double.unbox(p.getUndergradSize)), _.toReal)
  class PercentWhite extends RealExtract(p => Option(Double.unbox(p.getPercentWhite)), _.toReal)
  class PercentBlack extends RealExtract(p => Option(Double.unbox(p.getPercentBlack)), _.toReal)
  class PercentHispanic extends RealExtract(p => Option(Double.unbox(p.getPercentHispanic)), _.toReal)
  class PercentAsian extends RealExtract(p => Option(Double.unbox(p.getPercentAsian)), _.toReal)
  class PercentPartTime extends RealExtract(p => Option(Double.unbox(p.getPercentPartTime)), _.toReal)
  class AverageCostAcademicYear extends RealExtract(p => Option(Double.unbox(p.getAverageCostAcademicYear)), _.toReal)
  class AverageCostProgramYear extends RealExtract(p => Option(Double.unbox(p.getAverageCostProgramYear)), _.toReal)
  class TuitionInstate extends RealExtract(p => Option(Double.unbox(p.getTuitionInstate)), _.toReal)
  class TuitionOutOfState extends RealExtract(p => Option(Double.unbox(p.getTuitionOutOfState)), _.toReal)
  class SpendPerStudent extends RealExtract(p => Option(Double.unbox(p.getSpendPerStudent)), _.toReal)
  class FacultySalary extends RealExtract(p => Option(Double.unbox(p.getFacultySalary)), _.toReal)
  class PercentPartTimeFaculty extends RealExtract(p => Option(Double.unbox(p.getPercentPartTimeFaculty)), _.toReal)
  class CompletionRate extends RealExtract(p => Option(Double.unbox(p.getCompletionRate)), _.toReal)
  class PredominantDegree extends PickListExtract(p => Option(p.getPredominantDegree))
  class HighestDegree extends PickListExtract(p => Option(p.getHighestDegree))
  class Ownership extends PickListExtract(p => Option(p.getOwnership))
  class Region extends PickListExtract(p => Option(p.getRegion))
  class Gender extends PickListExtract(p => Option(p.getGender))
  class CarnegieBasicClassification extends PickListExtract(p => Option(p.getCarnegieBasicClassification))
  class CarnegieUndergraduate extends PickListExtract(p => Option(p.getCarnegieUndergraduate))
  class CarnegieSize extends PickListExtract(p => Option(p.getCarnegieSize))
  class ReligiousAffiliation extends PickListExtract(p => Option(p.getReligiousAffiliation))
  class PercentFemale extends RealExtract(p => Option(Double.unbox(p.getPercentFemale)), _.toReal)
  class Agege24 extends RealExtract(p => Option(Double.unbox(p.getAgege24)), _.toReal)
  class Faminc extends RealExtract(p => Option(Double.unbox(p.getFaminc)), _.toReal)
  class MeanEarnings6Years extends RealExtract(p => Option(Double.unbox(p.getMeanEarnings6Years)), _.toReal)
  class MedianEarnings6Years extends RealExtract(p => Option(Double.unbox(p.getMedianEarnings6Years)), _.toReal)
  class MeanEarnings10Years extends RealExtract(p => Option(Double.unbox(p.getMeanEarnings10Years)), _.toReal)
  class MedianEarnings10Years extends RealExtract(p => Option(Double.unbox(p.getMedianEarnings10Years)), _.toReal)
}
