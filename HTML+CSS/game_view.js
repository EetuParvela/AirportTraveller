const bounds = L.latLngBounds([30.0, -18.0], [55.0, 45.0]);

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
  fetch('http://127.0.0.1:3000/get_airports').
      then(res => res.json()).
      then(data => {
        data.forEach(marker => {
          L.marker([marker['latitude_deg'], marker['longitude_deg']]).
              addTo(map).
              bindPopup(marker.airport_name).on('click', () => {
            selectedAirport = marker;

            document.getElementById('airportInfo').innerHTML = `
                <strong>Airport Info:</strong>
                <h5>${marker.welcome_phrase}</h5>
                <h5>${marker.airport_name}</h5>
                <p>ICAO: ${marker.icao}</p>
                <p>Country: ${marker.country_name}</p>
                <button type="button" id="flyButton">Fly</button>
              `;

            document.getElementById('flyButton').
                addEventListener('click', () => {
                  if (selectedAirport) {
                    handleFly(selectedAirport);

                    const ul = document.getElementById('visitedList');
                    const li = document.createElement('li');
                    li.textContent = selectedAirport.airport_name;
                    ul.appendChild(li);

                  } else {
                    console.error('No airport selected.');
                  }
                });
          });
        }).
            catch(err => console.error('Fetch error:', err));
      });
}

function handleFly(icao_code) {
  const icao = icao_code;

  fetch('http://127.0.0.1:3000/fly_to', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({icao}),
  }).then(response => response.json()).then(data => {
    if (data.game_over) {
      window.location.href = 'end1.html';
    }
  }).catch(error => {
    console.error('Flight error:', error);
  });
}

function handleWork(days) {
  fetch('http://127.0.0.1:3000/work', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({days}),
  }).then(response => response.json()).then(data => {
    console.log(data.message);
    // You can also update the UI with new money here
  }).catch(error => {
    console.error('Work error:', error);
  });
}

document.getElementById('work1').addEventListener('click', () => handleWork(1));
document.getElementById('work2').addEventListener('click', () => handleWork(2));
document.getElementById('work3').addEventListener('click', () => handleWork(3));