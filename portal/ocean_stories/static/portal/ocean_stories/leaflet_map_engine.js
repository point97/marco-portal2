
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
      var leafletUrl = l.url.replace(/\$\{([xyz])\}/g, '\{$1\}')
      return L.tileLayer(leafletUrl);
    },
    'Vector': function(l) {
      var layerObj = L.Proj.geoJson(null, {
        "fillColor": l.vector_color,
        "fillOpacity": l.opacity * l.vector_fill,
        "color": l.vector_outline_color,
        "opacity": l.opacity * l.vector_outline_opacity,
      });
      $.getJSON(l.url, function(data) {
        layerObj.addData(data);
      });
      return layerObj;
    },
  }

  function createDataLayer(l) {
    console.log("Create data layer " + l.name + ' of layer_type ' +l.layer_type);
    if (typeCreateHandlers.hasOwnProperty(l.layer_type)) {
      var layerObj = typeCreateHandlers[l.layer_type](l);
      if (l.type == 'XYZ' || l.type == 'ArcRest') {
        layerObj.setOpacity(l.opacity);
      }
      return layerObj
    }
  }

  return {
    setView: function(center, zoom){ return map.setView(center, zoom) },
    createDataLayer: createDataLayer,
    addLayer: function(layer){ return map.addLayer(layer) },
    removeLayer: function(layer){ return map.removeLayer(layer) },
    baseLayers: baseLayers,
  };
}
