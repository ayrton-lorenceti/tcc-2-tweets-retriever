import json

from datetime import date, timedelta
from loguru import logger

from models.dynamodb_model import DynamoDB
from models.search_metadata_model import SearchMetadata
from models.tweepy_model import Tweepy
from models.tweet_model import Tweet

def retrieve_tweets_by_until_param(result_type):
  logger.info("### Method: retrieve_tweets_by_until_param() ###")

  # Set initial condition based on Lambda
  until_param = date.today() - timedelta(days = 7)

  # Search tweets based on initial condition
  search_results = Tweepy.search_tweets(Tweepy, result_type, until=until_param)

  # If no tweets have been found, finish Lambda
  if (len(search_results["statuses"]) == 0):
    logger.info("### Method: retrieve_tweets_by_until_param() - No tweets found. ###")

    return {
      'statusCode': 200,
      'message': json.dumps("No tweets found.")
    }

  Tweet.iterate_over_tweets(Tweet, search_results["statuses"])
  
  SearchMetadata.save_since_id(SearchMetadata, search_results["search_metadata"], result_type)

  return {
    'statusCode': 200,
    'message': json.dumps("Finished tweets retrieve.")
  }

def retrieve_tweets_by_result_type(result_type):
  logger.info("### Method: retrieve_tweets_by_result_type() ###")

  # Search 'since_id' based on 'result_type'
  since_id = DynamoDB.search(DynamoDB, "Search_Metadata", "result_type", result_type).pop()["since_id"]

  # Search tweets by 'since_id'
  search_results = Tweepy.search_tweets(Tweepy, result_type, since_id=since_id)

  # If no tweets have been found, finish Lambda
  if (len(search_results["statuses"]) == 0):
    logger.info("### Method: retrieve_tweets_by_result_type() - No tweets found. ###")
    
    return {
      'statusCode': 200,
      'message': json.dumps("No tweets found.")
    }

  Tweet.iterate_over_tweets(Tweet, search_results["statuses"])

  SearchMetadata.save_since_id(SearchMetadata, search_results["search_metadata"], result_type)

  return {
    'statusCode': 200,
    'message': json.dumps("Finished tweets retrieve.")
  }  
