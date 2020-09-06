from datetime import datetime

from models.dynamodb_model import DynamoDB
from loguru import logger

class Tweet:
  def __init__(self, id_str, text, urls):
    self.id_str = id_str
    self.text = text
    self.urls = urls
    self.insertion_date = str(datetime.now())
  
  @classmethod
  def get_entities_urls(cls, urls):
    logger.info( { "method": "Tweet.get_entities_urls()" } )

    return [url["expanded_url"] for url in urls if "expanded_url" in url]
  
  @classmethod
  def save_tweet(cls, tweet):
    logger.info( { "method": "Tweet.save_tweet()", "params": { "tweet": tweet } } )

    # Search tweet on DynamoDB
    dynamodb_tweet_response = DynamoDB.search(DynamoDB, "Tweets", "id_str", tweet.id_str)

    # If already has tweet on DynamoDB, go to the next tweet
    if (len(dynamodb_tweet_response) > 0):
      return
  
    # If hasn't found tweet on DynamoDB, save it
    DynamoDB.put(DynamoDB, "Tweets", tweet.json_with_string_set())

  def json(self):
    return self.__dict__

  def json_with_string_set(self):
    return {
      "id_str": self.id_str,
      "text": self.text,
      "urls": set(self.urls),
      "insertion_date": self.insertion_date
    }

  @staticmethod
  def iterate_over_tweets(statuses):
    logger.info( { "method": "Tweet.iterate_over_tweets()" } )

    tweets_saved = 0

    # Iterate over every tweet
    for status in statuses:
      tweet = Tweet(status["id_str"], status["text"], Tweet.get_entities_urls(status["entities"]["urls"]))

      tweet.save_tweet(tweet)

      tweets_saved += 1

    return tweets_saved 
  