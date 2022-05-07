from emotion import *

model = keras.models.load_model("speech_emotion.h5")

url = "https://firebasestorage.googleapis.com/v0/b/upspeech-48370.appspot.com/o/test%2Funtitled7.wav?alt=media&token=50ff4466-4ecb-48ce-b1da-c42e2aee9f41"
X = []
feature = get_features(url)
for item in feature:
    X.append(item)
# print("features")
# print(feature)
# print("X")
# print(X)

Features = pd.DataFrame(X)
single = Features.drop(axis=0,labels=[1])
encoder = OneHotEncoder()
my_features = pd.read_csv("my_features.csv")
Y = my_features['labels'].values
Y = encoder.fit_transform(np.array(Y).reshape(-1,1)).toarray()


scaler = StandardScaler()
X_input = scaler.fit_transform(single)
prediction = model.predict(single)
print(prediction)
predicted_label = encoder.inverse_transform(prediction)

print("Emotion:")
print(predicted_label.flatten()[0])

# Features.to_csv('features.csv', index=False)


#single.to_csv('single.csv',index=False)