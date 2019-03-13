
import boto3
import json



def lambda_handler(event, context):
    
    s3=boto3.client('s3')
    buckets=s3.list_buckets()
    bucketlist=[]
    for i in buckets['Buckets']:
        bucket= i['Name']
        bucketlist.append(bucket)
    
    
    #print(buckets)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'buckets': bucketlist
        }),
        "isBase64Encoded": False
    }

