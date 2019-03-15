

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=str(event['queryStringParameters']['profile'])
    
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)

    iam=boto3.client('iam', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    userdict={}
    count=0
    users=iam.list_users()
    userlist=[]
    print(users)
    for user in users['Users']:
        count+=1
        name=user['UserName']
        userid="user"+str(count)
        userlist.append({"Username":name})
            
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "users":userlist
        }),
        "isBase64Encoded": False
    }