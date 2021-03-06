from parselmouth.praat import run_file
import parselmouth
import os
import sys, contextlib, io
from six.moves.urllib.request import urlopen
import urllib.request
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
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
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