# Practicum
CMGT 597A&B

This repository will contain all source code, data, visualizations for my 597A&B Project for USC Annenberg's CMGT Program.

The project will use the Event Registry API to gather articles about Bitcoin, and then perform a lexical sentiment analysis on them to test for correlation and feedback between news sentiment and Bitcoin prices.


## API Call

This API call searches for and returns all articles in EventRegistry's database that fit the criteria set by `QueryArticlesIter`.


```python
from eventregistry import *
er = EventRegistry(apiKey = "API_KEY")
##API_KEY is a unique id for authorized users, the key used was omitted.

q = QueryArticlesIter(
    keywords = "bitcoin",
    categoryUri = er.getCategoryUri("business"),
    dateStart = "YYYY-MM-DD",
    dateEnd = "YYYY-MM-DD",
    keywordsLoc = "title",) 

#keyword limits search only to articles containing that specific word
#dateStart and dateEnd specify the dates between which articles are queried in the request
#keywordsLoc ensures that the request only queries headlines containing the keyword

for art in q.execQuery(er, sortBy = "date"):
    print(art)
    #this will need to be altered so that it also stores these articles for somewhere
    #but in the initial test run, I just had it print them.
```
