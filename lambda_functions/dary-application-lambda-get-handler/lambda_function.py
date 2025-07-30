import json

from data_models import Response
from dynamodb_client import get_table
from typing import TypedDict

table = get_table()


def lambda_handler(event, context):
    try:
        path_params = event.get("pathParameters")
        result = get_post_by_id(path_params["id"]) if path_params and "id" in path_params else get_all_posts()

    except Exception as e:
        result = Response(
            statusCode=500,
            body=str(e)
        )

    return result.model_dump()


def get_post_by_id(post_id: str) -> Response:
    response = table.get_item(Key={"id": post_id})
    # item = response.get("Item")
    if item := response.get("Item"):
        return Response(statusCode=200, body=json.dumps(item))
    return Response(statusCode=404, body=json.dumps({"error": "Post not found"}))


def get_all_posts() -> Response:
    response = table.scan()
    items = response.get('Items', [])
    return Response(
        statusCode=200,
        body=json.dumps(items)
    )


if __name__ == "__main__":
    event = {
        "pathParameters": {
            "id": "9f2320af-e78a-4cc5-b098-f0333c1ebfc"
        }
    }
    print(lambda_handler(event, None))
