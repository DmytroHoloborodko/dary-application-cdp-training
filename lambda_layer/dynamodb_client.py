import json
import os

import boto3
from botocore.exceptions import ClientError


def get_table():
    secret_name = os.environ.get('TABLE_NAME_SECRET') or "dev/DynamoDB/tablename"
    table_name = fetch_secret(secret_name)['dynamo-table-name']

    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table_name)


def fetch_secret(secret_name: str) -> dict:
    secrets_client = boto3.client("secretsmanager")

    try:
        get_secret_value_response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # to do some things
        raise e

    return json.loads(get_secret_value_response['SecretString'])
