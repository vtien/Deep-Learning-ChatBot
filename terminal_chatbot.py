#Version of chat bot that can run inside of your terminal shell

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pandas as pd
import html5lib
from textblob import TextBlob

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
data = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
labels = pickle.load(open('classes.pkl','rb'))

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    s_words = nltk.word_tokenize(sentence)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in s_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def chat():
    #this is the main function that allows for interaction with the bot
    print("Start talking with the bot (type quit to stop)")

    while True:
        inpt = input("You: ")
        if inpt.lower() == "quit":
            break
        
        p = bow(inpt, words, show_details=False)
        results = model.predict(np.array([p]))[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.75:
            if tag == "soccer_table":
                #webscraping component
                df = pd.read_html('https://www.premierleague.com/tables')
                table_df = df[0].iloc[::2]
                try:
                    table_df = table_df.drop(['Position  Pos', 'Unnamed: 11', 'Unnamed: 12'], axis=1)
                except:
                    pass
                print(table_df)

            elif tag=='feelings':
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg["responses"]
                #print normal response for this tag
                print(responses[0])

                while True:
                    feeling_inpt = input("You: ")

                    if feeling_inpt.lower() == 'end':
                        break

                    #now record user input and perform sentiment analysis
                    polarity = TextBlob(feeling_inpt).sentiment.polarity
                    if polarity > 0:
                        print("It seems you are feeling happy today. Great job, keep it up!")
                    elif polarity == 0:
                        print("You seem to be in a neutral state today")
                    else:
                        print("You seem to be feeling down or angry today :(")
            
            else:
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg['responses']
            
                print(random.choice(responses))
        else:
            print("I didn't get that, try typing something else")

if __name__ == "__main__":
    chat()