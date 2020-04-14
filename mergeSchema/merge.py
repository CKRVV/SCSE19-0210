#Imports
import json
import os
from datetime import datetime
import mergeParameters as mp
import parsers.parsingFunctions as pf

#Constants
JSONToMergeFolder = mp.JSONToMergeFolder
prdbFileName = mp.prdbFileName
vcdbFileName = mp.vcdbFileName
healthFileName = mp.healthFileName
risiFileName = mp.risiFileName
wikiFileName = mp.wikiFileName
nvdcve = mp.nvdcveType

JSONMergedFolder = mp.JSONMergedFolder
JSONMergedFileName = mp.JSONMergedFileName

def parsingFunctions(json_data,jsonFileName):														#Add new parsing functions to this function
	dbType = None
	if jsonFileName == prdbFileName:																#Parsing the privacyrights JSON file
		dbType = mp.prdbType
	elif jsonFileName == vcdbFileName:																		#Parsing the vcdb JSON file
		dbType = mp.vcdbType
	elif nvdcve in jsonFileName:
		dbType = nvdcve
	elif jsonFileName == healthFileName:
		dbType = mp.healthType
	elif jsonFileName == risiFileName:
		dbType = mp.risiType
	elif jsonFileName == wikiFileName:
		dbType = mp.wikiType
	if dbType != None:
		return pf.parseJSON(json_data,dbType)

#########################################################################################The Decoder Classes are defined here###########################################################################################################
class Decoder(json.JSONDecoder):																	#Decoder to parse strings with numbers into int values
    def decode(self, s):
        result = super().decode(s)  
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o
			
class dateTimeEncoder(json.JSONEncoder):															#Decoder to print datetime as a string
	def default(self, obj):
		if isinstance (obj, datetime): 
			return str(obj.isoformat())
		elif isinstance (obj, datetime.date):
			return str(obj.isoformat())
		return json.JSONEncoder.default(self, obj)
#########################################################################################The Encoder Classes are defined here###########################################################################################################

#########################################################################################The File Merging Code is defined here###########################################################################################################
def getJSONFiles():
	JSONFiles = [os.path.join(r,file) for r,d,f in os.walk(JSONToMergeFolder) for file in f]		#Store all files in specified directory to a list
	return JSONFiles

def openFilesAndParseData(JSONFiles):
	jsonList = []
	i = 0
	while i != len(JSONFiles):
		print("Merging " + JSONFiles[i].split("/")[-1]	 + " now")
		with open(JSONFiles[i], encoding='utf-8') as data:											#File must be opened with utf-8 encoding as there are symbols errors without it
			json_data = json.load(data,cls=Decoder)													#Call json.load to load json data. The decoder class parses strings with numbers into int values.
		data.close()
		json_data = parsingFunctions(json_data,JSONFiles[i])										#Parse JSON data by adding or removing fields
		if json_data != None:
			for line in json_data:
				jsonList.append(json.dumps(line,cls=dateTimeEncoder))									#To allow for the printing of double quotes and datetime
		appendToJSONFile(jsonList,i,len(JSONFiles))
		jsonList = []
		i+=1

def appendToJSONFile(json_data,currentFileCount,numOfFiles):
	lineCount = 0
	with open(JSONMergedFileName, 'a', encoding='utf-8') as f:										#'a' is used to append queries to the same json file, encoding required to print VERIS queries
		for line in json_data:
			print (line, file = f,end = '')
			if currentFileCount == numOfFiles-1 and lineCount == len(json_data)-1:					#If it is the last entry in the json merging do not append a comma
				continue
			else:
				print (",", file = f)																#Print a comma for each line
			lineCount += 1
	f.close()

def clearFileContents(fileName):																	#Function to clear file contents
	open(fileName, 'w').close()

def prepareFile(fileName):
	with open(fileName, 'a', encoding='utf-8') as f:	
		print('[', file = f)																		#Append a '['
	f.close()
	
def appendFileEnd(fileName):
	with open(fileName, 'a', encoding='utf-8') as f:	
		print(']', file = f)																		#Append a ']'
	f.close()
	
def doMerge():
	print("Start merging")
	JSONFiles = getJSONFiles()
	clearFileContents(JSONMergedFileName)
	prepareFile(JSONMergedFileName)
	openFilesAndParseData(JSONFiles)
	appendFileEnd(JSONMergedFileName)
	print("Merge Completed")
	#os.startfile(os.path.realpath(JSONMergedFolder))
#########################################################################################The File Merging Code is defined here###########################################################################################################