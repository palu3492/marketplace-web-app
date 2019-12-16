
let map;
function createLeafletMap(){

    // Create map with custom settings
    map = L.map('map', {
        zoom: 13,
        zoomControl: false
    });

    // Set map layers to mapbox
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        id: 'mapbox/streets-v11',
        accessToken: 'pk.eyJ1IjoiYWpwMCIsImEiOiJjazN4cGd4MGQxNW1hM3F0NnU5M3Jiem80In0.71DleDv1Fm-ArumkU37BjA', // token to use mapbox
    }).addTo(map);

    getCityLatLng(state, city)
        .then(data => {
            let latLng = [data[0].lat, data[0].lon];
            map.panTo(latLng);
            let popup = L.popup({closeOnClick: false, autoClose: false, closeButton: false, keepInView: true}).setContent(city+', '+state);
            L.marker(latLng).bindPopup(popup).addTo(map).openPopup();
        });
}

function getCityLatLng(state, city){
    let country = 'United States';
    let apiUrl = 'https://nominatim.openstreetmap.org/search?format=json&country='+country+'&state='+state+'&city='+city;
    return $.getJSON(apiUrl);
}