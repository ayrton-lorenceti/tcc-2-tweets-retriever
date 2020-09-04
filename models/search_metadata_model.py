from datetime import datetime

class SearchMetadata:
  def __init__(self, result_type, since_id):
    self.result_type = result_type
    self.since_id = since_id
    self.insertion_date = str(datetime.now())

  def json(self):
    return self.__dict__