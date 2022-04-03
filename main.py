from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app, storage
from google.cloud import storage
from google.cloud import firestore


app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
dbRef = db.collection('users')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/eval", methods=['POST', 'PUT'])
def evaluation():
    """
        evaluation(): Update fields from a document with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'
        
    """
    try:
        uid = request.json['uid']
        username = request.json['username']
        audioURL = request.json['audioURL']
        speechID = request.json['speechID']
        script = request.json['script']

        userRef = db.collection(u'users').document(u'uid')
        speechRef = userRef.collection(u'speeches').document(u'speechID')
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"