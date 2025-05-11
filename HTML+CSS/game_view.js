const bounds = L.latLngBounds([90, -180], [-90, 180]);

const map = L.map('map', {
  minZoom: 3, maxZoom: 10, maxBounds: bounds, maxBoundsViscosity: 1.0,
}).setView([51.505, -0.09], 3);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

loadAirportMarkers(map);

let selectedAirport = null;

async function loadAirportMarkers(map) {
  try {
    const res = await fetch('http://127.0.0.1:3000/get_airports');
    const data = await res.json();

    data.forEach(marker => {
      L.marker([marker['latitude_deg'], marker['longitude_deg']]).
          addTo(map).
          bindPopup(marker.airport_name).
          on('click', async () => {
            selectedAirport = marker;

            // saadan etäisyys ja lasketaan hintaa
            const costRes = await fetch(
                'http://127.0.0.1:3000/get_distance?icao=' + marker.icao);
            const costData = await costRes.json();
            const distance = costData.distance;
            const flightCost = Math.round(distance * 0.5);

            document.getElementById('airportInfo').innerHTML = `
              <strong>Airport Info:</strong>
              <h5>${marker.welcome_phrase}</h5>
              <h5>${marker.airport_name}</h5>
              <p>ICAO: ${marker.icao}</p>
              <p>Country: ${marker.country_name}</p>
              <p><strong>Flight cost:</strong> ${flightCost}€</p>
              <button type="button" id="flyButton">Fly</button>
            `;

            document.getElementById('flyButton').
                addEventListener('click', async () => {
                  if (selectedAirport) {
                    await handleFly(selectedAirport);
                  } else {
                    console.error('No airport selected.');
                  }
                });
          });
    });
  } catch (err) {
    console.error('Fetch error:', err);
  }
}

async function handleFly(icao_code) {
  const icao = icao_code;

  await fetch('http://127.0.0.1:3000/fly_to', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({icao}),
  }).then(response => response.json()).then(data => {
    if (data.can_fly) {
      current_player_info();

      const ul = document.getElementById('visitedList');
      const li = document.createElement('li');
      li.textContent = selectedAirport.airport_name;
      ul.appendChild(li);
    } else {
      alert(data.message || 'You cannot fly to this location.');
    }

    if (data.game_over) {
      window.location.href = 'end1.html';
    }
  }).catch(error => {
    console.error('Flight error:', error);
  });
}

function handleWork(days) {
  fetch('http://127.0.0.1:3000/work', {
    method: 'POST', headers: {
      'Content-Type': 'application/json',
    }, body: JSON.stringify({days}),
  }).then(response => response.json()).then(data => {
    console.log(data.message);
    current_player_info();
  }).catch(error => {
    console.error('Work error:', error);
  });
}

function current_player_info() {
  fetch('http://127.0.0.1:3000/get_player_info').
      then(response => response.json()).
      then(data => {
        const playerName = data.name;
        const score = Math.round(data.score);
        const money = Math.round(data.money);
        const co2 = Math.round(data.co2);
        const places = data.places_visited;
        const days = data.days;
        const current = data.location.airport_name;

        const playerData = document.getElementById('pdata');

        playerData.innerHTML = `
        <h1>Player Stats:</h1>
        <p>Player: ${playerName}</p>
        <p>Score: ${score}</p>
        <p>Money left: ${money}€</p>
        <p>Days: ${days}</p>
        <p>CO₂: ${co2} kg</p>
        <p>Places visited: ${places}</p>
        <p>Location: ${current}</p>
      `;
      }).
      catch(error => {
        console.error('Error loading player info:', error);
      });
}

document.getElementById('work1').addEventListener('click', () => handleWork(1));
document.getElementById('work2').addEventListener('click', () => handleWork(2));
document.getElementById('work3').addEventListener('click', () => handleWork(3));

document.addEventListener('DOMContentLoaded', () => {
  fetch('http://127.0.0.1:3000/get_player_info').
      then(response => response.json()).
      then(data => {
        const playerName = data.name;
        const score = Math.round(data.score);
        const money = data.money;
        const co2 = Math.round(data.co2);
        const places = data.places_visited;
        const days = data.days;
        const current = data.location.airport_name;

        const gameoverBox = document.querySelector('.pdata');

        gameoverBox.innerHTML = `
        <h1>Player Stats:</h1>
        <p>Player: ${playerName}</p>
        <p>Score: ${score}</p>
        <p>Money: ${money}€</p>
        <p>Time: ${days} days</p>
        <p>CO₂: ${co2} g</p>
        <p>Places visited: ${places}</p>
        <p>Location: ${current}</p>
      `;
      }).
      catch(error => {
        console.error('Error loading player info:', error);
      });
});