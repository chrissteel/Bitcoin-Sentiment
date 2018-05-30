# Practicum
CMGT 597A&B

This repository will contain all source code, data, visualizations for my 597A&B Project for USC Annenberg's CMGT Program.

The project will use the Event Registry API to gather articles about Bitcoin, and then perform a lexical sentiment analysis on them to test for correlation and feedback between news sentiment and Bitcoin prices.


## API Call (Initial Query)

This gathers data from all of the articles in EventRegistry's database that fit the criteria set by `QueryArticlesIter`.


```python

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
```

## Organization of Relevant Data

This takes the data collected from the API call above and extracts only the relevant information that will be used in this analysis: a unique identifier (useful for time series analysis) for each article, the date/time of publication, the title, the body, and the domain name of the source.

```python
#initializing dictionary for relevant article data
data = {}
adf = pd.DataFrame(data,
                   columns = ['Uri','Date','Time', 'DateTime','Title','Body','Source'])


#Sorting the data from the query into rows and columns for easy analysis and export to a csv file
i = 0
for art in q.execQuery(er, sortBy = "date", maxItems = 2):
    if i <= 5:
        adf.loc[i]= art['uri'], art['date'], art['time'], art ['dateTime'], art['title'], art['body'], art['source']['uri']
        i = i+1
        
        print(adf)
```
