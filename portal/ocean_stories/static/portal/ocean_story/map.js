var _ = require('lodash');

module.exports = function(engine, story, layerCatalog) {

  function normalizeSection(data) {
    data.view = {
      center: _.map(data.view.center, parseFloat),
      zoom: parseInt(data.view.zoom),
    };
  }
  story.sections.forEach(normalizeSection);

  var dataLayers = {};
  var visibleDataLayers = [];
  var currentBaseLayer;

  function defaultBaseLayer() {
    // return first base layer
    for (k in engine.baseLayers) {
      return k;
    }
  }

  function setBaseLayer(layer) {
    // return early if layer is unknown
    if (!engine.baseLayers.hasOwnProperty(layer)) {
      console.warn('attempt to set unknown base layer ' + layer);
      layer = currentBaseLayer || defaultBaseLayer();
    }

    if (layer == currentBaseLayer) return;

    console.debug('set base layer ' + layer);
    engine.showLayer(engine.baseLayers[layer], true);

    if (currentBaseLayer) {
      engine.hideLayer(engine.baseLayers[currentBaseLayer]);
    }

    currentBaseLayer = layer;

  }

  function fetchDataLayer(id) {
    if (!dataLayers.hasOwnProperty(id)) {
      if (!layerCatalog.hasOwnProperty(id)) {
        console.warn("Ignoring unknown layer id " + id);
        return false;
      }
      dataLayers[id] = engine.newDataLayer(layerCatalog[id]);
    }
    return dataLayers[id];
  }

  function setDataLayers(layers) {
    var layerKeys = Object.keys(layers)

    // trim unused layers
    _.each(_.difference(visibleDataLayers, layerKeys), function(id) {
      var l = fetchDataLayer(id);
      if (l){
        engine.hideLayer(l);
      }
    });

    // add new layers
    _.each(_.difference(layerKeys, visibleDataLayers), function(id) {
      var l = fetchDataLayer(id);
      if (l){
        engine.showLayer(l);
      }
    });
    visibleDataLayers = layerKeys;
  }

  return {
    goToSection: function(sectionIndex) {
      if (sectionIndex > story.sections.length - 1) {
        console.warn("Requested story sectionIndex " + (sectionIndex+1) + ", but only " + story.sections.length + " are present.")
        return;
      }
      var section = story.sections[sectionIndex];

      engine.setView(section.view.center, section.view.zoom, function(){
        setBaseLayer(section.baseLayer);
        setDataLayers(section.dataLayers);
      });
    },
  };
}
