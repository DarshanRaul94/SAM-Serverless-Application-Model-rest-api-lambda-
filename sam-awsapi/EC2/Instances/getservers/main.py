

import boto3
import firebase_auth as fa
import json

def lambda_handler(event, context):
    profile_name=str(event['queryStringParameters']['profile'])
    #profile_name = str(event["profile"])
    #profile_name = str(event['params']['querystring']['profile'])
    ref = fa.getReference(profile_name)

    ec2=boto3.client('ec2', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    serverdict={}
    serverlist=[]
    count=0
    servers=ec2.describe_instances()
    for reservation in servers['Reservations']:
        for inst in reservation['Instances']:
            count+=1
            name=inst['InstanceId']
            state=inst['State']['Name']
            print(name)
            print(state)
            serverid="server"+str(count)
            serverlist.append({ "instance id":name,"state":state})   
         
            
    
    
    
    #print(buckets)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "servers":serverlist
        }),
        "isBase64Encoded": False
    }