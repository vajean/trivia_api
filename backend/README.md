# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


```
Bellow is the documentation for each endpoint

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/int:category_id/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/int:question_id'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetch a dictionary of questions paginated in questions per page, with keys:
    categories - list of categories,
    questions - list of question dictionary:
        answer - correct answer,
        category - category of the question,
        difficulty - question difficulty (1-5),
        id - unique question id,
        question - question string
    total_questions - number of questions in db
- Request arguments: page number as ?page=1,2,3
- Return example:
{
  "categories": [
    "Art",
    "Entertainment",
    "Geography",
    "History",
    "Science",
    "Sports"
  ],
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions: 2
}

GET '/categories/int:category_id/questions'
- Fetch a dictionary of questions within a category ID paginated in questions per page, with keys:
    categories - list of categories,
    questions - list of question dictionary:
        answer - correct answer,
        category - category of the question,
        difficulty - question difficulty (1-5),
        id - unique question id,
        question - question string
    total_questions - number of questions in db
- Request arguments: category ID in the URL as int '/categories/int:category_id/questions'
- Returns: see GET '/questions' for formatting, but only questions within the requested category

POST '/questions'
- add or search question:
    if search_term key present in request - search using the search term and return a dictionary with questions matching the search
    else a new Question object is created with question, answer, difficulty and category keys from the request and added to the database
- request arguments -  search_term, or question, answer, difficulty, category - keys of JSON dictionary in request
- returns:
    if search:
        see GET '/questions' for formatting, but only questions matching the search term
    if add question:
        returns GET '/questions' for formatting, with the new question added

POST '/quizzes'
- return one random question from a category or from all categories if no category is requested,
    does not repeat questions based on the request argument "previous_questions"
        answer - correct answer,
        category - category of the question,
        difficulty - question difficulty (1-5),
        id - unique question id,
        question - question string
- request arguments: previous_question, quiz_category - keys of JSON dictionary in request
- return example:
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }

DELETE '/questions/int:question_id'
- delete the requested question by ID from the DB
- request parameter" question_id in the URL
- return GET '/questions'
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

or

dropdb trivia_test && createdb trivia_test && psql trivia_test <trivia.psql && python test_flaskr.py
```