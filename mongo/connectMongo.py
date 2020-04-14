import pymongo 
import parameters
import easygui as eg

title = "Connect"
mongoDBLocalConnection = "mongodb://localhost"
DBName = parameters.DBName
atlasExamples = parameters.atlasExamples
onlineExamples = parameters.onlineExamples

def askConnection():
	msg = "Please choose to either access the data from an instance of MongoDB or from MongoDB Atlas."		
	connectionType = eg.choicebox(msg,title,["Local Instance","Online Instance","Atlas"])							#Prompts the user to choose the connection method to MongoDB.
	if connectionType is None:
		quit() 
	return connectionType

def askAtlasConnectionDetails():																					#Asks for MongoDB Atlas details
	msg = "Enter the login details :"
	fieldNames = ["Hosting server :", "Cluster ID :", "User ID :", "Password :"]
	detailsList = eg.multpasswordbox(msg,title,fieldNames,atlasExamples)
	if detailsList is None:
		quit() 
	return detailsList

def askOnlineConnectionDetails():																					#Asks for online instance of MongoDB details
	msg = "Enter the login details :"
	fieldNames = ["Server IP Address :", "Port Number:","Database Name :", "User ID :", "Password :"]
	detailsList = eg.multpasswordbox(msg,title,fieldNames,onlineExamples)
	if detailsList is None:
		quit() 
	return detailsList

def doConnection():
	connectionType = askConnection()
	try:
		if connectionType == "Local Instance":
			connection = pymongo.MongoClient(mongoDBLocalConnection)												#Connects to the local instance of MongoDB
		elif connectionType == "Online Instance":
			detailsList = askOnlineConnectionDetails()																#Defines the MongoDB connection URL
			mongoDBConnection = "mongodb://" + detailsList[3] + ":" + detailsList[4] + "@" + detailsList[0] + ":" + detailsList[1] + "/" + detailsList[2]	
			connection = pymongo.MongoClient(mongoDBConnection)														#Connects to the online instance of MongoDB
		else :
			detailsList = askAtlasConnectionDetails()																#Defines the MongoDB Atlas connection URL
			mongoDBConnection = "mongodb+srv://" + detailsList[2] + ":" + detailsList[3] + "@" + detailsList[1] + "-" + detailsList[0] + ".mongodb.net/test?retryWrites=true"
			connection = pymongo.MongoClient(mongoDBConnection)														#Connects to MongoDB Atlas
		connection.server_info()
	except:
		eg.msgbox("The connection to MongoDB has failed. Please check your connection or entered details.")
		quit()
	print("Connection established")
	return connection, connectionType, connection[DBName]															#Setup connection to the desired database	