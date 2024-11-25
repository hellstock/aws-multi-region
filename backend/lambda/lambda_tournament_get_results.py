import boto3
import os

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMO_TABLE_NAME"]
table = dynamodb.Table(table_name)

def handler(event, context):
    tournament_id = event["pathParameters"].get("tournamentId")

    if not tournament_id:
        return {
            "statusCode": 400,
            "body": "Error: tournamentId is required in the path"
        }

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq(f"TOURNAMENT#{tournament_id}")
    )

    return {"results": response.get("Items", [])}
