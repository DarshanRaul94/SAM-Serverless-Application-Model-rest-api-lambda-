

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    body=json.loads(str(event['body']))
    group_name=body['group_name']
    ref = fa.getReference(profile_name)

    iam=boto3.client('iam', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    iam.create_group(GroupName=str(group_name))
    
            
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "group Created":group_name
        }),
        "isBase64Encoded": False
    }