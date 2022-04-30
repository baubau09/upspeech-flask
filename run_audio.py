from audio import *

audioURL="https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/uploads%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2%2FkmbSETfciMXU7ZKGkpXXE4fvnwK2_1650852629649.wav?alt=media&token=408c9528-5e5e-4acc-b738-47bf0b7f0510"
uid = "kmbSETfciMXU7ZKGkpXXE4fvnwK2"
fileName = "kmbSETfciMXU7ZKGkpXXE4fvnwK2_1650852629649.wav"
val_audio = validate_audio(audioURL, filename=fileName)

if val_audio == False:
    print ('Error')
if val_audio == True:
    transcript, alt = transcribe_gcs(file_url=audioURL, filename=fileName, uid="kmbSETfciMXU7ZKGkpXXE4fvnwK2")
if val_audio == fileName:
    transcript, alt = transcribe_gcs(file_url="", filename=fileName, uid=uid)
pace = get_pace(transcript=transcript, file_url=audioURL)
paceDesc = get_pace_desc(pace)
fillers = get_fillers(filename=fileName, url=audioURL)
words = count_words(transcript)
fillersPct = get_fillers_pct(fillers,words)
fillersDesc = get_fillers_desc(fillersPct)
ideal_transcript = "Hello, good morning everyone, this is Katie, nice to meet you"
ideal_words = count_words(ideal_transcript)
ideal_array = ideal_transcript.split()
transcript_array = transcript.split()
pronunWords = len(get_pronun_words(ideal_transcript,transcript,alt))
pronunPct = get_pronun_pct(words, pronunWords)
pronunDesc = get_pronun_desc(pronunPct)
get_pronun_desc
# print("Number of words: " + str(words))
print("Pace: " + str(pace))
print("Pace: " + paceDesc)
print("Filled pauses: "+ str(fillers))
print("Filled pauses %: "+ str(fillersPct))
print("Filled pauses Desc: "+ fillersDesc)
print("Ideal transcript: " + ideal_transcript)
print("Words: " + str())
print("Transcript: " + transcript)
print("Words: "+ str(words))
print("Pronunciation count: " + str(pronunWords))
print("Pronunciation %: " + str(pronunPct))
print("Pronunciation Desc: " + pronunDesc)
get_word_level_conf(alt)

# my_dict = {}
# for index, item in enumerate(alt.words):
#     if (item.confidence <= 0.81):
#         my_dict[index] = {
#             "index": index,
#             "word": item.word,
#             "conf": item.confidence
#         }
        

# print(my_dict)

# my_dict_keys = list(my_dict.keys())
# wrong_idx = []
# for item in my_dict_keys:
#     wrong_idx.append(item)

# for item in wrong_idx:
#     print(item)

# wrong_words = []
# if len(alt.words) < len(ideal_array):
#     for i in range(wrong_idx[0], wrong_idx[len(wrong_idx)-1]+1, 1):
#         if transcript_array[i] != ideal_array[i]:
#             wrong_words.append(ideal_array[i])

# for item in wrong_words:
#     print(item)


# print(chunks)
# print(sr)
os.remove(fileName)
textgrid_name = "voices/" + fileName[:-4] + ".TextGrid"
os.remove(textgrid_name)