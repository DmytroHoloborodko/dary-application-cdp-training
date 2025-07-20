import json

from dynamodb_client import get_table
from utils import generate_post_id, now_utc

table = get_table()


def lambda_handler(event, context):
    print("" + str(event))
    print(context)
    try:

        title = event.get("title")
        content = event.get("body")
        tags = event.get("tags", [])

        if not title or not content or not tags:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing at least one of required fields: title, body or tags"})
            }

        if not isinstance(tags, list):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Tags must be a list of strings"})
            }

        # Generate post metadata
        post_id = generate_post_id()
        now = now_utc()

        item = {
            "id": post_id,
            "title": title,
            "body": content,
            "tags": tags,
            "createdDate": now,
            "updatedDate": now
        }

        # Save to DynamoDB
        table.put_item(Item=item)
        print(item)

        return item

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


if __name__ == "__main__":
    # test how it runs on aws
    event = {
        "title": "Test title",
        "body": "Test body",
        "tags": ["test", "tag"]
    }
    lambda_handler(event, None)
