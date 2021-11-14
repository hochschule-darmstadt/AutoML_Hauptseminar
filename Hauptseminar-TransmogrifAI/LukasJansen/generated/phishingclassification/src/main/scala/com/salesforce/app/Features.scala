package com.salesforce.app

import de.lukas_jansen.hda.seminar.Phishing
import com.salesforce.op.features.{FeatureBuilder => FB}
import com.salesforce.op.features.types._
import FeatureOps._

trait Features extends Serializable {

  val result = FB
    .PickList[Phishing]
    .extract(asPickList(_.getResult))
    .asResponse

  val having_ip_address = FB
    .PickList[Phishing]
    .extract(asPickList(_.getHavingIPAddress))
    .asPredictor

  val url_length = FB
    .PickList[Phishing]
    .extract(asPickList(_.getURLLength))
    .asPredictor

  val shortining_service = FB
    .PickList[Phishing]
    .extract(asPickList(_.getShortiningService))
    .asPredictor

  val having_at_symbol = FB
    .PickList[Phishing]
    .extract(asPickList(_.getHavingAtSymbol))
    .asPredictor

  val double_slash_redirecting = FB
    .PickList[Phishing]
    .extract(asPickList(_.getDoubleSlashRedirecting))
    .asPredictor

  val prefix_suffix = FB
    .PickList[Phishing]
    .extract(asPickList(_.getPrefixSuffix))
    .asPredictor

  val having_sub_domain = FB
    .PickList[Phishing]
    .extract(asPickList(_.getHavingSubDomain))
    .asPredictor

  val sslfinal_state = FB
    .PickList[Phishing]
    .extract(asPickList(_.getSSLfinalState))
    .asPredictor

  val domain_registeration_length = FB
    .PickList[Phishing]
    .extract(asPickList(_.getDomainRegisterationLength))
    .asPredictor

  val favicon = FB
    .PickList[Phishing]
    .extract(asPickList(_.getFavicon))
    .asPredictor

  val port = FB
    .PickList[Phishing]
    .extract(asPickList(_.getPort))
    .asPredictor

  val https_token = FB
    .PickList[Phishing]
    .extract(asPickList(_.getHTTPSToken))
    .asPredictor

  val request_url = FB
    .PickList[Phishing]
    .extract(asPickList(_.getRequestURL))
    .asPredictor

  val url_of_anchor = FB
    .PickList[Phishing]
    .extract(asPickList(_.getURLOfAnchor))
    .asPredictor

  val links_in_tags = FB
    .PickList[Phishing]
    .extract(asPickList(_.getLinksInTags))
    .asPredictor

  val sfh = FB
    .PickList[Phishing]
    .extract(asPickList(_.getSFH))
    .asPredictor

  val submitting_to_email = FB
    .PickList[Phishing]
    .extract(asPickList(_.getSubmittingToEmail))
    .asPredictor

  val abnormal_url = FB
    .PickList[Phishing]
    .extract(asPickList(_.getAbnormalURL))
    .asPredictor

  val redirect = FB
    .PickList[Phishing]
    .extract(asPickList(_.getRedirect))
    .asPredictor

  val on_mouseover = FB
    .PickList[Phishing]
    .extract(asPickList(_.getOnMouseover))
    .asPredictor

  val rightclick = FB
    .PickList[Phishing]
    .extract(asPickList(_.getRightClick))
    .asPredictor

  val popupwidnow = FB
    .PickList[Phishing]
    .extract(asPickList(_.getPopUpWidnow))
    .asPredictor

  val iframe = FB
    .PickList[Phishing]
    .extract(asPickList(_.getIframe))
    .asPredictor

  val age_of_domain = FB
    .PickList[Phishing]
    .extract(asPickList(_.getAgeOfDomain))
    .asPredictor

  val dnsrecord = FB
    .PickList[Phishing]
    .extract(asPickList(_.getDNSRecord))
    .asPredictor

  val web_traffic = FB
    .PickList[Phishing]
    .extract(asPickList(_.getWebTraffic))
    .asPredictor

  val page_rank = FB
    .PickList[Phishing]
    .extract(asPickList(_.getPageRank))
    .asPredictor

  val google_index = FB
    .PickList[Phishing]
    .extract(asPickList(_.getGoogleIndex))
    .asPredictor

  val links_pointing_to_page = FB
    .PickList[Phishing]
    .extract(asPickList(_.getLinksPointingToPage))
    .asPredictor

  val statistical_report = FB
    .PickList[Phishing]
    .extract(asPickList(_.getStatisticalReport))
    .asPredictor

}

object FeatureOps {
  def asPickList[T](f: T => Any): T => PickList = x => Option(f(x)).map(_.toString).toPickList
}
