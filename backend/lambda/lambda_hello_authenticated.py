def handler(event, context):

    print("Getting claims")

    claims = event["requestContext"]["authorizer"]["claims"]
    username = claims["cognito:username"]

    response_body = f"Hello, {username}! Welcome to the authenticated API."

    print(f"Returning to client: {response_body}")

    return {
        "statusCode": 200,
        "body": response_body
    }
