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
from pysentiment.hiv4 import HIV4
from pysentiment.lm import LM

#Getting authorization from Event Registry with API key
er = EventRegistry(apiKey = "API-KEY")

#Querying data from event registry
q = QueryArticlesIter(
    keywords = "bitcoin",
    dateStart = "2014-01-01",
    dateEnd = "2018-07-05",
    dataType = "news",
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
for art in q.execQuery(er, sortBy = "date", maxItems = 200000):
    if i <= 200000:
        adf.loc[i]= art['uri'], art['date'], art['time'], art ['dateTime'], art['title'], art['body'], art['source']['uri']
        i = i+1 

```


## Sentiment Analysis

```python
##initializng dictionaries

lm = LM()
hiv4 = HIV4()

##Tokenizing ata from Titles and body##
lmtokdata = {}
lm_tdf = pd.DataFrame (lmtokdata,
                    columns = ['LMTokens'])

h4tokdata = {}
h4_tdf = pd.DataFrame (h4tokdata,
                    columns = ['H4Tokens'])

lm_tdf['LMTokens'] = adf.apply(lambda row: lm.tokenize(row['Title']), axis=1)
h4_tdf['H4Tokens'] = adf.apply(lambda row: hiv4.tokenize(row['Title']), axis=1)


##Sorting Data and Performing sentiment analysis on tokenized data##

lmscoredata = {}
lm_calc_df = pd.DataFrame (lmscoredata,
               columns = ['LMSentiment'])
lm_calc_df['LMSentiment'] = lm_tdf.apply(lambda row: lm.get_score(row['LMTokens']), axis = 1)

h4scoredata = {}
h4_calc_df = pd.DataFrame (h4scoredata,
               columns = ['H4Sentiment'])
h4_calc_df['H4Sentiment'] = h4_tdf.apply(lambda row: hiv4.get_score(row['H4Tokens']), axis = 1)

lm_scores = lm_calc_df['LMSentiment'].apply(pd.Series)
lm_scores.rename(columns={'Negative': 'LMNeg', 'Polarity': 'LMPol', 'Positive':'LMPos', 'Subjectivity':'LMSub'}, inplace=True)

h4_scores = h4_calc_df['H4Sentiment'].apply(pd.Series)
h4_scores.rename(columns={'Negative': 'H4Neg', 'Polarity': 'H4Pol', 'Positive':'H4Pos', 'Subjectivity':'H4Sub'}, inplace=True)


##Merging DataFrames into one for Analysis 
all_data = pd.concat([adf, lm_scores, h4_scores], axis=1)

all_data.to_csv('BTC_LM_H4_Scores.csv')

```
### Bitcoin Prices

The Bitcoin market data is simply downloaded from [Coinbase.com].


## Market Analysis

The analysis was conducted using Stata

*in progress*

```stata
import delimited /BTC_LM_H4_Scores.csv, bindquote(strict) varnames(1)
drop time-source lmpol lmsub h4pol h4sub
generate lm = lmpos - lmneg
generate h4 = h4pos - h4neg
collapse (mean) lm (mean) h4, by(date)
```

