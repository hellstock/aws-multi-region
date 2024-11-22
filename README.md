# aws-multi-region

Hello world demo of multi-region AWS deployment with Python CDK, testing with RobotFW

## Requirements for environment

Pip needs to be installed
Python 3 needs to be installed

## Prepare CDK related things

    cd infrastructure
    pip install -r requirements.txt
    npm install -g aws-cdk

## Prepare AWS Account

Create role "cdk-role" etc. to be used. Add "Maximum session duration" to 12h for convenience.

Add role ARN HUSH_CDK_ROLE environment variable, here we assume `.env_hush` file.

Assume role to get temporary credentials.

   cd infrastructure
   source .env_hush
   source ./assume-role.sh

Configure AWS CLI with credentials and region

    aws configure

Test credentials by running:

    aws sts get-caller-identity

Above should return the role you were defining.

## Use Pyhton virtual environment

    cd infrastructure
    source .venv/bin/activate

## Deploy stack

   cdk bootstrap
   cdk synth
   cdk deploy --require-approval everything

## Iterating

   cdk diff

## Get endpoints

    aws apigateway get-rest-apis --query "items[*].[name,id]" --output table
    aws apigateway get-stages --rest-api-id <api-id> --query "item[*].[stageName,invokeUrl]" --output table
    aws apigateway get-integration --rest-api-id {api_id} --resource-id {resource_id} --http-method GET


## Troubleshooting

    cdk bootstrap -v

## Limitations

Has been tested in Frankfurt (eu-central-1)
