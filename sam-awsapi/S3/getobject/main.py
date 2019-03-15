 
 
 

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=str(event['queryStringParameters']['profile'])
    bucket_name=str(event['pathParameters']['bucket_name'])
   
    ref = fa.getReference(profile_name)

    s3=boto3.client('s3', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    objectlist=[]
    objects=s3.list_objects_v2(Bucket=str(bucket_name))
    print(objects)
    if(objects['KeyCount']!=0):
        for object in objects['Contents']:
            objectlist.append(object['Key'])
        
 
    
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            bucket_name:objectlist
        }),
        "isBase64Encoded": False
    }
 
 #s3.create_bucket(Bucket=str(bucket_name), CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
