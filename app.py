from flask import Flask, request, redirect, url_for, session, flash, render_template
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def connect_db():
    return mysql.connector.connect(
        host='sql12.freemysqlhosting.net',
        port=3306,
        user='sql12739182',
        password='UVYGwb3aGU',
        database='sql12739182',
        ssl_disabled=True
    )


matches = [
    {
        "Field1": "Oct 27 2024, Tue - 21:00 (IST), Wanda Metropolitano, Madrid",
        "Field2": "Atletico Madrid",
        "Field3": "Vs",
        "Field4": "Real Sociedad",
        "Field5": "La Liga"
    },
    {
        "Field1": "Oct 27 2024, Wed - 21:00 (IST), Stadio Diego Armando Maradona, Naples",
        "Field2": "Napoli",
        "Field3": "Vs",
        "Field4": "AC Milan",
        "Field5": "Serie A"
    },
    {
        "Field1": "Oct 28 2024, Thu - 21:00 (IST), Parc des Princes, Paris",
        "Field2": "Paris Saint-Germain",
        "Field3": "Vs",
        "Field4": "Olympique Lyonnais",
        "Field5": "Ligue 1"
    },
    {
        "Field1": "Oct 28 2024, Fri - 21:00 (IST), Anfield, Liverpool",
        "Field2": "Liverpool",
        "Field3": "Vs",
        "Field4": "Manchester United",
        "Field5": "Premier League"
    }
]
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
        return render_template('welcome.html', user=session['username'], coins=session['coins'])
    return redirect(url_for('login'))

@app.route('/match')
def match_page():
    if 'username' in session:
        return render_template('match.html', matches=matches, coins=session['coins'])
    return redirect(url_for('login'))

@app.route('/predict')
def predict():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    match_index = request.args.get('i')

    if not team1 or not team2:
        flash('Invalid teams selected', 'danger')
        return redirect(url_for('match_page'))

    # Fetch players for both teams from the JSON structure
    teams_data = {
        "Atletico Madrid": ["Antoine Griezmann", "Jan Oblak", "Rodrigo De Paul", "Thomas Lemar", "Marcos Llorente"],
        "Real Sociedad": ["Mikel Oyarzabal", "Takefusa Kubo", "Martin Zubimendi", "David Silva", "Robin Le Normand"],
        "Napoli": ["Victor Osimhen", "Khvicha Kvaratskhelia", "Giovanni Di Lorenzo", "Piotr Zieliński", "André-Frank Zambo Anguissa"],
        "AC Milan": ["Rafael Leão", "Theo Hernández", "Christian Pulisic", "Mike Maignan", "Fikayo Tomori"],
        "Paris Saint-Germain": ["Kylian Mbappé", "Achraf Hakimi", "Marquinhos", "Marco Verratti", "Ousmane Dembélé"],
        "Olympique Lyonnais": ["Alexandre Lacazette", "Rayan Cherki", "Maxence Caqueret", "Nicolás Tagliafico", "Anthony Lopes"],
        "Liverpool": ["Mohamed Salah", "Virgil van Dijk", "Alisson Becker", "Trent Alexander-Arnold", "Dominik Szoboszlai"],
        "Manchester United": ["Bruno Fernandes", "Marcus Rashford", "Casemiro", "André Onana", "Lisandro Martínez"]
    }

    teamAPlayers = teams_data.get(team1, [])
    teamBPlayers = teams_data.get(team2, [])

    return render_template('predict.html', team1=team1, team2=team2, match_index=match_index, 
                           teamAPlayers=teamAPlayers, teamBPlayers=teamBPlayers)

@app.route('/widget')
def widget():
    if 'username' in session:
        return render_template('Widget.html', matches=matches, coins=session['coins'])
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('coins', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

import random

import random

@app.route('/check_prediction', methods=['POST'])
def check_prediction():
    if 'username' in session:
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        mvp_team1 = request.form.get('mvp_team1')
        mvp_team2 = request.form.get('mvp_team2')
        red_cards_prediction = request.form.get('red_cards')
        total_goals_prediction = request.form.get('total_goals')

        if not team1 or not team2:
            flash('Team selection is missing!', 'danger')
            return redirect(url_for('predict'))

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Deduct 20 coins from the user for submitting the prediction
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

            # Simulate actual outcomes
            actual_red_cards = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.15, 0.05])[0]
            actual_total_goals = random.choices([0, 1, 2, 3, 4, 5, 6], weights=[0.1, 0.3, 0.4, 0.15, 0.04, 0.01, 0.005])[0]

            # Simulate actual MVPs by randomly choosing players from the database
            cursor.execute("SELECT player_name FROM players WHERE team_id = (SELECT team_id FROM teams WHERE team_name = %s) ORDER BY RAND() LIMIT 1", (team1,))
            actual_mvp_team1 = cursor.fetchone()[0]

            cursor.execute("SELECT player_name FROM players WHERE team_id = (SELECT team_id FROM teams WHERE team_name = %s) ORDER BY RAND() LIMIT 1", (team2,))
            actual_mvp_team2 = cursor.fetchone()[0]

            # Debugging MVP logic
            print(f"Actual MVPs: {actual_mvp_team1} for {team1}, {actual_mvp_team2} for {team2}")

            # Check red cards prediction
            red_cards_awarded = 0
            if red_cards_prediction == "0" and actual_red_cards == 0:
                red_cards_awarded += 10
            elif red_cards_prediction == "1-2" and actual_red_cards in [1, 2]:
                red_cards_awarded += 10
            elif red_cards_prediction == ">2" and actual_red_cards > 2:
                red_cards_awarded += 10

            # Check total goals prediction
            goals_awarded = 0
            if total_goals_prediction == "0-1" and actual_total_goals <= 1:
                goals_awarded += 10
            elif total_goals_prediction == "1-3" and actual_total_goals in [1, 2, 3]:
                goals_awarded += 10
            elif total_goals_prediction == "3-5" and actual_total_goals in [3, 4, 5]:
                goals_awarded += 10
            elif total_goals_prediction == ">5" and actual_total_goals > 5:
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
