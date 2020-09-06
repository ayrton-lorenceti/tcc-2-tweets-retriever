import re

from datetime import datetime
from models.dynamodb_model import DynamoDB
from loguru import logger

class SearchMetadata:
  def __init__(self, result_type, since_id):
    self.result_type = result_type
    self.since_id = since_id
    self.insertion_date = str(datetime.now())

  def json(self):
    return self.__dict__
  
  @staticmethod
  def save_since_id(next_results):
    logger.info( { "method": "SearchMetadata.save_since_id()", "params": { "next_result": next_results } } )

    # Get since_id (max_id) from 'next_results'
    next_results_max_id = re.search("(?<=\?max_id=).*?(?=&)", next_results)

    search_metadata = SearchMetadata("popular", next_results_max_id.group(0))

    # Save since_id on DynamoDB
    DynamoDB.put(DynamoDB, "Search_Metadata", search_metadata.json())
    