let map;

function drawMap() {
    const bounds = L.latLngBounds([30.0, -18.0], [55.0, 45.0]);

    map = L.map('map', {
        minZoom: 3,
        maxZoom: 10,
        maxBounds: bounds,
        maxBoundsViscosity: 1.0
    }).setView([51.505, -0.09], 3);

    L.tileLayer('http://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
}

let selectedMarker = null; // Global

function loadAirportMarkers(map) {
  fetch('http://localhost:3000/get_airport_info')
    .then(res => res.json())
    .then(data => {
      data.forEach(marker => {
        L.marker([marker.lat, marker.lon])
          .addTo(map)
          .bindPopup(marker.name)
          .on('click', () => {
            selectedMarker = marker; // Store clicked marker

            document.getElementById('yellow').innerHTML = `
              <h5>Tervetuloa</h5>
              <h5>${marker.name}</h5>
              <p>ICAO: ${marker.icao}</p>
              <p>Country: ${marker.country_name}</p>
              <p>Weather: ${marker.weather.main}</p>
              <p>Temperature: ${marker.weather.temp} Celsius</p>
              <button type="button" onclick="flyToAirport()">Fly</button>
            `;
          });
      });
    });
}

async function flyToAirport() {
  if (!selectedMarker) {
    alert("No airport selected!");
    return;
  }

  try {
    const response = await fetch('http://localhost:3000/fly', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(selectedMarker) // Send full marker info
    });

    const result = await response.json();
    console.log("Flight response:", result);
    alert(`Flying to ${selectedMarker.name}!`);

  } catch (error) {
    console.error("Error sending flight data:", error);
  }
}


document.addEventListener('DOMContentLoaded', () => {
    drawMap();
    loadAirportMarkers()
});







