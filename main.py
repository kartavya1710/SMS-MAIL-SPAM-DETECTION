import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import sklearn

ps = PorterStemmer()

def Datapreprocessing(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []

    for i in text:
        if i.isalnum():
            y.append(i)
    text = y.copy()
    y.clear()

    for i in text:
        if i not in string.punctuation and i not in stopwords.words('english'):
            y.append(i)

    text = y.copy()
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    text = y[:]
    y.clear()

    text = " ".join(text)
    return text

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title('Email/SMS Spam Classifier   ')


input_sms = st.text_area('Enter the EmailSMS : ')

if st.button('Predict'):

    # 1. preprocess
    transformed_sms = Datapreprocessing(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header("Spam ! Be Careful AMIGO ;)")
    else:
        st.header("Not Spam ! Go ahead buddy :D ")