# Practicum
CMGT 597A&B

This repository will contain all source code, data, visualizations for my 597A&B Project for USC Annenberg's CMGT Program.

The project will use Event Registry to gather articles about Bitcoin, and then perform a lexical sentiment analysis on them to test for correlation and feedback between news sentiment and Bitcoin prices.




```python
from eventregistry import *
er = EventRegistry(apiKey = "API_KEY")
q = QueryArticlesIter(
    keywords = "bitcoin",
    categoryUri = er.getCategoryUri("business"),
    dateStart = "YYYY-MM-DD",
    dateEnd = "YYYY-MM-DD",
    keywordsLoc = "title",)
for art in q.execQuery(er, sortBy = "date"):
    print(art)
```
