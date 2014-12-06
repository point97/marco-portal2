function ol3MapEngine(selector) {

  var baseLayers = {
    "Open Street Map": new ol.layer.Tile({
      source: new ol.source.MapQuest({layer: 'osm'}),
      visible: false,
    }),
    "Esri Oceans": new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}'
      }),
      visible: false,
    }),

    //   "Esri Oceans": L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}', {
    //     attribution: 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
    //     maxZoom: 13
    //   }),
    //   "Open Street Map": L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
    //   }),
    //   "Google Street": new L.Google('STREET'),
    //   "Google Terrain": new L.Google('TERRAIN'),
    //   "Google Satellite": new L.Google('SATELLITE'),
  };

  var view = new ol.View();

  var map = new ol.Map({
    target: selector,
    layers: _.values(baseLayers),
    view: view,
    interactions: [],
    controls: [],
  });

  // var map = L.map(selector, {
  //   zoomControl: false,
  //   touchZoom: false,
  //   dragging: false,
  //   scrollWheelZoom: false,
  //   doubleClickZoom: false,
  //   boxZoom: false,
  //   tap: false,
  //   keyboard: false,
  //   attributionControl: false,
  // });
  //

  function hackyMarineCadastreLayerConversion(l) {
    l.layer_type = "WMS";
    l.url = l.url.replace(
      /^(http:\/\/coast.noaa.gov\/arcgis)\/rest\/(services\/MarineCadastre\/[^/]+\/MapServer)\/export$/,
      '$1/$2/WMSServer'
    );

    var idMappings = {
      "http://coast.noaa.gov/arcgis/services/MarineCadastre/NavigationAndMarineTransportation/MapServer/WMSServer": {
        7: 2,
        8: 1,
        9: 0,
      },
      "http://coast.noaa.gov/arcgis/services/MarineCadastre/OceanEnergy/MapServer/WMSServer": {
        4: 0,
        3: 1,
      }
    }

    if (idMappings.hasOwnProperty(l.url)) {
      var mapping = idMappings[l.url];
      var arcRestLayers = l.arcgis_layers.split(',');
      mappedLayers = _.map(arcRestLayers, function(restId) {
        return mapping.hasOwnProperty(restId) ? mapping[restId] : restId
      });
      l.arcgis_layers = mappedLayers.join(',');
    }
    return l;
  }

  var typeCreateHandlers = {
    'XYZ': function(l) {
      var fixedUrlTemplate = l.url.replace(/\$\{([xyz])\}/g, '\{$1\}')
      return new ol.layer.Tile({
        source: new ol.source.XYZ({
          url: fixedUrlTemplate,
        })
      });
    },
    'Vector': function(l) {
      return new ol.layer.Vector({
        source: new ol.source.GeoJSON({
          url: l.url,
        }),
        style: new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: l.vector_outline_color,
            width: 1.5,
          }),
          fill: new ol.style.Fill({
            color: l.vector_color,
          }),
        }),
        opacity: l.opacity,
      });
    },
    'WMS': function(l) {
      return new ol.layer.Tile({
        // extent: [-13884991, 2870341, -7455066, 6338219],
        source: new ol.source.TileWMS( ({
          url: l.url,
          params: {'LAYERS': l.arcgis_layers, 'TILED': true}
        }))
      })
    },
  }

  function createDataLayer(l) {
    console.log("Create data layer " + l.name + ' of layer_type ' +l.layer_type);

    if (l.layer_type == 'ArcRest') {
      console.log("converting to WMS: " + l.name);
      l = hackyMarineCadastreLayerConversion(l);
    }

    if (typeCreateHandlers.hasOwnProperty(l.layer_type)) {
      var layerObj = typeCreateHandlers[l.layer_type](l);
      layerObj.setVisible(false);
      map.addLayer(layerObj);
      return layerObj;
    }
  }

  return {
    setView: function(center, zoom){
      console.log("set view center: " + center + ", zoom: " + zoom);
      if (view.getCenter() && view.getZoom()) {
        map.beforeRender(
          ol.animation.pan({
            duration: 500,
            source: /** <at> type {ol.Coordinate} */ (view.getCenter())
          }),
          ol.animation.zoom({
            duration: 500,
            resolution: view.getResolution(),
            source: /** <at> type {ol.Coordinate} */ (view.getZoom())
          })
        );
      }
      view.setCenter(ol.proj.transform(center.slice().reverse(), 'EPSG:4326', 'EPSG:3857'));
      view.setZoom(zoom);
    },
    createDataLayer: createDataLayer,
    addLayer: function(layer){ return layer.setVisible(true) },
    removeLayer: function(layer){ return layer.setVisible(false) },
    baseLayers: baseLayers,
  };
}
