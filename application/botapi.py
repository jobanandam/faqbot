from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from faqbot import SentenceSimilarities

app = Flask(__name__)

cors = CORS(app, resources={r"/bot/dev-ops/<question>": {"origins": "http://localhost:8000"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/bot/dev-ops/<question>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def sentiment_index(question):
    feedback = request.args.get('feedback')
    conversation_key = request.args.get('conversation_key')
    SentenceSimilarities.perform_classification_on_test_data()
    print("Hi Welcome to FAQ BOT ")
    print("Question asked --> ", question)
    result = SentenceSimilarities.get_questions_from_user_interface(question, False, True)
    response = jsonify(result)
    print(response)
    return response


if __name__ == '__main__':
    app.run(port=9080)
