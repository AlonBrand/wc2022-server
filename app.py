import os
from flask import Flask, request, session
from flask_cors import CORS
from numpy import number
import jsonify
import json
from utils.file_manager import *
import sqlite3
import threading
import requests


currentdirectory = os.path.dirname(os.path.abspath(__file__))

api_tokken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MzcyOGIwYmZkOWFhYzIyNjcwNDUwMTAiLCJpYXQiOjE2Njg0NTEwODMsImV4cCI6MTY2ODUzNzQ4M30.0G3IlX1E8S4XyDQLXieaArzjLTlsXFqpcG2iKCfb7yw"

app = Flask(__name__, static_folder="./wc2022/build/static", template_folder="./wc2022/build")
cors = CORS(app)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'oh_so_secret'

userId = -1

@app.route('/')
def home():
    return {
        "msg": "Server is runnig..."
    }

@app.route('/sign-up', methods=['GET', 'POST'])
async def sign_up_func():
    headers = {
        'Authorization': 'Bearer {token}'.format(token=api_tokken),
        'Content-Type': 'application/json',
    }

    json_data = {
        'name': 'Alon Brand',
        'email': 'aaa@gmail.com',
        'password': '123456',
        'passwordConfirm': '123456',
    }

    response = await requests.get('http://api.cup2022.ir/api/v1/team', headers=headers)
    print(jsonify(response))


    user_name = request.get_json()['name']
    password = request.get_json()['password']
    return_msg = "{user_name} singed up!".format(user_name=user_name)
    user_id = None
    try:
        connection = sqlite3.connect(currentdirectory + "\db.db")
        curser = connection.cursor()

        params = (user_name, password, 0)
        query = "INSERT INTO Users (name, password, points) VALUES (?, ?, ?)"
        curser.execute(query, params)
        user_id = curser.lastrowid
        connection.commit()
        connection.close()

    except Exception as e:
        print(e)
        return {
            'user_name': 'fake',
            'msg': str(e)
        }
     
    return {
        'user_name': user_name,
        'msg': str(response),
        'user_id': user_id
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

# @app.route('/users')
# def get_users():
#     users = get_table("users")
#     print(users)
#     return {
#         'users': users
#     }

    # return_msg = "{user_name} singed up!".format(user_name=user_name)
    # if insert_row("users", [user_name, password]) == False:
    #     return_msg = "{user_name} Failed to singed up!".format(user_name=user_name)
    
    # return {
    #     'user_name': user_name,
    #     'msg': return_msg
    # }


@app.route('/games/bet-on-game', methods=['GET', 'POST'])
def bet_on_game():
    try:
        params = (request.get_json()['gameId'], request.get_json()['userId'], request.get_json()['teamA'], request.get_json()['teamB'], request.get_json()['scoreA'], request.get_json()['scoreB'])
        query = "INSERT INTO Bets (gameId, userId, teamA, teamB, scoreA, scoreB) VALUES (?, ?, ?, ?, ?, ?)"
        connection = sqlite3.connect(currentdirectory + "\db.db")
        curser = connection.cursor()
        curser.execute(query, params)
        connection.commit()
        connection.close()
        return {
            'msg': 'Good Luck!!!'
        }
    except Exception as e:
        print(e)
        return {
            'msg': str(e)
        }

@app.route('/users')
def get_games():
    try:
        connection = sqlite3.connect(currentdirectory + "\db.db")
        curser = connection.cursor()

        curser.execute("SELECT * FROM Users")
        users = curser.fetchall()
        connection.commit()
        connection.close()
    except Exception as e:
        return {
            'msg': e
        }

    return {
        'users': users
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)