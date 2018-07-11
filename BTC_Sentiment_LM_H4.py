# -*- encoding: utf-8 -*-

import pandas as pd
from eventregistry import *
from pysentiment.hiv4 import HIV4
from pysentiment.lm import LM



#Getting authorization from Event Registry with API key
er = EventRegistry(apiKey = "APIKEY")

#Loading data from event registry

q = QueryArticlesIter(
    keywords = "bitcoin",
    dateStart = "2014-01-01",
    dateEnd = "2018-07-10",
    dataType = "news",
    isDuplicateFilter = "skipDuplicates",
    keywordsLoc = "title",
    lang = "eng",
    ignoreLang = "deu",)

#initializing dictionary for relevant article data
data = {}
adf = pd.DataFrame(data,
                   columns = ['Uri','Date','Time', 'DateTime', 'Title','Body','Source'])




#Sorting the data from the query into rows and columns for easy analysis and export to a csv file
i = 0
for art in q.execQuery(er, sortBy = "date", maxItems = 2000000):
    if i <= 2000000:
        adf.loc[i]= art['uri'], art['date'], art['time'], art ['dateTime'], art['title'], art['body'], art['source']['uri']
        i = i+1

adf.dropna() 

lm = LM()
hiv4 = HIV4()



##Tokenizing ata from Titles and body##
lmtokdata = {}
lm_tdf = pd.DataFrame (lmtokdata,
                    columns = ['LMTokens'])

h4tokdata = {}
h4_tdf = pd.DataFrame (h4tokdata,
                    columns = ['H4Tokens'])


lm_tdf['LMTokens'] = adf.apply(lambda row: lm.tokenize(row['Body']), axis=1)
h4_tdf['H4Tokens'] = adf.apply(lambda row: hiv4.tokenize(row['Body']), axis=1)




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
all_data.to_csv("BTCscores.csv")








