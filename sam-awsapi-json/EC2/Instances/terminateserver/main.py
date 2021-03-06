

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    instance_id=str(event['pathParameters']['instance_id'])
    ref = fa.getReference(profile_name)

    ec2=boto3.client('ec2', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    ec2.terminate_instances(InstanceIds=[str(instance_id)])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "server Terminated":instance_id
        }),
        "isBase64Encoded": False
    }