import os

import boto3
import ujson

from .app_logger import app_logger
from .estimator import EstimationError, Estimator
from .interface import EstimatedShipment

sns_client = boto3.client("sns")


def lambda_handler(event: dict, context: object) -> bool:
    for record in event["Records"]:
        process_record(record, context.aws_request_id)

    return True


def process_record(record: dict, source: str):
    event_body = ujson.loads(record["body"])["Message"]
    event_body = ujson.loads(event_body)

    valid_shipments = [
        {
            "carrier": valid_shipment["carrier"],
            "weight": valid_shipment["weight"],
            "length": valid_shipment["length"],
            "width": valid_shipment["width"],
            "height": valid_shipment["height"],
            "is_sortable": valid_shipment["is_sortable"],
        }
        for valid_shipment in event_body
    ]

    try:
        carrier, estimated_shipment = Estimator(valid_shipments).estimate()
    except EstimationError as exception:
        notify_about_not_estimatable_shipment(valid_shipments, source)
        app_logger.error(f"Cannot estimate shipment", exc_info=exception)
        return

    notify_about_estimated_shipments(carrier, estimated_shipment, source)


def notify_about_estimated_shipments(
    carrier: str, estimated_shipment: EstimatedShipment, source: str
):
    sns_topic_arn = os.environ["SNS_ESTIMATED_SHIPMENT_TOPIC_ARN"]

    shipment_to_notify = {
        "carrier": carrier,
        **estimated_shipment,
        "price": {
            "amount": str(estimated_shipment["price"].amount),
            "currency": estimated_shipment["price"].currency.value,
        },
        "source": source,
    }
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=ujson.dumps(shipment_to_notify),
        Subject="Estimated shipment",
        MessageGroupId="default",
    )


def notify_about_not_estimatable_shipment(shipments: list[dict], source: str):
    sns_topic_arn = os.environ["SNS_INVALID_SHIPMENT_NOTIFICATION"]

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=f"Shipments with following parameters are invalid and cannot be estimated: {shipments}. Source: {source}",
        Subject="Invalid shipment",
    )
