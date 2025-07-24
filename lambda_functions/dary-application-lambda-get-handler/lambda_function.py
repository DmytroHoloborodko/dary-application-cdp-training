import json

from data_models import Response
from dynamodb_client import get_table

table = get_table()


def lambda_handler(event, context):
    path_params = event.get("pathParameters")

    try:
        result = get_post_by_id(path_params["id"]) if path_params and "id" in path_params else get_all_posts()
        return result.model_dump()

    except Exception as e:
        return Response(
            statusCode=500,
            body=str(e)
        ).model_dump()


def get_post_by_id(post_id) -> Response:
    response = table.get_item(Key={"id": post_id})
    item = response.get("Item")
    return Response(
        statusCode=200,
        body=json.dumps(item)
    )


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
            "id": "9957ffe0-afee-4e73-99b3-504c7f864d53"
        }
    }
    print(lambda_handler(event, None))
