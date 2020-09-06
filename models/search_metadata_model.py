import re

from datetime import datetime
from models.dynamodb_model import DynamoDB

class SearchMetadata:
  def __init__(self, result_type, since_id):
    self.result_type = result_type
    self.since_id = since_id
    self.insertion_date = str(datetime.now())

  def json(self):
    return self.__dict__

  @classmethod
  def get_max_id_from_next_results(cls, next_results):
    next_results_max_id = re.search("(?<=\?max_id=).*?(?=&)", next_results)

    return next_results_max_id.group(0)
  
  @staticmethod
  def save_since_id(self, search_metadata, result_type):
    # Get since_id (max_id) from 'next_results' or "max_id_str"
    since_id = self.get_max_id_from_next_results(search_metadata["next_results"]) if result_type == "popular" else search_metadata["max_id_str"]

    search_metadata_obj = SearchMetadata(result_type, since_id)

    # Save since_id on DynamoDB
    DynamoDB.put(DynamoDB, "Search_Metadata", search_metadata_obj.json())
    