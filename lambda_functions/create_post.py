import json

from data_models import Response, Post
from dynamodb_client import get_table
from utils import generate_post_id, now_utc

table = get_table()


def lambda_handler(event, context):
    try:
        now = now_utc()
        post = Post(**json.loads(event['body']), id=generate_post_id(), createdDate=now, updatedDate=now)

        table.put_item(Item=post.model_dump(mode="json"))

        return Response(
            statusCode=201,
            body=json.dumps(post.model_dump(mode="json"))
        ).model_dump()

    except Exception as e:
        return Response(
            statusCode=500,
            body=str(e)
        ).model_dump()


if __name__ == "__main__":
    test_event = {
        'resource': '/posts',
        'path': '/posts',
        'httpMethod': 'POST',
        'body': '{\r\n    "title": "Test title",\r\n    "body": "Test body",\r\n    "tags": [\r\n        "test",\r\n        "tag"\r\n    ]\r\n}'
    }
    print(lambda_handler(test_event, None))
