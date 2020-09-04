from datetime import date, timedelta

import boto3
import tweepy

from models.tweet_model import Tweet

auth = tweepy.OAuthHandler("7dFB2NWl4VoXHGtkdWwZywlH4", "DSnbtmsEStBXjpqzRRzywIbXun0IKopKM4tdbcUapTrZtAY8tw")
# auth.set_access_token("1234293662873460736-FS9OJMbD7JNdW2OgI13FxYUmJXC4Uu", "hnieCiQPK2xVyQlHVGDKo1zzbrRz33d6o3hF9rW00FWrY")
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Search_Metadata')

# tweet = Tweet("aaa", "bbbb", "asdasdsad")
# print(tweet.id_str)


dynamodb_search_metadata_response = table.get_item(
  Key= {
    "result_type": "popular"
  }
)

if ("Item" not in dynamodb_search_metadata_response):
  until_param = date.today() - timedelta(days = 7)

  search_results = api.search(q="coronavírus OR COVID-19 OR SARS-CoV-2", include_entities=1, lang="pt", result_type="popular", count=2, until=until_param)

  if (len(search_results["statuses"]) == 0):
    quit() #return

  for status in search_results["statuses"]:
    tweet = Tweet(status["id_str"], status["text"], Tweet.get_entities_urls(status["entities"]["urls"]))
    
    table = dynamodb.Table("Tweet")

    dynamodb_tweet_response = table.get_item(
      Key= {
        "id_str": tweet.id_str
      }
    )

    if ("Item" in dynamodb_tweet_response):
      break


