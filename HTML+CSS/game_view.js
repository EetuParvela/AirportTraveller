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
              addTo(map)}
        )})}
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);
































































































