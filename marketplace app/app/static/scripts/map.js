
function createLeafletMap(){
    let map;

    // Create map with custom settings
    map = L.map('map', {
        zoom: 13,
        zoomControl: false
    });

    // Set map layers to mapbox
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        id: 'mapbox/streets-v11',
        accessToken: 'pk.eyJ1IjoiYWFyb25ldWwiLCJhIjoiY2s0OHppeG9zMWI3YzNubjZ4NDJkb3l0diJ9.wjSxjtu576jVk52lzdjkDw', // token to use mapbox
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

function findDistance(){
    // source https://stackoverflow.com/questions/8658730/what-is-the-conversion-of-latitude-longitude-to-a-1-mile
    let myLatLng, otherLatLng;
    let p1 = getCityLatLng(myState, myCity)
        .then(data => {
            myLatLng = new google.maps.LatLng(data[0].lat, data[0].lon);
        });
    let p2 = getCityLatLng(otherState, otherCity)
        .then(data => {
            otherLatLng = new google.maps.LatLng(data[0].lat, data[0].lon);
        });
    Promise.all([p1, p2])
        .then(() => {
            let distance = google.maps.geometry.spherical.computeDistanceBetween(myLatLng,otherLatLng,3956);
            let miles = parseInt(distance * 1609.34);
            if(miles) {
                let text = miles + ' miles away';
                $('#miles-away').text(text)
            }
        });
}