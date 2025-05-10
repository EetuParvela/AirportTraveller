document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:3000/get_player_info")
    .then(response => response.json())
    .then(data => {
      const playerName = data.name;
      const money = data.money;
      const co2 = Math.round(data.co2);
      const places = data.places_visited;
      const days = data.days;

      const gameoverBox = document.querySelector(".gameover-box");

      gameoverBox.innerHTML = `
        <h1>Game Over</h1>
        <p>Player: ${playerName}</p>
        <p>Money: ${money}</p>
        <p>Time: ${days} days</p>
        <p>CO₂: ${co2} g</p>
        <p>Places visited: ${places}</p>
      `;
    })
    .catch(error => {
      console.error("Error loading player info:", error);
    });
});
