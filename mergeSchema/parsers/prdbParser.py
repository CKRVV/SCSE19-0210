import dateutil.parser
import mergeParameters as mp
import parsers.prdbReplacement as pr
import re

nullValue = mp.nullValue
prdbType = mp.prdbType
No = "No"
date = "date"
victim = "victim"
org_type = "org_type"
location = "location"
variety = "variety"
records_affected = "records_affected"
description = "description"
info_source = "info_source"
source_link = "source_link"
country = "country"
US = "US"
paper = "paper"
date = "date"
day = "day"
month = "month"
year = "year"
isEstimate = "isEstimate"

vectorList = pr.vectorList
varietyDict = pr.varietyDict
varietyList = pr.varietyList		
toolReplacementDict = pr.toolReplacementDict
vulnerabilityReplacementDict = pr.vulnerabilityReplacementDict
actionReplacementDict = pr.actionReplacementDict		
TVARemoveList = pr.TVARemoveList
#Check if need paper data breaches
# def checkDescriptionPaper(JSONDict):														
	# if description in JSONDict:
		# if re.search(paper,JSONDict[description],re.IGNORECASE): 															#prdb has data breach incidents from the mishandling of paper documents so they are removed
				# return False
		# else:
			# return True

def parseList(elist):																#Clean lists to remove unknown other and na
	if isinstance(elist,list): 
		elist = list(dict.fromkeys(elist))											#Remove duplicates
		while nullValue in elist:
			elist.remove(nullValue)
		if len(elist) >= 1:
			return elist
		else:
			return nullValue
	else:
		return nullValue	

def addEntryDate(JSONDict):															
	if date in JSONDict:		
		dt = dateutil.parser.parse(JSONDict[date])															#Dates have to be parsed to ISO date
		return 	{date : dt, year : dt.year, month : dt.month, day : dt.day, isEstimate : No}

def addVictim(JSONDict):
	vList = []
	if victim in JSONDict:
		vList.append(JSONDict[victim])
		if len(vList) >= 1:
			return vList
		else:
			return nullValue
		
def addIndustry(JSONDict):
	if org_type in JSONDict:
		return JSONDict[org_type]
		
def addCountry(JSONDict):																				#prdb incidents are based in US
	if country in JSONDict:
		return US

def addState(JSONDict):
	if location in JSONDict:
		return JSONDict[location]

def getVector(JSONDict):
	vectors = []
	if description in JSONDict:
		for substr in vectorList:
			if re.search(substr,JSONDict[description],re.IGNORECASE): 
				vectors.append(substr)
	return vectors
		
def getVariety(JSONDict):																				#Translation of the variety short form to the long form
	varietys = []
	if variety in JSONDict:
		for vary in varietyDict:
			if JSONDict[variety] == vary :
				varietys.append(varietyDict[vary])
	if description in JSONDict:
		for substr in varietyList:
			if re.search(substr,JSONDict[description],re.IGNORECASE): 
				varietys.append(substr)
	return varietys 

def addTVA(JSONDict):		#attribute.integrity.variety
	fullList = []
	fullList.extend(getVariety(JSONDict))
	fullList.extend(getVector(JSONDict))
	return parseList(parseToolList(fullList)),parseList(parseVulnerabilityList(fullList)),parseList(parseActionList(fullList))

def parseToolList(fullList):
	toolList = []
	for tool,toReplaceList in toolReplacementDict.items():
		for term in toReplaceList:
			for t in fullList:
				if t == term: 
					toolList.append(tool)
					toolList.append(term)	
	for elem in TVARemoveList:
		while elem in toolList:
			toolList.remove(elem)
	return toolList

def parseVulnerabilityList(fullList):
	vulnerabilityList = []
	for vulnerability,toReplaceList in vulnerabilityReplacementDict.items():
		for term in toReplaceList:
			for vuln in fullList:
				if vuln == term: 
					vulnerabilityList.append(vulnerability)
					vulnerabilityList.append(term)	
	for elem in TVARemoveList:
		while elem in vulnerabilityList:
			vulnerabilityList.remove(elem)
	return vulnerabilityList
	
def parseActionList(fullList):
	actionList = []
	for action,toReplaceList in actionReplacementDict.items():
		for term in toReplaceList:
			for act in fullList:
				if act == term: 
					actionList.append(action)
					actionList.append(term)	
	for elem in TVARemoveList:
		while elem in actionList:
			actionList.remove(elem)
	return actionList	
				
def addRecordsAffected(JSONDict):
	if records_affected in JSONDict:
		ra = JSONDict[records_affected]
		if ra >= 10401504580:
			return nullValue
		else:
			return ra

def addTarget(JSONDict):
	ra = addRecordsAffected(JSONDict)
	return {"targeted" : nullValue, "records_affected" : ra, "assets_affected" : nullValue}
		
def addDescription(JSONDict):
	if description in JSONDict:
		return JSONDict[description]

def addInfoSource(JSONDict):
	if info_source in JSONDict:
		return JSONDict[info_source]
		
def addSourceLink(JSONDict):
	if source_link in JSONDict and JSONDict[source_link] != "":
		return JSONDict[source_link]

def addValues(JSONDict,parseDict):
	#parseDict["type"] = prdb																							#Always type 
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)															#Date
	parseDict["victim"] = addVictim(JSONDict)																	#victim
	parseDict["industry"] = addIndustry(JSONDict)																#industry
	parseDict["country"] = addCountry(JSONDict)																#country
	parseDict["state"] = addState(JSONDict)																	#state
	parseDict["tool"],parseDict["vulnerability"],parseDict["action"] = addTVA(JSONDict)							#Tool Vulnerability and Action
	parseDict["target"] = addTarget(JSONDict)												#Records Affected
	parseDict["description"] = addDescription(JSONDict)														#Description
	parseDict["info_source"] = addInfoSource(JSONDict)														#Info Source
	parseDict["source_link"] = addSourceLink(JSONDict)														#Source Link
	return parseDict