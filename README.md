# SCSE19-0210

OPEN SOURCE INTELLIGENCE GATHERING AND TOPIC MODELLING ON CYBER SECURITY INCIDENTS

- Data Harvesting  

CSV or JSON files can be downloaded from the respositories or obtained through scraping of the respository or website. 
Webscraper.py utilizes Beautiful Soup, Request and CSV libraries to scrape and store the scraped data in CSV file format.
Convert.py is used to convert the CSV file to JSON file format for future manipulation.

- Data Processing  

*For ease of access to a unified common database, the earlier scraped data from the Data Harvesting phase will undergo consolidation with data from another project, SCSE19-0209. 
Parsers are used to ensure terminologies in the JSON files between the projects are standardised. 
After all JSON files are standardized, merge.py and mergeParameters.py are used to merge the JSON files into one common JSON file which will be SCSE19-0209.json.
The above can be seen in the mergeSchema folder.

MongoDB will be used to store the SCSE19-0209.json file as it is fast to setup, works well with JSON file format and utilizes a NoSQL approach for queries, which is beneficial for data analytics. 
pymongo is used interface with the database to obtain query results. 
A python GUI interface allows for queries to be formed through selection or typed as code. 
Results are saved into a JSON file.
The above can be seen in the mongo folder.

- Data Analysis  

2 forms of analysis will be ran on the data, Regression and NLP.

For regression, numpy and sklearn libraries will be used to perform the regression operations on the variables and plot the graph to visualize the relationships between the variables.

For NLP, genism, pyLDAvis and spacy libraries will be used to perform topic modelling on the dataset's Description field. It will train a LDA model which is built with the relevant corpus and dictionary created from bigram and trigram model. After running the model, the keywords and its relevant weights will be shown. The perplexity and coherence score will be displayed. PyLDAvis library is used to plot out the results of the topic model.

Data Visualization  

Various types of graphs can be plotted from the information obtained from the database.


