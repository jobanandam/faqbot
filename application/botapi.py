from flask import Flask
from flask_cors import CORS, cross_origin
from faqbot import SentenceSimilarities

app = Flask(__name__)

cors = CORS(app, resources={r"/bot/dev-ops/<question>": {"origins": "http://localhost:8000"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/bot/dev-ops/<question>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def sentiment_index(question):
    SentenceSimilarities.perform_classification_on_test_data()
    print("Hi Welcome to FAQ BOT ")
    print("Question asked --> ", question)
    result = SentenceSimilarities.get_questions_from_user_interface(question, False)
    print(result)
    return result


if __name__ == '__main__':
    app.run(port=9080)
