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
  fetch('http://127.0.0.1:3000/get_airports_from_cache').
      then(res => res.json()).
      then(data => {
        data.forEach(marker => {
          L.marker([marker['latitude_deg'], marker['longitude_deg']]).
              addTo(map).
              bindPopup(marker.airport_name).on('click', () => {
            selectedAirport = marker;

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

function updateLocation(selectedAirport) {
  const next_location = {
    icao: selectedAirport.icao,
    airport_name: selectedAirport.airport_name,
    country: selectedAirport.country_name,
    latitude_deg: selectedAirport.latitude_deg,
    longitude_deg: selectedAirport.longitude_deg,
  };

  console.log('Location updated:', next_location);
  return next_location;
}

document.addEventListener('DOMContentLoaded', () => {
  const updateLocationButton = document.getElementById('flyButton');

  if (updateLocationButton) {
    updateLocationButton.addEventListener('click', () => {
      try {
        if (!selectedAirport) {
          alert('Please select an airport first');
          return;
        }

        const location = updateLocation(selectedAirport);

      } catch (error) {
        console.error('Failed to update location:', error);
        alert(`Error updating location: ${error.message}`);
      }
    });
  } else {
    console.error('Update location button not found in the DOM');
  }
});