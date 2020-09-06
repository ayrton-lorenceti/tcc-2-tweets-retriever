import os
import tweepy

class Tweepy:
  consumer_key = os.environ["consumer_key"]
  consumer_secret = os.environ["consumer_secret"]
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
  query = "coronavírus OR COVID-19 OR SARS-CoV-2"
  include_entities = 1
  lang = "pt"
  count = 5

  def __init__(self):
    pass
  
  @staticmethod
  def search_tweets(self, result_type, until = None, since_id = None):
    search_results = self.api.search(q=self.query, include_entities=self.include_entities, lang=self.lang, result_type=result_type, count=self.count, until=until, since_id=since_id)

    return search_results

    
    

