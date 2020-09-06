import boto3

from boto3.dynamodb.conditions import Key
from loguru import logger

class DynamoDB:
  dynamodb = boto3.resource('dynamodb')

  def __init__(self):
    pass
  
  @staticmethod
  def search(self, table_name, key, value):
    logger.info("### DynamoDB.search(table_name, key, value) ###")
    logger.info("table_name: {} - key: {} - value: {}".format(table_name, key, value))
    logger.info("### DynamoDB.search(table_name_ key, value) ###")

    table = self.dynamodb.Table(table_name)

    search_response = table.query( 
      KeyConditionExpression=Key(key).eq(value)
    )

    return search_response["Items"]
  
  @staticmethod
  def put(self, table_name, item):
    logger.info("### DynamoDB.put(table_name, key, value) ###")
    logger.info("table_name: {} - item: {}".format(table_name, item))
    logger.info("### DynamoDB.put(table_name, key, value) ###")    

    table = self.dynamodb.Table(table_name)

    table.put_item(Item=item)