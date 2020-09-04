import json

class Tweet:
  def __init__(self, id_str, text, urls):
    self.id_str = id_str
    self.text = text
    self.urls = urls
  
  @staticmethod
  def get_entities_urls(urls):
    return [url["expanded_url"] for url in urls if "expanded_url" in url]

  def json(self):
    return self.__dict__