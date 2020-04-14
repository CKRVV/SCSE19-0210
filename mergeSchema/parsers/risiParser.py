import mergeParameters as mp
import parsers.risiReplacement as rr
from datetime import datetime

country = "country"
description = "description"
source_link = "source_link"
industry = "industry"
No = "No"
date = "date"
year = "year"
month = "month"
day = "day"
isEstimate = "isEstimate"
industryReplacementDict = rr.industryReplacementDict
nullValue = mp.nullValue

def addEntryDate(JSONDict):															
	if year in JSONDict and JSONDict[year] != "":
		if JSONDict[year] != nullValue:
			eyear = JSONDict[year]
			emonth = 1
			eday = 1
			dt = datetime(eyear,emonth,eday)		#Dates have to be parsed to ISO date
			return 	{date : dt, year : eyear, month : emonth, day : eday, isEstimate : No}

def addDescription(JSONDict):
	if description in JSONDict:
		if JSONDict[description] != "":
			return JSONDict[description]
		else:
			return nullValue

def addCountry(JSONDict):
	if country in JSONDict:
		if JSONDict[country] != "":
			return JSONDict[country]
		else:
			return nullValue

def addIndustry(JSONDict):
	if industry in JSONDict:
		for ind,toReplaceList in industryReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[industry] == term:
					return list(ind)	

def addSourceLink(JSONDict):
	if source_link in JSONDict:
		if JSONDict[source_link] != "":
			return JSONDict[source_link]
		else:
			return nullValue

def addValues(JSONDict, parseDict):
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)													#Date
	parseDict["victim"] = nullValue																	#victim
	parseDict["industry"] = addIndustry(JSONDict)																#industry
	parseDict["country"] = addCountry(JSONDict)															#country
	parseDict["state"] = nullValue																#state
	#parseDict["tool"],parseDict["vulnerability"],parseDict["action"] = nullValue							#Tool Vulnerability and Action
	parseDict["description"] = addDescription(JSONDict)														#Description
	parseDict["info_source"] = nullValue														#Info Source
	parseDict["source_link"] = addSourceLink(JSONDict)														#Source Link
	return parseDict