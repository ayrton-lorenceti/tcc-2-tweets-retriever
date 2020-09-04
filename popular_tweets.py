import re
from datetime import date, timedelta

from models.dynamodb_model import DynamoDB
from models.search_metadata_model import SearchMetadata
from models.tweepy_model import Tweepy
from models.tweet_model import Tweet

def retrieve_tweets_by_until_param():
  # Set initial condition to 'popular'
  until_param = date.today() - timedelta(days = 7)

  # Search tweets based on initial condition
  search_results = Tweepy.search_tweets(Tweepy, "popular", until=until_param)

  # If hasn't found tweets, finishes Lambda
  if (len(search_results["statuses"]) == 0):
    return

  Tweet.iterate_over_tweets_and_save(Tweet, search_results["statuses"])

  # Get since_id (max_id) from 'next_results'
  next_results_max_id = re.search("(?<=\?max_id=).*?(?=&)", search_results["search_metadata"]["next_results"])

  search_metadata = SearchMetadata("popular", next_results_max_id.group(0))

  # Save since_id on DynamoDB
  DynamoDB.put(DynamoDB, "Search_Metadata", search_metadata.json())

def retrieve_tweets_by_result_type():
  print("result type")
  # Search since_id based on result_type
  since_id = DynamoDB.search(DynamoDB, "Search_Metadata", "result_type", "popular").pop()["since_id"]

  # Search tweets by since_id
  search_results = Tweepy.search_tweets(Tweepy, "popular", since_id=since_id)

  # If hasn't found tweets, finishes Lambda
  if (len(search_results) == 0):
    return

  Tweet.iterate_over_tweets_and_save(Tweet, search_results["statuses"])

  # Get since_id (max_id) from next_results
  next_results_max_id = re.search("(?<=\?max_id=).*?(?=&)", search_results["search_metadata"]["next_results"])

  search_metadata = SearchMetadata("popular", next_results_max_id.group(0))

  # Save since_id on DynamoDB
  DynamoDB.put(DynamoDB, "Search_Metadata", search_metadata.json())

# Search result_type on DynamoDB
dynamodb_search_metadata_response = DynamoDB.search(DynamoDB, "Search_Metadata", "result_type", "popular")

# Check if has found 'result_type'. If not, search by 'until'
if (len(dynamodb_search_metadata_response) == 0):
  print("until")
  retrieve_tweets_by_until_param()
  quit()

retrieve_tweets_by_result_type()

