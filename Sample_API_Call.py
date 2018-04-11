
# coding: utf-8

# In[3]:


from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='9e206b60edf84e0cbdc278f413e92c8a')

all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bloomberg,cnbc,financial-times,the-wall-street-journal,the-economist',
                                      from_parameter='2018-01-10',
                                      to='2018-04-10',
                                      language='en',
                                      sort_by='relevancy',
                                      page=3)

all_articles

