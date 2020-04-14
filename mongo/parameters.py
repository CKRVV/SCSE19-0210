import os

#programName = "mongo/"

#Declaration of file extensions
JSONEXT = ".json"
TXTEXT = ".txt"

#PyMongo Connection
DBName = "Incidents"												#Database that holds the various cyber security incidents						
atlasExamples = ["l0uqk", "scse19-0209", "nicholassyt"]
onlineExamples = ["13.250.96.171", "27017", DBName ,"nicholassyt"]

operationsList = ["Query","Store","Drop"]

#Collections defined and stored in a string list
# vcdb = "vcdb" 													#VERIS Community Database https://github.com/vz-risk/VCDB
# privacyrights = "privacyrights"									#Data Breaches from https://www.privacyrights.org/
# nvdcve = "nvdcve"													#CVEs from https://nvd.nist.gov/vuln/data-feeds#JSON_FEED
SCSE19_0209 = "SCSE19_0209"											#Merge schema from vcdb and prdb
collectionsList = [SCSE19_0209] 	 								#List of collections to be iterated	

ratesAgainstUSD = {"GBP" : 1.22, "EUR" : 1.10, "ZAR" : 0.065, "INR" : 0.014, "THB" : 0.033, "KRW" : 0.00083, "CAD" : 0.75, "AUD" : 0.67, "CZK" : 0.043}

#Query Dictionary based on schemas of the databases
queryDict = {
  "nvdcve" : {
    "Datetime Incident Submitted YYYY-MM-DDT00:00Z" : "publishedDate",
	"CVE ID" : "cve.CVE_data_meta.ID",
    "Victim" : "cve.affects.vendor.vendor_data.vendor_name",
	"Victim Product" : "cve.affects.vendor.vendor_data.product.product_data.product_name",
	"Severity" : "impact.baseMetricV3.cvssV3.baseSeverity",
	"Attack Vector" : "impact.baseMetricV3.cvssV3.attackVector",
	"Access Vector" : "impact.baseMetricV2.cvssV2.accessVector",
	"Description" : "cve.description.description_data.value",
	"URL Tag" : "cve.references.reference_data.tags",
	"Reference URL" : "cve.references.reference_data.url"
  },
  "privacyrights" : {
	"Date submitted" : "date",
    "Victim" : "victim",
	"Organisation Type" : "org_type",
	"Location" : "location",
	"Attack Vector": "breach_type",
	"Records Affected": "records_affected",
	"Description" : "description",
	"Information Source" : "info_source",
	"Source URL" : "source_link"
  },
  "vcdb" : {
    "Year of Incident" : "timeline.incident.year",
	"Month of Incident" : "timeline.incident.month",
	"Datetime Incident Created YYYY-MM-DDT00:00Z" : "plus.created",
	"Incident ID" : "incident_id",
	"Targeted" : "targeted",
	"Confidence" : "confidence",
	"Description" : "summary",
	"Main Victim" : "victim.victim_id",
	"Secondary Victim" : "victim.secondary.victim_id",
	"Victim Country" : "victim.country",
	"Victim US State" : "victim.state",
	"Victim Data" : "attribute.confidentiality.data_victim",
	"Victim Records Type" : "attribute.confidentiality.data.variety",
	"Victim Employee Count" : "victim.employee_count",
	"Victim Number Of Locations Affected" : "victim.locations_affected",
	"Victim Revenue" : "victim.revenue.amount",
	"Currency" : "impact.iso_currency_code",
	"Monetary Loss" : "impact.loss.amount",
	"Monetary Loss Rating" : "impact.loss.rating",
	"Monetary Loss Variety" : "impact.loss.variety",
	"Overall Loss" : "impact.overall_amount",
	"Overall Loss Rating" : "impact.overall_rating",
	"Environmental Impact" : "action.environmental.variety",
	"Error Variety" : "action.error.variety",
	"Error Vector" : "action.error.vector",
	"Hacking CVE ID" : "action.hacking.cve",
	"Hacking Variety" : "action.hacking.variety",
	"Hacking Vector" : "action.hacking.vector",
	"Hacking Result" : "action.hacking.result",
	"Malware CVE ID" : "action.malware.cve",
	"Malware Name" : "action.malware.name",
	"Malware Result" : "action.malware.result",
	"Malware Variety" : "action.malware.variety",
	"Malware Vector" : "action.malware.vector",
	"Misuse Result" : "action.misuse.result",
	"Misuse Variety" : "action.misuse.variety",
	"Misuse Vector" : "action.misuse.vector",
	"Physical Result" : "action.physical.result",
	"Physical Variety" : "action.physical.variety",
	"Physical Vector" : "action.physical.vector",
	"Social Result" : "action.social.result",
	"Social Target" : "action.social.target",
	"Social Variety" : "action.social.variety",
	"Social Vector" : "action.social.vector",
	"External Actor Countries" : "actor.external.country",
	"External Actor Motive" : "actor.external.motive",
	"External Actor Name" : "actor.external.name",
	"External Actor Variety" : "actor.external.variety",
	"Internal Actor Job Change" : "actor.internal.job_change",
	"Internal Actor Motive" : "actor.internal.motive",
	"Internal Actor Variety" : "actor.internal.variety",
	"Partner Actor Country" : "actor.partner.country",
	"Partner Actor Motive" : "actor.partner.motive",
	"Partner Actor Name" : "actor.partner.name",
	"Lost Assets Amount" : "asset.assets.amount",
	"Assets Variety" : "asset.assets.variety",
	"Cloud Asset" : "asset.cloud",
	"Assets Country" : "asset.country",
	"Total Assets" : "asset.total_amount",
	"Amount Data Loss" : "attribute.confidentiality.data.amount",
	"Data Variety" : "attribute.confidentiality.data.variety",
	"Data Disclosed" : "attribute.confidentiality.data_disclosure",
	"Total Amount Data Loss" : "attribute.confidentiality.data_total",
	"Data Loss Victim" : "attribute.confidentiality.data_victim",
	"Data Loss State" : "attribute.confidentiality.state",
	"Integrity Variety" : "attribute.integrity.variety",
	"External Discovery Method Variety" : "discovery_method.external.variety",
	"Internal Discovery Method Variety" : "discovery_method.internal.variety",
	"Partner Discovery Method Variety" : "discovery_method.partner.variety",
	"OS Affected" : "plus.asset_os",
	"Information Source" : "source_id",
	"URL" : "reference"
  }
}						