import easygui as eg
import parameters

def askOperationMongo():														#Ask for the MongoDB operation
	msg = "Choose the MongoDB operation : "
	choices = parameters.operationsList											
	confirmBool = False
	while confirmBool is False:
		op = eg.choicebox(msg,"MongoDB Operation",choices)
		if op is None:
			quit()
		elif op != "Query":
			confirmBool = confirmMongo(op)
		else:
			confirmBool = True
	return op

def confirmMongo(op):															#Ask for confirmation before executing the MongoDB operation
	msg = "MongoDB will be altered by the operation. Please confirm the " + op + " operation : "										
	confirmBool = eg.boolbox(msg,"MongoDB Operation",choices=('[Y]es', '[N]o'))
	if confirmBool is None:
		quit()
	return confirmBool

def askCollectionSelection(collectionsList):													#Ask for the collections to conduct operations on
	msg = "Select the collections to conduct operations on:"
	selColList = eg.multchoicebox(msg,"Collections",collectionsList)
	if selColList is None:
		quit() 
	return selColList
