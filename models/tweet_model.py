from datetime import datetime

from models.dynamodb_model import DynamoDB

class Tweet:
  def __init__(self, id_str, text, urls):
    self.id_str = id_str
    self.text = text
    self.urls = urls
    self.insertion_date = str(datetime.now())
  
  @staticmethod
  def get_entities_urls(urls):
    return [url["expanded_url"] for url in urls if "expanded_url" in url]

  def json(self):
    return self.__dict__

  def json_with_string_set(self):
    return {
      "id_str": self.id_str,
      "text": self.text,
      "urls": set(self.urls),
      "insertion_date": self.insertion_date
    }

  def iterate_over_tweets_and_save(self, statuses):
    # tweets_saved = 0

    # Iterate over every tweet
    for status in statuses:
      tweet = Tweet(status["id_str"], status["text"], Tweet.get_entities_urls(status["entities"]["urls"]))
      
      # Search tweet on DynamoDB
      dynamodb_tweet_response = DynamoDB.search(DynamoDB, "Tweets", "id_str", tweet.id_str)

      # If already has tweet on DynamoDB, go to the next tweet
      if (len(dynamodb_tweet_response) > 0):
        continue
      
      # If hasn't found tweet on DynamoDB, save it
      DynamoDB.put(DynamoDB, "Tweets", tweet.json_with_string_set())