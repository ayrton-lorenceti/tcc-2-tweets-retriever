from popular_tweets.popular_tweets import retrieve_tweets_by_result_type, retrieve_tweets_by_until_param

from models.dynamodb_model import DynamoDB

# import json

def lambda_handler(event, context):
  # Search result_type on DynamoDB
  dynamodb_search_metadata_response = DynamoDB.search(DynamoDB, "Search_Metadata", "result_type", "popular")

  # Check if has found 'result_type'. If not, search by 'until'
  if (len(dynamodb_search_metadata_response) == 0):
    return retrieve_tweets_by_until_param()

  retrieve_tweets_by_result_type()

lambda_handler(None, None)