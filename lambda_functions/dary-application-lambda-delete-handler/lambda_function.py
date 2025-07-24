import json

from data_models import Response
from dynamodb_client import get_table

table = get_table()


def lambda_handler(event, context):
    post_id = event.get("pathParameters")["id"]

    try:
        # First check if item exists
        response = table.get_item(Key={"id": post_id})
        if "Item" not in response:
            result = Response(
                statusCode=404,
                body=json.dumps({"error": "Post not found"})
            )
        else:
            # Delete the item
            table.delete_item(Key={"id": post_id})

            result = Response(statusCode=204)

    except Exception as e:
        result = Response(
            statusCode=500,
            body=str(e)
        )

    return result.model_dump()
