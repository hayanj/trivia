import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# a function to help in paginating the questions
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]

    return formatted_questions[start:end]

def create_app(test_config=None):
    # create and configure the app
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
    
    """
    endpoint to handle GET requests for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        categories = [category.type for category in selection]
        return jsonify({
            'success': True,
            'categories': categories,
        })


    """
    endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions')
    def get_questions():
        try:
            # select all questions to paginate
            selection = Question.query.order_by(Question.id).all() 
            current_questions = paginate_questions(request, selection)

            #if there are no more questions return 404
            if (len(current_questions) == 0):
                abort(404)

            # get current category from args if exists
            current_category = request.args.get('category')

            # select all categories and extract the type
            c_selection = Category.query.order_by(Category.id).all()
            categories = [category.type for category in c_selection]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions':len(selection),
                'categories': categories,
                'current_category': current_category
                })
        except:
            abort(400)
    
    """
    endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            # if the question is not found return 404
            if (question is None):
                abort(404)

            question.delete()

            # get current category from args if exists
            current_category = request.args.get('category')

            # select all questions to paginate
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            # select all categories and extract the type
            c_selection = Category.query.order_by(Category.id).all()
            categories = [category.type for category in c_selection]

            return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions':len(selection),
            'categories': categories,
            'current_category': current_category
            })
        
        except:
            abort(400)


    """
    endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            # get questions parameters
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            # create new question and add to db
            question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            question.insert()

            # select all questions to paginate
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            # select all categories and extract the type
            c_selection = Category.query.order_by(Category.id).all()
            categories = [category.type for category in c_selection]

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': categories,
                'current_category': question.category
            })
        except:
            abort(405)

    """
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            # get search term
            body = request.get_json()
            search_term = body.get("searchTerm")

            # select all questions that includes the search term and paginate them
            selection = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%".format(search_term))
            )
            current_questions = paginate_questions(request, selection)

            # get current category from args if exists
            current_category = request.args.get('category')

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection.all()),
                    "current_category": current_category
                }
                )
        except:
            abort(404)

    """
    GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # get the specific category
        category = Category.query.filter_by(id=category_id).one_or_none()
        try:
            # select all questions that belongs to the category and paginate
            questions = Question.query.filter_by(category=str(category.id)).all()
            current_questions = paginate_questions(request, questions)
            
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": category.type
            })
        
        except:
            abort(404)

    """
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            # get all quiz info and add 1 to category id
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions', None)
            category_id = int(quiz_category['id'])+1

            # if user selects all
            if( quiz_category['type'] == 'click'):
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            
            else:
                questions = Question.query.filter_by(category=str(category_id)).filter(Question.id.notin_(previous_questions)).all()

            # select a random question from the questions list    
            index = random.randint(0, len(questions)-1)
            random_question = questions[index]
            print(random_question.format())
            return jsonify({
                'success': True,
                'question': random_question.format()            
                })
        except:
            abort(404)


    """
    error handlers
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

