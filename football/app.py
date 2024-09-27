from flask import Flask

app = Flask(__name__)

# Player Data (Top 5 + Bottom 6 players)
players_data = [
    # Top 5 players
    {
        'id': 1,
        'name': 'Lionel Messi',
        'team': 'Paris Saint-Germain',
        'logo': 'psg.png',
        'image': 'MESSI.jpg',
        'skills': {
            'Dribbling': 10,
            'Passing': 9,
            'Shooting': 9,
            'Pace': 8,
            'Physical': 6,
            'Defending': 5
        },
        'achievements': [
            '7 Ballon d\'Or',
            '4 Champions League titles',
            '10 La Liga titles',
            '2022 FIFA World Cup Winner'
        ],
        'matches_played': 940
    },
    {
        'id': 2,
        'name': 'Cristiano Ronaldo',
        'team': 'Al Nassr',
        'logo': 'Alnassr.png',
        'image': 'ronaldo.png',
        'skills': {
            'Dribbling': 8,
            'Passing': 7,
            'Shooting': 10,
            'Pace': 9,
            'Physical': 9,
            'Defending': 4
        },
        'achievements': [
            '5 Ballon d\'Or',
            '5 Champions League titles',
            '3 Premier League titles',
            '2020 Euro Winner'
        ],
        'matches_played': 1050
    },
    {
        'id': 3,
        'name': 'Robert Lewandowski',
        'team': 'Barcelona',
        'logo': 'barca.png',
        'image': 'lewandowski.jpg',
        'skills': {
            'Dribbling': 7,
            'Passing': 6,
            'Shooting': 10,
            'Pace': 8,
            'Physical': 9,
            'Defending': 5
        },
        'achievements': [
            '2 FIFA Best Men\'s Player Awards',
            'Champions League title',
            'Multiple Bundesliga titles',
        ],
        'matches_played': 800
    },
    {
        'id': 4,
        'name': 'Mohamed Salah',
        'team': 'Liverpool',
        'logo': 'liverpool.png',
        'image': 'salah.jpg',
        'skills': {
            'Dribbling': 9,
            'Passing': 8,
            'Shooting': 9,
            'Pace': 10,
            'Physical': 7,
            'Defending': 5
        },
        'achievements': [
            'Premier League Golden Boot',
            'Champions League title',
            'Premier League title'
        ],
        'matches_played': 600
    },
    {
        'id': 5,
        'name': 'Erling Haaland',
        'team': 'Manchester City',
        'logo': 'mancity.png',
        'image': 'haaland.jpg',
        'skills': {
            'Dribbling': 7,
            'Passing': 6,
            'Shooting': 9,
            'Pace': 10,
            'Physical': 9,
            'Defending': 5
        },
        'achievements': [
            'Premier League title',
            'Golden Boot (Premier League)',
            'Multiple Bundesliga titles'
        ],
        'matches_played': 200
    }
]

# Additional 6 players for the table
bottom_players_data = [
    {
        'id': 6,
        'name': 'Virgil van Dijk',
        'team': 'Liverpool',
        'logo': 'liverpool.png',
        'image': 'vandijk.jpg',
        'skills': {
            'Dribbling': 5,
            'Passing': 7,
            'Shooting': 4,
            'Pace': 7,
            'Physical': 9,
            'Defending': 10
        },
        'achievements': [
            'Champions League title',
            'Premier League title',
            'FIFA Best Men\'s Player Nominee'
        ],
        'matches_played': 500
    },
    {
        'id': 7,
        'name': 'Harry Kane',
        'team': 'Tottenham Hotspur',
        'logo': 'tottenham.png',
        'image': 'kane.jp',
        'skills': {
            'Dribbling': 7,
            'Passing': 6,
            'Shooting': 9,
            'Pace': 7,
            'Physical': 8,
            'Defending': 4
        },
        'achievements': [
            'Premier League Golden Boot',
            'World Cup Golden Boot'
        ],
        'matches_played': 450
    },
    {
        'id': 8,
        'name': 'Sadio Mané',
        'team': 'Bayern Munich',
        'logo': 'bayern.png',
        'image': 'mane.jpeg',
        'skills': {
            'Dribbling': 8,
            'Passing': 7,
            'Shooting': 8,
            'Pace': 9,
            'Physical': 8,
            'Defending': 6
        },
        'achievements': [
            'Premier League title',
            'Champions League title',
            'African Player of the Year'
        ],
        'matches_played': 450
    },
    {
        'id': 9,
        'name': 'Sergio Ramos',
        'team': 'Paris Saint-Germain',
        'logo': 'psg.png',
        'image': 'ramos.jpg',
        'skills': {
            'Dribbling': 6,
            'Passing': 7,
            'Shooting': 5,
            'Pace': 7,
            'Physical': 9,
            'Defending': 10
        },
        'achievements': [
            '4 Champions League titles',
            '2 European Championships',
            '2010 FIFA World Cup Winner'
        ],
        'matches_played': 800
    },
    {
        'id': 10,
        'name': 'Jan Oblak',
        'team': 'Atlético Madrid',
        'logo': 'atletico.png',
        'image': 'oblak.jpg',
        'skills': {
            'Dribbling': 4,
            'Passing': 5,
            'Shooting': 3,
            'Pace': 6,
            'Physical': 7,
            'Defending': 9
        },
        'achievements': [
            'La Liga title',
            'Best Goalkeeper Award',
            'Multiple Zamora Trophies'
        ],
        'matches_played': 400
    }
]


@app.route('/')
def index():
    html_content = '''
    <html>
    <head>
        <title>Football Players Ranking</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background-image: url('/static/background.jpg');
                background-size: cover;
                background-position: center;
                color: white;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            h1 { 
                font-size: 3rem; 
                padding-top: 20px; 
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px #000;
            }
            ul { 
                list-style-type: none; 
                padding: 0; 
                margin: 0;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }
            li { 
                display: inline-block; 
                margin: 20px; 
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                width: 300px; 
                transition: all 0.3s ease; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            li:hover { 
                transform: scale(1.05); 
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            }
            img { 
                margin-top: 10px; 
                border-radius: 50%;
                transition: all 0.3s ease;
            }
            img:hover { 
                transform: rotate(360deg); 
            }
            strong { 
                font-size: 1.5rem; 
                color: white;
            }
            .ranking {
                font-size: 2rem;
                color: #FFC300;
                font-weight: bold;
            }
            a { 
                display: inline-block; 
                margin: 10px; 
                padding: 10px 20px; 
                background-color: #FFC300; 
                color: black; 
                border-radius: 5px; 
                text-decoration: none; 
                font-weight: bold;
                transition: background-color 0.3s ease; 
            }
            a:hover { 
                background-color: #FF5733; 
            }
            /* Table for Bottom Players */
            table { 
                margin: 50px auto; 
                width: 80%; 
                border-collapse: collapse; 
                background-color: rgba(255, 255, 255, 0.1); 
                text-align: center;
            }
            th, td { 
                padding: 15px; 
                border: 1px solid white; 
            }
            th { 
                background-color: rgba(0, 0, 0, 0.5);
                color: #FFC300;
                font-size: 1.2rem;
            }
            td a { 
                padding: 8px 16px;
            }
        </style>
    </head>
    <body>
        <h1>Top 5 Football Players</h1>
        <ul>
    '''

    # Top 5 players
    for index, player in enumerate(players_data):
        html_content += f'''
        <li>
            <span class="ranking">#{index + 1}</span><br>
            <img src="/static/{player['logo']}" alt="{player['team']} logo" width="50" height="50"><br>
            <strong>{player['name']}</strong><br>
            <a href="/player/{player['id']}">See Profile</a>
        </li>
        '''

    html_content += '''
        </ul>
        <h1>Top 6 Football Club</h1>
        <table>
            <tr>
                <th>Team Name</th>
                <th>Player Name</th>
                <th>See Profile</th>
            </tr>
    '''

    # Bottom 6 players
    for player in bottom_players_data:
        html_content += f'''
            <tr>
                <td><img src="/static/{player['logo']}" alt="{player['team']} logo" width="30" height="30"> {player['team']}</td>
                <td>{player['name']}</td>
                <td><a href="/player/{player['id']}">See Profile</a></td>
            </tr>
        '''

    html_content += '''
        </table>
    </body>
    </html>
    '''

    return html_content


@app.route('/player/<int:player_id>')
def player_profile(player_id):
    # Find the player by ID
    player = next((p for p in players_data + bottom_players_data if p['id'] == player_id), None)

    if player is None:
        return f"<h1>Player with ID {player_id} not found.</h1>"

    # Player profile page
    html_content = f'''
    <html>
    <head>
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            h1 {{
                font-size: 2.5rem;
                margin-bottom: 20px;
            }}
            img {{
                margin-top: 10px;
                width: 150px;
                height: 150px;
                border-radius: 50%;
            }}
            .skill-bar-container {{
                margin: 10px 0;
                width: 70%;
                height: 20px;
                background-color: #ddd;
                border-radius: 5px;
                overflow: hidden;
                margin-left: auto;
                margin-right: auto;
            }}
            .skill-bar {{
                height: 100%;
                background-color: #4CAF50;
                text-align: center;
                line-height: 20px;
                color: white;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 10px;
                text-align: center;
            }}
            .achievements-list {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            .achievements-list li {{
                text-align: center;
                margin: 10px 0;
            }}
            a {{
                display: inline-block;
                margin: 20px 0;
                padding: 10px 20px;
                background-color: #FFC300;
                color: black;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                background-color: #FF5733;
            }}
        </style>
    </head>
    <body>
        <h1>{player['name']} - {player['team']}</h1>
        <img src="/static/{player['image']}" alt="{player['name']}"><br>
        <h2>Matches Played: {player['matches_played']}</h2>
        <h3>Skills:</h3>
        <ul>
    '''

    # Display skills
    for skill, rating in player['skills'].items():
        html_content += f'''
        <li>
            {skill}: {rating}/10
            <div class="skill-bar-container">
                <div class="skill-bar" style="width: {rating * 10}%;">{rating * 10}%</div>
            </div>
        </li>
        '''

    # Display achievements
    html_content += "</ul><h3>Achievements:</h3><ul class='achievements-list'>"
    for achievement in player['achievements']:
        html_content += f"<li>{achievement}</li>"

    html_content += '''
        </ul>
        <a href="/">Back to List</a>
    </body>
    </html>
    '''

    return html_content


if __name__ == '__main__':
    app.run(debug=True)
