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

app = flask.Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    processed_request = process_request(req)
    return {
        'fulfillmentText': processed_request
    }

def making_dataset():
    df = pd.read_csv('animals.csv', index_col='animal')
    
    return df

def taking_random_animal(df):
    num_animals = df.shape[0]
    idx = random.randint(0, num_animals)
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
        global a, df

        if 'a' in globals():
            del a
        if 'df' in globals():
            del df
        df = making_dataset()
        a = taking_random_animal(df)
        s = "great! I've chosen an animal!"
    elif intent == 'exit': #ok
        s = "okay, see you next time!"
        
    elif intent == 'request_color': # ok...
        s = get_hint('color', df, a)
        with open('log.csv', 'a', encoding='utf-8') as f:
            f.write(a)

    elif intent == 'request_numLegs':  #???
        s = get_hint('numLegs', df, a)

    elif intent == 'guess_color': # ok
        color = parameters.get("color")
        s = process_color(color, df, a)

    elif intent == 'guess_ifBiggerHuman': # ok
        size = parameters.get("size")
        s = process_ifBiggerHuman(size, df, a)

    elif intent == 'guess_ifFlies': #ok
        ifFlies = parameters.get("ifFlies")
        s = process_ifFlies(ifFlies, df, a)
    elif intent == 'guess_ifUnderwater':
        ifUnderwater = parameters.get("underwater") 
        s = process_ifUnderwater(ifUnderwater, df, a)

    elif intent == 'guess_numLegs': # ?
        num_legs = parameters.get("num_legs")
        s = process_numLegs(num_legs, df, a)

    elif intent == 'guess_animal':
        animal = parameters.get("animal")
        s = process_animal(animal, a)

    else:
        s = 'could you rephrase or restart?'

    return s 

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
        if value == 0:
            info = 'does not have legs'
        else:
            info = f'has {str(value)} legs'
    return info

def get_hint(parameter, df, chosen_animal):
    if parameter == 'color':
        hint = df.loc[chosen_animal, 'color']
        s = f'the color of the animal is {hint}.'
        
    elif parameter == 'numLegs':
        hint = df.loc[chosen_animal, 'numLegs']
        processed_hint = info_to_text(df, parameter, hint)
        s = f'this animal {processed_hint}.'
    
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
    processed_info = info_to_text(df, 'ifBiggerHuman', size)

    if size == df.loc[chosen_animal, 'ifBiggerHuman']:
        s = f'yes, the animal is {processed_info}.'
    else:
       s = f'no, the animal is not {processed_info}.'
    return s

def process_numLegs(num_legs, df, chosen_animal):
    num_legs = int(num_legs)
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

if __name__ == "__main__":

    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

