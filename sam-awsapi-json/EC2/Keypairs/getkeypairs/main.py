

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    ref = fa.getReference(profile_name)

    ec2=boto3.client('ec2', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    keypairdict={}
    keypairlist=[]
    keypairs=ec2.describe_key_pairs()
    for keypair in keypairs['KeyPairs']:
        keypairlist.append(keypair['KeyName'])
    
            
    
    
    
    #print(buckets)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "keypairs":keypairlist
        }),
        "isBase64Encoded": False
    }