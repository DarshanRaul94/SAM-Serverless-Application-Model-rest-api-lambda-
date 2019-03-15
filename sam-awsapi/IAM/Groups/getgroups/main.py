

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=str(event['queryStringParameters']['profile'])
    
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)

    iam=boto3.client('iam', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    groups=iam.list_groups()
    grouplist=[]
        
    for group in groups['Groups']:
            
        name=group['GroupName']
        arn=group['Arn']
        grouplist.append({"Name":name,"ARN":arn})
            
   
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "groups":grouplist
        }),
        "isBase64Encoded": False
    }