import connectMongo as cm
import storeMongo as sm
import dropMongo as dm
import queryMongo as qm
import askMongo as am

def main():
	connection,connectionType,db = cm.doConnection()								#Connect to instance of MongoDB or MongoDb Atlas												
	op = am.askOperationMongo()
	if op == "Store": 
		sm.doStore(db, connectionType)												#Do store
	elif op == "Drop":
		dm.doDrop(db, connectionType)												#Do drop
	elif op == "Query":
		qm.doQuery(db)																#Do query

if __name__== "__main__":
  main()