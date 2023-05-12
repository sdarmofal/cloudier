import os

import boto3
import ujson

sqs = boto3.client("sqs")


def lambda_handler(event: dict, context: object) -> dict:
    queue_url = os.environ["QUEUE_URL"]

    # sqs.send_message(QueueUrl=queue_url, MessageBody=ujson.dumps(message))

    return {
        "statusCode": 200,
        "body": ujson.dumps({"message": queue_url}),
    }
