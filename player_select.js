function submitPlayers() {
  const player1 = document.getElementById("uname1").value;
  const player2 = document.getElementById("uname2").value;

  fetch("http://localhost:5000/get_name", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      player1: player1,
      player2: player2
    })
  }).then(response => response.json())
    .then(data => console.log(data));
}