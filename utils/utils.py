class Utils:
  def __init__(self):
    self

  @staticmethod
  def get_entities_urls(urls):
    return [url["expanded_url"] for url in urls if "expanded_url" in url]