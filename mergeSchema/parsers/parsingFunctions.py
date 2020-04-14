import mergeParameters as mp
import parsers.prdbParser as prp
import parsers.vcdbParser as vcp
import parsers.nvdcveParser as nvdcve
import parsers.healthParser as hp
import parsers.risiParser as rp
import parsers.wikiParser as wp

def getParsedJSONDict(JSONDict,parseDict,dbType):								
	parseDict["type"] = dbType 
	if dbType == mp.prdbType:
		return prp.addValues(JSONDict,parseDict)
	elif dbType == mp.vcdbType:
		return vcp.addValues(JSONDict,parseDict)
	elif dbType == mp.nvdcveType:
		return nvdcve.addValues(JSONDict,parseDict)
	elif dbType == mp.healthType:
		return hp.addValues(JSONDict,parseDict)
	elif dbType == mp.risiType:
		return rp.addValues(JSONDict,parseDict)
	elif dbType == mp.wikiType:
		return wp.addValues(JSONDict,parseDict)

def parseJSON(json_data,dbType):											#json_data is list of dictionaries																					
	#Declarations of empty Lists and Dicts
	parsedJSON = []
	parseAgainst = mp.fieldsToAdd
	
	for JSONDict in json_data:												#For each Dict in json_data	
		parseDict = parseAgainst.copy()										#Copy is required as an assignment is just a pointer to the original dict
		parsedJSONDict = getParsedJSONDict(JSONDict,parseDict,dbType)		#Retrieve the relevant values from the JSON dict and store to the new Dict
		if list(parsedJSONDict.values())[4] != mp.nullValue:				#If there is no date, do not append
			parsedJSON.append(parsedJSONDict)																
	return parsedJSON														#Return the parsed json file