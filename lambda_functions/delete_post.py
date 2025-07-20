import json
from dynamodb_client import get_table

def lambda_handler(event, context):
    table = get_table()
    path_params = event.get("pathParameters")

    if not path_params or "id" not in path_params:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing path parameter 'id'"}),
            "headers": {"Content-Type": "application/json"}
        }

    post_id = path_params["id"]

    try:
        # First check if item exists
        response = table.get_item(Key={"id": post_id})
        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Post not found"}),
                "headers": {"Content-Type": "application/json"}
            }

        # Delete the item
        table.delete_item(Key={"id": post_id})

        return {
            "statusCode": 204,
            "body": "",
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
