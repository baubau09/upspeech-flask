from numpy import true_divide
import soundfile as sf
from soundfile import SoundFile
import io
import os
from six.moves.urllib.request import urlopen
from scipy.io import wavfile
import scipy.signal as sps
from pydub import AudioSegment

def validate_audio(url, filename):
    """
        Validate if the audio is in correct format for Google Speech API
        44.1kHz sample rate
        1 channel
        16-bit depth
    """
    #audio = sf.SoundFile(io.BytesIO(urlopen(url).read()))
    sound = AudioSegment.from_wav(io.BytesIO(urlopen(url).read()))
    # if ((audio.samplerate < 44100) or audio.subtype == 'PCM_S8'):
    #     return 'Current audio is < 44100Hz or < 16-bit depth, please input a better audio file'
    # if ((audio.samplerate == 44100) and audio.subtype == 'PCM_16' and audio.channels == 1 ):
    #     return True
    # else:
    #     sf.write(file=filename+'.wav', samplerate=44100, subtype='PCM_16', )
    if ((sound.frame_rate < 44100) or sound.sample_width == 1):
        return 'Current audio is < 44100Hz or < 16-bit depth, please input a better audio file'
    if ((sound.frame_rate == 44100) and sound.sample_width == 2 and sound.channels == 1 ):
        return True
    else:
        sound2 = sound.set_sample_width(2)
        sound2 = sound2.set_frame_rate(44100)
        sound2 = sound2.set_channels(1)
        file_handle = sound2.export(filename, format="wav")
    # data, samplerate  = sf.read(io.BytesIO(urlopen(url).read()))
    return 'The new sample rate is ' + str(sound2.frame_rate) + ', bit-depth is ' + str(sound2.sample_width*8) + ', channel is ' + str(sound2.channels)

# print(validate_audio("https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled5.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6", "test_untitled5.wav"))