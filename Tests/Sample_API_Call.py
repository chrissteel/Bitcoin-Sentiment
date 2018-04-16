
# coding: utf-8
# notes with the '#' next to them are used here to explain what I'm doing to CMGT peers who aren't necessarily familiar with python

from newsapi import NewsApiClient

#api_key is a unique key that gives me access to the database, but has been changed here to keep it private.
newsapi = NewsApiClient(api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


# all_articles searches the API database for articles about bitcoin from the sources indicated, between the dates indicated below.  Sorting by 'relevancy' prioritizes the results that most closely match the 'q' value, but doesn't really matter for our purposes.

all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bloomberg,cnbc,financial-times,the-wall-street-journal,the-economist',
                                      from_parameter='2018-01-10',
                                      to='2018-04-10',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

#this command prompts the code to print the data.
all_articles

