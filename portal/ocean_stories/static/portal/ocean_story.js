var OceanStory = (function() {

  function ifChangedSetter(set, remove) {
    var current;
    return function(value) {
      if (value == current) return;
      // return if set failed
      if (!set(value)) return;
      if (current) remove(current);
      current = value;
    }
  }

  /* if obj.k exists, call f(obj[k]) */
  function ifExistsCaller(obj, f) {
    return function(k) {
      return obj.hasOwnProperty(k) ? f(obj[k]) : false;
    }
  }

  function baseLayerSetter(map, baseLayers) {
    return ifChangedSetter(
      ifExistsCaller(baseLayers, function(l){return map.addLayer(l)}),
      ifExistsCaller(baseLayers, function(l){return map.removeLayer(l)})
    )
  }

  function create(selector, story, layerCatalog) {
    var map = L.map(selector, {
      zoomControl: false,
      touchZoom: false,
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      boxZoom: false,
      tap: false,
    });
    var activeSection;

    var dataLayers = {};
    var setBaseLayer = baseLayerSetter(map, {
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
    })

    function goToSection(section) {
      s = story.sections[section];
      setBaseLayer(s.baseLayer);

      map.setView(s.view.center, s.view.zoom);

      activeSection = section;
    }
    goToSection(0);

    return {
      map: map,
      goToSection: goToSection,
    };
  }

  return {
    create: create,
  };
}());
