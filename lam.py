import boto3
import botocore.config
import json
from datetime import datetime


def generate_code_using_bedrock(message:str) ->str:


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
        bedrock = boto3.client("bedrock-runtime",region_name="us-west-2",config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dumps(body),modelId="anthropic.claude-3-sonnet-20240229-v1:0")
        response_content = response.get('body').read().decode('utf-8')
        # print(response_content)
        response_data = json.loads(response_content)
        # print(response_data)
        
        textdata = response_data['content'][0]['text']
        # print(textdata)
        return textdata
        

    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""

def save_code_to_s3_bucket(textdata, s3_bucket, s3_key):

    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = textdata)
        print("Code saved to s3")

    except Exception as e:
        print("Error when saving the code to s3")

def lambda_handler(event, context):
    event = json.loads(event['body'])
    message = event['message']
    # language = event['key']
    # print(message, language)

    generated_code = generate_code_using_bedrock(message)

    if generated_code:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'code-output/{current_time}.py'
        s3_bucket = 'awscodegen'

        save_code_to_s3_bucket(generated_code,s3_bucket,s3_key)

    else:
        print("No code was generated")
    # return textdata

    return {
        'statusCode':200,
        'body':json.dumps(generated_code)

    }
