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
    event_body = ujson.loads(record["body"])

    shipment = {
        "weight": event_body["weight"],
        "length": event_body["length"],
        "width": event_body["width"],
        "height": event_body["height"],
        "is_sortable": event_body["is_sortable"],
    }

    try:
        carrier, estimated_shipment = Estimator(**shipment).estimate()
    except EstimationError as exception:
        notify_about_not_estimatable_shipment(shipment, source)
        app_logger.error(f"Cannot estimate shipment for {shipment}", exc_info=exception)
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


def notify_about_not_estimatable_shipment(shipment: dict, source: str):
    sns_topic_arn = os.environ["SNS_INVALID_SHIPMENT_NOTIFICATION"]

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=f"Shipment with following parameters is invalid and cannot be estimated: {shipment}. Source: {source}",
        Subject="Invalid shipment",
    )
