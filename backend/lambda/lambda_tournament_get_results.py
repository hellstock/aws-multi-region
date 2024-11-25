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

    print(f'Got request to get results of tournament: {tournament_id}')

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq(f"TOURNAMENT#{tournament_id}")
    )

    if not response["Items"]:
        print('No results found for tournament, returning 404 to client')
        return {
            "statusCode": 404,
            "body": f"Tournament with ID '{tournament_id}' not found."
        }

    response_items = response.get("Items", [])

    print(f'Returning to client: {response_items}')

    return {"results": response_items}
