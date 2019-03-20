

import boto3
import firebase_auth as fa
import json

docker_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
"""
nginx_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
sudo docker run -d -p 80:80 nginx
"""
jenkins_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
sudo docker run -d -p 8080:8080 jenkinsci/blueocean
"""
elk_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
cd ~
git clone https://github.com/deviantony/docker-elk.git
cd docker-elk
sudo docker-compose up -d
"""

mean_script ="""#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo apt install -y docker-compose
docker run -i -t -d -p 80:3000 maccam912/meanjs 
"""

osdict={"Amazon_Linux":"ami-0937dcc711d38ef3f","Ubuntu":"ami-0d773a3b7bb2bb1c1","Red Hat Enterprise Linux 7.5":"ami-5b673c34"}
userdatadict={"Docker":docker_script,"Nginx":nginx_script,"Jenkins":jenkins_script,"Elk":elk_script,"Mean":mean_script}

def lambda_handler(event, context):
    profile_name=event['headers']['profile']
    body=json.loads(str(event['body']))
    os=body['os']
    instance_type=body['instance_type']
    count=body['count']
    keyname=body['keyname']
    app=body['app']
    
    
    ref = fa.getReference(profile_name)

    ec2=boto3.client('ec2', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
    
    ec2.run_instances( ImageId=str(osdict[str(os)]),
    InstanceType=str(instance_type),MaxCount=int(count),
    MinCount=int(count),KeyName=str(keyname),UserData=userdatadict[app])
  
    
    
    #print(buckets)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
           "instance ran successfully":os
        }),
        "isBase64Encoded": False
    }