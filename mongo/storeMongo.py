import json
import os
import pymongo 
import dateutil.parser

JSONFileFolder = os.path.join(os.path.dirname(__file__), "jsons/")
dateList = ["incident_date","resolution_date","notification_date","entry_date"]

class Decoder(json.JSONDecoder):																		#Decoder to parse strings with numbers into int values
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

def parseDatesToISODate(json_data):																		#Dates have to be parsed to ISO date
	for line in json_data:
		for dateField in dateList:
			if line[dateField] != None:
				if line[dateField]["date"] != None:
					line[dateField]["date"] = dateutil.parser.parse(line[dateField]["date"])

def parsingFunctions(json_data,col):
	parseDatesToISODate(json_data)

def openFileAndStore(fileName,collection,col):
	try:
		with open(fileName, encoding='utf-8') as data:													#File must be opened with utf-8 encoding as there are symbols errors without it
			json_data = json.load(data,cls=Decoder)														#Call json.load to load json data. The decoder class parses strings with numbers into int values.
		data.close()
		parsingFunctions(json_data,col)
		result = collection.insert_many(json_data)														#Call pymongo insert_many to insert multiple documents
	except Exception as e: 
		print(e)
		quit()

def getJSONFiles():
	JSONFiles = [os.path.join(r,file) for r,d,f in os.walk(JSONFileFolder) for file in f]				#All the files in the json folder
	return JSONFiles 

def doStore(db,connectionType):
	JSONFiles = getJSONFiles()
	for fileName in JSONFiles :																			#Loop for all the collections in collectionsList
		col = fileName.split("/")[-1].split(".")[0]															
		print("Storing " + col + " to " + connectionType)												#Print current collection being stored
		collection = db[col]																			#Store db[col] as collection variable
		openFileAndStore(fileName,collection,col)														#Pass the file name and collection to store function
		print("Stored " + col)																			#Print stored collection