import boto3
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMO_TABLE_NAME"]
table = dynamodb.Table(table_name)

def handler(event, context):
    tournament_id = event["tournament_id"]
    match_id = event["match_id"]
    player1 = event["player1"]
    player2 = event["player2"]
    score = event["score"]

    item = {
        "PK": f"TOURNAMENT#{tournament_id}",
        "SK": f"MATCH#{match_id}",
        "Player1": player1,
        "Player2": player2,
        "Score": score,
        "Timestamp": datetime.utcnow().isoformat(),
    }

    table.put_item(Item=item)

    return {"message": "Match result saved successfully!"}
