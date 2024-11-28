import boto3 # type: ignore
import requests # type: ignore
from botocore.exceptions import NoCredentialsError # type: ignore
import os
from dotenv import load_dotenv # type: ignore


# AWS Configuration
dynamodb_table = "Movies"
s3_bucket = "movie-cover-images-bucket"

# TMDB API Configuration
load_dotenv()
tmdb_api_key = os.environ.get('TMDB_API_KEY')
tmdb_api_url = "https://api.themoviedb.org/3/movie/popular"

# Initialize AWS Clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table)
s3 = boto3.client('s3')

def fetch_movies_from_tmdb():
    """Fetch popular movies from TMDB API."""
    params = {'api_key': tmdb_api_key, 'language': 'en-US', 'page': 1}
    response = requests.get(tmdb_api_url, params=params)
    response.raise_for_status()
    return response.json()['results']

def upload_cover_to_s3(title, poster_path):
    """Upload movie cover image to S3 and return the URL."""
    if not poster_path:
        return None
    image_url = f"https://image.tmdb.org/t/p/original{poster_path}"
    response = requests.get(image_url, stream=True)

    if response.status_code == 200:
        file_name = f"{title.replace(' ', '_').lower()}.jpg"
        try:
            s3.upload_fileobj(
                response.raw,
                s3_bucket,
                file_name,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            return f"https://{s3_bucket}.s3.amazonaws.com/{file_name}"
        except NoCredentialsError:
            print("S3 credentials not found.")
            return None
    return None

def save_movie_to_dynamodb(movie):
    """Save movie data to DynamoDB."""
    movie_id = str(movie['id'])  # Use TMDB's 'id' as the partition key
    title = movie['title']
    release_year = movie['release_date'].split("-")[0] if 'release_date' in movie else "Unknown"
    genre = "Unknown"  # TMDB genres can be mapped if needed
    cover_url = upload_cover_to_s3(title, movie.get('poster_path'))

    item = {
        "movie_id": movie_id,  # Partition key
        "title": title,
        "releaseYear": release_year,
        "genre": genre,
        "coverUrl": cover_url or "No Image Available"
    }
    table.put_item(Item=item)

def main():
    """Main function to fetch and save movies."""
    movies = fetch_movies_from_tmdb()
    for movie in movies:
        save_movie_to_dynamodb(movie)
    print("Movies have been saved to DynamoDB.")

if __name__ == "__main__":
    main()
