import boto3

client = boto3.client('ssm')

response = client.get_parameters(
    Names=[
        'consumer_key',
    ],
    WithDecryption=False
)
print(response["Parameters"][0]["Value"])