

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

  fetch('http://localhost:3000/get_airport_info').then(res => res.json()).then(data => {
    data.forEach(marker => {
      L.marker([marker['lat'], marker['lon']])
      .addTo(map)
      .bindPopup(marker.name)
      .on('click', () => {

        document.getElementById('yellow').innerHTML = `
            <h5>Tervetuloa</h5>
            <h5>${marker.name}</h5>

            <p>ICAO: ${marker.icao}</p>
            <p>Country: ${marker.country_name}</p>
            <button type="button">Fly</button>


            `;
      });
    });
  })
  .catch(err => console.error('Fetch error:', err));


