import os

import boto3
import ujson

sqs_client = boto3.client("sqs")


def lambda_handler(event: dict, context: object) -> dict:
    queue_url = os.environ["QUEUE_URL"]
    event_body = ujson.loads(event["body"])

    try:
        message = {
            "source": context.aws_request_id,
            "weight": event_body["weight"],
            "length": event_body["length"],
            "width": event_body["width"],
            "height": event_body["height"],
            "should_fail": event_body.get("should_fail", False),
        }
    except KeyError:
        return {"statusCode": 400, "body": "Invalid request"}

    sqs_client.send_message(
        QueueUrl=queue_url, MessageGroupId="default", MessageBody=ujson.dumps(message)
    )

    return {"statusCode": 202}
