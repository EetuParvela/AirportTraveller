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

async function updateLocation(selectedAirport) {
  const next_location = {
    icao: selectedAirport.icao,
    airport_name: selectedAirport.airport_name,
    country: selectedAirport.country_name,
    latitude_deg: selectedAirport.latitude_deg,
    longitude_deg: selectedAirport.longitude_deg,
  };

  const response = await fetch('http://localhost:3000/change_player_stats', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(selectedAirport),
        });


  console.log('Location updated:', next_location);
  return next_location;
}


document.addEventListener('DOMContentLoaded', function() {
  const pinkPostit = document.querySelector('.postit.pink');

  //on 40% tödennäköisyys saada nopan
  if (Math.random() < 0.4 && pinkPostit) {
    pinkPostit.innerHTML = `
            <h2>🎉 Vau!</h2>
            <h3>Sait mahdollisuus tuplata kierroksen pisteet, jos nopasta tulee 4 tai enemmän.</h3>
            <h3>Klikkaa noppaa nähdäksesi tuloksen!</h3>
            <img id="dice" class="dice" src="image/R.png" alt="Dice">
            <h3 id="resultMsg"></h3>
        `;
    const dice = document.getElementById('dice');
    const resultMsg = document.getElementById('resultMsg');
    let tossAllowed = true;

    dice.addEventListener('click', () => {
      if (!tossAllowed) return;
      tossAllowed = false;

      fetch('http://127.0.0.1:3000/get_bonus', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      }).then(response => {
        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }
        return response.json();
      }).then(data => {
        const diceRoll = data.roll;

        dice.src = `image/${diceRoll}.png`;
        dice.alt = `Roll ${diceRoll}`;

        if (diceRoll >= 4) {
          resultMsg.textContent = '✅ Yes! Pisteet tuplattiin!';
          resultMsg.style.color = 'green';
        } else {
          resultMsg.textContent = '❌ Valitettavasti ei tärpännyt tällä kertaa!';
          resultMsg.style.color = 'red';
        }

        setTimeout(() => {
          tossAllowed = true;
        }, 5000);
      });
    });
  }
});

fetch('http://localhost:3000/get_player_stats').
    then(res => res.json()).
    then(data => {
      data.forEach(player => {

        document.getElementById('green').innerHTML = `
            <h5>${player.name}Stats<h5>
                <ul>
                    <li>current airport: ${player.current_airport}</li>
                    <li>points : ${player.points}</li>
                    <li>CO2 consumed: ${player.co2_consumed}</li>
                    <li>Distance: ${player.distance}</li>
                </ul>`;
      });
    })

fetch('http://localhost:3000/closest_airports/EFHK')
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('blue');
    container.innerHTML = `<h5>Ehdotukset</h5>`;

    const list = document.createElement('ol');

    data.forEach(airport => {
      const li = document.createElement('li');
      li.textContent = `ICAO: ${airport.ident} Name: ${airport.airport_name}`;
      li.style.cursor = 'pointer';

      li.addEventListener('click', () => {
        selectedAirport = airport;

        document.getElementById('yellow').innerHTML = `
          <h5>${airport.welcome_phrase || 'Welcome!'}</h5>
          <h5>${airport.airport_name}</h5>
          <p>ICAO: ${airport.ident}</p>
          <p>Country: ${airport.country_name}</p>
          <p>Weather: ${airport.weather?.main || 'Unknown'}</p>
          <p>Temperature: ${airport.weather?.temp ?? 'N/A'} celsius</p>
          <button type="button" id="flyButton">Fly</button>
        `;

        document.getElementById('flyButton').addEventListener('click', () => {
          if (selectedAirport) {
            updateLocation(selectedAirport);
          } else {
            console.error('No airport selected.');
          }
        });
      });

      list.appendChild(li);
    });

    container.appendChild(list);
  })
  .catch(err => {
    console.error('Error fetching airports:', err);
    document.getElementById('blue').innerHTML = `<p>Error loading airport suggestions.</p>`;
  });
