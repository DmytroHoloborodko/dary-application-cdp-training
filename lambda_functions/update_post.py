import json
from dynamodb_client import get_table
from utils import now_utc

def lambda_handler(event, context):
    table = get_table()
    path_params = event.get("pathParameters")
    body = json.loads(event.get("body", "{}"))

    if not path_params or "id" not in path_params:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing path parameter 'id'"}),
            "headers": {"Content-Type": "application/json"}
        }

    post_id = path_params["id"]
    update_fields = {}
    allowed_fields = ["title", "body", "tags"]

    # Build update fields only from allowed list
    for field in allowed_fields:
        if field in body:
            update_fields[field] = body[field]

    if not update_fields:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No valid fields to update"}),
            "headers": {"Content-Type": "application/json"}
        }

    # Always update the updatedDate
    update_fields["updatedDate"] = now_utc()

    # Build UpdateExpression and ExpressionAttributeValues
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    try:
        response = table.update_item(
            Key={"id": post_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW"
        )

        updated_item = response.get("Attributes", {})
        return {
            "statusCode": 200,
            "body": json.dumps(updated_item),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
