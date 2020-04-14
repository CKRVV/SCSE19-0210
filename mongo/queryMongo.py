import json
import ast
import pymongo 
import parameters
import easygui as eg
import re
from datetime import datetime
import os
import dateutil.parser

#Declarations
schemaFilesFolder  = os.path.join(os.path.dirname(__file__), "schemas/")						#Modify this if the folder of the various schemas is modified
SCHEMAEXT = "_schema" + parameters.TXTEXT 														#Modify this if the naming convention of the various schemas is modified
queryTypeFile = schemaFilesFolder + "query_type" + parameters.TXTEXT							#Modify this if the name of the query type txt file is modified

resultsFilesFolder  = os.path.join(os.path.dirname(__file__), "results/")						#Modify this if the folder for the results is modified
findFileName = resultsFilesFolder + "find_results" + parameters.JSONEXT 						#Modify this to change the name of the query results file
distinctFileName = resultsFilesFolder + "distinct_results" + parameters.TXTEXT					#Modify this to change the name of the distinct results txt file
aggregateFileName = resultsFilesFolder + "aggregate_results" + parameters.JSONEXT				#Modify this to change the name of the aggregate results file
descriptionFileName = resultsFilesFolder+ "count" + parameters.TXTEXT							#Modify this to change the name of the descriptions file

title = "Query"																					#Modify this to change the header text of the GUI	
mongoOperations = {0 : "Find", 1 : "Distinct", 2 : "Aggregate"}									#Modify this to add more MongoDB operations
queryRegex = "^(\{|\[)(\s|.)+(\}|\])$"															#Matches a query 
isodateRegex = "\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)"		#Match a isodate
idField = "_id"

#########################################################################################The GUI code is defined here###################################################################################################################

def askTimesToQuery():														#Prompts the user to enter the number of times queries to be made
	msg = "Enter the number of times to query : "
	example = "1"
	timesToQuery = eg.integerbox(msg,title,example)
	if timesToQuery is None or timesToQuery <= 0:
		quit() 
	return timesToQuery

def askCollectionToQuery():													#Prompts the user to choose the collection to query
	msg = "Choose the collection to query : "
	choices = parameters.collectionsList
	colToQuery = eg.choicebox(msg,title,choices)
	if colToQuery is None:
		quit() 
	return colToQuery

def askSelectOrType():
	msg = "Please choose to either do a selection or type the query.\nA selection will display available columns to query.\nA typed query supports logical operators."		
	selectOrType = eg.boolbox(msg,title,["Select","Type"])					#Prompts the user to choose Select or Type. A bool value is returned.
	if selectOrType is None:
		quit() 
	return selectOrType

# def askSimpleOrAdvanced():
	# msg = "Please choose to either do a simple or advanced query : "		#Prompts the user to choose Simple or Advanced. A bool value is returned.
	# simpleOrAdvanced = eg.boolbox(msg,title,["Simple","Advanced"])
	# if simpleOrAdvanced is None:
		# quit()
	# return simpleOrAdvanced 

def askColumnToQuery(col):													#Prompts the user to choose the column to query
	msg = "Choose the column to query : "
	choices = openSchema(col)												#Displays the schema list
	columnToQuery = eg.choicebox(msg,title,choices)
	if columnToQuery is None:
		quit()
	return columnToQuery

# def askTranslatedColumnToQuery(col):										#Prompts the user to choose the simple column to query
	# msg = "Choose the column to query : "
	# choices = []
	# for k in parameters.queryDict[col]:										#Reference the query dictionary in parameters and append them to a string list
		# choices.append(k)
	# columnToQuery = eg.choicebox(msg,title,choices)
	# if columnToQuery is None:
		# quit()
	# return parameters.queryDict[col][columnToQuery]							#Return the corresponding column from the dictionary
	
def askQueryType():															#Prompts the user to choose the query type 
	msg = "Choose the Query Type : "					
	choices = openQueryType()
	queryType = eg.choicebox(msg,title,choices)					
	if queryType is None:
		quit()
	return queryType.split()[0]												#split is used to remove everything after the first whitespace. Only the relevant query type like $eq or $regex will remain.

def askSearchTerm():														#Prompts the user to enter the search term
	msg = "Enter the search term : "
	example = "Malware"
	while 1: 
		searchTerm = eg.enterbox(msg,title,example)
		if searchTerm != "":
			break
	if searchTerm is None:
		quit()
	if searchTerm.isdigit():
		searchTerm = ast.literal_eval(searchTerm)								#Convert numbers to python literals
	elif re.match(isodateRegex,searchTerm):
		searchTerm = dateutil.parser.parse(searchTerm)
	return searchTerm	

def askQueryCode():																#Prompts the user to enter the query as code
	msg = "Columns, Operators and SearchTerms have to be encapsulated in quotes \"\". Numbers do not.\nLogical operators : $and $not $or $nor\nFind query code example : { \"Column\" : { \"$queryType\" : \"searchTerm\" }}"
	while 1: 
		queryCode = eg.codebox(msg,title)
		if queryCode is None:
			quit()
		elif re.search(isodateRegex,queryCode):
			eg.msgbox("ISODates are not supported in typed queries. Please refer to the examples.")
		elif re.match(queryRegex,queryCode):
			break
		eg.msgbox("An improper query has been entered.\nPlease modify the query.")
	return queryCode	

def askOperation():
	msg = "Please choose the operation : "										#Prompts the user to choose a mongo db operation.
	operation = eg.choicebox(msg,title,mongoOperations.values())
	if operation is None:
		quit()
	return operation

def askDescription(resultsRetrieved):											#Prompts the user to enter the description
	msg = str(resultsRetrieved) + " results have been retrieved.\nEnter a description for the number of results returned : "		
	example = "Year"
	while 1:
		description = eg.enterbox(msg,title,example)
		if description != "":
			break
	if description is None:
		quit()
	return description 

def showSuccess(operation):
	msg = "The " + operation + " operation was a success."
	eg.msgbox(msg)

#########################################################################################The GUI code is defined here#####################################################################################################################

#########################################################################################The Schema access code is defined here###########################################################################################################

def openSchema(col):																		
	try:
		schemaList = [line.rstrip('\n') for line in open(schemaFilesFolder + col + SCHEMAEXT)]				#Open schema list for display
	except:
		eg.msgbox(schemaFilesFolder + col + SCHEMAEXT + " is not present")
		quit()
	return schemaList
	
def openQueryType():
	try:
		QueryTypeList = [line.rstrip('\n') for line in open(queryTypeFile)]									#Open query type list for display
	except:
		eg.msgbox(queryTypeFile + " is not present")
		quit()
	return QueryTypeList

#########################################################################################The Schema access code is defined here###########################################################################################################

#########################################################################################The Printing code is defined here################################################################################################################
class dateTimeEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance (obj, datetime): 
			return str(obj.isoformat())
		elif isinstance (obj, datetime.date):
			return str(obj.isoformat())
		return json.JSONEncoder.default(self, obj)

def clearFileContents(fileName):															#Function to clear file contents
	open(fileName, 'w').close()

def prepareFile(fileName):
	with open(fileName, 'a', encoding='utf-8') as f:	
		print('[', file = f)																#Append a '['
	f.close()

def cursorParsing(findCursor):
	jsonList = []																			#Declare empty string list
	for line in findCursor:
		if idField in line:
			del line[idField]																#Remove '_id' field as it is not required for viewing
			jsonList.append(json.dumps(line,cls=dateTimeEncoder))							#Add cursor results to the string list
		else:
			jsonList.append(json.dumps(line,cls=dateTimeEncoder))
	return jsonList
	
def printQueryToFile(findCursor,timesToQuery):
	i = 0																					#Declare counter
	findList = cursorParsing(findCursor)													#Assign the parsed string list from the function to the local string list
	if findCursor.retrieved != 0:															#If the query does not have empty results
		with open(findFileName, 'a', encoding='utf-8') as f:								#'a' is used to append queries to the same json file, encoding required to print VERIS queries
			for line in findList:
				print (line, file = f, end ='')												#Print the line from the string list into the out file
				if timesToQuery != 0 : 														#If timesToQuery is not 0, printing of commas will occur
						print(',', file = f)
				else :	
					if i != len(findList)-1 :												#If timesToQuery is 0, the last comma will not be printed	
						print(',', file = f)
						i+=1					
			if timesToQuery == 0:															#If timesToQuery is 0, the closing ']' will be printed	
				print(']', file = f)
		f.close()																			#Close the file
	findCursor.close()																		#Close the Cursor object
	return len(findList)

def printDescriptionToFile(resultsRetrieved):
	with open(descriptionFileName, 'a', encoding='utf-8') as f:								#Prints descriptions for the number of results to a file
		print(askDescription(resultsRetrieved) + " : " + str(resultsRetrieved), file = f) 
	f.close()	
	
def printDistinctToFile(List):
	with open(distinctFileName, 'w', encoding='utf-8') as f:								#Prints results to a file
		for x in List:
			print(x, file = f)	
	f.close()

def printAggregateToFile(aggregateResults):
	i = 0
	aggregateList = cursorParsing(aggregateResults)
	with open(aggregateFileName, 'a', encoding='utf-8') as f:
		for line in aggregateList:
			print (line, file = f)
			if i != len(aggregateList)-1 :									
					print(',', file = f)
					i+=1
		print(']', file = f)
	f.close()

#########################################################################################The Printing code is defined here################################################################################################################

#########################################################################################The Query code is defined here###################################################################################################################
def findQuery(db):											
	col = askCollectionToQuery()																		#The collection to query is assigned
	collection = db[col]								
	if askSelectOrType():
		query = { askColumnToQuery(col) : {askQueryType() : askSearchTerm()}}
		# if askSimpleOrAdvanced():																		#A simple query will show translated columns to query
			# findResults = { askTranslatedColumnToQuery(col) : {askQueryType() : askSearchTerm()}}
		# else:
			# 				#The advanced query will show the original columns to query
	else:
		query = ast.literal_eval((askQueryCode()))												#ast.literal.eval allows the user to type in a query instead as the query is serialized from the string format
	findCursor = collection.find(query)															#Do the query and store the results as a Cursor object
	return findCursor

def distinctQuery(db):
	col = askCollectionToQuery()
	# if askSimpleOrAdvanced():
		# distinctList = db[col].find().distinct(askTranslatedColumnToQuery(col))
	# else :
	distinctList = db[col].find().distinct(askColumnToQuery(col))
	print(distinctList)
	printDistinctToFile(distinctList)
	
def aggregateQuery(db):
	aggregateResults = db[askCollectionToQuery()].aggregate(ast.literal_eval((askQueryCode())))
	printAggregateToFile(aggregateResults)

def doQuery(db):
	operation = askOperation()
	if operation == "Find" :
		timesToQuery = askTimesToQuery()															#Store the result from asking the times to query
		clearFileContents(findFileName)																#Clear file contents to allow writing to be done to the file
		prepareFile(findFileName)																	#Prepare the json file by first appending a '['
		while timesToQuery != 0:																	#Prompt the user based on the number entered for times to query
			timesToQuery-=1																			#Decrement timesToQuery
			resultsRetrieved = printQueryToFile(findQuery(db),timesToQuery)							#Call the functions to do the query and do printing of the query results
			printDescriptionToFile(resultsRetrieved)
	
	elif operation == "Distinct" :
		clearFileContents(distinctFileName)
		distinctQuery(db)
	
	elif operation == "Aggregate" :
		clearFileContents(aggregateFileName)
		prepareFile(aggregateFileName)
		aggregateQuery(db)
	showSuccess(operation)
	os.startfile(os.path.realpath(resultsFilesFolder))
#########################################################################################The Query code is defined here###################################################################################################################