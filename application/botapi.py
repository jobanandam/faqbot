from flask import Flask
from faqbot import SentenceSimilarities
app = Flask(__name__)


@app.route('/bot/dev-ops/<question>', methods=['GET'])
def sentiment_index(question):
    SentenceSimilarities.perform_classification_on_test_data()
    print("Hi Welcome to FAQ BOT ")
    print("Question asked --> ", question)
    result = SentenceSimilarities.get_questions_from_user_interface(question, False)
    print(result)
    return result



if __name__ == '__main__':
    app.run(port=9080)
