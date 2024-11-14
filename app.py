from flask import Flask, request, redirect, url_for, session, flash, render_template
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import re
import mysql.connector

app = Flask(__name__)
connection_string = "mongodb+srv://anwayeedas05:KqvTHDQoDhyx8rZt@cluster0.hj2id.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true"

# Connect to the MongoDB client
client = MongoClient(connection_string)
db = client['desthink']  # Database name
collection = db['usbhaius']  # Collection name
def find_player_by_name(player_name):
    name_parts = player_name.split()
    regex_pattern = '.' + '.'.join(name_parts) + '.*'
    pattern = re.compile(regex_pattern, re.IGNORECASE)
    players = list(collection.find({"Name": pattern}))
    return players

app.secret_key = 'your_secret_key'  

def connect_db():
    return mysql.connector.connect(
        host='sql12.freemysqlhosting.net',
        port=3306,
        user='sql12744082',
        password='8klPmHKVJq',
        database='sql12744082',
        ssl_disabled=True
    )


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_coins/<int:amount>', methods=['POST'])
def add_coins(amount):
    if 'username' in session:
        conn = connect_db()
        cursor = conn.cursor()
        try:
            current_coins = session['coins']
            new_coins = current_coins + amount
            session['coins'] = new_coins
            query = "UPDATE users SET coins = %s WHERE username = %s"
            cursor.execute(query, (new_coins, session['username']))
            conn.commit()
            flash(f'{amount} coins added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('welcome'))
    else:
        flash('You need to log in to perform this action', 'danger')
        return redirect(url_for('login'))

@app.route('/deduct_coins/<int:amount>', methods=['POST'])
def deduct_coins(amount):
    if 'username' in session:
        conn = connect_db()
        cursor = conn.cursor()
        try:
            current_coins = session['coins']
            if current_coins >= amount:
                new_coins = current_coins - amount
                session['coins'] = new_coins
                query = "UPDATE users SET coins = %s WHERE username = %s"
                cursor.execute(query, (new_coins, session['username']))
                conn.commit()
                flash(f'{amount} coins deducted successfully!', 'success')
            else:
                flash('Insufficient coins!', 'danger')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('welcome'))
    else:
        flash('You need to log in to perform this action', 'danger')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        coins = 100  # Initialize coins to 0 for every new user
        conn = connect_db()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO users (username, password, coins) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, coins))
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()  # Fetch the result of the query
            if user:
                session['username'] = user['username']
                session['coins'] = user['coins']  # Store user's coin count in session
                flash('Login successful!', 'success')
                return redirect(url_for('welcome'))
            else:
                flash('Invalid username or password', 'danger')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.fetchall()  # Clear any unread results
            cursor.close()
            conn.close()
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        conn = connect_db()
        cursor = conn.cursor()
        try:
            # Query to count the number of users
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]  # Fetch the count

            return render_template('welcome.html', user=session['username'], coins=session['coins'], user_count=user_count)
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
            return redirect(url_for('login'))
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('login'))
    

@app.route('/match')
def match_page():
    if 'username' in session:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        try:
            # Fetch all upcoming matches with team names
            cursor.execute("""
                SELECT m.match_id, m.team1_id, m.team2_id, m.match_date, 
                       t1.team_name AS team1_name, t2.team_name AS team2_name
                FROM matches m
                JOIN teams t1 ON m.team1_id = t1.team_id
                JOIN teams t2 ON m.team2_id = t2.team_id
            """)
            matches = cursor.fetchall()

            # Return the matches with team names
            return render_template('match.html', matches=matches, coins=session['coins'])
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
            return redirect(url_for('login'))
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('login'))



@app.route('/predict')
def predict():
    team1_id = request.args.get('team1')  # Get team1's ID from the URL
    team2_id = request.args.get('team2')  # Get team2's ID from the URL
    match_index = request.args.get('i')  # Get match index, for reference if needed

    if not team1_id or not team2_id:
        flash('Invalid teams selected', 'danger')
        return redirect(url_for('match_page'))

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch players for team1
        cursor.execute("SELECT player_name FROM players WHERE team_id = %s", (team1_id,))
        teamAPlayers = cursor.fetchall()

        # Fetch players for team2
        cursor.execute("SELECT player_name FROM players WHERE team_id = %s", (team2_id,))
        teamBPlayers = cursor.fetchall()

        # Check if players are found for both teams
        if not teamAPlayers or not teamBPlayers:
            flash('No players found for one or both teams', 'danger')
            return redirect(url_for('match_page'))

        return render_template('predict.html', team1=team1_id, team2=team2_id, match_index=match_index, 
                               teamAPlayers=[player['player_name'] for player in teamAPlayers], 
                               teamBPlayers=[player['player_name'] for player in teamBPlayers])
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
        return redirect(url_for('match_page'))
    finally:
        cursor.close()
        conn.close()

@app.route('/widget')
def widget():
    if 'username' in session:
        return render_template('Widget.html')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('coins', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/info', methods=['GET', 'POST'])
def index():
    players = []
    no_result = False
    top_5_players = get_top_5_players()  # Flag to indicate if no players were found
    if request.method == 'POST':
        player_name = request.form['player_name']
        players = find_player_by_name(player_name)
        if not players:
            no_result = True  

    return render_template("info.html", players=players, no_result=no_result, top_5_players=top_5_players)
def get_top_5_players():
    top_players = collection.find().sort("Score", -1).limit(5)
    return top_players

import random


@app.route('/check_prediction', methods=['POST'])
def check_prediction():
    if 'username' in session:
        # Get form data with default value to avoid 'None' errors
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        mvp_team1 = request.form.get('mvp_team1')
        mvp_team2 = request.form.get('mvp_team2')
        red_cards_prediction = request.form.get('red_cards')
        total_goals_prediction = request.form.get('total_goals')

        # Debugging: Print the received team1 and team2 values
        print(f"Received team1: {team1}, team2: {team2}")

        # Check if any of the required fields are missing
        if not team1 or not team2 or not mvp_team1 or not mvp_team2 or not red_cards_prediction or not total_goals_prediction:
            flash('All fields are required!', 'danger')
            return redirect(url_for('predict'))

        team1 = team1.strip() if team1 else None
        team2 = team2.strip() if team2 else None

        if not team1 or not team2:
            flash('Invalid team names!', 'danger')
            return redirect(url_for('predict'))

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Fetch team IDs based on team names
            cursor.execute("SELECT player_name FROM players WHERE team_id = %s", (team1,))
            team1_data = cursor.fetchall()
            cursor.execute("SELECT player_name FROM players WHERE team_id = %s", (team2,))
            team2_data = cursor.fetchall()

            # Debugging: Print the team data fetched from the database
            print(f"Fetched team1 data: {team1_data}, team2 data: {team2_data}")

            if not team1_data or not team2_data:
                flash('Invalid teams selected', 'danger')
                return redirect(url_for('predict'))

            # team1_id = team1_data[0]
            # team2_id = team2_data[0]

            # Fetch players for both teams
            # cursor.execute("SELECT player_name FROM players WHERE team_id = %s", (team1_id,))
            # team1_players = cursor.fetchall()

            # cursor.execute("SELECT player_name FROM players WHERE team_id = %s", (team2_id,))
            # team2_players = cursor.fetchall()

            if not team1_data or not team2_data:
                flash('No players found for one or both teams', 'danger')
                return redirect(url_for('predict'))
            
            current_coins = session['coins']
            if current_coins >= 20:
                new_coins = current_coins - 20
                session['coins'] = new_coins
                query = "UPDATE users SET coins = %s WHERE username = %s"
                cursor.execute(query, (new_coins, session['username']))
                conn.commit()
            else:
                flash('Insufficient coins to submit prediction!', 'danger')
                return redirect(url_for('predict'))

            # Generate random red cards and total goals
            actual_red_cards = random.choice([0, 1, 2, ">2"])  # Randomly choose between 0, 1-2, or >2
            actual_total_goals = random.choice([0, 1, 2, 3, 4, 5, ">5"])  # Random goals choice
            
            # Randomly select an MVP from the available players for each team
            actual_mvp_team1 = random.choice([player[0] for player in team1_data])
            actual_mvp_team2 = random.choice([player[0] for player in team2_data])

            # Debugging MVP logic
            print(f"Actual MVPs: {actual_mvp_team1} for {team1}, {actual_mvp_team2} for {team2}")

            # Check red cards prediction
            red_cards_awarded = 0
            if red_cards_prediction == "0" and actual_red_cards == 0:
                red_cards_awarded += 10
            elif red_cards_prediction == "1-2" and actual_red_cards in [1, 2]:
                red_cards_awarded += 10
            elif red_cards_prediction == ">2" and actual_red_cards == ">2":
                red_cards_awarded += 10

            # Check total goals prediction
            goals_awarded = 0
            if total_goals_prediction == "0-1" and actual_total_goals in [0, 1]:
                goals_awarded += 10
            elif total_goals_prediction == "1-3" and actual_total_goals in [1, 2, 3]:
                goals_awarded += 10
            elif total_goals_prediction == "3-5" and actual_total_goals in [3, 4, 5]:
                goals_awarded += 10
            elif total_goals_prediction == ">5" and actual_total_goals == ">5":
                goals_awarded += 10

            # Check MVP predictions
            mvp_awarded = 0
            if mvp_team1 == actual_mvp_team1:
                mvp_awarded += 20
            if mvp_team2 == actual_mvp_team2:
                mvp_awarded += 20

            # Update user's coins/points based on predictions
            total_awarded = red_cards_awarded + goals_awarded + mvp_awarded
            if total_awarded > 0:
                new_coins = session['coins'] + total_awarded
                session['coins'] = new_coins
                query = "UPDATE users SET coins = %s WHERE username = %s"
                cursor.execute(query, (new_coins, session['username']))
                conn.commit()
                flash(f'Correct predictions! You earned {total_awarded} points! '
                      f'Actual outcomes: {actual_red_cards} red cards, {actual_total_goals} total goals, '
                      f'MVPs: {actual_mvp_team1} for {team1} and {actual_mvp_team2} for {team2}.', 'success')
            else:
                flash(f'Incorrect predictions! Actual outcomes: {actual_red_cards} red cards, {actual_total_goals} total goals, '
                      f'MVPs: {actual_mvp_team1} for {team1} and {actual_mvp_team2} for {team2}.', 'danger')

        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('welcome'))
    else:
        flash('You need to log in to perform this action', 'danger')
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
