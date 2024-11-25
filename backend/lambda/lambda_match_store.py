import boto3
import os
import json
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMO_TABLE_NAME"]
table = dynamodb.Table(table_name)

def handler(event, context):

    print(f'Incoming event: {event}')

    try:
        body = json.loads(event["body"])  # Extract and parse the request body
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
        "Score": score,
        "Timestamp": datetime.utcnow().isoformat(),
    }

    print(f'Storing to Dynamo: {item}')

    table.put_item(Item=item)

    return {"message": "Match result saved successfully!"}
