import csv
import re
import string
import numpy as np
import unicodedata
from keras.layers.embeddings import Embedding
from numpy import array

#RNN Settings
maxAuthorizedSiseOfSentencesInWords = 128
embedding_size = 64    #Keras will make his own embeddings here
dropOutList = [0.0, 0.0] #List of dropouts per layer
nbEpochs = 10
vocab_size = 100000 #Upper bound estimate (to avoid collisions in each word Id allocation) of our corpus word count
numberOfLSTMLayers = 2

#Raw data : Here in UTF-8
reader = csv.reader(open(r"myDataFile.csv", encoding = 'utf-8'), delimiter = ";")
mydata = np.array(list(reader))
labels = array(list(mydata[:, 1]))

#Pre-treatment of raw data (example lowercase or remove punctuation)
##Lowercasing
mydata[:,0] = np.array(list(map(str.lower, mydata[:,0])))
##Replace accents and add space between word and punctuation so that "toto!" is not
def strip_accents(text): #Remove accents and finaly punctuation too
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)
    return str(text)
for i in range (0, len(mydata[:,0])):
    mydata[i,0] = strip_accents(mydata[i,0])
    #Remove punctuation accolate to words
    mydata[i,0] = str(' '.join(re.findall(r"\w+|[^\w\s]", mydata[i,0], re.UNICODE)))

#Keras tokenization
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
docs = list(mydata[:,0])
encoded_docs = [one_hot(word, vocab_size) for word in docs]

#Padding or truncate to make each word sequence the same length
padded_docs = pad_sequences(encoded_docs, maxlen=maxAuthorizedSiseOfSentencesInWords, padding='post')

#The RNN
from keras import Sequential
from keras.layers import LSTM, Dense, Dropout
model=Sequential()
model.add(Embedding(vocab_size, embedding_size, input_length=maxAuthorizedSiseOfSentencesInWords))
for i in range (0, numberOfLSTMLayers):
    dropOut = dropOutList[i]
    if i == numberOfLSTMLayers - 1:
        model.add(LSTM(maxAuthorizedSiseOfSentencesInWords, return_sequences=False))
        model.add(Dropout(rate = dropOut))
    else:
        model.add(LSTM(maxAuthorizedSiseOfSentencesInWords, return_sequences=True)) #return_sequences=True for the last LSTM layer
        model.add(Dropout(rate = dropOut))
model.add(Dense(1, activation='sigmoid')) #Dense dimension : 1 for sigmoid single output, 2 for softmax with 2 outputs etc...
print(model.summary())

#Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

#Evaluate on test data
reader = csv.reader(open(r"myNewdata.csv", encoding = 'utf-8'), delimiter = ";")
mydata = np.array(list(reader))
labels2 = array(list(mydata[:, 1]))
mydata[:,0] = np.array(list(map(str.lower, mydata[:,0])))
for i in range (0, len(mydata[:,0])):
    mydata[i,0] = strip_accents(mydata[i,0])
    mydata[i,0] = str(' '.join(re.findall(r"\w+|[^\w\s]", mydata[i,0], re.UNICODE)))
docs = list(mydata[:,0])
encoded_docs = [one_hot(word, vocab_size) for word in docs]
padded_docs2 = pad_sequences(encoded_docs, maxlen=maxAuthorizedSiseOfSentencesInWords, padding='post')

#Train the model
model.fit(padded_docs, labels, validation_data=(padded_docs2, labels2), epochs = nbEpochs)

#Save the model for further reuse, let's take JSON
model_jsonLight = model.to_json()
with open("modelLight.json", "w") as json_file:
    json_file.write(model_jsonLight)
model.save_weights("modelLight.h5")  #serialize weights to HDF5
