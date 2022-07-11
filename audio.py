import io
import os
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
# import soundfile as sf
# from soundfile import SoundFile
from six.moves.urllib.request import urlopen
import urllib.request
from parselmouth.praat import run_file
import parselmouth
from google.oauth2 import service_account
from string import punctuation

gg_cred = service_account.Credentials.from_service_account_file("upspeech-firebase-key.json")

def validate_audio(url, filename):
    """
        Validate if the audio is in correct format for Google Speech API
        44.1kHz sample rate
        1 channel
        16-bit depth
    """
    #audio = sf.SoundFile(io.BytesIO(urlopen(url).read()))
    sound = AudioSegment.from_file(io.BytesIO(urlopen(url).read()))
    # if ((audio.samplerate < 44100) or audio.subtype == 'PCM_S8'):
    #     return 'Current audio is < 44100Hz or < 16-bit depth, please input a better audio file'
    # if ((audio.samplerate == 44100) and audio.subtype == 'PCM_16' and audio.channels == 1 ):
    #     return True
    # else:
    #     sf.write(file=filename+'.wav', samplerate=44100, subtype='PCM_16', )
    if ((sound.frame_rate < 44100) or sound.sample_width == 1):
        print('Current audio is < 44100Hz or < 16-bit depth, please input a better audio file')
        return False
    if ((sound.frame_rate == 44100) and sound.sample_width == 2 and sound.channels == 1 ):
        return True
    else:
        sound2 = sound.set_sample_width(2)
        sound2 = sound2.set_frame_rate(44100)
        sound2 = sound2.set_channels(1)
        file_handle = sound2.export(filename, format="wav")
    # data, samplerate  = sf.read(io.BytesIO(urlopen(url).read()))
    return filename

# print(validate_audio("https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled5.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6", "test_untitled5.wav"))

def transcribe_gcs(file_url, filename, uid):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient(credentials=gg_cred)

    if file_url == "":
        speech_file = filename
        with open(speech_file, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
    else:
        url = "gs://upspeech-48370.appspot.com/uploads/" + uid + "/" + filename
        audio = speech.RecognitionAudio(uri=url)

    ### Config 
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_confidence=True
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=5000)

    k = ""
    chunks = 0

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        # print("-" * 20)
        # print("First alternative of result {}".format(i))
        # print(u"Transcript: {}".format(alternative.transcript))
        """Print a whole transcript sentence"""
        k = k + alternative.transcript
        
        """Print the number of consecutive portions"""
        chunks = chunks + 1

        """Print all words and its confidence level from the alternative.words array"""
        # for item in alternative.words:
        #     print(item.word, item.confidence)

        # print(
        #     u"First Word and Confidence: ({}, {})".format(
        #         alternative.words[0].word, alternative.words[0].confidence
        #     )
        # )
    return k, alternative

def count_words(k):
    return len(k.split())

def get_pace(transcript, file_url):
    url = file_url
    words = len(transcript.split())
    duration = AudioSegment.from_file(io.BytesIO(urlopen(url).read())).duration_seconds
    s_to_m = (duration)*(1.0/60.0)
    wpm = words/s_to_m
    return int(wpm)

def run_praat_file(m, p):
    """
    p : path to dataset folder
    m : file name
    returns : objects outputed by the praat script
    """
    sound=p+"/"+m
    sourcerun=p+"/"+"essen"+"/"+"myspsolution.praat"
    path=p+"/"+"voices"

    assert os.path.isfile(sound), "Wrong path to audio file"
    assert os.path.isfile(sourcerun), "Wrong path to praat script"
    assert os.path.isdir(path), "Wrong path to audio files"
    try:
        objects= run_file(sourcerun, -20, 4, 0.6, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        #print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        # print(z1)
        # print(z2)
        return z2
    except:
        z3 = 0
        print ("Try again the sound of the audio was not clear")
        pass

def get_fillers(filename, url):
    """
    Detect and count number of fillers and pauses
    """
    
    file = ''
    # Check if a processed file is already on disk
    if (os.path.isfile(filename)):
        file = filename
    else:
        # If not, download from Firebase and Save file to disk
        file = "filler_" + filename
        urllib.request.urlretrieve(url, file)

    p = "/Users/katietran/UpSpeech/upspeech-flask"
    z2 = run_praat_file(filename, p)
    z3=int(z2[1])
    z4=float(z2[3]) 
    #print ("fillers=", z3)
    return z3

def get_pace_desc(pace):
    if (pace >= 100 and pace <= 160):
        return 'Just Right'
    if (pace < 100):
        return 'Too Slow'
    if (pace > 160):
        return 'Too Fast'

def get_fillers_pct(fillers, words):
    return round(((fillers/words) * 100),1)

def get_fillers_desc(pct):
    if (pct <= 3.0):
        return 'Perfect'
    if (pct > 3.0 and pct < 25.0):
        return 'Good'
    if (pct >= 25.0 and pct <= 65.0):
        return 'Needs Improvement'
    if (pct > 65.0):
        return 'Bad'    

def get_word_level_conf(alternative):
    words = alternative.words
    for item in alternative.words:
        print(item.word, item.confidence)

def get_pronun_words(ideal_transcript, transcript, alt):
    ideal_array = ideal_transcript.lower().split()
    transcript_array = transcript.lower().split()
    my_dict = {}
    for index, item in enumerate(alt.words):
        if (item.confidence <= 0.81):
            my_dict[index] = {
                "index": index,
                "word": item.word,
                "conf": item.confidence
            }

    my_dict_keys = list(my_dict.keys())
    wrong_idx = []
    wrong_words = []
    wrong_words_idx = []
    for item in my_dict_keys:
        wrong_idx.append(item)

    if len(wrong_idx) == 0:
        return wrong_words
    
    for i in range(wrong_idx[0], wrong_idx[len(wrong_idx)-1]+1, 1):
        if transcript_array[i] != ideal_array[i].strip(punctuation):
            wrong_words.append(ideal_array[i])
            wrong_words_idx.append(i)

    return wrong_words, wrong_words_idx

def get_pronun_pct(words, wrong_words_count):
    return round(((wrong_words_count/words) * 100),1)

def get_pronun_desc(pct):
    if (pct <= 3.0):
        return 'Perfect'
    if (pct > 3.0 and pct < 30.0):
        return 'Good'
    if (pct >= 30.0 and pct <= 70.0):
        return 'Needs Improvement'
    if (pct > 70.0):
        return 'Bad'

