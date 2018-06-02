# Practicum
CMGT 597A&B

This repository will contain all source code, data, visualizations for my 597A&B Project for USC Annenberg's CMGT Program.

The project will use the Event Registry API to gather articles about Bitcoin, and then perform a lexical sentiment analysis on them to test for correlation and feedback between news sentiment and Bitcoin prices.

## Gathering Data

### API Call

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

### Organization of Relevant Data

This takes the data collected from the API call above and extracts only the relevant information that will be used in this analysis, then saves it to a .csv file:

* a unique identifier `art['uri']`
* the date `art['date']` and time `art['time']` of each article's publication
* the article's title `art['title']`
* the article's body/text `art['body']`
* the source of the article `art['source']['uri']`

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

#Saves the data to a .csv file:
adf.to_csv('BTCArticles.csv')
```
### Bitcoin Prices

The Bitcoin market data is simply downloaded from [Coinbase.com].


## Sentiment Analysis

*In Progress*
```python

import nltk
import pandas as pd

pd.read_csv('BTCArticles.csv')

###stop words


###lemmatization


###sentiment scores by article



###sentiment scores by date




###write new sentiment scores to csv
df.to_csv('BTCArticles_Sentiment.csv')
```

## Market Analysis

*Coming Soon*




