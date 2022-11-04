import os
from flask import Flask, request, render_template, session
from flask_cors import CORS, cross_origin
from numpy import number
from openpyxl import load_workbook
import json
from utils.file_manager import *

app = Flask(__name__, static_folder="./wc2022/build/static", template_folder="./wc2022/build")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
    return {
        'msg': "Server is running"
    }

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up_func():
    user_name = request.get_json()['name']
    password = request.get_json()['password']
    return_msg = "{user_name} singed up!".format(user_name=user_name)
    if insert_row("users", [user_name, password]) == False:
        return_msg = "{user_name} Failed to singed up!".format(user_name=user_name)
    
    return {
        'user_name': user_name,
        'msg': return_msg
    }

@app.route('/log-in', methods=['GET', 'POST'])
def log_in_func():
    user_name = request.get_json()['name']
    user_password = request.get_json()['password']    
    print(user_name)
    print(user_password)
    return {
        'user_name': user_name,
        'msg': search_in_table("users", user_name=user_name, user_password=user_password)
    }

@app.route('/games/bet-on-game', methods=['GET', 'POST'])
def bet_on_game():
    print(request.get_json()['teamA'])
    print(request.get_json()['teamB'])
    print(request.get_json()['scoreA'])
    print(request.get_json()['scoreB'])
    return {
        'msg': 'Good Luck!!!'
    }

@app.route('/games/get_games')
def get_games():
    games = get_table("games")

    return {
        'games': json.dumps(games, default=str) 
    }

if __name__ == '__main__':
    app.run(debug=True)