import db_connection
from flask import Flask

app = Flask(__name__)

def update_user_suggestible_questions_to_db(user_id, sorted_suggestible_questions):
    with app.app_context():
        q_id = 0
        for res in db_connection.query_db(f"select id from mybot_questionanswermodel where question='{sorted_suggestible_questions[0]['question']}'"):
            q_id = res[0]
        if q_id != 0:
            asked_question = sorted_suggestible_questions[0]['question']
            answer = sorted_suggestible_questions[0]['answer']
            score = sorted_suggestible_questions[0]['score']
            processed = True if sorted_suggestible_questions[0]['processed'] == 'Y' else False
            accepted = True if sorted_suggestible_questions[0]['accepted'] == 'Y' else False
            db_connection.query_db("insert into "
                                              "mybot_feedbackmodel (user_id, actual_question_id, asked_question, answer, score, processed, accepted) "
                                              f"values ('{user_id}', '{q_id}', '{asked_question}', '{answer}', {score}, {processed}, {accepted})"
                                              "", one=True)
            print('Inserted successfully ! ! !')