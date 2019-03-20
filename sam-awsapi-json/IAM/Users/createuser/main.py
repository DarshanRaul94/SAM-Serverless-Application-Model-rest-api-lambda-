

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    body=json.loads(str(event['body']))
    user_name=body['user_name']
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)

    iam=boto3.client('iam', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    iam.create_user(UserName=str(user_name))
    
            
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "user Created":user_name
        }),
        "isBase64Encoded": False
    }