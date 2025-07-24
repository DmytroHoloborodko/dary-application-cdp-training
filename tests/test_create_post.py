import json

import boto3
import pytest
from moto import mock_aws

from lambda_functions import create_post as post_handler


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="dary-application-dynamodb",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        table.wait_until_exists()
        yield table


def test_create_post():
    event = {
        "body": json.dumps({
            "title": "Test title",
            "body": "Test body",
            "tags": ["test", "tag"]
        })
    }

    response = post_handler.lambda_handler(event, None)

    assert response["statusCode"] == 201
    assert json.loads(response["body"])["title"] == "Test title"
