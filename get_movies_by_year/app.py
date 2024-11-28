import boto3
import json

# AWS Configuration
dynamodb_table = "Movies"

# Initialize AWS Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table)

def get_movies_by_year(event, context):
    """Fetch movies from DynamoDB by release year."""
    try:
        year = event['pathParameters']['year']
        response = table.scan(
            FilterExpression="releaseYear = :year",
            ExpressionAttributeValues={":year": year}
        )
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
