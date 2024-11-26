import boto3
import botocore.exceptions
import os
import json

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMO_TABLE_NAME"]
table = dynamodb.Table(table_name)


def handler(event, context):

    print(f'Incoming event: {event}')

    http_method = event.get("httpMethod", "").upper()
    print(f"HTTP method: {http_method}")

    try:
        body = json.loads(event["body"])
        print(f"Request body: {body}")
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

    if not (tournament_id and match_id and player1 and player2 and score):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required fields"})
        }

    item = {
        "PK": f"TOURNAMENT#{tournament_id}",
        "SK": f"MATCH#{match_id}",
        "Player1": player1,
        "Player2": player2,
        "Score": score
    }

    print(f'Storing to Dynamo: {item}')

    try:
        if http_method == "PUT":
            table.put_item(Item=item)
        elif http_method == "POST":
            table.put_item(Item=item,
            ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)")
        else:
            # Should not be possible to come here unless Stack is wrongly configured,
            # but let's handle it anyway to be on the safe side.
            return {
                "statusCode": 405,
                "body": json.dumps({"error": f"HTTP method {http_method} not allowed"})
            }
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print('Item already exist, returning 409 to client')
            return {
                "statusCode": 409,
                "body": json.dumps({"error": "Match already exists"})
            }
        raise
    except Exception as e:
        print(f"Error writing to DynamoDB: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to save match result", "details": str(e)})
        }

    print("All good, returning 200 to client")

    # ToDo: Common return handling pattern with log included
    return {
        "statusCode": 200,
        "body": "Item saved successfully"
    }
