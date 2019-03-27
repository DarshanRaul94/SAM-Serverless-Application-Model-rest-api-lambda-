 
 
 

import boto3
import firebase_auth as fa
import json


def lambda_handler(event, context):
  profile_name=event['headers']['profile']
  
  
  ref = fa.getReference(profile_name)
  template='''{
    "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "AWS CloudFormation Template Description",



  "Resources" : {
    
  }
  }'''
  cfn=boto3.client('cloudformation', region_name=str(ref.get()['region']), aws_access_key_id=str(ref.get()['access_key']), aws_secret_access_key=str(ref.get()['secret_access_key']))
     
  s3_bucket_type="AWS::S3::Bucket"
  iam_user_type="AWS::IAM::User"
  iam_group_type="AWS::IAM::Group"


  stack=json.loads(template)
  resources=stack["Resources"]

  body=json.loads(str(event["body"]))


  resourcetypes = { 
    "S3Bucket": s3_bucket_type, 
    "IAMUser": iam_user_type,
    "IAMGroup": iam_group_type
  } 

  def gettype(res_type):
    return resourcetypes.get(res_type,"nothing") 

  for resource in body:
    resource_name=resource["resource_name"]
    print(resource_name)

    resource_type=gettype(resource["resource_type"])
    print(resource_type)
    subdict={"Properties":{}}
    subdict["Type"]=resource_type
    for property in resource["Properties"]:
      subdict["Properties"].update(
      {property:resource["Properties"][property]}## unsual jugaad but need to use it as I dont know the amount of properties that may come
      )  
      #print(property)
      #print(resource["Properties"][property])## unsual jugaad but need to use it as I dont know the amount of properties that may come
    print(subdict)
    resources.update({resource_name:subdict})
  
  j = json.dumps(stack, indent=4)

  cfn.create_stack(
    StackName="test",
    TemplateBody=str(j),
    
    OnFailure='ROLLBACK',
    EnableTerminationProtection=True,
    Capabilities=[
        'CAPABILITY_NAMED_IAM'
    ]
  )
    
  return {
        'statusCode': 200,
        'body': j
  }
