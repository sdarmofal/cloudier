import os

import boto3
import ujson

sns_client = boto3.client("sns")


def lambda_handler(event: dict, context: object) -> dict:
    sns_topic_arn = os.environ["SNS_ARN"]

    for record in event["Records"]:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=ujson.dumps(record),
            Subject="Invalid shipment",
        )

    return {"statusCode": 200}
