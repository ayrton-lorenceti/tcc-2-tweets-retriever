from datetime import datetime
from loguru import logger

from models.dynamodb_model import DynamoDB

class Tweet:
  tweets_saved = 0

  def __init__(self, id_str, text):
    self.id_str = id_str
    self.text = text

  @classmethod
  def save_tweet(cls, tweet):
    # Search tweet on DynamoDB
    dynamodb_tweet_response = DynamoDB.search(DynamoDB, "Tweets2", "id_str", tweet.id_str)

    # If already has tweet on DynamoDB, go to the next tweet
    if (len(dynamodb_tweet_response) > 0):
      return

    # If hasn't found tweet on DynamoDB, save it
    DynamoDB.put(DynamoDB, "Tweets2", tweet.json_with_string_set())

    cls.tweets_saved += 1

  @staticmethod
  def iterate_over_tweets(self, statuses):
    # Iterate over every tweet
    for status in statuses:
      tweet = Tweet(status["id_str"], status["text"])

      tweet.save_tweet(tweet)
    
    logger.info("### Class: Tweet, Method: iterate_over_tweets() - Tweets saved: {} ###".format(self.tweets_saved))

  def json(self):
    return self.__dict__

  def json_with_string_set(self):
    return {
      "id_str": self.id_str,
      "text": self.text
    }
  