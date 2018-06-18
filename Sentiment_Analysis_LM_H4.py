# -*- encoding: utf-8 -*-

import pandas as pd
from pysentiment.hiv4 import HIV4
from pysentiment.lm import LM

adf = pd.read_csv('BTCarticles.csv', low_memory = False)

#####SENTIMENT ANALYSIS#########

#initializng dictionary
        
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

all_data.to_csv('BTCArticle_AllData.csv')








