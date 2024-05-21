# Fyle Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to intern at Fyle and work with our engineering team. You should be able to commit to at least 6 months of dedicated time for internship.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).


## Challenge outline

**You are allowed to use any online/AI tool such as ChatGPT, Gemini, etc. to complete the challenge. However, we expect you to fully understand the code and logic involved.**

This challenge involves writing a backend service for a classroom. The challenge is described in detail [here](./Application.md)


## What happens next?

You will hear back within 48 hours from us via email. 


## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/Scripts/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```


### Running the application with the help of Docker 

Following are the steps to run the application with Docker

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed  and running on your machine.

## Getting Started

### Clone the Repository

```
git clone https://github.com/Shilpi-droid/fyle-interview-intern-backend
cd fyle-interview-intern-backend
```

## Building and Running the Application

To build the Docker images and start the containers, run:

```
docker-compose up --build
```

This command will:

- Build the Docker image for the Flask application.
- Start the container and make the Flask application available at http://localhost:5000.

## Accessing the Application

Once the containers are up and running, you can access the application by navigating to http://localhost:5000 in your web browser.

## Environment Variables

- FLASK_APP: Entry point for the Flask application, set to core/server.py.
- FLASK_ENV: Environment mode, set to production for production deployment.

## Important Notes

Ensure that no other service is running on port 5000 as it will be used by the Flask application.

## Example Endpoints

You can test the application using tools like curl, Postman, or your web browser. For example:

```
curl -X GET \ -H "X-Principal: {\"user_id\": 5, \"principal_id\": 1}" \http://localhost:5000/principal/assignments
```  

This should return a JSON response indicating the status and time:

```
{
"data": [
    {
    "content": "test content",
    "created_at": "2024-05-20T23:09:41.125361",
    "grade": "D",
    "id": 1,
    "state": "GRADED",
    "student_id": 1,
    "teacher_id": 1,
    "updated_at": "2024-05-20T23:09:41.125367"
    },
    {
    "content": "test content",
    "created_at": "2024-05-20T23:09:41.125774",
    "grade": "D",
    "id": 2,
    "state": "GRADED",
    "student_id": 1,
    "teacher_id": 1,
    "updated_at": "2024-05-20T23:09:41.125777"
    },
    ...
}
```