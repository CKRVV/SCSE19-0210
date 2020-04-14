#import dateutil.parser
import mergeParameters as mp
import parsers.healthReplacement as hr
from datetime import datetime

state = "state"
victim = "victim"
country = "country"
description = "description"
location = "location"
info_source = "info_source"
records_affected = "records_affected"
industry = "industry"
year = "year"
month = "month"
day = "day"
type = "type"
No = "No"
date = "date"
isEstimate = "isEstimate"
unAuthResultReplacementDict = hr.unAuthResultReplacementDict
industryReplacementDict = hr.industryReplacementDict
actionReplacementDict = hr.actionReplacementDict
nullValue = mp.nullValue

def addEntryDate(JSONDict):															
	if year in JSONDict and JSONDict[year] != "":
		if JSONDict[year] != nullValue:
			eyear = JSONDict[year]
			emonth = JSONDict[month]
			eday = JSONDict[day]
			dt = datetime(eyear,emonth,eday)		#Dates have to be parsed to ISO date
			return 	{date : dt, year : eyear, month : emonth, day : eday, isEstimate : No}

def addVictim(JSONDict):
	vList = []
	if victim in JSONDict:
		vList.append(JSONDict[victim])
		if len(vList) >= 1:
			return vList
		else:
			return nullValue

def addIndustry(JSONDict):
	if industry in JSONDict:
		for ind,toReplaceList in industryReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[industry] == term:
					return list(ind)	

def addCountry(JSONDict):
	if country in JSONDict:
		if JSONDict[country] != "":
			return JSONDict[country]
		else:
			return nullValue

def addState(JSONDict):
	if state in JSONDict:
		if JSONDict[state] != "":
			return JSONDict[state]
		else:
			return nullValue

def addTarget(JSONDict):
	ra = addRecordsAffected(JSONDict)
	if ra != nullValue:
		return {"targeted" : nullValue, "records_affected" : ra, "assets_affected" : nullValue}
	else:
		return nullValue
	
def addRecordsAffected(JSONDict):
	if records_affected in JSONDict:
		if JSONDict[records_affected] != "\"\"":
			return JSONDict[records_affected]
		else:
			return nullValue
			
def addDescription(JSONDict):
	if description in JSONDict:
		if JSONDict[description] != "":
			return JSONDict[description]
		else:
			return nullValue

def addAction(JSONDict):
	actionList = []
	if type in JSONDict:
		for action,toReplaceList in actionReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[type] == term:
					actionList.append(action)
					actionList.append(JSONDict[type])
					return actionList			

def addUnAuthResult(JSONDict):
	unAuthList = []
	if type in JSONDict:
		for unAuth,toReplaceList in unAuthResultReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[type] == term:
					unAuthList.append(unAuth)
					return unAuthList			

def addValues(JSONDict, parseDict):
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)													#Date
	parseDict["victim"] = addVictim(JSONDict)		# this															#victim
	parseDict["industry"] = addIndustry(JSONDict)	# this															#industry
	parseDict["country"] = addCountry(JSONDict)		# this														#country
	parseDict["state"] = addState(JSONDict)			# this														#state
	#parseDict["tool"],parseDict["vulnerability"] = nullValue							#Tool Vulnerability and Action
	parseDict["action"] = addAction(JSONDict)
	parseDict["unauthorized_result"] = addUnAuthResult(JSONDict)
	parseDict["target"] = addTarget(JSONDict)		# this										#Records Affected
	parseDict["description"] = addDescription(JSONDict)				# this										#Description
	parseDict["info_source"] = nullValue														#Info Source
	parseDict["source_link"] = nullValue														#Source Link
	return parseDict