import pandas as pd
import numpy as np
import io
import os
import soundfile as sf
from six.moves.urllib.request import urlopen
import librosa
import librosa.display as ld
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
import joblib
from tensorflow import keras

### Data augmentation
def noise(data):
    noise_amp = 0.035*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data

def stretch(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate)

def shift(data):
    shift_range = int(np.random.uniform(low=-5, high = 5)*1000)
    return np.roll(data, shift_range)

def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)

# Feature extraction functions
def extract_features(data, sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result = np.hstack((result, zcr))  # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft))  # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc))  # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms))  # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel))  # stacking horizontally

    return result

def get_features(url, fileName):
    if (os.path.isfile(fileName)):
        data, sample_rate = librosa.load(fileName, duration=2.5, offset=0.6)
    else:
        data, sample_rate = librosa.load(io.BytesIO(urlopen(url).read()), duration=2.5, offset=0.6)
    # duration and offset are used to take care of the no audio in start and the ending of each audio files as seen above.
    
    
    # without augmentation
    res1 = extract_features(data, sample_rate)
    result = np.array(res1)
    
    # data with noise
    noise_data = noise(data)
    res2 = extract_features(noise_data,sample_rate)
    result = np.vstack((result, res2)) # stacking vertically
    
    # data with stretching and pitching
    # new_data = stretch(data)
    # data_stretch_pitch = pitch(new_data, sample_rate)
    # res3 = extract_features(data_stretch_pitch,sample_rate)
    # result = np.vstack((result, res3)) # stacking vertically
    
    return result

def emotion_result(audioURL, filename):
    ## Initialize model
    model = keras.models.load_model("ml/speech_emotion.h5")

    ## Initialize X array
    X = []

    ## Extract audio features
    audio_feature = get_features(audioURL, filename)
    for item in audio_feature:
        X.append(item)

    ### Added features to dataframe
    features_with_augmentation = pd.DataFrame(X)
    original_feature = features_with_augmentation.drop(axis=0,labels=[1])

    ## Normalize features
    scaler = StandardScaler()
    X_input = scaler.fit_transform(original_feature)

    ## Encoder for output labels
    encoder = OneHotEncoder()
    my_features = pd.read_csv("ml/my_features.csv")
    Y = my_features['labels'].values
    Y = encoder.fit_transform(np.array(Y).reshape(-1,1)).toarray()

    ## Prediction
    prediction = model.predict(original_feature)
    predicted_label = encoder.inverse_transform(prediction)

    print("Emotion:")
    print(predicted_label.flatten()[0])

    return str(predicted_label.flatten()[0])