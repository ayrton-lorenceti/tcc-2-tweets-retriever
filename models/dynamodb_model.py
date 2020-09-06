import boto3

from boto3.dynamodb.conditions import Key
from loguru import logger

class DynamoDB:
  dynamodb = boto3.resource('dynamodb')

  def __init__(self):
    pass
  
  @staticmethod
  def search(self, table_name, key, value):
    logger.info( { "method": "DynamoDB.search()", "params": { "table_name": table_name, "key": key, "value": value } } )

    table = self.dynamodb.Table(table_name)

    search_response = table.query( 
      KeyConditionExpression=Key(key).eq(value)
    )

    return search_response["Items"]
  
  @staticmethod
  def put(self, table_name, item):
    logger.info( { "method": "DynamoDB.put()", "params": { "table_name": table_name, "item": item } } )

    table = self.dynamodb.Table(table_name)

    table.put_item(Item=item)