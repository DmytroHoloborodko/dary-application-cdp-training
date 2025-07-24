import json

from data_models import Response
from dynamodb_client import get_table
from utils import now_utc

ALLOWED_FIELDS = ["title", "body", "tags"]

table = get_table()


def lambda_handler(event, context):
    try:
        post_id = event.get("pathParameters")["id"]
        body = json.loads(event.get("body", "{}"))

        update_fields = {}

        # Build update fields only from an allowed list
        for field in ALLOWED_FIELDS:
            if field in body:
                update_fields[field] = body[field]

        if update_fields:
            update_fields["updatedDate"] = now_utc()

            # Build UpdateExpression and ExpressionAttributeValues
            update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
            expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
            expr_attr_names = {f"#{k}": k for k in update_fields}

            response = table.update_item(
                Key={"id": post_id},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW"
            )

            updated_item = response.get("Attributes", {})
            result = Response(statusCode=200, body=json.dumps(updated_item))
        else:
            result = Response(statusCode=400, body=json.dumps({"error": "No valid fields to update"}))

    except Exception as e:
        result = Response(statusCode=500, body=str(e))

    return result.model_dump()
