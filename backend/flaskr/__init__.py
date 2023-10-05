import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

###################################################################
#  Categories
###################################################################
    """
    Endpoint to handle GET requests for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            selection = Category.query.order_by(Category.id).all()
            categories = [category.type for category in selection]

            return jsonify({
                'success': True,
                'categories': categories,
            })
        except BaseException:
            abort(404)
    
    """
    Endpoint to create a new category,
    which will require the type.
    """
    @app.route('/categories', methods=['POST'])
    def create_category():
        try:
            # Get questions parameters
            body = request.get_json()
            type = body.get('type', None)

            # Create new question and add to db
            category = Category(type=type)
            if(category is not None):
                category.insert()
            else:
                abort(422)

            # Select all questions
            questions = Question.query.order_by(Question.id).all()

            return jsonify({
                'success': True,
                'created': category.id,
                'total_questions': len(questions)
            })
        except BaseException:
            abort(405)

###################################################################
#  Questions
###################################################################
    """
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions')
    def get_questions():
        try:
            # Select all questions to paginate
            page = request.args.get('page', 1, type=int)
            selection = Question.query.order_by(
                Question.id).paginate(
                page=page, per_page=QUESTIONS_PER_PAGE).items
            current_questions = [question.format()
                                 for question in selection]

            # If there are no more questions return 404
            if (len(current_questions) == 0):
                abort(404)

            # Get current category from args if exists
            current_category = request.args.get('category')

            # Select all categories and extract the type
            c_selection = Category.query.order_by(Category.id).all()
            categories = [category.type for category in c_selection]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': categories,
                'current_category': current_category
            })
        except BaseException:
            abort(404)

    """
    Endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            # If the question is not found return 404
            if (question is None):
                abort(404)

            question.delete()

            # Get current category from args if exists
            current_category = request.args.get('category')

            # Select all questions to paginate
            page = request.args.get('page', 1, type=int)
            selection = Question.query.order_by(
                Question.id).paginate(
                page=page, per_page=QUESTIONS_PER_PAGE).items
            current_questions = [question.format()
                                 for question in selection]

            # Select all categories and extract the type
            c_selection = Category.query.order_by(Category.id).all()
            categories = [category.type for category in c_selection]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': categories,
                'current_category': current_category
            })

        except BaseException:
            abort(404)

    """
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            # Get questions parameters
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            # Create new question and add to db
            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            if(question is not None):
                question.insert()
            else:
                abort(422)

            # Select all questions
            questions = Question.query.order_by(Question.id).all()

            return jsonify({
                'success': True,
                'created': question.id,
                'total_questions': len(questions)
            })
        except BaseException:
            abort(405)

    """
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # Get search term
        body = request.get_json()
        search_term = body.get("searchTerm")
        try:
            # Select all questions that includes the search term and paginate
            # them
            page = request.args.get('page', 1, type=int)
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search_term))
            ).paginate(page=page, per_page=QUESTIONS_PER_PAGE).items
            current_questions = [question.format()
                                 for question in selection]

            # Get current category from args if exists
            current_category = request.args.get('category')

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search_term))).all()),
                    "current_category": current_category
                }
            )
        except BaseException:
            abort(404)

    """
    GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        #Get the specific category
        category = Category.query.filter_by(id=category_id).one_or_none()
        try:
            #Select all questions that belongs to the category and paginate
            page = request.args.get('page', 1, type=int)
            questions = Question.query.filter_by(category=str(category.id)).paginate(page=page, per_page=QUESTIONS_PER_PAGE).items
            current_questions = [question.format()
                                    for question in questions]

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len( Question.query.filter_by(category=str(category.id)).all()),
                "current_category": category.type
            })

        except BaseException:
            abort(404)

###################################################################
#  Quiz
###################################################################
    """
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            # Get all quiz info and add 1 to category id
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions', None)
            category_id = int(quiz_category['id']) + 1

            # If user selects all
            if(quiz_category['type'] == 'click'):
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()

            else:
                questions = Question.query.filter_by(
                    category=str(category_id)).filter(
                    Question.id.notin_(previous_questions)).all()

            # Select a random question from the questions list
            index = random.randint(0, len(questions) - 1)
            random_question = questions[index]
            print(random_question.format())
            return jsonify({
                'success': True,
                'question': random_question.format()
            })
        except BaseException:
            abort(404)

    """
    Error handlers
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'resource not found',
            'error': 404
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': 'resource unprocessable',
            'error': 422
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': 400
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'method not allowed',
            'error': 405
        }), 405

    return app
