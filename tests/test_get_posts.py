import json
from uuid import uuid4

import boto3
import pytest
from moto import mock_aws

from lambda_functions import get_post as get_handler


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


def test_get_posts(dynamodb_table):
    dynamodb_table.put_item(Item={
        "id": str(uuid4()),
        "title": "Post 1",
        "body": "Content 1",
        "tags": ["tag1"],
        "createdDate": "2025-07-15T12:00:00Z",
        "updatedDate": "2025-07-15T12:00:00Z"
    })
    dynamodb_table.put_item(Item={
        "id": str(uuid4()),
        "title": "Post 2",
        "body": "Content 2",
        "tags": ["tag2"],
        "createdDate": "2025-07-15T12:01:00Z",
        "updatedDate": "2025-07-15T12:01:00Z"
    })

    response = get_handler.lambda_handler({}, None)

    assert response["statusCode"] == 200

    posts = json.loads(response["body"])
    assert isinstance(posts, list)
    assert len(posts) == 2
    assert all("title" in post for post in posts)
