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

async function getAirportInfo() {
    try {
        const response = await fetch('http://localhost:3000/get_airport_info');
        const data = await response.json();

        data.forEach(marker => {
            const lat = marker.lat || marker.latitude_deg;
            const lon = marker.lon || marker.longitude_deg;
            if (lat && lon) {
                L.marker([lat, lon]).addTo(map).bindPopup(marker.name || "Unnamed");
            }
        });
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    drawMap();
    getAirportInfo();
});

async function getCurrentPlayerStat() {

}