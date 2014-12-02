
/* ocean stories map engine using leaflet */
function leafletMapEngine(selector) {
  var map = L.map(selector, {
    zoomControl: false,
    touchZoom: false,
    dragging: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    tap: false,
    keyboard: false,
    attributionControl: false,
  });

  var baseLayers = {
    "Esri Oceans": L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
      maxZoom: 13
    }),
    "Open Street Map": L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
    }),
    "Google Street": new L.Google('STREET'),
    "Google Terrain": new L.Google('TERRAIN'),
    "Google Satellite": new L.Google('SATELLITE'),
  };


  var typeCreateHandlers = {
    'XYZ': function(l) {
      console.log("XYZ: " + l.url);
      leafletUrl = l.url.replace(/\$\{([xyz])\}/g, '\{$1\}')
      return L.tileLayer(leafletUrl);
    },
    'Vector': function(l) {
      var layerObj = L.geoJson();
      $.getJSON(l.url, function(data) {
        layerObj.addData(data);
      });
      return layerObj;
    },
  }

  return {
    setView: function(center, zoom){ return map.setView(center, zoom) },
    typeCreateHandlers: typeCreateHandlers,
    addLayer: function(layer){ return map.addLayer(layer) },
    removeLayer: function(layer){ return map.removeLayer(layer) },
    baseLayers: baseLayers,
  };
}
