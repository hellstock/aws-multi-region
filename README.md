# aws-multi-region

Hello world demo of multi-region AWS deployment with Python CDK, testing with RobotFW

## Requirements for environment

Pip needs to be installed
Python 3 needs to be installed

## Prepare CDK related things

    cd infrastructure
    pip install -r requirements.txt
    npm install -g aws-cdk

## Use virtual environment

    cd infrastructure
    source .venv/bin/activate


## Deploy stack

   cdk bootstrap
   cdk synth
   cdk deploy


## Limitations

Has been tested in Frankfurt (eu-central-1)
