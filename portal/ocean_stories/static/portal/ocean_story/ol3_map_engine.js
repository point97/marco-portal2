var _ = require('lodash');
var ol = require('openlayers');
var dataLayerFactory = require('./data_layer_factory');

module.exports = function(element, animate) {

  var baseLayers = {
    "Ocean": new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 17,
      }),
      visible: false,
    }),
    "Open Street Map": new ol.layer.Tile({
      source: new ol.source.OSM(),
      visible: false,
    }),
    "Streets": new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 17,
      }),
      visible: false,
    }),
    "Physical": new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 20,
      }),
      visible: false,
    }),
    "Satellite": new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maxZoom: 20,
      }),
      visible: false,
    }),
    "Nautical Charts": new ol.layer.Tile({
      source: new ol.source.TileWMS({
        url: "http://egisws02.nos.noaa.gov/ArcGIS/services/RNC/NOAA_RNC/ImageServer/WMSServer",
        maxZoom: 13,
        projection: "EPSG:3857",
      }),
      visible: false,
    }),
  };

  var baseLayerGroup = new ol.layer.Group({
    layers: _.values(baseLayers),
  });
  var dataLayerGroup = new ol.layer.Group({
    layers: [],
  });


  var view = new ol.View();

  var map = new ol.Map({
    target: element,
    layers: [
      baseLayerGroup,
      dataLayerGroup,
    ],
    view: view,
    interactions: [],
    controls: [],
  });
  map.on("render", function(){
    console.log(e);
  });


  function wrapAnimations(animations, after) {
    return function(map, state) {
      for (i = 0; i < animations.length; ++i) {
        if (!animations[i](map, state)) {
          animations.splice(i--, 1);
        }
      }
      if (animations.length == 0) {
        after(map, state);
        return false;
      }
      return true;
    }
  }

  return {
    setView: function(center, zoom, afterFunc){
      console.info("set view center: " + center + ", zoom: " + zoom);
      // only animate if enabled and there is a previous view state
      if (animate && view.getCenter() && view.getZoom()) {
        // dataLayerGroup.setVisible(false);
        map.beforeRender(wrapAnimations([
          ol.animation.pan({
            duration: 2000,
            source: /** <at> type {ol.Coordinate} */ (view.getCenter())
          }),
          ol.animation.zoom({
            duration: 2000,
            resolution: view.getResolution(),
            source: /** <at> type {ol.Coordinate} */ (view.getZoom())
          })
          ], function() {
            afterFunc();
            // dataLayerGroup.setVisible(true);
          })
        );
      } else {
        afterFunc();
      };

      view.setCenter(ol.proj.transform(center, 'EPSG:4326', 'EPSG:3857'));
      view.setZoom(zoom);
    },
    newDataLayer: function(l) {
      var layerObj = dataLayerFactory(l);
      if (layerObj) {
        layerObj.setVisible(false);
        dataLayerGroup.getLayers().push(layerObj);        
      }
      return layerObj;
    },
    showLayer: function(layer){ return layer.setVisible(true) },
    hideLayer: function(layer){ return layer.setVisible(false) },
    baseLayers: baseLayers,
    updateSize: function(){
      map.updateSize();
      // render in the same frame as our main requestAnimationFrame loop
      map.renderSync();
    }
  };
}
