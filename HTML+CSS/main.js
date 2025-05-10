document.getElementById("playerSelectButton").addEventListener("click", async () => {
  try {
    const response = await fetch("http://127.0.0.1:3000/start_game");
    const data = await response.json();

    if (response.ok) {
      console.log("Airport data loaded:", data.airports);
    } else {
      console.error("Failed to start game", data);
    }
  } catch (error) {
    console.error("Error calling /start_game:", error);
  }
});



function playerSelect() {
  const name = document.getElementById('uname1').value.trim();
  if (name === '') {
    alert('Please enter your name before starting the game.');
    return;
  }
  else {
    window.location.href='game_view.html'
  }
}


function showInstructions() {
    document.getElementById('iPopup').style.display = 'flex';
  }

  function closeInstructions() {
    document.getElementById('iPopup').style.display = 'none';
  }


