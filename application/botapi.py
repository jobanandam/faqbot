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
def faqbot_api(question):
    print("Hi Welcome to FAQ BOT ")
    print("Question asked --> ", question)

    feedback = request.args.get('feedback')
    conversation_key = request.args.get('conversation_key')
    index = request.args.get('index')
    if not feedback:
        print("Get answer")
        result = get_answer(question)
    else:
        print("Get answer for feedback")
        result = get_answer_for_feedback(question, feedback, conversation_key, index)
    response = jsonify(result)
    print(result)
    print(response)
    return response


def get_answer(question):
    SentenceSimilarities.perform_classification_on_test_data()
    return SentenceSimilarities.get_questions_from_user_interface(question, False, True)


def get_answer_for_feedback(question, feedback, conversation_key, index):
    return SentenceSimilarities.respond_to_user_feedback(feedback, conversation_key, index)


if __name__ == '__main__':
    app.run(port=9080)
