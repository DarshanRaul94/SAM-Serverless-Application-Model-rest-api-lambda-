

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    
    group_name=str(event['pathParameters']['group_name'])
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)

    iam=boto3.client('iam', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    group_details=iam.get_group(
         GroupName=str(group_name)
        )
    
            
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "group Details":str(group_details)
        }),
        "isBase64Encoded": False
    }