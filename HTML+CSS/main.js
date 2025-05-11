document.getElementById('startGameButton').addEventListener('click', startGame);

async function startGame() {
  const playerName = playerSelect();

  try {
    const response = await fetch('http://127.0.0.1:3000/start_game', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({player_name: playerName}),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error('Failed to start game:', data);
      return;
    }

    console.log('Game started successfully');
  } catch (error) {
    console.error('Error starting game:', error);
  }
}

function playerSelect() {
  const name = document.getElementById('uname1').value.trim();
  if (name === '') {
    alert('Please enter your name before starting the game.');
  } else {
    window.location.href = 'game_view.html';
    return name;
  }
}

function showInstructions() {
  document.getElementById('iPopup').style.display = 'flex';
}

function closeInstructions() {
  document.getElementById('iPopup').style.display = 'none';
}

async function highscore() {

  try {
    const response = await fetch('http://127.0.0.1:3000/get_highscore');
    const scores = await response.json();
    console.log(scores);
    const ol2 = document.querySelector('#rank');
    for (let i = 0; i < scores.length; i++) {
      const li2 = document.createElement('li');
      console.log(i);
      li2.innerHTML = `${scores[i]['player']}, ${scores[i]['score']}`;
      ol2.appendChild(li2);
    }

  } catch (error) {
    console.error('Virhe hakiessa highscores-tietoja:', error);
  }
}

window.onload = highscore;