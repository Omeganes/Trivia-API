import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "trivia_test"
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'Raymond')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '0000')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'\
            .format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions_without_pages(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 19)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions_with_pages(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions_with_pages_error(self):
        res = self.client().get('/questions?page=900')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")

    def test_delete_question(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 9)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)

    def test_delete_question_fail(self):
        res = self.client().delete('/questions/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_create_question_success(self):
        res = self.client().post('/questions', json={
                                     'question': 'Do you love me?',
                                     'answer': 'Do you do you?',
                                     'difficulty': '5',
                                     'category': '2',
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['created'])
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 20)

    def test_create_question_negative_difficulty_error(self):
        res = self.client().post('/questions', json={
                                     'question': 'Do you love me?',
                                     'answer': 'Do you do you?',
                                     'difficulty': '-1',
                                     'category': '1',
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_create_question_out_of_range_category_error(self):
        res = self.client().post('/questions', json={
                                     'question': 'Do you love me?',
                                     'answer': 'Do you do you?',
                                     'difficulty': '1',
                                     'category': '10',
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_create_question_question_not_provided_error(self):
        res = self.client().post('/questions', json={
                                     'answer': 'Do you do you?',
                                     'difficulty': '1',
                                     'category': '10',
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_create_question_answer_not_provided_error(self):
        res = self.client().post('/questions', json={
                                     'question': 'Do you love me?',
                                     'difficulty': '1',
                                     'category': '10',
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_create_question_difficulty_not_int_error(self):
        res = self.client().post('/questions', json={
                                     'question': 'Do you love me?',
                                     'answer': 'Do you do you?',
                                     'difficulty': 'Hey!',
                                     'category': '10',
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_create_question_category_not_int_error(self):
        res = self.client().post('/questions', json={
            'question': 'Do you love me?',
            'answer': 'Do you do you?',
            'difficulty': '4',
            'category': 'Hey!',
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_questions_search(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'title',
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['questions_num'], 2)

    def test_questions_search_error(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'dfadfa',
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")

    def test_questions_by_category_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['questions_num'], 3)

    def test_questions_by_category_error(self):
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")

    def test_quizzes_success(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [20, 21],
            'quiz_category': {
                'type': 'Science',
                'id': 1
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"   # noqa
        })

    def test_quizzes_error(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
