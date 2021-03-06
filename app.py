from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
import datetime
import threading
from time import sleep
from flask_cors import CORS, cross_origin
from audio import *
#from filler import *
from emotion import *

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
        Main Evaluation API route
        
    """
    try:

        # Request params
        uid = request.json['uid']
        username = request.json['username']
        fileName = request.json['fileName']
        audioURL = request.json['audioURL']
        speechID = request.json['speechID']
        script = request.json['script']

        # Firestore Document reference params
        userRef = db.collection(u'users').document(uid)
        speechRef = userRef.collection(u'speeches').document(speechID)

        # Result values initialize
        wordCount = 0
        fillers = 0
        fillersDesc = ''
        fillersPct = 0.0
        pace = 0
        paceDesc = ''
        transcript = ''
        

        # Audio validation value
        val_audio = validate_audio(audioURL, filename=fileName)

        if val_audio == False:
            error_result = jsonify({"message":'Current audio is < 44100Hz or < 16-bit depth, please input a better audio file'})
            return error_result, 500
        if val_audio == True:
            transcript, alternative = transcribe_gcs(file_url=audioURL, filename=fileName, uid=uid)
        if val_audio == fileName:
            transcript, alternative = transcribe_gcs(file_url="", filename=fileName, uid=uid)
        print("Transcript: " + transcript)
        print("Ideal transcript: " + script)

        wordCount = count_words(transcript)
        print("Words: "+ str(wordCount))

        pace = get_pace(transcript, audioURL)
        print("Pace: " + str(pace))

        paceDesc = get_pace_desc(pace)
        print("Pace: " + paceDesc)

        fillers = get_fillers(fileName, audioURL)
        print("Filled pauses: "+ str(fillers))

        fillersPct = get_fillers_pct(fillers,wordCount)
        print("Filled pauses %: "+ str(fillersPct))

        fillersDesc = get_fillers_desc(fillersPct)
        print("Filled pauses Desc: "+ fillersDesc)

        print("Ideal Words: " + str(count_words(script)))

        emotion = emotion_result(audioURL, fileName)
        print("Emotion: " + emotion)
        

        # Remove file after processing
        if os.path.isfile("filler_" + fileName):
            os.remove("filler_" + fileName)
        textgrid_name = "voices/" + fileName[:-4] + ".TextGrid"
        os.remove(fileName)
        os.remove(textgrid_name)

        
        # initialize variables to avoid API crash because of errors in get_pronun_words #
        pronunWords = ''
        pronunWordsIdx = []
        pronunCount = 0
        pronunPct = 0
        pronunDesc = ''
        # initialize variables to avoid API crash #

        # TODO: Fix bugs in get_pronun_words
        #### errors in get_pronun_words. Must fix
        pronunWords, pronunWordsIdx = get_pronun_words(script, transcript, alternative)
        pronunCount = len(pronunWords)
        print("Pronunciation count: " + str(pronunCount))

        pronunPct = get_pronun_pct(wordCount, pronunCount)
        print("Pronunciation %: " + str(pronunPct))
        
        pronunDesc = get_pronun_desc(pronunPct)
        print("Pronunciation Desc: " + pronunDesc)
        
        # get_word_level_conf(alternative)
        # for item in pronunWords:
        #     print(item)
        
        result = jsonify({
            "uid": uid,
            "username": username,
            "speechID": speechID,
            "fileName": fileName,
            "audioURL": audioURL,
            "script": script,
            "pace": pace,
            "paceDesc": paceDesc,
            "fillers": fillers,
            "fillersDesc": fillersDesc,
            "fillersPct": fillersPct,
            "wordCount": wordCount,
            "pronunErr": pronunCount,
            "pronunErrPct": pronunPct,
            "pronunErrDesc": pronunDesc,
            "pronunWords": pronunWords,
            "pronunWordsIdx": pronunWordsIdx,
            "emotion": emotion
        })

        # print results to console
        print(result)

        # Update firebase parameters
        speechRef.update({u'fillers': fillers ,u'fillersDesc': fillersDesc, u'fillersPct': fillersPct, u'pace': pace, u'paceDesc': paceDesc, u'wordCount': wordCount, u"pronunErr": pronunCount,u"pronunErrPct": pronunPct,u"pronunErrDesc": pronunDesc, u'pronunWords': pronunWords, u'pronunWordsIdx': pronunWordsIdx, u'emotion': emotion, u'updatedAt': datetime.datetime.now()})

        
        

        # return
        return result, 200
    except Exception as e:
        return f"An Error Occured: {e}"