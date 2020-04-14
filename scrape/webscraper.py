from bs4 import BeautifulSoup
import requests
import csv
import json
l = []
s = ""
i = 0
incident = " "
date = " "
industry = " "
country = " "

#Webscraper.py is a specialised script meant for scraping specific website, 
#in this case which is RISI and Wikipedia breached data events
#Change the relevant website link and structure, tr and td for use.


source = requests.get('https://www.risidata.com/Database/event_date/asc').text

soup = BeautifulSoup(source, 'lxml')


article = soup.find('table')


#print(headline)

#csv_file = open('RISI.csv','w')

#csv_writer = csv.writer(csv_file)
#csv_writer.writerow(['Content'])

for info in article.find_all('tr'):
    for data in info.find_all('td'):
        information = str(data.text)
        if "Page" not in information:
            s = s + ";" + information
        else:
            s is None
    #print(s)
    if s != ' ' and s != '': 
        l.append(s)
    s = ""
    
    
#print(l)

for i in l:
    print(i)



        #csv_writer.writerow([information])




#csv_file.close()

