from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
import datetime
import threading
from time import sleep

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('upspeech-firebase-key.json')
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
        # fileName = request.json['fileName']
        # audioURL = request.json['audioURL']
        speechID = request.json['speechID']
        # script = request.json['script']

        userRef = db.collection(u'users').document(uid)
        speechRef = userRef.collection(u'speeches').document(speechID)

        result = jsonify({
            "uid": uid,
            "username": username,
            # "fileName": fileName,
            # "audioURL": audioURL,
            "speechID": speechID,
            # "script": script,
            # "userRef": userRef,
            # "speechRef": speechRef

        })

        speechRef.update({u'fillers': 4, u'fillersDesc': 'abc'})
        my_result = speechRef.get()
        print(my_result.to_dict())
        return result, 200
    except Exception as e:
        return f"An Error Occured: {e}"