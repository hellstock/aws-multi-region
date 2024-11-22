#!/bin/bash

if [ -z "$HUSH_CDK_ROLE" ]; then
  echo "Error: HUSH_CDK_ROLE environment variable is not set."
  exit 1
fi

ROLE_ARN="$HUSH_CDK_ROLE"
SESSION_NAME="CDKRoleSession"

CREDS=$(aws sts assume-role --role-arn $ROLE_ARN --role-session-name $SESSION_NAME)

export AWS_ACCESS_KEY_ID=$(echo $CREDS | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo $CREDS | jq -r '.Credentials.SessionToken')

echo "Temporary credentials set for AWS CLI/SDK use."
