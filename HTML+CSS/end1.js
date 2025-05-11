document.addEventListener('DOMContentLoaded', () => {
  fetch('http://127.0.0.1:3000/get_player_info').
      then(response => response.json()).
      then(data => {
        const playerName = data.name;
        const money = Math.round(data.money);
        const co2 = Math.round(data.co2);
        const score = Math.round(data.score)
        const places = data.places_visited;
        const days = data.days;

        const gameoverBox = document.querySelector('.gameover-box');

        gameoverBox.innerHTML = `
        <h1>Game Over</h1>
        <p>Player: ${playerName}</p>
        <p>Score: ${score}</p>
        <p>Money left: ${money}€</p>
        <p>Days: ${days}</p>
        <p>CO₂: ${co2} kg</p>
        <p>Places visited: ${places}</p>
      `;
      }).
      catch(error => {
        console.error('Error loading player info:', error);
      });
});

document.getElementById('playAgainButton').
    addEventListener('click', resetStats);

function resetStats() {
  fetch('http://127.0.0.1:3000/reset_player_stats').
      then(response => response.json()).
      then(data => {
        console.log(data.message);
        window.location.href = 'main.html';
      }).
      catch(error => {
        console.error('Error resetting player stats:', error);
      });
}

window.onload(fetch('http://127.0.0.1:3000/update_database_highscore').
      then(response => response.json()).
      then(data => {
        console.log(data.message);
      }).
      catch(error => {
        console.error('Error resetting player stats:', error);
      }))
async function highscore() {

  try {
    const response = await fetch('http://127.0.0.1:3000/get_highscore')
    const scores = await response.json();
    console.log(scores)
    const ol2 = document.querySelector('#rank')
    for (let i = 0; i < scores.length; i++) {
      const li2 = document.createElement('li')
      console.log(i)
      li2.innerHTML = `Name: ${scores[i]['player']}, Points: ${scores[i]['score']}`;
      ol2.appendChild(li2)
    }

  } catch (error) {
    console.error('Virhe hakiessa highscores-tietoja:', error);
  }
}
window.onload = highscore;
