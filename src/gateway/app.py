import os

import boto3
import ujson

sqs_client = boto3.client("sqs")


def lambda_handler(event: dict, context: object) -> dict:
    queue_url = os.environ["QUEUE_URL"]

    try:
        message = {
            "weight": event["weight"],
            "length": event["length"],
            "width": event["width"],
            "height": event["height"],
        }
    except KeyError:
        return {"statusCode": 400, "body": "Invalid request"}

    sqs_client.send_message(
        QueueUrl=queue_url, MessageGroupId="default", MessageBody=ujson.dumps(message)
    )

    return {"statusCode": 202}
