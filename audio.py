import io
import os
import librosa
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf
import base64
from six.moves.urllib.request import urlopen



def transcribe_gcs():
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri="gs://upspeech-48370.appspot.com/test/untitled3.wav")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-UK",
        enable_word_confidence=True
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=3000)

    k = ""



    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        # print("-" * 20)
        # print("First alternative of result {}".format(i))
        # print(u"Transcript: {}".format(alternative.transcript))
        k = k + alternative.transcript
        # print(
        #     u"First Word and Confidence: ({}, {})".format(
        #         alternative.words[0].word, alternative.words[0].confidence
        #     )
        # )
    return k

def count_words_from_transcribed(k):
    return len(k.split())

def get_pace(words):
    url = "https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled3.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6"
    data, samplerate = sf.read(io.BytesIO(urlopen(url).read()))
    # filename = librosa.ex('')
    # y, sr = librosa.load(filename)
    duration = librosa.get_duration(y=data, sr=samplerate)
    s_to_m = (duration)*(1.0/60.0)
    wpm = words/s_to_m
    return wpm

transcript = transcribe_gcs()
words = count_words_from_transcribed(transcript)
pace = get_pace(words)
print(transcript)
print(words)
print(pace)