async function submitPlayers() {
  try {
    const player1 = document.getElementById("uname1").value.trim();
    const player2 = document.getElementById("uname2").value.trim();

    if (!player1 || !player2) {
      alert("Please enter names for both players.");
      return;
    }

    const response = await fetch("http://localhost:3000/get_name", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ player1, player2 })
    });

    const data = await response.json();
    console.log("Players submitted:", data);
    // Optionally update UI or transition game state here

  } catch (error) {
    console.error("Failed to submit players:", error);
    alert("Could not start the game. Please try again.");
  }
}
