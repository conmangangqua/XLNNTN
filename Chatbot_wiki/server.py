#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from flask import Flask, render_template, request, json
import os
from chatbot import Chatbot

CWD_PATH = os.getcwd()

host = '192.168.137.226'
port = 8000

app = Flask(__name__, static_url_path='/static')
app.config.update(
    ENV = "development"
)

@app.route('/', methods = ['GET'])
def open_web():
    return render_template("chatbot.html")

@app.route('/up', methods = ['POST'])
def response_chat():
    chatbot = Chatbot()
    if request.method == 'POST':
        string = request.form["text"]
        response_string = chatbot.chat(string)
        return response_string

if __name__ == '__main__':
   app.run(host = host, port = port)