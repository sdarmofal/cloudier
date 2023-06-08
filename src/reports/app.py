import datetime
import os

import psycopg2
import ujson


def lambda_handler(event: dict, context: object) -> dict:
    result = get_report_for_date_range(
        event["queryStringParameters"]["date_from"],
        event["queryStringParameters"]["date_to"],
    )

    return {
        "statusCode": 200,
        "body": ujson.dumps(
            [
                {
                    "amount": amount,
                    "currency": currency,
                }
                for amount, currency in result
            ]
        ),
    }


def get_report_for_date_range(date_from: datetime.date, date_to: datetime.date) -> list:
    host = os.environ["RDS_HOST"]
    port = os.environ["RDS_PORT"]
    username = os.environ["RDS_USERNAME"]
    password = os.environ["RDS_PASSWORD"]

    conn = psycopg2.connect(
        host=host, port=port, database="postgres", user=username, password=password
    )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(price), currency FROM orders WHERE created_at BETWEEN SYMMETRIC %s AND %s GROUP BY currency",
        (
            date_from,
            date_to,
        ),
    )

    result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return result
