import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # Set Access-Control-Allows
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Endpoint handling  GET requests for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.order_by(Category.type).all()
        categories = [category.type for category in selection]

        return jsonify({
            'success': True,
            'categories': categories,
        })

    # Endpoint to handle GET requests for questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)
        categories_selection = Category.query.order_by(Category.type).all()
        categories = [category.type for category in categories_selection]

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(Question.query.all()),
            'categories': categories
        })

    # Endpoint to DELETE question using a question ID.

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    # Endpoint to POST a new question or get questions based
    # on a search term

    @app.route('/questions', methods=['POST'])
    def create_or_search_questions():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection.all())
                })

            else:
                question = Question(question=new_question, answer=new_answer,
                                    difficulty=new_difficulty, category=str(int(new_category) + 1))
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions0': len(Question.query.all())
                })
        except:
            abort(405)

    # GET endpoint to get questions based on category

    @app.route('/categories/<int:category>/questions', methods=['GET'])
    def get_questions_by_categories(category):
        selection = Question.query.filter(Question.category == category + 1).all()
        questions = paginate_questions(request, selection)
        categories_selection = Category.query.order_by(Category.type).all()
        categories = [category.type for category in categories_selection]

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'categories': categories
        })

    # POST endpoint to get questions to play the quiz.

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category['id'] == 0:

            questions = Question.query.all()
            print(len(questions))
            remaining_questions = []
            for question in questions:
                if question.id not in previous_questions:
                    remaining_questions.append(question)
            # Shuffle the questions
            random.shuffle(remaining_questions)

            return jsonify({
                'success': True,
                'question': remaining_questions.pop().format()
            })

        else:
            try:

                questions = Question.query.filter(Question.category == int(quiz_category['id']) + 1).all()
                print(len(questions))
                remaining_questions = []
                for question in questions:
                    if question.id not in previous_questions:
                        remaining_questions.append(question)
                # Shuffle the questions
                random.shuffle(remaining_questions)

                return jsonify({
                    'success': True,
                    'question': remaining_questions.pop().format()
                })
            except:
                abort(405)

    # Create error handlers for expected errors

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
