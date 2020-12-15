# import os
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def paginate_question(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    '''
    Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'categories': formatted_categories,
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    '''
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_question(request, selection)

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': formatted_categories,
            # 'current_category': 5,  # TODO: make it dynamic
            'total_questions': len(selection),
        })

    '''
    DELETE question using a question ID.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_question(request, selection)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(selection),
            })
        except Exception:
            abort(422)

    '''
    Create a new question,
    which will require the question and answer text,
    category, and difficulty score.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        try:
            new_question = body.get('question')
            if not new_question:
                abort(422)

            new_answer = body.get('answer')
            if not new_answer:
                abort(422)

            new_difficulty = int(body.get('difficulty'))
            if new_difficulty < 1:
                abort(422)

            new_category = int(body.get('category'))
            if not new_difficulty:
                abort(422)
            elif new_category not in range(1, 7):
                abort(422)
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty
                                )
            question.insert()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_question(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(selection),
            })

        except Exception:
            abort(422)

    '''
    Get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        question_param = body.get('searchTerm')
        try:
            selection = Question.query \
                .filter(Question.question.ilike('%' + question_param + '%')) \
                .order_by(Question.question) \
                .all()

            current_questions = paginate_question(request, selection)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "questions_num": len(selection),
            })
        except Exception:
            abort(404)

    '''
    Get questions based on category.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_categories_questions(category_id):
        try:
            selection = Question.query.filter_by(category=category_id).all()

            if len(selection) == 0:
                abort(404)

            current_questions = paginate_question(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "questions_num": len(selection),
            })

        except Exception:
            abort(404)

    '''
    Get questions to play the quiz.
    takes category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            if quiz_category['type'] != "all":
                category = Category.query\
                    .filter_by(type=quiz_category['type'])\
                    .one_or_none()
                questions = Question.query\
                    .filter_by(category=category.id).all()
            else:
                questions = Question.query.all()

            try:
                def create_questions_lst(question):
                    if question.id not in previous_questions:
                        return question
                questions_lst = [question
                                 for question in
                                 map(create_questions_lst, questions)
                                 if question is not None]
                new_question = random.choice(questions_lst).format()
            except Exception:
                new_question = None

            return jsonify({
                'success': True,
                'question': new_question,
            })
        except Exception:
            abort(422)

    '''
    Error handlers
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server internal error"
        }), 500

    return app
