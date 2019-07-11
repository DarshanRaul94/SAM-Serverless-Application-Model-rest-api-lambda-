# AWS SAM(Serverless Application Model) Python Lambda API application

This is the code for the Serverless backend I have created for my project on AWS lambda [AWS Konsole](https://github.com/darshan-raul/awsdashboard).

## Steps to deploy a SAM application

#### REQUIREMENTS:


* AWS CLI already configured with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* [SAM CLI installed](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

#### Initialize a sample application 

Initialize a sample application from a template using ```sam init --runtime <runtime_name> --name <app_name>```

#### Similar structure will be created:
```
    ├── README.md                   <-- This instructions file
├── event.json                  <-- API Gateway Proxy Integration event payload
├── hello_world                 <-- Source code for a lambda function
│   ├── __init__.py
│   ├── app.py                  <-- Lambda function code
│   ├── requirements.txt        <-- Lambda function code
├── template.yaml               <-- SAM Template
└── tests                       <-- Unit tests
    └── unit
        ├── __init__.py
        └── test_handler.py
```


#### Local development
After doing the changes to the template you can test it locally

**Invoking function locally using a local sample payload**

```bash
sam local invoke HelloWorldFunction --event event.json
```

**Invoking function locally through local API Gateway**

```bash
sam local start-api
```

If the previous command ran successfully you should now be able to hit the following local endpoint to invoke your function `http://localhost:3000/hello`

**SAM CLI** is used to emulate both Lambda and API Gateway locally and uses our `template.yaml` to understand how to bootstrap this environment (runtime, where the source code is, etc.) 


#### Creating a bucket for the templates

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```
#### Packaging the template

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

#### Deploying the template

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-awsapi \
    --capabilities CAPABILITY_IAM
```


##### Tips for python code

- Python packages have to be installed in the path: `/opt/python/lib/python3.6<3.7>/site-packages`
- **Lambda-layers** To use Lambda Layers use the following steps:
    - Create a lambda_layers folder
    - Create the following folder structure in this folder : lambda_layers/python/lib/python3.6/site-packages
    - Create all the python files you want to create in the site-packages folder
    - Install all the pip packages you need ```pip install -r requirements.txt -t <dir>```
    - Create a data folder if you need to use any JSON files
    - zip all the folders and name it lambda-layers.zip
    - in the template.yaml file mention this property in each serverless function:
    ``` 
    Layers:
        - !Ref MyLambdaLayer
    ```
