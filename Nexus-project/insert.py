import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='sql12.freemysqlhosting.net',
            port=3306,
            user='sql12739182',
            password='UVYGwb3aGU',
            database='sql12739182',
            ssl_disabled=True
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def insert_players():
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

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        team_id = 1
        try:
            for team, players in teams_data.items():
                for player in players:
                    cursor.execute(
                        "INSERT INTO players (player_name, team_id) VALUES (%s, %s)",
                        (player, team_id)
                    )
                team_id += 1
            conn.commit()
            print("Players inserted successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database")

insert_players()
