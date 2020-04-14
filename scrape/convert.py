import json
import csv

#Convert.py is a script written to convert csv file to json file format.
#Change the relevant csv file path and json file path for use.

csvFilePath = 'health.csv' 
jsonFilePath = 'health.json'

csvFile = open(csvFilePath)

reader = csv.DictReader(csvFile, fieldnames = ("state","country","victim","industry","records_affected","year","month","day","type","location","description"))

out = json.dumps([row for row in reader])

f = open(jsonFilePath, 'w')
f.write(out)

print(out)