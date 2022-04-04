import io
import os
import librosa
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf
import base64
from six.moves.urllib.request import urlopen
from scipy.io import wavfile
import scipy.signal as sps

def format_audio():
    """
        Format the audio file for Google Speech API
    """
    return 0

def validate_audio(url):
    """
        Validate if the audio is in correct format for Google Speech API
        16kHz sample rate
        1 channel
    """
    data, samplerate = sf.read(io.BytesIO(urlopen(url).read()))
    return samplerate



def transcribe_gcs(file_url, samplerate):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=file_url)

    ### Config for Tri's voice
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=samplerate,
        language_code="en-UK",
        enable_word_confidence=True,
        audio_channel_count=1
    )

    ### Config for Anh's voice
    # config = speech.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=samplerate,
    #     language_code="en-US",
    #     enable_word_confidence=True,
    #     audio_channel_count=2
    # )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=3000)

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
    return k, chunks

def count_words(k):
    return len(k.split())

def get_pace(words, file_url):
    url = file_url
    # data, samplerate = sf.read(io.BytesIO(urlopen(url).read()))
    # filename = librosa.ex('')
    # y, sr = librosa.load(filename)
    #duration = librosa.get_duration(y=data, sr=samplerate)
    duration = AudioSegment.from_file(io.BytesIO(urlopen(url).read())).duration_seconds
    s_to_m = (duration)*(1.0/60.0)
    wpm = words/s_to_m
    return int(wpm)

sr = validate_audio("https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled4.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6")
# sr = validate_audio("https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2F7%20filler%20words.wav?alt=media&token=e1cbc2fd-1d76-469b-835b-47357e77252d")
transcript, chunks = transcribe_gcs(file_url="gs://upspeech-48370.appspot.com/test/untitled4.wav", samplerate=sr)
words = count_words(transcript)
pace = get_pace(words, "https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled4.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6")
# pace = get_pace(words, "https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2F7%20filler%20words.wav?alt=media&token=e1cbc2fd-1d76-469b-835b-47357e77252d")


print("Transcript: " + transcript)
print("Number of words: " + str(words))
print("Pace: " + str(pace))
# print(chunks)
# print(sr)