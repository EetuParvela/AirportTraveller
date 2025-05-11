  const bounds = L.latLngBounds(
    [90, -180], 
    [-90, 180]  
  );

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
                <h5>${marker.welcome_phrase}</h5>
                <h5>${marker.airport_name}</h5>
                <p>ICAO: ${marker.icao}</p>
                <p>Country: ${marker.country_name}</p>
                <button type="button" id="flyButton">Fly</button>
              `;

            document.getElementById('flyButton').
                addEventListener('click', () => {
                  if (selectedAirport) {
                    updateLocation(selectedAirport);
                  } else {
                    console.error('No airport selected.');
                  }
                });
          });
        }).
            catch(err => console.error('Fetch error:', err));
      });
}