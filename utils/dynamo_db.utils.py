import boto3

class DynamoDBUtils:
  def __init__(self):
    self.dynamodb = boto3.resource('dynamodb')