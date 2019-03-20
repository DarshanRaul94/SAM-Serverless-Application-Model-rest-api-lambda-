

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    
    
    ref = fa.getReference(profile_name)

    s3=boto3.client('s3', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    buckets=s3.list_buckets()
    bucketlist=[]
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
    
    objectdict={}
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
        for bucket in bucketlist:
            print(bucket)
            objectlist=[]
            objects=s3.list_objects(Bucket=str(bucket))
            print(objects)

            for object in objects['Contents']:
                objectlist.append(object['Key'])
                objectdict.update({bucket:objectlist})
        

    
    #print(buckets)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            objectdict
        }),
        "isBase64Encoded": False
    }


        