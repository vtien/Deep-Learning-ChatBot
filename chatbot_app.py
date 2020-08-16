from chat_bot import chat, chat_feelings, bow
from flask import Flask, render_template, request
import json
import pickle

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "My creator is Vishal Tien "

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg') #gets user input from html
    chatbot_response = chat(userText)

    if chatbot_response == "Sure thing! Please write a few sentences regarding your current mood/how you have been feeling today. I will keep giving you feedback on your mood until you type 'end'":
        feelings = chatbot_feelings()
        return feelings

    else:
        return str(chat(userText))

def chatbot_feelings():
    userText = request.args.get('msg')
    return str(chat_feelings(userText))

if __name__ == "__main__":
    app.run(debug=True)

