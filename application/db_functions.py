import db_connection
from flask import Flask

app = Flask(__name__)

def get_questionanswermodel():
    with app.app_context():
        conn = db_connection.get_db()
        db = conn.faqbot
        collection = db['mybot_questionanswermodel']
        records = collection.find()
        return records

def get_categorymodel():
    with app.app_context():
        conn = db_connection.get_db()
        db = conn.faqbot
        collection = db['mybot_categorymodel']
        records = collection.find()
        return records

def get_genericquestionmodel():
    with app.app_context():
        conn = db_connection.get_db()
        db = conn.faqbot
        collection = db['mybot_genericquestionmodel']
        records = collection.find()
        return records