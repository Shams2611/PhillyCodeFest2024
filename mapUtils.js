markers = [[], [], [], [], [], []];

numberOfPoints = 200
numberOfClusters = 20

let container = document.getElementById("mapContainer")

// var startCoords = [39.9596, -75.1904] //millenium 
var startCoords = [39.95666455911189, -75.19516684736305] //cci

let map = L.map(container).setView(startCoords, 14);
let osmLayer = L.tileLayer('https://api.maptiler.com/maps/basic-v2-light/{z}/{x}/{y}.png?key=itORzsoRJTMoPJkSZRLH', {
    attribution: '<a href="http://osm.org/copyright">OpenStreetMap</a>'
}).addTo(map);

bbox = [startCoords[1] - .01, startCoords[0] - .01, startCoords[1] + .01, startCoords[0] + .01];

pointsSet = []

var iconsList = []
//red, blue, yellow, green
//also do this differently later -- this is stupid
var markerColors = ["#EE5A24", "#12CBC4", "#FFC312", "#C4E538",]
var markerIcons = ["marker_studying.png", "marker_tutoring.png", "marker_career.png", "marker_scholarship.png",
    "marker_studying_grey.png", "marker_tutoring_grey.png", "marker_career_grey.png", "marker_scholarship_grey.png"]
markerIcons.forEach(item => {
    var myIcon = L.icon({
        iconUrl: "/images/markers/" + item,
        iconSize: [30, 30],
        shadowSize: [0, 0]
    });
    iconsList.push(myIcon)
})

function degrees_to_radians(degrees) {
    var pi = Math.PI;
    return degrees * (pi / 180);
}

function calculateDistance(coord1, coord2) {
    const earthRadius = 6371;
    const lat1 = degrees_to_radians(coord1[0]);
    const lon1 = degrees_to_radians(coord1[1]);
    const lat2 = degrees_to_radians(coord2[0]);
    const lon2 = degrees_to_radians(coord2[1]);
    const latDiff = lat2 - lat1;
    const lonDiff = lon2 - lon1;
    const a =
        Math.sin(latDiff / 2) ** 2 +
        Math.cos(lat1) * Math.cos(lat2) * Math.sin(lonDiff / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return earthRadius * c;
}

let locationNameLabel = document.getElementById("locationNameLabel")
let locationTypeLabel = document.getElementById("locationTypeLabel")
let locationAddressLabel = document.getElementById("locationAddressLabel")
let infoImg = document.getElementById("infoImg")

let campusRow = document.getElementById("campusRow")
let locationCampusLabel = document.getElementById("locationCampusLabel")

// console.log(infoImg)

function addRandomOffset(coordinates) {
    return coordinates.map(([x, y]) => [
        x + Math.floor(Math.random() * 11) - 5,
        y + Math.floor(Math.random() * 11) - 5
    ]);
}

function reformatDate(dateString) {
    const [year, month, day, time] = dateString.split(/[-\s]/);
    return `${time} ${month}/${day}/${year}`;
}

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

let i = 0
let ind = 0

function getData() {
    const xhttp = new XMLHttpRequest();
    xhttp.responseType = "json";
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            coordsList = [];
            stuff = [...xhttp.response];


            stuff.forEach((thing) => {
                const [latStr, longStr] = thing.coords.slice(1, -1).split(',');

                const latitude = parseFloat(latStr);
                const longitude = parseFloat(longStr);

                var coords = [latitude + (Math.floor(Math.random() * 11) - 5) * 0.0001, longitude + (Math.floor(Math.random() * 11) - 5) * 0.0001]
                var dist = calculateDistance(startCoords, coords)
                //change these lines to make the icon different
                // var ind = Math.min(Math.floor(dist / 2.5), 3);
                // var ind = getRandomNumber(0, 3)
                switch (thing.type) {
                    case "study":
                        ind = 0;
                        break;
                    case "tutor":
                        ind = 1;
                        break;
                    case "career":
                        ind = 2;
                        break;
                    case "scholarship":
                        ind = 3;
                        break;
                }
                // if(dist > 5){
                //     ind+=4
                // }
                // console.log("-"+coords+"-"+i++)
                var newMarker = new L.marker(coords, { icon: iconsList[ind] })
                markers[ind].push(newMarker)
                newMarker.addTo(map).on("click", function (e) {
                    console.log(ind)
                    routeToPoint(coords, markerColors[ind])
                    validateCheck("math", thing.math)
                    validateCheck("science", thing.science)
                    validateCheck("english", thing.english)
                    validateCheck("arts", thing.arts)
                    locationNameLabel.innerText = thing.name
                    locationTypeLabel.innerText = capitalizeWords(thing.type)
                    locationAddressLabel.innerText = thing.address
                    for(let i = 0; i<5; i++){
                        evaluateStar(thing.rating, i)
                    }
                    infoImg.style = "background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0)), url('"+thing.cover+"')";
                })
            })
        }
    }
    //   xhttp.open('GET', 'https://birdwatch-6f587-default-rtdb.firebaseio.com/.json');
    xhttp.open('GET', 'https://studyspaces-96140-default-rtdb.firebaseio.com/.json');
    xhttp.send();
}

function capitalizeWords(str) {
    let words = str.split(' ');

    for (let i = 0; i < words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    }

    return words.join(' ');
}

function validateCheck(name, val) {
    //sorry bad convention
    check = document.getElementById(name + "-check")
    x = document.getElementById(name + "-x")
    if (val == "yes") {
        x.style = "display: block;"
        check.style = "display: none;"
    }
    else {
        x.style = "display: none;"
        check.style = "display: block;"
    }
}

function evaluateStar(rating, index) {
    num = rating-index
    
    divElement = document.getElementById("star"+(index+1))
    children = divElement.children
    children[0].style = "display: none;"
    children[1].style = "display: none;"
    children[2].style = "display: none;"
    //this is very bad code please fix later
    if(num >= 1){
        children[0].style = "display: block;"
    }
    else if (num >= 0.5){
        children[1].style = "display: block;"
    }
    else{
        children[2].style = "display: block;"
    }
}

getData()

const secondFunction = async () => {
    const result = await getData()
    console.log("Data Recieved.")
}

function hideMarkers(ind) {
    console.log(markers[ind])
    markers[ind].forEach((element, i) => {
        setTimeout(() => {
            map.removeLayer(element)
        }, 20 * i);
    })
}

function showMarkers(ind) {
    console.log(markers[ind])
    markers[ind].forEach((element, i) => {
        setTimeout(() => {
            map.addLayer(element)
        }, 20 * i);
    })
}

var customControl = L.Control.extend({
    options: {
        position: 'topright'
    },

    onAdd: function (map) {
        var div = L.DomUtil.create('div', 'l-overlay');
        div.innerHTML = '<button id="outBtn">\
    <i class="fa-solid fa-minus"></i>\
    </button>\
    <button id="resetBtn">\
    <i class="fa-solid fa-crosshairs"></i>\
    </button>\
    <button id="inBtn">\
    <i class="fa-solid fa-plus"></i>\
    </button>';
        div.querySelector('#outBtn').addEventListener('click', function () {
            map.setZoom(map.getZoom() - 1)
        });
        div.querySelector('#resetBtn').addEventListener('click', function () {
            map.setView(startCoords)
        });
        div.querySelector('#inBtn').addEventListener('click', function () {
            map.setZoom(map.getZoom() + 1)
        });
        return div;
    }
});

map.addControl(new customControl());

var checkboxes = document.querySelectorAll('input[type="checkbox"]');

checkboxes.forEach(function (checkbox) {
    checkbox.checked = true;
    // console.log(checkbox.value);
    checkbox.addEventListener('change', function () {
        handleMapPreference(this);
    });
    handleMapPreference(checkbox)
});

function handleMapPreference(checkbox) {
    switch (checkbox.value) {
        case "study":
            checkbox.checked ? showMarkers(0) : hideMarkers(0)
            break;
        case "tutor":
            checkbox.checked ? showMarkers(1) : hideMarkers(1)
            break;
        case "career":
            checkbox.checked ? showMarkers(2) : hideMarkers(2)
            break;
        case "scholarship":
            checkbox.checked ? showMarkers(3) : hideMarkers(3)
            break;
    }
}

var startIcon = L.icon({
    iconUrl: '/images/markers/marker_start.png',
    iconSize: [30, 30]
});

var endIcon = L.icon({
    iconUrl: '/images/markers/marker_blank.png',
    iconSize: [30, 30]
});

var start = L.marker(startCoords, { icon: startIcon }).addTo(map);
// var end = L.marker([startCoords[0], startCoords[1] + 1], { icon: endIcon }).addTo(map);

// L.Routing.control({ createMarker: function() { return null; } });

// $scope.routingControl;

let routingControl;

function routeToPoint(coords, lineColor) {
    // map.eachLayer((layer) => {
    //   if (layer.options.waypoints && layer.options.waypoints.length) {
    //     map.removeLayer(layer);
    //    }
    // });
    // if (route != null){
    //   leafletData.getMap().then(function (map) {
    //     map.removeControl(route);
    //   });
    // }
    // $scope.removeRouting = function () {
    //   leafletData.getMap().then(function (map) {
    //     map.removeControl($scope.routingControl);
    //   });
    // };

    if (routingControl) {
        map.removeControl(routingControl);
        map.removeLayer(routingControl._line);
        routingControl = null; // Reset the routing control variable
      }

    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(start.getLatLng()),
            L.latLng(coords)
            // L.latLng(end.getLatLng())
        ],
        lineOptions: {
            styles: [{ color: lineColor, opacity: 1, weight: 4 }]
        },
        show: false,
        addWaypoints: false,
        draggableWaypoints: false,
        fitSelectedRoutes: true,
        showAlternatives: false,
        createMarker: function () { return null; }
    }).addTo(map);
}

var form = document.getElementById("information");
function getFormData(event) {
  event.preventDefault();
  info = Array.prototype.slice.call(form.elements, 0, 6);
  Array.prototype.forEach.call(info, item => {
    console.log(item.value); //to get the form values 
  });
}
form.addEventListener('submit', getFormData);