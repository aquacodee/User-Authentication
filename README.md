# User-Authentication

This is a simple API built using the FastAPI framework and Pydantic library in Python. The API allows users to register and authenticate, create, read, update and delete posts and vote for them.

# Prerequisites
Before running the API, ensure you have the following installed:

# Python 3.8 or higher 
* Pipenv

# Installation
* Clone the repository
```
git clone https://github.com/aquacodee/User-Authentication.git
cd fastapi-pydantic-auth-post-vote-api 
```
* Install dependencies
```
pip install virtualenv 
```
* Activate the virtual environment
```
venv\Script\activate.bat
```

# Usage
* Run the server
```
uvicorn app.main:app --reload
```
* Open your web browser and navigate to [http://localhost:8000/docs](#http://localhost:8000/docs) to access the Swagger UI for the API.

* To test the endpoints, click on the endpoint and then click the "Try it out" button. Enter the required parameters and click "Execute" to test the endpoint.

# Endpoints
The following endpoints are available in the API:

# Authentication
## Register
* POST /auth/register
* Required fields: username, password
* Response: token

## Login
* POST /auth/login
* Required fields: username, password
* Response: token

# Posts
### Create a post
* POST /posts
* Required fields: title, content
* Response: Post

### Get all posts
* GET /posts
* Response: List of Post

### Get a single post
* GET /posts/{post_id}
* Response: Post

### Update a post
* PUT /posts/{post_id}
* Required fields: title, body
* Response: Post

### Delete a post
* DELETE /posts/{post_id}
* Response: HTTP 204 No Content





