# **Serverless Movie API**

 This project fetches movie data from an external database (TMDB), stores the data in AWS resources, and provides endpoints to retrieve the movie information stored in the aws resources with the help of a simple and scalable serverless architecture.

## Features:
* Fetches popular movies from TMDB and stores them in DynamoDB.
* Stores movie cover images in S3 and links them to movie records.
* creates a url for the images stored in S3 and saves the url in DynamoDB
* Provides a serverless API endpoint to;
  * Fetch a list of all movies stored in DynamoDB.
  * Retrieve movies filtered by release year.
  * Get detailed information about a specific movie with a summary.

## Architecture
The project follows a serverless architecture utilizing AWS services:
  1. DynamoDB Table
    - Stores movie details
  2. S3 Bucket
    - Hosts and serves movie cover images.
  3. Lambda Functions
    - Handles API requests for:
      - Fetching all movies 
      - Fetching movies by year 
      - Fetching movie details with a summary
  4. API Gateway
    - Routes incoming API requests to appropriate Lambda functions.

## Setup Instructions

### Prerequisites
 - AWS Account
 - TMDB API Key ([Sign up here](https://www.themoviedb.org/documentation/api))
 - Python 3.8+
 - AWS CLI installed and configured ([Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))
 - Git installed ([Download Git](https://git-scm.com/downloads))
 - Optional: **Postman** for testing or you can test with the curl command in your cli.

### Getting Started
1. **Clone the Repository:**
     ```bash
     https://github.com/Nwaubani-Godson/Serverless-Movie-API.git
2. **Set up a Virtual Environment:** Set up a virtual environment for the populate_movie directory workspace.
     ```bash
     python -m venv <folder_name>
3. **Install Dependencies:** This project require some libraries, explore the requirement.txt file in the different directories to install dependencies.
     ```bash
     pip install -r requirements.txt
4. **Configure Environment Variables:** Create a .env file to store your API key.
5. **Configure AWS:** Configure your AWS CLI to create a conncetion to your account.
     ```bash
     aws configure
6. **Role Setup:** Create a role with the permissions to access dynamodb and s3 bucket.
7. **Create AWS Resources:*** Setup dynamodb, s3 bucket and lambda function.

### Fetching the movie data from TMDB
* Navigate to the populate directory.
     ```bash
     cd populate_movies
* Run the python file.
     ```bash
     python app.py

### Deploying the lambda functions
* Navigate to each of the function directories and zip each of the directory.
     ```bash
     zip -r <directory_name>.zip .
* Create a lambda function on AWS Lambda for each of the functions.
* Select the .zip from the upload from option and navigate to the file directory and select the zip file.
* Select your runtime to the version of python you used for the code.
* Under Execution permission, select the role you created earier which have the necessary permissions.
* Set the handler in this format;
     ```bash
     <python_file>.<function_name>

 ### Configuring API Gateway
