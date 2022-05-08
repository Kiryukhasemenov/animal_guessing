# -*- coding: utf-8 -*-
"""
Created on Thu May  5 22:10:58 2022

@author: Kirill Semenov
"""

import flask
import json
import os
import pandas as pd
from flask import send_from_directory, request
import random

# Flask app should start in global layout
app = flask.Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    processed_request = process_request(req)
    #'reply from webhook!'
    #if processed_request == 'CHOOSE':
    #    global a, df
    #    df = making_dataset()
    #   a = taking_random_animal(df)
    #   processed_request = "great! I've chosen an animal!"
        #global a, df
    #else:
    #    pass
    # if 'color' in req['queryResult']['parameters']:
    #     s = req['queryResult']['parameters']['color']
    # else:
    #     s = 'hello'
    #req = str(req)
    #result = str(df.loc['elephant'])
    return {
        'fulfillmentText': processed_request
    }

def making_dataset():
    df = pd.read_csv('animals.csv', index_col='animal')
#    dictionary = {
#            "elephant": ["grey","4","False","False","True"],
#            "frog":["green","4","False","False","False"],
#            "flamingo":["pink","2","True","False","False"],
#            "shark":["grey","0","False", "True", "True"],
#            "spyder":["various", "8", "False", "False", "False"]
#        }
#    
#    df = pd.DataFrame.from_dict(dictionary, orient='index', 
#                                columns=['color', 'numLegs', 'ifFlies', 'ifUnderwater', 'ifBiggerHuman'])
    
    return df

def taking_random_animal(df):
    num_animals = df.shape[0]
    idx = random.randint(0, num_animals)
    #global chosen_animal
    animal = df.iloc[idx].name
    return animal

def process_request(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    if intent =='welcome': # ok
        s = '''Hi! I am a bot for animal guessing game. 
        I think of an animal, you ask the questions and try to guess it. 
        Would you like to play?'''
    elif intent == 'start': # ok
        #chosen_animal = taking_random_animal(df)
        #global chosen_animal
        #s = 'CHOOSE'
        global a, df
        df = making_dataset()
        a = taking_random_animal(df)
        s = "great! I've chosen an animal!"
    elif intent == 'exit': #ok
        s = "okay, see you next time!"
        
    elif intent == 'request_color': # ok...
#        s = 'request_color detected'
        s = get_hint('color', df, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
# # strange to implement
#     elif intent == 'request_ifBiggerHuman': 
#         s = get_hint('ifBiggerHuman', df, a)
# # strange to implement
#     elif intent == 'request_ifFlies': 
#         s = get_hint('ifFlies', df, a)
# # strange to implement
#     elif intent == 'request_ifUnderwater': 
#         s = get_hint('ifUnderwater', df, a)

    elif intent == 'request_numLegs':  #???
        s = get_hint('numLegs', df, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    elif intent == 'guess_color': # ok
        color = parameters.get("color")
        #if color == 'red':
        #    s = 'yes, its red'
        #else:
        #    s = 'no, its red'
        s = process_color(color, df, a)
        #s = f'animal for color'
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    elif intent == 'guess_ifBiggerHuman': # ok
        size = parameters.get("size")
#        s = a
        s = process_ifBiggerHuman(size, df, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    elif intent == 'guess_ifFlies': #ok
        ifFlies = parameters.get("ifFlies")
        s = process_ifFlies(ifFlies, df, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    elif intent == 'guess_ifUnderwater':
        ifUnderwater = parameters.get("underwater") 
        #s = 'ifunderwater detected'
        s = process_ifUnderwater(ifUnderwater, df, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    elif intent == 'guess_numLegs': # ?
        num_legs = parameters.get("num_legs")
        s = process_numLegs()
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    elif intent == 'guess_animal':
        animal = parameters.get("animal")
        #if animal == 'elephant':
        #    s = 'yes, it is!'
        #else:
        #    s = 'no, try again'
#        s = f'animal'
        s = process_animal(animal, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)
    else:
        s = 'any other'
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)

    return intent+':   '+ s #+ '(animal: ' + a + ')'

def info_to_text(df, parameter, value):
    if parameter == 'ifFlies':
        if value == 'True':
            info = 'flies'
        else:
            info = 'cannot fly'
    elif parameter == 'ifUnderwater':
        if value == 'True':
            info = 'lives underwater'
        else:
            info = 'lives on land'
    elif parameter == 'ifBiggerHuman':
        if value == 'gt':
            info = 'bigger than human'
        elif value == 'lt':
            info = 'smaller than human'
        else:
            info = 'of the same size as human'
            
    elif parameter == 'ifFurry':
        if value == 'True':
            info = 'has fur'
        else:
            info = 'does not have fur'
    elif parameter == 'numLegs':
        if value != 0:
            info = 'does not have legs'
        else:
            info = f'has {str(value)} legs'
    return info

def get_hint(parameter, df, chosen_animal):
    #hint = df.loc[chosen_animal, parameter]
    if parameter == 'color':
        hint = df.loc[chosen_animal, 'color']
        s = f'the color of the animal is {hint}.'
        
    elif parameter == 'numLegs':
        hint = df.loc[chosen_animal, 'numLegs']
        processed_hint = info_to_text(df, parameter, hint)

#    elif parameter == :
#        processed_hint = hint_to_text(df, parameter, hint)
#    elif parameter == :
#        processed_hint = hint_to_text(df, parameter, hint)
#
#    elif parameter == :
#        processed_hint = hint_to_text(df, parameter, hint)#
#
#    elif parameter == :
#        processed_hint = hint_to_text(df, parameter, hint)
    
    #s = f'this animal {processed_hint}.'
    
    return s

def process_color(color, df, chosen_animal):
    if color == df.loc[chosen_animal, 'color']:
        s = f'yes, it is {color}.'
    else:
        s = f'no, it is {df.loc[chosen_animal, "color"]}.'
    return s

def process_ifFlies(ifFlies, df, chosen_animal):
    if ifFlies == df.loc[chosen_animal, 'ifFlies']:
        processed_ifFlies = info_to_text(df, 'ifFlies', ifFlies)
        s = f'yes, it {processed_ifFlies}.'
    else:
        processed_ifFlies = info_to_text(df, 'ifFlies', df.loc[chosen_animal, 'ifFlies'])        
        s = f'wrong, it {processed_ifFlies}.'
    return s

def process_ifUnderwater(ifUnderwater, df, chosen_animal):
    if ifUnderwater == df.loc[chosen_animal, 'ifUnderwater']:
        processed_ifUnderwater = info_to_text(df, 'ifUnderwater', ifUnderwater)
        s = f'yes, it {processed_ifUnderwater}.'
    else:
        processed_ifUnderwater = info_to_text(df, 'ifUnderwater', df.loc[chosen_animal, 'ifUnderwater'])
        s = f'no, it {processed_ifUnderwater}.'
    return s

def process_ifBiggerHuman(size, df, chosen_animal):
#    s = 'in process size'
    processed_info = info_to_text(df, 'ifBiggerHuman', size)

    if size == df.loc[chosen_animal, 'ifBiggerHuman']:
        s = f'yes, the animal is {processed_info}.'
    else:
       s = f'no, the animal is not {processed_info}.'
    return s

def process_numLegs(num_legs, df, chosen_animal):
    if num_legs == df.loc[chosen_animal, 'numLegs']:
        num_legs_corrected = info_to_text(df, 'numLegs', num_legs)
        s = f'yes, the animal {num_legs_corrected}.'
    else:
        s = 'no, the animal has another number of legs.'
    return s

def process_animal(animal, chosen_animal):
    if animal == chosen_animal:
        s = f'Congratulations, you win! It is {animal}. Would you like to play once more?'
    else:
        s = 'you are wrong; try again!'
    return s
    #cust_name = parameters.get("cust_name")
    #cust_contact = parameters.get("cust_contact")
    #cust_email = parameters.get("cust_email")

if __name__ == "__main__":
    #df = making_dataset()
    #animal = taking_random_animal(df)
    #import logging
    #logging.basicConfig(filename='error.log',level=logging.ERROR)
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()


# from flask import Flask, request

# app = Flask(__name__)

# @app.route('/', methods=["POST", "GET"])
# def webhook():
#     if request.method == "GET":
#         return "Not connected to DF bro"
#     elif request.method == "POST":
#         payload = request.json
#         user_response = (payload['queryResult']['queryText'])
#         bot_response = (payload['queryResult']['fulfillmentText'])
#         if user_response or bot_response != "":
#             print("User: " + user_response)
#             print("Bot: " + bot_response)
#         return "Message received"
#     else:
#         print(request.data)
#         return "200"
    
# if __name__ == "__main__":
#     app.run(debug=True)