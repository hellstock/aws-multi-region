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

Create role "cdk-role" etc. to be used.

Add role ARN HUSH_CDK_ROLE environment variable

Assume role to get temporary credentials.

   cd infrastructure
   ./assume-role.sh

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

## Troubleshooting

    cdk bootstrap -v

## Limitations

Has been tested in Frankfurt (eu-central-1)
