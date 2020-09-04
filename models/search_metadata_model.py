class SearchMetadata:
  def __init__(self, result_type, since_id):
    self.result_type = result_type
    self.since_id = since_id

  def json(self):
    return self.__dict__