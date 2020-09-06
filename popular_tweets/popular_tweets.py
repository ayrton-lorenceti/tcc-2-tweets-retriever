from datetime import date, timedelta
from loguru import logger

from models.dynamodb_model import DynamoDB
from models.search_metadata_model import SearchMetadata
from models.tweepy_model import Tweepy
from models.tweet_model import Tweet

def retrieve_tweets_by_until_param():
  logger.info( { "method": "retrieve_tweets_by_until_param()" } )

  # Set initial condition based on Lambda
  until_param = date.today() - timedelta(days = 7)

  # Search tweets based on initial condition
  search_results = Tweepy.search_tweets(Tweepy, "popular", until=until_param)

  # If hasn't found tweets, finishes Lambda
  if (len(search_results["statuses"]) == 0):
    return

  tweets_saved = Tweet.iterate_over_tweets(search_results["statuses"])
  
  SearchMetadata.save_since_id(search_results["search_metadata"]["next_results"])

  logger.info( { "tweets_saved": tweets_saved } )

def retrieve_tweets_by_result_type():
  logger.info( { "method": "retrieve_tweets_by_result_type()" } )

  # Search since_id based on result_type
  since_id = DynamoDB.search(DynamoDB, "Search_Metadata", "result_type", "popular").pop()["since_id"]

  # Search tweets by since_id
  search_results = Tweepy.search_tweets(Tweepy, "popular", since_id=since_id)

  # If hasn't found tweets, finishes Lambda
  if (len(search_results) == 0):
    return

  tweets_saved = Tweet.iterate_over_tweets(search_results["statuses"])

  SearchMetadata.save_since_id(search_results["search_metadata"]["next_results"])

  logger.info( { "tweets_saved": tweets_saved } )

