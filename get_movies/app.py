import boto3
import json

# AWS Configuration
dynamodb_table = "Movies"

# Initialize AWS Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table)

def get_movies(event, context):
    """Fetch all movies from DynamoDB."""
    try:
        response = table.scan()  # Retrieves all items from the table
        movies = response.get('Items', [])
        return {
            "statusCode": 200,
            "body": json.dumps(movies)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


