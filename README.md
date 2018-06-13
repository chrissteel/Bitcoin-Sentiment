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

import csv
import glob
import re
import string
import sys
import time
sys.path.append('/Users/admin/Desktop/Bitcoin/Modules')  # Modify to identify path for custom modules
import Load_MasterDictionary as LM

# User defined directory for files to be parsed
TARGET_FILES = r'/Users/admin/Desktop/Bitcoin/*.*'
# User defined file pointer to LM dictionary
MASTER_DICTIONARY_FILE = r'/Users/admin/Desktop/Bitcoin/' + \
                         'LoughranMcDonald_MasterDictionary_2014.csv'
# User defined output file
OUTPUT_FILE = r'/Users/admin/Desktop/Bitcoin/Parser.csv'
# Setup output
OUTPUT_FIELDS = ['file name,', 'file size,', 'number of words,', '% positive,', '% negative,',
                 '% uncertainty,', '% litigious,', '% modal-weak,', '% modal moderate,',
                 '% modal strong,', '% constraining,', '# of alphanumeric,', '# of digits,',
                 '# of numbers,', 'avg # of syllables per word,', 'average word length,', 'vocabulary']

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, True)


def main():

    f_out = open(OUTPUT_FILE, 'w')
    wr = csv.writer(f_out, lineterminator='\n')
    wr.writerow(OUTPUT_FIELDS)

    file_list = glob.glob(TARGET_FILES)
    for file in file_list:
        print(file)
        with open(file, 'r', encoding='UTF-8', errors='ignore') as f_in:
            doc = f_in.read()
        doc_len = len(doc)
        doc = re.sub('(May|MAY)', ' ', doc)  # drop all May month references
        doc = doc.upper()  # for this parse caps aren't informative so shift

        output_data = get_data(doc)
        output_data[0] = file
        output_data[1] = doc_len
        wr.writerow(output_data)


def get_data(doc):

    vdictionary = {}
    _odata = [0] * 17
    total_syllables = 0
    word_length = 0
    
    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].positive: _odata[3] += 1
            if lm_dictionary[token].negative: _odata[4] += 1
            if lm_dictionary[token].uncertainty: _odata[5] += 1
            if lm_dictionary[token].litigious: _odata[6] += 1
            if lm_dictionary[token].weak_modal: _odata[7] += 1
            if lm_dictionary[token].moderate_modal: _odata[8] += 1
            if lm_dictionary[token].strong_modal: _odata[9] += 1
            if lm_dictionary[token].constraining: _odata[10] += 1
            total_syllables += lm_dictionary[token].syllables

    _odata[11] = len(re.findall('[A-Z]', doc))
    _odata[12] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[13] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
    _odata[14] = total_syllables / _odata[2]
    _odata[15] = word_length / _odata[2]
    _odata[16] = len(vdictionary)
    
    # Convert counts to %
    for i in range(3, 10 + 1):
        _odata[i] = (_odata[i] / _odata[2]) * 100
    # Vocabulary
        
    return _odata


if __name__ == '__main__':
    print('\n' + time.strftime('%c') + '\nGeneric_Parser.py\n')
    main()
    print('\n' + time.strftime('%c') + '\nNormal termination.')
```

## Market Analysis

```python
import pandas as pd
import numpy as np

sdf = pd.read_csv('BTCArticles_Sentiment.csv')
mdf = pd.read_csv('BTC_Daily_Prices.csv')
```



