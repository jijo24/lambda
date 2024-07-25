import boto3
import botocore.config
import json
from datetime import datetime


def generate_data(message:str) ->str:


    body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": message
          }
        ]
      }
    ]
    }

    try:
        bedrock = boto3.client("bedrock-runtime",region_name="us-east-1",config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dumps(body),modelId="anthropic.claude-3-sonnet-20240229-v1:0")
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        textdata = response_data['content'][0]['text']
        return textdata
        

    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""



def lambda_handler(event, context):
    event = json.loads(event['body'])
    message = event['message']

    generaterdata = generate_data(message)

    if generaterdata:
        print("Data was generated")
    else:
        print("No Data was generated")


    return {
        'statusCode':200,
        'body':json.dumps(generaterdata)

    }
