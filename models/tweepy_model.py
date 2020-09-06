import boto3
import os
import tweepy

def get_parameters(parameter_name):
  client = boto3.client('ssm')

  parameters_response = client.get_parameters(
    Names=[parameter_name],
    WithDecryption=False
  )

  return parameters_response["Parameters"][0]["Value"]

class Tweepy:
  consumer_key = get_parameters("CONSUMER_KEY")
  consumer_secret_key = get_parameters("CONSUMER_SECRET_KEY")
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
  api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
  query = "coronavírus OR COVID-19 OR SARS-CoV-2"
  include_entities = 1
  lang = "pt"
  count = 100

  def __init__(self):
    pass
  
  @staticmethod
  def search_tweets(self, result_type, until = None, since_id = None):
    search_results = self.api.search(q=self.query, include_entities=self.include_entities, lang=self.lang, result_type=result_type, count=self.count, until=until, since_id=since_id)

    return search_results

    
    

