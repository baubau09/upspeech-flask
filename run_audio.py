from audio import *

audioURL="https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/uploads%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2_1650813052577.wav?alt=media&token=193fec13-387e-43d5-a2c7-851d9fab5d5f"
uid = "kmbSETfciMXU7ZKGkpXXE4fvnwK2"
fileName = "kmbSETfciMXU7ZKGkpXXE4fvnwK2_1650813052577.wav"
val_audio = validate_audio(audioURL, filename=fileName)

if val_audio == False:
    print ('Error')
if val_audio == True:
    transcript = transcribe_gcs(file_url=audioURL, filename=fileName, uid="kmbSETfciMXU7ZKGkpXXE4fvnwK2")
if val_audio == fileName:
    transcript = transcribe_gcs(file_url="", filename=fileName, uid=uid)
pace = get_pace(transcript=transcript, file_url=audioURL)
paceDesc = get_pace_desc(pace)
fillers = get_fillers(filename=fileName, url=audioURL)
words = count_words(transcript)
fillersPct = get_fillers_pct(fillers,words)
fillersDesc = get_fillers_desc(fillersPct)
# transcript = transcribe_gcs(file_url="kmbSETfciMXU7ZKGkpXXE4fvnwK2_1650675485622", filename="kmbSETfciMXU7ZKGkpXXE4fvnwK2_1650675485622.wav", uid="kmbSETfciMXU7ZKGkpXXE4fvnwK2")
# pace = get_pace(transcript, file_url="https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/uploads%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2_1650675485622.wav?alt=media&token=656ce1a5-c373-4a34-92ce-9c2ce2ee444b")
# sr = validate_audio("https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled4.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6")
# sr = validate_audio("https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2F7%20filler%20words.wav?alt=media&token=e1cbc2fd-1d76-469b-835b-47357e77252d")
# transcript, chunks = transcribe_gcs(file_url="gs://upspeech-48370.appspot.com/test/untitled4.wav", samplerate=sr)
# words = count_words(transcript)
# pace = get_pace(words, "https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled4.wav?alt=media&token=3284d1a0-5db2-4d39-963d-bd216b3f48f6")
# pace = get_pace(words, "https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2F7%20filler%20words.wav?alt=media&token=e1cbc2fd-1d76-469b-835b-47357e77252d")


print("Transcript: " + transcript)
# print("Number of words: " + str(words))
print("Pace: " + str(pace))
print("Pace: " + paceDesc)
print("Filled pauses: "+ str(fillers))
print("Filled pauses %: "+ str(fillersPct))
print("Filled pauses Desc: "+ fillersDesc)
print("Words: "+ str(words))
# print(chunks)
# print(sr)
os.remove(fileName)