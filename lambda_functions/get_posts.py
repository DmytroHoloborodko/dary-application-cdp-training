import json
from dynamodb_client import get_table

def lambda_handler(event, context):
    table = get_table()

    path_params = event.get("pathParameters")

    try:

        if path_params and "id" in path_params:
            # Handle GET /post/{id}
            post_id = path_params["id"]

            response = table.get_item(Key={"id": post_id})
            item = response.get("Item")
            print(item)
            return {
                "statusCode": 200,
                "body": json.dumps(item),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        response = table.scan()
        print(response)
        items = response.get('Items', [])

        return {
            "statusCode": 200,
            "body": json.dumps(items),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

if __name__ == "__main__":
    event = {
        "pathParameters": {
            "id": "9957ffe0-afee-4e73-99b3-504c7f864d53"
        }
    }
    lambda_handler(event, None)
