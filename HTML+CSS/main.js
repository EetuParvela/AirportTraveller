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

function showInstructions() {
    document.getElementById('iPopup').style.display = 'flex';
  }

  function closeInstructions() {
    document.getElementById('iPopup').style.display = 'none';
  }

  function playerSelect() {
    window.location.href = 'playerselect.html';
  }
