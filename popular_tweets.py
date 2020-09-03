import boto3
import tweepy

from utils.utils import Utils

auth = tweepy.OAuthHandler("7dFB2NWl4VoXHGtkdWwZywlH4", "DSnbtmsEStBXjpqzRRzywIbXun0IKopKM4tdbcUapTrZtAY8tw")
# auth.set_access_token("1234293662873460736-FS9OJMbD7JNdW2OgI13FxYUmJXC4Uu", "hnieCiQPK2xVyQlHVGDKo1zzbrRz33d6o3hF9rW00FWrY")
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Search_Metadata')

dynamodb_get_item_response = table.get_item(
  Key= {
    "result_type": "popular"
  }
)

if ("Item" not in dynamodb_get_item_response):
  search_results = api.search(q="coronavírus OR COVID-19 OR SARS-CoV-2", include_entities=1, lang="pt", result_type="popular", count=1)

  print(search_results)

# for status in search_results["statuses"]:
#   urls = Utils.get_entities_urls(status["entities"]["urls"])
#   print(urls)


