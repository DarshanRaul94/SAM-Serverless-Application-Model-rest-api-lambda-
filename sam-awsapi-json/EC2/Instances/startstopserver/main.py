

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    body=json.loads(str(event['body']))
    instance_id=body['instance_id']
    running_state=body['running_state']
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)
    response=""
    ec2=boto3.client('ec2', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    if(str(running_state)=="running"):
        ec2.start_instances(InstanceIds=[
        str(instance_id)
        ])
        response="Server"+instance_id+"Started"
    elif(str(running_state)=="stopped"):
        ec2.stop_instances(InstanceIds=[
        str(instance_id)
        ])
        response="Server"+instance_id+"stopped"

    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "Status": response
        }),
        "isBase64Encoded": False
    }