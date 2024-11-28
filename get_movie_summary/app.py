import boto3
import json

# AWS Configuration
dynamodb_table = "Movies"

# Initialize AWS Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table)

def get_movie_summary(event, context):
    """Generate a summary for a specific movie."""
    try:
        movie_id = event['pathParameters']['movie_id']
        response = table.get_item(Key={"movie_id": movie_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Movie not found"})
            }

        movie = response['Item']
        summary = f"{movie['title']} is a {movie['genre']} movie released in {movie['releaseYear']}."

        return {
            "statusCode": 200,
            "body": json.dumps({**movie, "summary": summary})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
