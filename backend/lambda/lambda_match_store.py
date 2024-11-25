import boto3
import os
import json

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMO_TABLE_NAME"]
table = dynamodb.Table(table_name)

def handler(event, context):

    print(f'Incoming event: {event}')

    try:
        body = json.loads(event["body"])
    except (KeyError, json.JSONDecodeError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid request body"})
        }

    tournament_id = body.get("tournament_id")
    match_id = body.get("match_id")
    player1 = body.get("player1")
    player2 = body.get("player2")
    score = body.get("score")

    item = {
        "PK": f"TOURNAMENT#{tournament_id}",
        "SK": f"MATCH#{match_id}",
        "Player1": player1,
        "Player2": player2,
        "Score": score
    }

    print(f'Storing to Dynamo: {item}')

    try:
        table.put_item(Item=item)
    except Exception as e:
        print(f"Error writing to DynamoDB: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to save match result", "details": str(e)})
        }

    return {"message": "Match result saved successfully!"}
