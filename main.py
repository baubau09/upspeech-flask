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


@app.route("/api/eval", methods=['POST'])
def evaluation():
    """
        Test API routes
        
    """
    try:
        uid = request.json['uid']
        username = request.json['username']
        fileName = request.json['fileName']
        audioURL = request.json['audioURL']
        speechID = request.json['speechID']
        script = request.json['script']

        userRef = db.collection(u'users').document(u'uid')
        speechRef = userRef.collection(u'speeches').document(u'speechID')

        result = jsonify({
            "uid": uid,
            "username": username,
            "fileName": fileName,
            "audioURL": audioURL,
            "speechID": speechID,
            "script": script,
            "userRef": userRef,
            "speechRef": speechRef

        })
        return result, 200
    except Exception as e:
        return f"An Error Occured: {e}"