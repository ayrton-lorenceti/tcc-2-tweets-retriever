import boto3
from boto3.dynamodb.conditions import Key

class DynamoDB:
  dynamodb = boto3.resource('dynamodb')

  def __init__(self):
    self
  
  @staticmethod
  def search(self, table_name, key, value):
    table = self.dynamodb.Table(table_name)

    search_response = table.query( 
      KeyConditionExpression=Key(key).eq(value)
    )

    return search_response["Items"]
  
  @staticmethod
  def put(self, table_name, item):
    table = self.dynamodb.Table(table_name)

    table.put_item(Item=item)