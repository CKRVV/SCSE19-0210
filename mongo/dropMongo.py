import pymongo
import askMongo as am 

def doDrop(db,connectionType):
	collectionsList = []
	for col in db.list_collection_names():
		collectionsList.append(col)
	dropList = am.askCollectionSelection(collectionsList)
	for col in dropList:										#Loop for all the collections in collectionsList
		db[col].drop()											#Open collection and execute drop command
		print("Dropped " + col + " from " + connectionType)		#Print dropped collection