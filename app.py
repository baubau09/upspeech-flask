from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
import datetime
import threading
from time import sleep
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Initialize Firestore DB
cred = credentials.Certificate('upspeech-firebase-key.json')
default_app = initialize_app(cred)
db = firestore.client()
dbRef = db.collection('users')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/test", methods=['POST'])
def getBlob():
    try:
        blobFile = request.files['file']
        if blobFile.filename != '':
            blobFile.save(blobFile.filename)

        result = jsonify({
            "fileName": blobFile.filename,
            # "audioURL": audioURL,
            # "script": script,
            # "userRef": userRef,
            # "speechRef": speechRef

        })
        return result, 200
    except Exception as e:
        return f"An Error Occured: {e}"

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

        userRef = db.collection(u'users').document(uid)
        speechRef = userRef.collection(u'speeches').document(speechID)

        result = jsonify({
            "uid": uid,
            "username": username,
            "speechID": speechID,
            "fileName": fileName,
            "audioURL": audioURL,
            "script": script,
            "userRef": userRef,
            "speechRef": speechRef

        })

        speechRef.update({u'fillers': 33, u'fillersDesc': 'Needs Improvement'})
        my_result = speechRef.get()
        print(my_result.to_dict())
        return result, 200
    except Exception as e:
        return f"An Error Occured: {e}"