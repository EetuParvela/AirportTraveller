const bounds = L.latLngBounds(
    [30.0, -18.0],
    [55.0, 45.0],
);

const map = L.map('map', {
  minZoom: 3,
  maxZoom: 10,
  maxBounds: bounds,
  maxBoundsViscosity: 1.0,
}).setView([51.505, -0.09], 3);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

loadAirportMarkers(map);

let selectAirport = null;

function getCurrentPlayer() {
  fetch("http://127.0.0.1:3000/get_current_player")


}

function loadAirportMarkers(map) {
  fetch('http://127.0.0.1:3000/get_airports_from_cache').
      then(res => res.json()).
      then(data => {
        data.forEach(marker => {
          const leafletMarker = L.marker(
              [marker['latitude_deg'], marker['longitude_deg']]).
              addTo(map).
              bindPopup(marker.airport_name);

          leafletMarker.on('click', () => {
            selectAirport = marker;

            document.getElementById('yellow').innerHTML = `
            <h5>${marker.welcome_phrase}</h5>
            <h5>${marker.airport_name}</h5>
            <p>ICAO: ${marker.icao}</p>
            <p>Country: ${marker.country_name}</p>
            <p>Weather: ${marker.weather['main']}</p>
            <p>Temperature: ${marker.weather['temp']} celsius</p>
            <button type="button" id="flyButton">Fly</button>
          `;

            document.getElementById('flyButton').
                addEventListener('click', () => {
                  if (selectedAirport) {
                    flyToAirport(selectedAirport);
                  } else {
                    console.error('No airport selected.');
                  }
                });
          });
        });
      }).
      catch(err => console.error('Fetch error:', err));
}

function flyToAirport() {
  const current_player = getCurrentPlayer()

  fetch('http://127.0.0.1:5000/change_player_stats', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      current_player: {
        name: 'Player1',
      },
      next_location: {
        icao: airport.icao,
        airport_name: airport.airport_name,
        country: airport.country_name,
        latitude_deg: airport.latitude_deg,
        longitude_deg: airport.longitude_deg,
      },
    }),
  };

