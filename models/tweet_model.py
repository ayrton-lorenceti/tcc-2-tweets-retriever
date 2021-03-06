from datetime import datetime
from loguru import logger

from models.dynamodb_model import DynamoDB

class Tweet:
  tweets_saved = 0

  def __init__(self, id_str, text, urls):
    self.id_str = id_str
    self.text = text
    self.urls = urls
    self.insertion_date = str(datetime.now())
  
  @classmethod
  def get_entities_urls(cls, urls):
    # If has 'urls', get every 'url' from 'urls'. If not, return [""]
    return [url["expanded_url"] for url in urls if "expanded_url" in url] if len(urls) > 0 else [""]
  
  @classmethod
  def save_tweet(cls, tweet):
    # Search tweet on DynamoDB
    dynamodb_tweet_response = DynamoDB.search(DynamoDB, "Tweets", "id_str", tweet.id_str)

    # If there is already tweet on DynamoDB, go on to the next tweet
    if (len(dynamodb_tweet_response) > 0):
      return

    # If no tweets have been found on DynanoDB, save it
    DynamoDB.put(DynamoDB, "Tweets", tweet.json_with_string_set())

    cls.tweets_saved += 1

  @staticmethod
  def iterate_over_tweets(self, statuses):
    # Iterate over every tweet
    for status in statuses:
      tweet = Tweet(status["id_str"], status["text"], Tweet.get_entities_urls(status["entities"]["urls"]))

      tweet.save_tweet(tweet)
    
    logger.info("### Class: Tweet, Method: iterate_over_tweets() - Tweets saved: {} ###".format(self.tweets_saved))

  def json(self):
    return self.__dict__

  def json_with_string_set(self):
    return {
      "id_str": self.id_str,
      "text": self.text,
      "urls": set(self.urls),
      "insertion_date": self.insertion_date
    }
  