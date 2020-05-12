from pymongo import MongoClient
from flask import g
from flask import Flask

app = Flask(__name__)

class MongoConnection:
    client = None

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = MongoClient(self.connection_string)

    def get_client(self):
        return self.client

    def close(self):
        self.client.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn_string = 'mongodb+srv://admin:admin@faqbot-cluster-56f3s.mongodb.net/test?retryWrites=true&w=majority'
        db = g._database = MongoConnection(conn_string).get_client()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()