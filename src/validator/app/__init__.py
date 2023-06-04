import os
import uuid

import boto3
import ujson

from .validator import Validator, ValidShipment

sns_client = boto3.client("sns")


def lambda_handler(event: dict, context: object) -> bool:
    for record in event["Records"]:
        process_record(record, context.aws_request_id)

    return True


def process_record(record: dict, source: uuid.UUID):
    event_body = ujson.loads(record["body"])

    if event_body.get("should_fail", False):  # For testing purposes
        raise Exception("Should fail")

    shipment = {
        "weight": event_body["weight"],
        "length": event_body["length"],
        "width": event_body["width"],
        "height": event_body["height"],
    }

    valid_shipments = Validator(
        weight=shipment["weight"],
        length=shipment["length"],
        width=shipment["width"],
        height=shipment["height"],
    ).validate()

    if not valid_shipments:
        notify_about_invalid_shipment(shipment)

    notify_about_valid_shipments(valid_shipments, source)


def notify_about_valid_shipments(
    valid_shipments: list[ValidShipment], source: uuid.UUID
):
    sns_topic_arn = os.environ["SNS_VALID_SHIPMENT_TOPIC_ARN"]

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=ujson.dumps(valid_shipments),
        Subject="Valid shipments",
        MessageGroupId="default",
        MessageDeduplicationId=str(source),
    )


def notify_about_invalid_shipment(shipment: dict):
    sns_topic_arn = os.environ["SNS_EMAIL_TOPIC_ARN"]

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=f"Shipment with following parameters is invalid: {shipment}",
        Subject="Invalid shipment",
    )
