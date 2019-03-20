#s3.delete_bucket(Bucket=str(bucket_name))

 
 
 

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    body=json.loads(str(event['body']))
    bucket_name=body['bucket_name']
    
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)

    s3=boto3.client('s3', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    s3.delete_bucket(Bucket=str(bucket_name))
    
    
    
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'Successful': "Bucket deleted "
        }),
        "isBase64Encoded": False
    }
 
 #s3.create_bucket(Bucket=str(bucket_name), CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})

        