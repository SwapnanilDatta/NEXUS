
    document.addEventListener('DOMContentLoaded', function () {
        const username = 'your_username'; // Replace with your actual username
        const token = 'your_actual_api_key'; // Replace with your actual API key
        const apiUrl = `https://api.soccersapi.com/v2.2/search/?user=${username}&token=${token}&t=all&q=dazn`;

        // Function to fetch and display data
        function fetchData() {
            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    displayMatches(data);
                    displayPlayers(data);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }

        // Function to display matches
        function displayMatches(data) {
            const matchesContainer = document.getElementById('matches');
            if (data.matches && data.matches.length > 0) {
                data.matches.forEach(match => {
                    const matchElement = document.createElement('div');
                    matchElement.className = 'match';
                    matchElement.innerHTML = `
                        <h3>${match.homeTeam} vs ${match.awayTeam}</h3>
                        <p>Date: ${match.date}</p>
                        <p>Time: ${match.time}</p>
                    `;
                    matchesContainer.appendChild(matchElement);
                });
            } else {
                matchesContainer.innerHTML += '<p>No matches found.</p>';
            }
        }

        // Function to display player stats
        function displayPlayers(data) {
            const playersContainer = document.getElementById('players');
            if (data.players && data.players.length > 0) {
                data.players.forEach(player => {
                    const playerElement = document.createElement('div');
                    playerElement.className = 'player';
                    playerElement.innerHTML = `
                        <h3>${player.name}</h3>
                        <p>Team: ${player.team}</p>
                        <p>Position: ${player.position}</p>
                        <p>Goals: ${player.goals}</p>
                    `;
                    playersContainer.appendChild(playerElement);
                });
            } else {
                playersContainer.innerHTML += '<p>No players found.</p>';
            }
        }

        // Fetch data when the page loads
        fetchData();
    });

