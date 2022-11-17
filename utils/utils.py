import mysql.connector
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

def calculate_score():
    try:
        connection = connect_to_db()
        curser = connection.cursor()

        # Games
        curser.execute("SELECT * FROM Games")
        games = curser.fetchall()

        curser.execute("SELECT * FROM Bets")
        bets = curser.fetchall()

        
        curser.execute("SELECT * FROM Users")
        users = curser.fetchall()



        for user in users:
            curr_points=0
            for game in games:
                if(len(game) > 3):
                    game_id = game[0]
                    game_realA = game[3]
                    game_realB = game[4]
                    for bet in bets:
                        print(user)
                        if(len(bet) > 4 and bet[2] == game_id and bet[1] == user[0]):
                            user_id = bet[1]
                            user_scoreA = bet[3]
                            user_scoreB = bet[4]
                            new_points = calculate_game_points(game_realA, game_realB, user_scoreA, user_scoreB)
                            curr_points = curr_points + new_points
                            print(curr_points)
            query = "UPDATE Users SET points=%s WHERE id=%s"
            params = (curr_points, user_id)
            curser.execute(query, params)
            connection.commit()
    
    except Exception as e:
        print(str(e))


def calculate_game_points(game_realA, game_realB, user_scoreA, user_scoreB):
    if game_realA == user_scoreA and game_realB == user_scoreB:
        return 3
    elif game_realA > game_realB and user_scoreA > user_scoreB:
        return 1
    elif game_realB > game_realA and user_scoreB > user_scoreA:
        return 1
    elif game_realA == game_realB and user_scoreA == user_scoreB:
        return 1

    return 0

