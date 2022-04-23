from audio import *

audioURL="https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/uploads%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2_1650676225600.wav?alt=media&token=85b9b27e-bdce-415a-98f5-6fbb06abb598"
uid = "kmbSETfciMXU7ZKGkpXXE4fvnwK2"
fileName = "kmbSETfciMXU7ZKGkpXXE4fvnwK2_1650676225600.wav"
val_audio = validate_audio(audioURL, filename=fileName)

if val_audio == False:
    print ('Error')
if val_audio == True:
    transcript = transcribe_gcs(file_url=audioURL, filename=fileName, uid="kmbSETfciMXU7ZKGkpXXE4fvnwK2")
if val_audio == fileName:
    transcript = transcribe_gcs(file_url="", filename=fileName, uid=uid)
pace = get_pace(transcript=transcript, file_url=audioURL)
fillers = get_fillers(filename=fileName, url=audioURL)
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
print("Filled pauses: "+ str(fillers))
# print(chunks)
# print(sr)
os.remove(fileName)