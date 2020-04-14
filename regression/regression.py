import os
import itertools 
import json
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing 
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split 

jsonFile = os.path.join(os.path.dirname(__file__), "Ransomware.json")
mapFile = os.path.join(os.path.dirname(__file__), "mapping.txt")
x = "x"
y = "y"
count = "count"

numToFilter = 10
xLimitLower = 0
xLimitHigher = 600					#300
yLimitLower = 0
yLimitHigher = 50000					#10000

def doRegression():
	le = preprocessing.LabelEncoder() 	# Declare label_encoder object that will understand word labels. 
	reg = linear_model.LinearRegression()
	
	df = pd.DataFrame(parseListOfDicts())
	df[x] = le.fit_transform(df[x]) # Encode labels in column
	#df[y] = le.fit_transform(df[y]) # Encode labels in column
	#df.sort_values(by = [y,x], ascending=True, inplace=True)		#[y,x]
	print(df.info())
	print(df)
	
	#df = filterNumOfElements(df,y,numToFilter) 
	
	X = df[x].values.reshape(-1,1)
	Y = df[y].values.reshape(-1,1)
	
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
	
	reg.fit(X_train, Y_train)
	y_pred = reg.predict(X_test)
	
	print(Y_test)
	
	plt.scatter(X_test, Y_test,  color='black')
	plt.plot(X_test, y_pred, color='red', linewidth=3)
	
	plt.xlim(xLimitLower, xLimitHigher)
	plt.ylim(yLimitLower, yLimitHigher)
	
	saveToFileConsolePrint(df,le,y,reg,Y_test,y_pred)
	plt.show()

def printRegressionDetails(reg,Y_test,y_pred):
	#The intercept
	print("Intercept: %.2f" % reg.intercept_)
	
	# The coefficients
	print('Coefficients: %.2f' % reg.coef_)
	
	# The mean absolute Error
	print('Mean Absolute Error: %.2f' % mean_absolute_error(Y_test, y_pred)) 
	
	# The mean squared error
	print('Mean squared error: %.2f' % mean_squared_error(Y_test, y_pred))
	
	# The coefficient of determination: 1 is perfect prediction
	print('Coefficient of determination: %.2f' % r2_score(Y_test, y_pred))

def saveToFileConsolePrint(df,le,y,reg,Y_test,y_pred):
	f = open(mapFile, 'w')
	sys.stdout = f
	printRegressionDetails(reg,Y_test,y_pred)
	showMapping(df,le)
	showCountOfDF(df,y)
	f.close()	

def showMapping(df,le):
	mapping = dict(zip(le.classes_, range(0, len(le.classes_))))
	print(mapping)
	
def showCountOfDF(df,colName):
	df[count] = df.groupby(colName)[colName].transform(count)
	printall(df)

def filterNumOfElements(df,colName,filterNum):
	return df[df.groupby(colName)[colName].transform(count)>filterNum].copy()

def printall(df):
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
		print(df)

def getX(dict):
	#return str(dict["action"])
	#return str(dict["malware_used"])
	#return str(dict["discovered_by"])
	#return str(dict["vulnerability"])
	#return str(dict["tool"])
	#return str(dict["country"])
	#return str(dict["industry"])
	return dict["entry_date"]["date"]
	
def getY(dict):
	#ml = dict["monetary_loss"]
	ra = dict["target"]["records_affected"]
	if ra != None: #and ra <= 4500000:
		return dict["target"]["records_affected"]
		#return dict["monetary_loss"]["amount"]
	else:
		return 0

def formDicts(dict):
	listOfDicts = []
	xValue = getX(dict)
	yValue = getY(dict)
	if yValue != None:
		makeDict = {x : xValue, y : yValue}
		listOfDicts.append(makeDict)
	return listOfDicts

def getListOfDictFromJSONFile():		#JSON file is a list of dictionaries
	with open(jsonFile, 'r') as f:
		listOfDict = json.load(f)
	return listOfDict	

def parseListOfDicts():
	listOfDicts = getListOfDictFromJSONFile()		#df = pd.read_json(jsonFile)
	parsedListOfDicts = []
	for dict in listOfDicts:
		parsedListOfDicts.extend(formDicts(dict))
	return parsedListOfDicts