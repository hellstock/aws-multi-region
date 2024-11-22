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

Add role ARN HUSH_CDK_ROLE environment variable.here we assume `.env_hush` file.

Assume role to get temporary credentials.

   cd infrastructure
   source .env_hush
   source ./assume-role.sh

Configure AWS CLI with credentials and region

    aws configure

Test credentials by running:

    aws sts get-caller-identity

Above should return the role you were defining.

## Use Python virtual environment

    cd infrastructure
    python3 -m venv .venv
    source .venv/bin/activate

## Deploy stack

   cdk bootstrap
   cdk synth
   cdk deploy --require-approval any-change

## Iterating

   cdk diff

## Get endpoints

    aws apigateway get-rest-apis --query "items[*].[name,id]" --output table
    aws apigateway get-stages --rest-api-id <api-id> --query "item[*].[stageName,invokeUrl]" --output table
    aws apigateway get-integration --rest-api-id {api_id} --resource-id {resource_id} --http-method GET


## Troubleshooting

    cdk bootstrap -v

## Running tests

### Preparation

You need to add API GW base URL and AWS region to environment variables. For example add to `.env-tests` file:

    export HUSH_APIGW_URL=https://<your-api-gw-url-here>/prod
    export HUSH_AWS_REGION=<your-region-here>

For test running with python unit test framework, prepare this:

    cd tests/rest-api
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt

### Running API tests

    cd tests/rest-api
    python3 -m unittest api-test.py

## Limitations

Has been tested in Frankfurt (eu-central-1)
