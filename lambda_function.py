import os

from models.dynamodb_model import DynamoDB
from retrieve_tweets.retrieve_tweets import retrieve_tweets_by_result_type, retrieve_tweets_by_until_param

def lambda_handler(event, context):
  result_type = os.environ["result_type"]

  # Search result_type on DynamoDB
  dynamodb_search_metadata_response = DynamoDB.search(DynamoDB, "Search_Metadata", "result_type", result_type)

  # Check if has found 'result_type'. If not, search by 'until'
  if (len(dynamodb_search_metadata_response) == 0):
    return retrieve_tweets_by_until_param(result_type)

  return retrieve_tweets_by_result_type(result_type)