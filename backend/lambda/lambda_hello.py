import os


def handler(event, context):
    region = os.environ.get('AWS_REGION', 'Unknown Region')

    response_string = f"Hello from Hush Lambda in {region}!"
    print(f"Returning to client: {response_string}")

    return {
        "statusCode": 200,
        "body": response_string
    }
