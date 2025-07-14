import boto3

def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table('Posts')
