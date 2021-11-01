package com.salesforce.app

import de.lukas_jansen.hda.seminar.College
import com.salesforce.op.features.{FeatureBuilder => FB}
import com.salesforce.op.features.types._
import FeatureOps._

trait Features extends Serializable {

  val percent_pell_grant = FB
    .Real[College]
    .extract(_.getPercentPellGrant.toReal)
    .asResponse

  val school_name = FB.Text[College].extract(_.getSchoolName.toText).asPredictor

  val city = FB.Text[College].extract(_.getCity.toText).asPredictor

  val state = FB
    .PickList[College]
    .extract(asPickList(_.getState))
    .asPredictor

  val zip = FB.Text[College].extract(_.getZip.toText).asPredictor

  val school_webpage = FB.Text[College].extract(_.getSchoolWebpage.toText).asPredictor

  val latitude = FB
    .Real[College]
    .extract(_.getLatitude.toReal)
    .asPredictor

  val longitude = FB
    .Real[College]
    .extract(_.getLongitude.toReal)
    .asPredictor

  val admission_rate = FB
    .Real[College]
    .extract(_.getAdmissionRate.toReal)
    .asPredictor

  val sat_verbal_midrange = FB
    .Real[College]
    .extract(_.getSatVerbalMidrange.toReal)
    .asPredictor

  val sat_math_midrange = FB
    .Real[College]
    .extract(_.getSatMathMidrange.toReal)
    .asPredictor

  val sat_writing_midrange = FB
    .Real[College]
    .extract(_.getSatWritingMidrange.toReal)
    .asPredictor

  val act_combined_midrange = FB
    .Real[College]
    .extract(_.getActCombinedMidrange.toReal)
    .asPredictor

  val act_english_midrange = FB
    .Real[College]
    .extract(_.getActEnglishMidrange.toReal)
    .asPredictor

  val act_math_midrange = FB
    .Real[College]
    .extract(_.getActMathMidrange.toReal)
    .asPredictor

  val act_writing_midrange = FB
    .Real[College]
    .extract(_.getActWritingMidrange.toReal)
    .asPredictor

  val sat_total_average = FB
    .Real[College]
    .extract(_.getSatTotalAverage.toReal)
    .asPredictor

  val undergrad_size = FB
    .Real[College]
    .extract(_.getUndergradSize.toReal)
    .asPredictor

  val percent_white = FB
    .Real[College]
    .extract(_.getPercentWhite.toReal)
    .asPredictor

  val percent_black = FB
    .Real[College]
    .extract(_.getPercentBlack.toReal)
    .asPredictor

  val percent_hispanic = FB
    .Real[College]
    .extract(_.getPercentHispanic.toReal)
    .asPredictor

  val percent_asian = FB
    .Real[College]
    .extract(_.getPercentAsian.toReal)
    .asPredictor

  val percent_part_time = FB
    .Real[College]
    .extract(_.getPercentPartTime.toReal)
    .asPredictor

  val average_cost_academic_year = FB
    .Real[College]
    .extract(_.getAverageCostAcademicYear.toReal)
    .asPredictor

  val average_cost_program_year = FB
    .Real[College]
    .extract(_.getAverageCostProgramYear.toReal)
    .asPredictor

  val tuition_instate = FB
    .Real[College]
    .extract(_.getTuitionInstate.toReal)
    .asPredictor

  val tuition_out_of_state = FB
    .Real[College]
    .extract(_.getTuitionOutOfState.toReal)
    .asPredictor

  val spend_per_student = FB
    .Real[College]
    .extract(_.getSpendPerStudent.toReal)
    .asPredictor

  val faculty_salary = FB
    .Real[College]
    .extract(_.getFacultySalary.toReal)
    .asPredictor

  val percent_part_time_faculty = FB
    .Real[College]
    .extract(_.getPercentPartTimeFaculty.toReal)
    .asPredictor

  val completion_rate = FB
    .Real[College]
    .extract(_.getCompletionRate.toReal)
    .asPredictor

  val predominant_degree = FB
    .PickList[College]
    .extract(asPickList(_.getPredominantDegree))
    .asPredictor

  val highest_degree = FB
    .PickList[College]
    .extract(asPickList(_.getHighestDegree))
    .asPredictor

  val ownership = FB
    .PickList[College]
    .extract(asPickList(_.getOwnership))
    .asPredictor

  val region = FB
    .PickList[College]
    .extract(asPickList(_.getRegion))
    .asPredictor

  val gender = FB
    .PickList[College]
    .extract(asPickList(_.getGender))
    .asPredictor

  val carnegie_basic_classification = FB
    .PickList[College]
    .extract(asPickList(_.getCarnegieBasicClassification))
    .asPredictor

  val carnegie_undergraduate = FB
    .PickList[College]
    .extract(asPickList(_.getCarnegieUndergraduate))
    .asPredictor

  val carnegie_size = FB
    .PickList[College]
    .extract(asPickList(_.getCarnegieSize))
    .asPredictor

  val religious_affiliation = FB
    .PickList[College]
    .extract(asPickList(_.getReligiousAffiliation))
    .asPredictor

  val percent_female = FB
    .Real[College]
    .extract(_.getPercentFemale.toReal)
    .asPredictor

  val agege24 = FB
    .Real[College]
    .extract(_.getAgege24.toReal)
    .asPredictor

  val faminc = FB
    .Real[College]
    .extract(_.getFaminc.toReal)
    .asPredictor

  val mean_earnings_6_years = FB
    .Real[College]
    .extract(_.getMeanEarnings6Years.toReal)
    .asPredictor

  val median_earnings_6_years = FB
    .Real[College]
    .extract(_.getMedianEarnings6Years.toReal)
    .asPredictor

  val mean_earnings_10_years = FB
    .Real[College]
    .extract(_.getMeanEarnings10Years.toReal)
    .asPredictor

  val median_earnings_10_years = FB
    .Real[College]
    .extract(_.getMedianEarnings10Years.toReal)
    .asPredictor

}

object FeatureOps {
  def asPickList[T](f: T => Any): T => PickList = x => Option(f(x)).map(_.toString).toPickList
}
