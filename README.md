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
#I was able to get more articles by doing multiple queries with shorter dateStart and dateEnd windows

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


## Sentiment Data

The analysis was conducted using Stata.

First, the LM and H4 scores were imported, and total scores of the following variables for each article were calculated:
* `lmpos`: positive LM scores
* `lmneg`: negative LM scores
* `lm`: total LM scores for each article `lmpos - lmneg`

* `h4pos`: positive H4 scores
* `h4neg`: negative H4 scores
* `h4`: total H4scores for each article `h4pos - h4neg`

```stata
import delimited /BTC_LM_H4_Scores.csv, bindquote(strict) varnames(1)
drop time-source lmpol lmsub h4pol h4sub
generate lm = lmpos - lmneg
generate h4 = h4pos - h4neg
```
Next, the averages for each day were calculated:

```stata
collapse (mean)lmpos (mean)lmneg (mean) h4pos (mean) h4neg (mean) lm (mean) h4, by(date)
```

## Market Analysis

A data set containing BTC prices was then merged with the data set containing scores by date, and the daily percent changes in price from the previous day (index return) were calculated using a logarithmic transformation. 

```stata
merge 1:1 date using "/Users/admin/Desktop/Bitcoin/Scores/BTCPrices.dta"
generate btc_return = ln(price[_n]/price[_n - 1])
```

A linear regression was used to determine relationships between the sentiment data and price data.  The one that turned out to be the most useful was between LM polarity scores and the index returns.

```stata
regress btc_return lmpol if endate >= 20089
```

The regression was then tested across multiple time lags, first the effect of returns from 3-1 days ago on LM polarity scores.

```stata
regress lmpol L1.btc_return L2.btc_return L3.btc_return if endate >=20089
```

Next was the effect of LM polarity scores on returns 1-3 days later.

```stata
regress btc_return L1.lmpol L2.lmpol L3.lmpol if endate >=20089
```

The output of these results showed that the markets were predictive of news sentiment, but not the other way around when time lags were taken into account. 

## Vector Autoregression (VAR) 

First a Dickey-Fuller test was applied to test for stationarity of each variable (three versions of the test used as a robustness check):

```stata
dfuller lmpol, drift
dfuller lmpol, trend
dfuller lmpol, noconstant

dfuller btc_return, drift
dfuller btc_return, trend
dfuller btc_return, noconstant
```
Both variables were stationary according to all three versions of the test, so the VAR was conducted next.

```stata
varbasic lmpol btc_return if endate >= 20089, lags(1/3)
```

