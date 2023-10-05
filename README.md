# Trivia App


Trivia App is a quiz application that allows it's users to play and answer trivia questions in multiple categories. 

## Getting Started


### Pre-requisites and Local Development


Developers who wishes to work on this project should already have Python3, pip and node installed.

#### Backend


From the backend folder, run ```bash pip install requirements.txt```. All required packages are included in the requirements file.

To run this application, run the following commands:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

* ```bash export FLASK_APP=flaskr ``` this command will insure that Flask is going to use __init__.py in our flaskr folder.
* ```bash export FLASK_ENV=development ``` this command will insure that we will be working in development mode, which will show us an interactive debugger in the console and resart the server whenever a change is made.
* ```bash flask run ``` this command will start the application.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

#### Frontend


From the frontend folder, run 
```bash
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on  http://127.0.0.1:3000/.

## API Reference


### Getting Started


Base URL: The application can only run on the localhost as it is not hosted yet:
http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Error Messages


The API will return 4 possible error types when requests fail
Error code | Message
--- | --- 
400 | Bad request
404 | resource not found
405 | method not allowed
422 | resource unprocessable

Errors are returned as JSON objects in the following format:
#### 400 Bad request


```json
{
    'success': False,
    'message': 'Bad request',
    'error': 400
}
```

#### 404 resource not found


```json
{
    'success': False,
    'message': 'resource not found',
    'error': 404
}
```

#### 405 method not allowed


```json
{
    'success': False,
    'message': 'method not allowed',
    'error': 404
}
```

#### 422 method not allowed


```json
{
    'success': False,
    'message': 'resource unprocessable',
    'error': 422
}
```

### API Endpoints


#### GET '/categories'


Expects: None
Returns: 
* A list of categoris and success value.

Sample: 
```curl
curl http://127.0.0.1:5000/categories
```
```json
  {
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'success: true
}
```

#### GET '/questions?page=${integer}'


Expects: page - integer.
Returns: 
* A list of 10 paginates questions, total questions, a list of categories, current category, and success value.

Sample: 
```curl
curl http://127.0.0.1:5000//questions?page=1
```
```json
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'current_category': 'History',
    'success': true
}
```


#### GET '/categories/${id}/questions'


Gets all of the questions that belongs to a specific category.
Expects: category's id - integer.
Returns: 
* A list of 10 pagenated questions, number of total questiona, current category, and success value

Sample: 
```curl
curl http://127.0.0.1:5000/categories/4/questions
```
```json
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'total_questions': 100,
    'current_category': 'History',
    'success': true
}
```

#### DELETE '/questions/${id}'


Deletes a question with a specfic id
Expects: Question's id - integer
Returns: 
* A list of 10 paginates questions, total questions, a list of categories, current category, and success value.

Sample: 
```curl
curl -X DELETE http://127.0.0.1:5000/questions/2
```
```json
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'current_category': 'History',
    'success': true
}
```

#### POST '/quizzes'


Sends a post request in order to get the next question. 
Expects: A request body with this structure:
```json
{
    'previous_questions': [1, 4, 20, 15]
    'quiz_category': 'current category'
 }
```
Returns: 
* A single random question object and success value.


Sample: 
```curl
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{'previous_questions': [8], 'quiz_category': { 'type': 'Geography', 'id': '3' } }'
```
```json
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    },
    'success': true
}
```

#### POST '/questions'


Sends a post request in order to add a new question
Expects: A request body with this structure:
```json
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
 }
```
Returns: 
* New question's id, total number of questions, and success value


Sample: 
```curl
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{'question': 'Who is she? A singer?', 'answer': 'She is much more than a singer chris. She is a queen.', 'category': 2, 'difficulty': 3}'
```
```json
{
    'created': 15,
    'total_questions': 100,
    'success': true
}
```

#### POST '/questions'


Sends a post request in order to search for a specific question by search term
Expects: A request body with this structure:
```json
{
    'searchTerm': 'this is the term the user is looking for'
}
```
Returns: 
* A list of 10 paginated questions, total number of questions, current category, and success value


Sample: 
```curl
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{'previous_questions': [8], 'quiz_category': { 'type': 'Geography', 'id': '3' } }'
```
```json
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'total_questions': 100,
    'current_category': 'Entertainment',
    'success': true
}
```

#### POST '/categories'


Sends a post request in order to create a new category
Expects: A request body with this structure:
```json
{
    'type': 'a new category type'
}
```
Returns: 
* The new category ID, total number of questions, and success value


Sample: 
```curl
curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{ 'type': 'a new category type' } '
```
```json
{
    'total_questions': 100,
    'current_category': 15,
    'success': true
}
```