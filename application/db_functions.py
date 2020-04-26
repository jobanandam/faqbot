import db_connection
from flask import Flask
from file_reader import read_json_file

app = Flask(__name__)

def update_user_suggestible_questions_to_db(user_id, sorted_suggestible_questions):
    with app.app_context():
        q_id = 0
        for res in db_connection.query_db(f"select id from mybot_questionanswermodel where question='{sorted_suggestible_questions[0]['question']}'"):
            q_id = res[0]
        if q_id != 0:
            suggestible_questions_file = "../application/resources/suggestible_questions.json"
            root_json_obj = read_json_file(suggestible_questions_file)
            exiting_results_of_one_question = root_json_obj[user_id]
            asked_question = exiting_results_of_one_question["user_question"]
            answer = sorted_suggestible_questions[0]['answer']
            score = sorted_suggestible_questions[0]['score']
            processed = 1 if sorted_suggestible_questions[0]['processed'] == 'Y' else 0
            accepted = 1 if sorted_suggestible_questions[0]['accepted'] == 'Y' else 0
            db_connection.query_db(f"insert into mybot_feedbackmodel (user_id, actual_question_id, asked_question, answer, score, processed, accepted) values ('{user_id}', '{q_id}', '{asked_question}', '{answer}', {score}, {processed}, {accepted})", one=True)
            print('Inserted successfully ! ! !')