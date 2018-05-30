import pandas as pd
from eventregistry import *


#Getting authorization from Event Registry with API key
er = EventRegistry(apiKey = "API-KEY")

#Loading data from event registry
#These specifications might need to be reconsidered 
q = QueryArticlesIter(
    keywords = "bitcoin",
    categoryUri = er.getCategoryUri("business"),
    dateStart = "2018-05-20",
    dateEnd = "2018-05-21",
    keywordsLoc = "title",
    lang = "eng",)

#initializing dictionary for relevant article data
data = {}
adf = pd.DataFrame(data,
                   columns = ['Uri','Date','Time', 'DateTime','Title','Body','Source'])


#Sorting the data from the query into rows and columns for easy analysis and export to a csv file
i = 0
for art in q.execQuery(er, sortBy = "date", maxItems = 100):
    if i <= 100:
        adf.loc[i]= art['uri'], art['date'], art['time'], art ['dateTime'], art['title'], art['body'], art['source']['uri']
        i = i+1
        
        print(adf)
        
adf.to_csv('BTCarticles.csv')



