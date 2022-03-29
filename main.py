from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage
from google.cloud import storage

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"