# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

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

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

OR you can run this command directly
```
start test.bat
```

## API Reference
* Base URL: At present, this app can only run locally and is not hosted as a base URL. the backend app is hosted at the default, `http://127.0.0.1:500/`, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format
```
{
    "success": False,
    "error": 404,
    "message": "Not Found",
}
```
The API will return three error types when requests fail:
* 404: Not found
* 400: Bad request
* 422: Unprocessable
* 500: Server internal error

### Endpoints

#### GET /categories
   - Returns a list of categories each with its id, success value.
   - Sample curl http://127.0.0.1:5000/categories
   
        ```
        {
            "categories": [
                {
                    "id": 1,
                    "type": "Science"
                },
                {
                    "id": 2,
                    "type": "Art"
                },
                {
                    "id": 3,
                    "type": "Geography"
                },
                {
                    "id": 4,
                    "type": "History"
                },
                {
                    "id": 5,
                    "type": "Entertainment"
                },
                {
                    "id": 6,
                    "type": "Sports"
                }
            ],
            "success": true
        }
        ```


#### GET /questions
   - General:
     - Returns a list of categories, questions each with its id, success value and total number of questions.
     - values are paginated in groups of 10
     - Optional args `?page=int` to choose a specific page
   - Sample curl http://127.0.0.1:5000/questions?page=2

        ```
        {
            "categories": [
                {
                    "id": 1,
                    "type": "Science"
                },
                {
                    "id": 2,
                    "type": "Art"
                },
                {
                    "id": 3,
                    "type": "Geography"
                },
                {
                    "id": 4,
                    "type": "History"
                },
                {
                    "id": 5,
                    "type": "Entertainment"
                },
                {
                    "id": 6,
                    "type": "Sports"
                }
            ],
            "questions": [
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Escher",
                    "category": 2,
                    "difficulty": 1,
                    "id": 16,
                    "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
                },
                {
                    "answer": "Mona Lisa",
                    "category": 2,
                    "difficulty": 3,
                    "id": 17,
                    "question": "La Giaconda is better known as what?"
                },
                {
                    "answer": "One",
                    "category": 2,
                    "difficulty": 4,
                    "id": 18,
                    "question": "How many paintings did Van Gogh sell in his lifetime?"
                },
                {
                    "answer": "Jackson Pollock",
                    "category": 2,
                    "difficulty": 2,
                    "id": 19,
                    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
                },
                {
                    "answer": "The Liver",
                    "category": 1,
                    "difficulty": 4,
                    "id": 20,
                    "question": "What is the heaviest organ in the human body?"
                },
                {
                    "answer": "Alexander Fleming",
                    "category": 1,
                    "difficulty": 3,
                    "id": 21,
                    "question": "Who discovered penicillin?"
                },
                {
                    "answer": "Blood",
                    "category": 1,
                    "difficulty": 4,
                    "id": 22,
                    "question": "Hematology is a branch of medicine involving the study of what?"
                },
                {
                    "answer": "Scarab",
                    "category": 4,
                    "difficulty": 4,
                    "id": 23,
                    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
                }
            ],
            "success": true,
            "total_questions": 19
        }
        ```


#### POST /questions
   - General:
     - Creates a new question using submitted question, answer, category and difficulty.
     - returns the id of the created question, paginated list of current page questions, success value, total number of questions
   - Sample curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question": "Do you love me?", "answer": "Yes", "difficulty": "1", "category": "5"}'

        ```
        {
            "created": 38,
            "questions": [
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Tom Cruise",
                    "category": 5,
                    "difficulty": 4,
                    "id": 4,
                    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
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
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                }
            ],
            "success": true,
            "total_questions": 20
        }
        ```


#### DELETE /questions/{id}
   - General:
     - Deleted a question with the id provided
     - Returns a id of the deleted question, success value, total number of questions and paginated list of questions
   - Sample Sample curl http://127.0.0.1:5000/questions/2 -X DELETE
        
        ```
        {
              "deleted": 2,
              "questions": [
                    {
                        "answer": "Tom Cruise",
                        "category": 5,
                        "difficulty": 4,
                        "id": 4,
                        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                    },
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
                    },
                    {
                        "answer": "Muhammad Ali",
                        "category": 4,
                        "difficulty": 1,
                        "id": 9,
                        "question": "What boxer's original name is Cassius Clay?"
                    },
                    {
                        "answer": "Brazil",
                        "category": 6,
                        "difficulty": 3,
                        "id": 10,
                        "question": "Which is the only team to play in every soccer World Cup tournament?"
                    },
                    {
                        "answer": "Uruguay",
                        "category": 6,
                        "difficulty": 4,
                        "id": 11,
                        "question": "Which country won the first ever soccer World Cup in 1930?"
                    },
                    {
                        "answer": "George Washington Carver",
                        "category": 4,
                        "difficulty": 2,
                        "id": 12,
                        "question": "Who invented Peanut Butter?"
                    },
                    {
                        "answer": "Lake Victoria",
                        "category": 3,
                        "difficulty": 2,
                        "id": 13,
                        "question": "What is the largest lake in Africa?"
                    },
                    {
                        "answer": "The Palace of Versailles",
                        "category": 3,
                        "difficulty": 3,
                        "id": 14,
                        "question": "In which royal palace would you find the Hall of Mirrors?"
                    },
                    {
                        "answer": "Agra",
                        "category": 3,
                        "difficulty": 2,
                        "id": 15,
                        "question": "The Taj Mahal is located in which Indian city?"
                    }
              ],
              "success": true,
              "total_questions": 20
        }
        ```


#### POST /questions/search
   - General:
     - Searches for a question using a search term.
     - Returns a paginated list of search results, success value and number of results.
   - Sample curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'
        
        ```
        {
            "questions": [
                {
                    "answer": "Edward Scissorhands",
                    "category": 5,
                    "difficulty": 3,
                    "id": 6,
                    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                }
            ],
            "questions_num": 2,
            "success": true
        }
        ```

#### GET /categories/{id}/questions
   - General:
     - Fetches questions of a certain category by providing the category id.
     - Returns a paginated list of questions, success value and number of questions of the category.
   - Sample curl http://127.0.0.1:5000/categories/6/questions
        ```
        {
            "questions": [
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                }
            ],
            "questions_num": 2,
            "success": true
        }
        ```


#### POST /quizzes
   - General:
     - Get questions to play the quiz.
     - Takes category and previous question parameters.
     - Return a random questions within the given category, if provided, and that is not one of the previous questions.
   - Sample curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": 1}}'
        ```
        {
            "question": {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
            },
            "success": true
        }
        ```