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
import mysql.connector


api_tokken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MzcyOGIwYmZkOWFhYzIyNjcwNDUwMTAiLCJpYXQiOjE2Njg0NTEwODMsImV4cCI6MTY2ODUzNzQ4M30.0G3IlX1E8S4XyDQLXieaArzjLTlsXFqpcG2iKCfb7yw"

app = Flask(__name__, static_folder="./wc2022/build/static", template_folder="./wc2022/build")
cors = CORS(app)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'oh_so_secret'
db_url = "server.oversight.co.il"

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=db_url,
            user="rotem_private",
            password="T$l3715ml",
            database="rotem_private"
        )
        return connection
    except Exception as e:
        print(e)


@app.route('/')
def home():
    return {
        "msg": "Server is runnig..."
    }

    # headers = {
    #     'Authorization': 'Bearer {token}'.format(token=api_tokken),
    #     'Content-Type': 'application/json',
    # }

    # json_data = {
    #     'name': 'Alon Brand',
    #     'email': 'aaa@gmail.com',
    #     'password': '123456',
    #     'passwordConfirm': '123456',
    # }

    # response = await requests.get('http://api.cup2022.ir/api/v1/team', headers=headers)
    # print(jsonify(response))



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up_func():
    user_name = request.get_json()['name']
    password = request.get_json()['password']
    return_msg = "{user_name} singed up!".format(user_name=user_name)
    user_id = None
    try:
        connection = connect_to_db()
        curser = connection.cursor()
        query = "INSERT INTO Users (name, password, points) VALUES (%s, %s, %s)"
        params = (user_name, password, 0)
        curser.execute(query, params)
        user_id = curser.lastrowid
        print(user_id)
        connection.commit()
        # connection.close()

    except Exception as e:
        print(e)
        return {
            'user_name': 'fake',
            'msg': str(e)
        }
     
    return {
        'user_name': user_name,
        'msg': 'User Connected',
        'user_id': user_id
    }

@app.route('/log-in', methods=['GET', 'POST'])
def log_in_func():
    user_name = request.get_json()['name']
    user_password = request.get_json()['password']    
    try:
        connection = connect_to_db()
        curser = connection.cursor()
        query = "SELECT * FROM Users WHERE (name = %s AND password = %s)"
        curser.execute(query, (user_name, user_password))

        response = curser.fetchone()
        if len(response) > 0:
            id, name, password, points = response

        connection.commit()
        # connection.close()

    except Exception as e:
        print(e)
        return {
            'msg': 'Wrong user name or password!',
            'user_name': user_name,
        }

    return {
        'user_id': id,
        'msg': 'User connected',
        'user_name': name,
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
    print(request.get_json())
    game_id = request.get_json()['gameId']
    user_id = request.get_json()['userId']
    scoreA = request.get_json()['scoreA']
    scoreB = request.get_json()['scoreB']
    query = ''
    bet_id = None
    try:
        print(scoreA, scoreB)
        connection = connect_to_db()
        curser = connection.cursor()
        
        curser.execute("SELECT * FROM Bets WHERE (userId = %s AND gameId = %s)", (user_id, game_id))
        bets = curser.fetchall()
        if len(bets) > 0 and len(bets[0]) > 0:
            bet_id = bets[0][0]

        print(bet_id)

        if bet_id is not None:
            query = "UPDATE Bets SET scoreA=%s, scoreB=%s WHERE betId = %s"
            params = (scoreA, scoreB, bet_id)
        else:
            query = "INSERT INTO Bets (userId, gameId, scoreA, scoreB) VALUES (%s, %s, %s, %s)"
            params = (user_id, game_id, scoreA, scoreB)

        curser.execute(query, params)
        connection.commit()
        # connection.close()

    except Exception as e:
        print(e)
        return {
            'user_name': 'fake',
            'msg': str(e)
        }

    return {
        'msg': 'Nice Bet!'
    }


@app.route('/users')
def get_games():
    try:
        connection = connect_to_db()
        curser = connection.cursor()
        curser.execute("SELECT * FROM Users")
        users = curser.fetchall()
    except Exception as e:
        return {
            'msg': e
        }

    return {
        'users': users
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)