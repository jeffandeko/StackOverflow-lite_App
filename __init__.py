from os import abort

from flask import request
from flask.json import jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name, ):
    from models.py import Questions
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    @app.route('v1/questions/', methods=['POST', 'GET'])
    def questions():
        global quiz
        if request.method == "POST":
            users_name = str(request.data.get('users_name', ''))
            if users_name:
                question = Questions(users_name=users_name)
                question.save()
                respond = jsonify({
                    'users_name': question.users_name,
                    'date_created': question.date_created,
                    'date_modified': question.date_modified,
                })
                respond.status_code = 201
                return respond
            else:
                # This is the GET command
                question = Questions.get_all()
                gives = []

                for question in question:
                    quiz = {
                        'users_name': question.users_name,
                        'date_created': question.date_created,
                        'date_modified': question.date_modified,
                    }
                    gives.append(quiz)
                respond = jsonify(quiz)
                respond.status_code = 200
                return respond

    @app.route('v1/questions/', methods=['GET', 'PUT', 'DELETE'])
    def handle_questions():
        question = Questions.query.filter().first
        if not questions:
            # 40$ HTTP exception to be raised
            abort(404)

        if request.method == 'DELETE':
            question.delete()
            return {"THe question was deleted successfully".format(questions.user_name)
                    }, 200

        elif request.method == 'PUT':
            users_name = str(request.data.get('name', ''))
            question.users_name = users_name
            question.save()
            respond = jsonify({
                'users_name': question.users_name,
                'date_created': question.date_created,
                'date_modified': question.date_modified
            })
            respond.status_code = 200
            return respond
        else:
            respond = jsonify({
                'users_name': question.users_name,
                'date_created': question.date_created,
                'date_modified': question.date_modified
            })
            respond.status_code = 200
            return respond

        return app
