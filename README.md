# Football Fantasy Web App

## Overview
This **Football Fantasy Web App** is a Flask-based platform designed for football enthusiasts. The app offers an engaging experience where users can explore live match scores, manage virtual teams, and view detailed player statistics. The player database is sourced from the FIFA football game, ensuring accurate and high-quality information.

---

## Features
1. **User Authentication**
   - Secure registration and login system to manage user accounts.
   - Users can log in to access personalized features.

2. **Player Database**
   - Comprehensive database of football players sourced from FIFA.
   - Search and filter players based on attributes like skill ratings, nationality, and team.

3. **Live Match Scores**
   - Integrated widget to display real-time match scores and updates.

4. **Match Prediction**
   - Users can predict match outcomes and earn virtual coins based on the accuracy of their predictions.

5. **Virtual Coins**
   - Gamified currency system where users earn coins for activities such as successful predictions.

6. **Responsive Design**
   - Clean and intuitive user interface with mobile and desktop compatibility.

7. **SQL Database Integration**
   - Efficient data storage for users, teams, matches, and coins using SQL.

---

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: SQL (MySQL/SQLite)
- **Frontend**: HTML, CSS (Interactive styles for dynamic behavior)
- **Live Data**: Widgets for real-time match scores
- **Source for Player Data**: FIFA Football Game

---

## Installation
### Prerequisites
- Python 3.9+
- Flask and required libraries (see `requirements.txt`)
- MySQL and Mongodb database setup

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/football-fantasy-app.git
   cd football-fantasy-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the database in `config.py` or `app.py` with your credentials.
4. Run the app:
   ```bash
   flask run
   ```
5. Open the app in your browser:
   ```bash
   http://127.0.0.1:5000/
   ```

---

## Future Enhancements
- **Enhanced Prediction System**: Incorporate machine learning models to improve match prediction accuracy.
- **Leaderboard**: Display a leaderboard for users based on their coins or achievements.
- **Additional Features**: Include options for creating custom leagues and competing with friends.

---

## Credits
- **Player Data**: FIFA Football Game
- **Live Scores**: Integrated using external widgets/APIs
- **Development**: Flask framework with SQL database

---

## License
This project is open-source and licensed under the [MIT License](LICENSE). Feel free to contribute or modify the code!

**Visit our website**
[Click Here](https://nexus-ayzn.onrender.com)
