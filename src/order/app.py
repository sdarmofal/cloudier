import os
import uuid

import psycopg2
import ujson


def lambda_handler(event: dict, context: object) -> bool:
    for record in event["Records"]:
        process_record(record, context.aws_request_id)

    return True


def process_record(record: dict, source: uuid.UUID):
    event_body = ujson.loads(record["body"])["Message"]
    event_body = ujson.loads(event_body)

    shipment = {
        "carrier": event_body["carrier"],
        "weight": event_body["weight"],
        "length": event_body["length"],
        "width": event_body["width"],
        "height": event_body["height"],
        "is_sortable": event_body["is_sortable"],
        "price": {
            "amount": event_body["price"]["amount"],
            "currency": event_body["price"]["currency"],
        },
    }

    # There should be some order logic

    persist_order(shipment, source)


def persist_order(shipment: dict, source_id: uuid):
    host = os.environ["RDS_HOST"]
    port = os.environ["RDS_PORT"]
    username = os.environ["RDS_USERNAME"]
    password = os.environ["RDS_PASSWORD"]

    conn = psycopg2.connect(
        host=host, port=port, database="postgres", user=username, password=password
    )

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (carrier, weight, length, width, height, is_sortable, price, currency, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            shipment["carrier"],
            shipment["weight"],
            shipment["length"],
            shipment["width"],
            shipment["height"],
            shipment["is_sortable"],
            shipment["price"]["amount"],
            shipment["price"]["currency"],
            source_id,
        ),
    )

    conn.commit()
    cursor.close()
    conn.close()
