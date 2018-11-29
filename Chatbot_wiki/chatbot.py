# coding: utf-8

import nltk

#nltk.download() # for downloading packages
import random
import string  # to process standard python strings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

class Chatbot :
    f = open('chatbot.txt', 'r', errors='ignore')
    raw = f.read()
    raw = raw.lower()  # converts to lowercase
    # nltk.download('punkt') # first-time use only
    # nltk.download('wordnet') # first-time use only
    sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
    word_tokens = nltk.word_tokenize(raw)  # converts to list of words

    sent_tokens[:2]

    word_tokens[:5]

    lemmer = nltk.stem.WordNetLemmatizer()

    def LemTokens(self, tokens):
        lemmer = self.lemmer
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    # Checking for greetings
    def greeting(self, sentence):
        """If user's input is a greeting, return a greeting response"""
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    # Generating response
    def response(self, user_response):
        robo_response = ''
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if (req_tfidf == 0):
            robo_response = robo_response + "I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            return robo_response

    def chat(self, user_response):
        str = ""
        user_response = user_response.lower()
        if (user_response != 'bye' and user_response != 'clear'):
            if (user_response == 'thanks' or user_response == 'thank you'):
                str += "You are welcome.."
            else:
                if (self.greeting(user_response) != None):
                    str += self.greeting(user_response)
                else:
                    self.sent_tokens.append(user_response)
                    word_tokens = self.word_tokens + nltk.word_tokenize(user_response)
                    final_words = list(set(word_tokens))
                    str += self.response(user_response)
                    self.sent_tokens.remove(user_response)
        return str


